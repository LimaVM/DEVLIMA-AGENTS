package br.com.vegasolucoes.agent

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import java.time.*
import java.time.format.DateTimeFormatter
import java.time.format.ResolverStyle
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject

val localFormat: DateTimeFormatter =
    DateTimeFormatter.ofPattern("dd/MM/uuuu HH:mm").withResolverStyle(ResolverStyle.STRICT)

// Documentação: Converte data/hora local usando timezone da conta e recusa horário
// ambíguo/inexistente.
fun localToInstant(value: String, zone: String): Instant {
    val local = LocalDateTime.parse(value, localFormat)
    val tz = ZoneId.of(zone)
    val offsets = tz.rules.getValidOffsets(local)
    require(offsets.size == 1) { "Horário inexistente ou ambíguo nesta timezone" }
    return local.toInstant(offsets.first())
}

// Documentação: Implementa displayDate como parte do fluxo descrito para este arquivo.
fun displayDate(value: String?, zone: String): String =
    if (value.isNullOrEmpty() || value == "null") "Sem horário"
    else
        runCatching { Instant.parse(value).atZone(ZoneId.of(zone)).format(localFormat) }
            .getOrDefault("Horário indisponível")

// Documentação: Implementa arrayRows como parte do fluxo descrito para este arquivo.
fun arrayRows(value: String): List<JSONObject> =
    JSONArray(value).let { arr -> (0 until arr.length()).map { arr.getJSONObject(it) } }

@Composable
// Documentação: Implementa RoutineScreen como parte do fluxo descrito para este arquivo.
fun RoutineScreen(session: SessionData) {
    val scope = rememberCoroutineScope()
    val revision by AgentRuntime.revision.collectAsStateWithLifecycle()
    var kind by remember { mutableIntStateOf(0) }
    var today by remember { mutableStateOf(false) }
    var active by remember { mutableStateOf(true) }
    var rows by remember { mutableStateOf<List<JSONObject>>(emptyList()) }
    var error by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var edit by remember { mutableStateOf<JSONObject?>(null) }
    var form by remember { mutableStateOf(false) }
    val paths = listOf("/tasks", "/reminders", "/scheduled-calls")
    val path = paths[kind]
    // Documentação: Atualiza refresh, segundo o contrato e as verificações deste módulo.
    suspend fun refresh() {
        busy = true
        try {
            val query =
                "?limit=100" +
                    (if (active) "&status=" + if (kind == 0) "OPEN" else "SCHEDULED" else "") +
                    (if (today) "&date=" + LocalDate.now(ZoneId.of(session.timezone)) else "")
            rows = arrayRows(AgentRuntime.auth.api(path + query))
            error = null
        } catch (_: Exception) {
            error = "Não foi possível atualizar. Confira sua conexão."
        } finally {
            busy = false
        }
    }
    LaunchedEffect(kind, today, active, revision) { refresh() }
    Column(
        Modifier.fillMaxSize().padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Row {
            listOf("Tarefas", "Lembretes", "Chamadas").forEachIndexed { i, label ->
                FilterChip(
                    selected = kind == i,
                    onClick = { kind = i },
                    label = { Text(label) },
                    modifier = Modifier.padding(end = 6.dp),
                )
            }
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            FilterChip(today, { today = !today }, label = { Text("Hoje") })
            FilterChip(active, { active = !active }, label = { Text("Pendentes") })
            TextButton(onClick = { scope.launch { refresh() } }, enabled = !busy) {
                Text("Atualizar")
            }
        }
        Button(
            onClick = {
                edit = null
                form = true
            }
        ) {
            Text(
                if (kind == 0) "Nova tarefa"
                else if (kind == 1) "Novo lembrete" else "Agendar chamada"
            )
        }
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        LazyColumn(
            Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(bottom = 20.dp),
        ) {
            if (rows.isEmpty())
                item {
                    Text(
                        if (busy) "Carregando…" else "Nenhum item neste filtro.",
                        Modifier.padding(16.dp),
                    )
                }
            items(rows, key = { it.getString("id") }) { row ->
                Card(Modifier.fillMaxWidth()) {
                    Column(
                        Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Text(
                            row.optString(if (kind == 0) "title" else "text"),
                            style = MaterialTheme.typography.titleMedium,
                        )
                        if (kind == 0 && !row.isNull("description"))
                            Text(row.getString("description"))
                        Text(
                            displayDate(
                                row.optString(if (kind == 0) "due_at" else "next_run_at"),
                                session.timezone,
                            ),
                            style = MaterialTheme.typography.bodySmall,
                        )
                        val state = row.getString("status")
                        Text(
                            when (state) {
                                "OPEN" -> "Pendente"
                                "SCHEDULED" -> "Agendado"
                                "CANCELLED" -> "Cancelado"
                                else -> "Concluído"
                            },
                            style = MaterialTheme.typography.labelSmall,
                        )
                        if (!row.isNull("rrule") && row.has("rrule"))
                            Text("Recorrente", style = MaterialTheme.typography.labelSmall)
                        Row {
                            if (kind < 2 && state in listOf("OPEN", "SCHEDULED"))
                                TextButton(
                                    onClick = {
                                        edit = row
                                        form = true
                                    }
                                ) {
                                    Text("Editar")
                                }
                            if (state in listOf("OPEN", "SCHEDULED"))
                                TextButton(
                                    onClick = {
                                        scope.launch {
                                            busy = true
                                            try {
                                                AgentRuntime.auth.api(
                                                    path +
                                                        "/" +
                                                        row.getString("id") +
                                                        (if (kind == 0) "/complete" else ""),
                                                    if (kind == 0) "POST" else "DELETE",
                                                    if (kind == 0) JSONObject() else null,
                                                )
                                                refresh()
                                            } catch (_: Exception) {
                                                error = "Não foi possível salvar esta alteração."
                                            } finally {
                                                busy = false
                                            }
                                        }
                                    },
                                    enabled = !busy,
                                ) {
                                    Text(if (kind == 0) "Concluir" else "Cancelar")
                                }
                        }
                    }
                }
            }
        }
    }
    if (form)
        RoutineEditor(
            kind,
            edit,
            session.timezone,
            onDismiss = { form = false },
            onSave = { data ->
                busy = true
                try {
                    AgentRuntime.auth.api(
                        path + (edit?.let { "/" + it.getString("id") } ?: ""),
                        if (edit == null) "POST" else "PATCH",
                        data,
                    )
                    form = false
                    refresh()
                } finally {
                    busy = false
                }
            },
        )
}

