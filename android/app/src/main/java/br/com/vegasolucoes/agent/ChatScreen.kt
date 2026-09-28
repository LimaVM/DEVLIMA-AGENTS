package br.com.vegasolucoes.agent

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.launch
import org.json.JSONArray

@Composable fun ChatScreen(onConnect: ()->Unit) {
    val revision by AgentRuntime.revision.collectAsStateWithLifecycle()
    val scope=rememberCoroutineScope();var selected by remember {mutableStateOf<String?>(null)};var chooser by remember {mutableStateOf(false)}
    var text by remember {mutableStateOf("")};var error by remember {mutableStateOf<String?>(null)};var syncing by remember {mutableStateOf(false)}
    val threads=remember(revision){AgentRuntime.events.threads()};val thread=threads.firstOrNull {it.id==selected} ?: threads.firstOrNull()
    val bubbles=remember(revision,thread){thread?.let{AgentRuntime.events.bubbles(it)} ?: emptyList()};val list=rememberLazyListState()
    suspend fun sync() {
        syncing=true
        try {
            val rows=JSONArray(AgentRuntime.auth.api("/chat/conversations?limit=100"));withContext(Dispatchers.IO){AgentRuntime.events.importThreads(rows)}
            thread?.serverId?.let { id -> val all=JSONArray();var after=0;var more=true;while(more && all.length()<2000) {val page=JSONArray(AgentRuntime.auth.api("/chat/conversations/$id/messages?after_sequence=$after&limit=200"));for(i in 0 until page.length()){val m=page.getJSONObject(i);all.put(m);after=m.getInt("sequence")};more=page.length()==200};withContext(Dispatchers.IO){AgentRuntime.events.cacheHistory(id,all)} }
            AgentRuntime.refreshEvents();error=null
        }catch(_:Exception){error="Histórico local disponível. Conecte para atualizar."}finally{syncing=false}
    }
    LaunchedEffect(selected){sync()}
    LaunchedEffect(bubbles.size){if(bubbles.isNotEmpty())list.animateScrollToItem(bubbles.lastIndex)}
    Column(Modifier.fillMaxSize().padding(horizontal=16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
        Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
            TextButton(onClick={chooser=true},modifier=Modifier.weight(1f)){Text(thread?.title ?: "Nova conversa",maxLines=1)}
            TextButton(onClick={selected=AgentRuntime.events.newThread();AgentRuntime.refreshEvents()}){Text("Nova")}
            TextButton(onClick={scope.launch{sync()}},enabled=!syncing){Text("Atualizar")}
        }
        error?.let{Text(it,style=MaterialTheme.typography.bodySmall,color=MaterialTheme.colorScheme.onSurfaceVariant)}
        LazyColumn(state=list,modifier=Modifier.weight(1f).fillMaxWidth(),verticalArrangement=Arrangement.spacedBy(12.dp),contentPadding=PaddingValues(vertical=12.dp)) {
            if(bubbles.isEmpty())item{Text("Como posso ajudar? Peça um lembrete, organize uma tarefa ou converse.",Modifier.padding(20.dp))}
            items(bubbles){bubble -> Row(Modifier.fillMaxWidth(),horizontalArrangement=if(bubble.mine)Arrangement.End else Arrangement.Start){Card(colors=CardDefaults.cardColors(containerColor=if(bubble.mine)MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant),modifier=Modifier.widthIn(max=320.dp).clickable(enabled=bubble.retryId!=null){bubble.retryId?.let{AgentRuntime.events.retry(it);AgentRuntime.refreshEvents();onConnect()}}){Column(Modifier.padding(14.dp)){Text(bubble.text);if(bubble.state.isNotEmpty())Text(bubble.state,style=MaterialTheme.typography.labelSmall,color=MaterialTheme.colorScheme.onSurfaceVariant)}}}}
        }
        Row(verticalAlignment=Alignment.CenterVertically,horizontalArrangement=Arrangement.spacedBy(8.dp),modifier=Modifier.padding(bottom=12.dp)) {
            OutlinedTextField(text,{if(it.length<=4000)text=it},label={Text("Mensagem")},maxLines=4,modifier=Modifier.weight(1f))
            Button(onClick={val id=thread?.id ?: AgentRuntime.events.newThread();selected=id;AgentRuntime.events.enqueue(id,text.trim());text="";AgentRuntime.refreshEvents();onConnect()},enabled=text.isNotBlank()){Text("Enviar")}
        }
    }
    if(chooser)AlertDialog(onDismissRequest={chooser=false},title={Text("Conversas")},text={LazyColumn{items(threads){row->TextButton(onClick={selected=row.id;chooser=false},modifier=Modifier.fillMaxWidth()){Text(row.title)}}}},confirmButton={TextButton(onClick={chooser=false}){Text("Fechar")}})
}
