# backend/app/schemas/chat.py

Define contratos de conversas, mensagens, resumos e envio/resposta de chat; client_message_id é a chave estável de idempotência do cliente.

[Arquivo fonte](../../../../../backend/app/schemas/chat.py) · 76 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [ConversationCreate](#L9) | Define o tipo ConversationCreate e reúne o estado/contrato descrito para este módulo. |
| [ConversationResponse](#L16) | Define o tipo ConversationResponse e reúne o estado/contrato descrito para este módulo. |
| [MessageResponse](#L26) | Define o tipo MessageResponse e reúne o estado/contrato descrito para este módulo. |
| [ChatSend](#L39) | Define o tipo ChatSend e reúne o estado/contrato descrito para este módulo. |
| [ChatSend.not_blank](#L48) | Implementa ChatSend.not_blank como parte do fluxo descrito para este arquivo. |
| [ChatReply](#L55) | Define o tipo ChatReply e reúne o estado/contrato descrito para este módulo. |
| [SummaryResponse](#L71) | Define o tipo SummaryResponse e reúne o estado/contrato descrito para este módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import datetime</code> | Importa datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from pydantic import BaseModel, ConfigDict, Field, field_validator</code> | Importa BaseModel, ConfigDict, Field, field_validator de pydantic. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code># Documentação: Define o tipo ConversationCreate e reúne o estado/contrato descrito para este</code> | Comentário: Documentação: Define o tipo ConversationCreate e reúne o estado/contrato descrito para este |
| <a id="L8"></a>8 | <code># módulo.</code> | Comentário: módulo. |
| <a id="L9"></a>9 | <code>class ConversationCreate(BaseModel):</code> | Define o tipo ConversationCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L10"></a>10 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L11"></a>11 | <code>    title: str = Field(default=&quot;Nova conversa&quot;, min_length=1, max_length=100)</code> | Define title com Field(default=&#x27;Nova conversa&#x27;, min_length=1, max_length=100). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=&#x27;Nova conversa&#x27;, min_length=1, max_length=100 |
| <a id="L12"></a>12 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code># Documentação: Define o tipo ConversationResponse e reúne o estado/contrato descrito para este</code> | Comentário: Documentação: Define o tipo ConversationResponse e reúne o estado/contrato descrito para este |
| <a id="L15"></a>15 | <code># módulo.</code> | Comentário: módulo. |
| <a id="L16"></a>16 | <code>class ConversationResponse(BaseModel):</code> | Define o tipo ConversationResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L17"></a>17 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L18"></a>18 | <code>    id: UUID</code> | Define id com None. |
| <a id="L19"></a>19 | <code>    title: str</code> | Define title com None. |
| <a id="L20"></a>20 | <code>    archived: bool</code> | Define archived com None. |
| <a id="L21"></a>21 | <code>    created_at: datetime</code> | Define created_at com None. |
| <a id="L22"></a>22 | <code>    updated_at: datetime</code> | Define updated_at com None. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L25"></a>25 | <code># Documentação: Define o tipo MessageResponse e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo MessageResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L26"></a>26 | <code>class MessageResponse(BaseModel):</code> | Define o tipo MessageResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L28"></a>28 | <code>    id: UUID</code> | Define id com None. |
| <a id="L29"></a>29 | <code>    conversation_id: UUID</code> | Define conversation_id com None. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L30"></a>30 | <code>    sequence: int</code> | Define sequence com None. |
| <a id="L31"></a>31 | <code>    role: str</code> | Define role com None. |
| <a id="L32"></a>32 | <code>    content: str</code> | Define content com None. |
| <a id="L33"></a>33 | <code>    status: str</code> | Define status com None. |
| <a id="L34"></a>34 | <code>    error_code: str &#124; None</code> | Define error_code com None. |
| <a id="L35"></a>35 | <code>    created_at: datetime</code> | Define created_at com None. |
| <a id="L36"></a>36 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L37"></a>37 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L38"></a>38 | <code># Documentação: Define o tipo ChatSend e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ChatSend e reúne o estado/contrato descrito para este módulo. |
| <a id="L39"></a>39 | <code>class ChatSend(BaseModel):</code> | Define o tipo ChatSend e reúne o estado/contrato descrito para este módulo. |
| <a id="L40"></a>40 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L41"></a>41 | <code>    conversation_id: UUID &#124; None = None</code> | Define conversation_id com None. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L42"></a>42 | <code>    client_message_id: UUID</code> | Define client_message_id com None. UUID estável do envio; retries devem conservar este identificador para evitar duplicação. |
| <a id="L43"></a>43 | <code>    content: str = Field(min_length=1, max_length=4000)</code> | Define content com Field(min_length=1, max_length=4000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=4000 |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L45"></a>45 | <code>    @field_validator(&quot;content&quot;)</code> | Aplica o decorator field_validator(&quot;content&quot;) à definição que segue. |
| <a id="L46"></a>46 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L47"></a>47 | <code>    # Documentação: Implementa ChatSend.not_blank como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa ChatSend.not_blank como parte do fluxo descrito para este arquivo. |
| <a id="L48"></a>48 | <code>    def not_blank(cls, value):</code> | Implementa ChatSend.not_blank como parte do fluxo descrito para este arquivo. |
| <a id="L49"></a>49 | <code>        if not value.strip():</code> | Executa este ramo somente se not value.strip(); caso contrário, segue o ramo alternativo. |
| <a id="L50"></a>50 | <code>            raise ValueError(&quot;Mensagem vazia&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Mensagem vazia&#x27;). |
| <a id="L51"></a>51 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L52"></a>52 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L53"></a>53 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L54"></a>54 | <code># Documentação: Define o tipo ChatReply e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ChatReply e reúne o estado/contrato descrito para este módulo. |
| <a id="L55"></a>55 | <code>class ChatReply(BaseModel):</code> | Define o tipo ChatReply e reúne o estado/contrato descrito para este módulo. |
| <a id="L56"></a>56 | <code>    conversation_id: UUID</code> | Define conversation_id com None. Vincula a mensagem/chamada à conversa cujo contexto deve ser conservado. |
| <a id="L57"></a>57 | <code>    user_message_id: UUID</code> | Define user_message_id com None. |
| <a id="L58"></a>58 | <code>    assistant_message_id: UUID</code> | Define assistant_message_id com None. |
| <a id="L59"></a>59 | <code>    request_id: UUID</code> | Define request_id com None. |
| <a id="L60"></a>60 | <code>    reply: str</code> | Define reply com None. |
| <a id="L61"></a>61 | <code>    provider: str</code> | Define provider com None. |
| <a id="L62"></a>62 | <code>    fallback_used: bool</code> | Define fallback_used com None. |
| <a id="L63"></a>63 | <code>    latency_ms: int</code> | Define latency_ms com None. |
| <a id="L64"></a>64 | <code>    memory_candidates: list[dict]</code> | Define memory_candidates com None. |
| <a id="L65"></a>65 | <code>    actions: list[dict]</code> | Define actions com None. |
| <a id="L66"></a>66 | <code>    context_stats: dict</code> | Define context_stats com None. |
| <a id="L67"></a>67 | <code>    replayed: bool = False</code> | Define replayed com False. |
| <a id="L68"></a>68 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L69"></a>69 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L70"></a>70 | <code># Documentação: Define o tipo SummaryResponse e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo SummaryResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L71"></a>71 | <code>class SummaryResponse(BaseModel):</code> | Define o tipo SummaryResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L72"></a>72 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L73"></a>73 | <code>    id: UUID</code> | Define id com None. |
| <a id="L74"></a>74 | <code>    through_sequence: int</code> | Define through_sequence com None. |
| <a id="L75"></a>75 | <code>    content: dict</code> | Define content com None. |
| <a id="L76"></a>76 | <code>    created_at: datetime</code> | Define created_at com None. |