@Composable
// Documentação: Implementa RoutineEditor como parte do fluxo descrito para este arquivo.
private fun RoutineEditor(
    kind: Int,
    row: JSONObject?,
    zone: String,
    onDismiss: () -> Unit,
    onSave: suspend (JSONObject) -> Unit,
) {
    val scope = rememberCoroutineScope()
    var text by remember {
        mutableStateOf(row?.optString(if (kind == 0) "title" else "text") ?: "")
    }
    var description by remember {
        mutableStateOf(row?.optString("description")?.takeUnless { it == "null" } ?: "")
    }
    var date by remember {
        mutableStateOf(
            row?.optString(if (kind == 0) "due_at" else "next_run_at")
                ?.takeUnless { it == "null" }
                ?.let { displayDate(it, zone) }
                ?: if (kind == 0) ""
                else Instant.now().plusSeconds(300).atZone(ZoneId.of(zone)).format(localFormat)
        )
    }
    var recurrence by remember { mutableIntStateOf(0) }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    AlertDialog(
        onDismissRequest = { if (!busy) onDismiss() },
        title = { Text(if (row == null) "Criar" else "Editar") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedTextField(
                    text,
                    {
                        if (it.length <= if (kind == 0) 300 else if (kind == 1) 1000 else 500)
                            text = it
                    },
                    label = {
                        Text(if (kind == 0) "Título" else if (kind == 1) "Lembrete" else "Motivo")
                    },
                    maxLines = 3,
                )
                if (kind == 0)
                    OutlinedTextField(
                        description,
                        { if (it.length <= 2000) description = it },
                        label = { Text("Descrição (opcional)") },
                        maxLines = 3,
                    )
                OutlinedTextField(
                    date,
                    { date = it },
                    label = { Text("dd/mm/aaaa hh:mm") },
                    supportingText = { Text(zone + (if (kind == 0) " · opcional" else "")) },
                    singleLine = true,
                )
                if (kind > 0)
                    Row {
                        TextButton(
                            onClick = {
                                date =
                                    Instant.now()
                                        .plusSeconds(120)
                                        .atZone(ZoneId.of(zone))
                                        .format(localFormat)
                            }
                        ) {
                            Text("2 min")
                        }
                        TextButton(
                            onClick = {
                                date =
                                    Instant.now()
                                        .plusSeconds(300)
                                        .atZone(ZoneId.of(zone))
                                        .format(localFormat)
                            }
                        ) {
                            Text("5 min")
                        }
                    }
                if (kind > 0 && row == null) {
                    Text("Repetir (até 30 ocorrências)")
                    Row {
                        listOf("Nunca", "Diária", "Semanal").forEachIndexed { i, label ->
                            FilterChip(
                                recurrence == i,
                                { recurrence = i },
                                label = { Text(label) },
                                modifier = Modifier.padding(end = 4.dp),
                            )
                        }
                    }
                }
                error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            }
        },
        confirmButton = {
            TextButton(
                enabled = !busy && text.isNotBlank(),
                onClick = {
                    scope.launch {
                        busy = true
                        try {
                            val data =
                                JSONObject()
                                    .put(
                                        if (kind == 0) "title"
                                        else if (kind == 1 || row != null) "text" else "reason",
                                        text.trim(),
                                    )
                            if (kind == 0)
                                data
                                    .put("description", description)
                                    .put(
                                        "due_at",
                                        if (date.isBlank()) JSONObject.NULL
                                        else localToInstant(date, zone).toString(),
                                    )
                            else {
                                val instant = localToInstant(date, zone)
                                require(instant.isAfter(Instant.now())) {
                                    "Escolha um horário futuro"
                                }
                                data.put("datetime", instant.toString())
                                if (row == null && recurrence > 0)
                                    data.put(
                                        "rrule",
                                        "FREQ=" +
                                            (if (recurrence == 1) "DAILY" else "WEEKLY") +
                                            ";COUNT=30",
                                    )
                            }
                            onSave(data)
                        } catch (issue: Exception) {
                            error =
                                if (issue is IllegalArgumentException) issue.message
                                else "Não foi possível salvar. Confira data e conexão."
                        } finally {
                            busy = false
                        }
                    }
                },
            ) {
                Text(if (busy) "Salvando…" else "Salvar")
            }
        },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !busy) { Text("Fechar") } },
    )
}

@Composable
// Documentação: Implementa MemoryScreen como parte do fluxo descrito para este arquivo.
fun MemoryScreen() {
    val scope = rememberCoroutineScope()
    var candidates by remember { mutableStateOf<List<JSONObject>>(emptyList()) }
    var error by remember { mutableStateOf<String?>(null) }
    // Documentação: Carrega load, segundo o contrato e as verificações deste módulo.
    suspend fun load() {
        try {
            candidates = arrayRows(AgentRuntime.auth.api("/memories/candidates"))
            error = null
        } catch (_: Exception) {
            error = "Não foi possível consultar memórias."
        }
    }
    Text("Memórias propostas", style = MaterialTheme.typography.titleMedium)
    TextButton(onClick = { scope.launch { load() } }) { Text("Consultar") }
    error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    for (row in candidates) {
        Text(row.getString("content"))
        Row {
            listOf("accept" to "Aceitar", "reject" to "Recusar").forEach { (action, label) ->
                TextButton(
                    onClick = {
                        scope.launch {
                            try {
                                AgentRuntime.auth.api(
                                    "/memories/candidates/${row.getString("id")}/$action",
                                    "POST",
                                    JSONObject(),
                                )
                                load()
                            } catch (_: Exception) {
                                error = "Não foi possível atualizar a memória."
                            }
                        }
                    }
                ) {
                    Text(label)
                }
            }
        }
    }
}
