# backend/app/api/planning.py

Adapta HTTP aos serviços de tarefas, lembretes e chamadas agendadas; valida payloads e retorna representações serializáveis dos registros.

[Arquivo fonte](../../../../../backend/app/api/planning.py) · 191 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [TaskPatch](#L19) | Define o tipo TaskPatch e reúne o estado/contrato descrito para este módulo. |
| [ReminderPatch](#L27) | Define o tipo ReminderPatch e reúne o estado/contrato descrito para este módulo. |
| [TaskResponse](#L35) | Define o tipo TaskResponse e reúne o estado/contrato descrito para este módulo. |
| [ScheduleResponse](#L48) | Define o tipo ScheduleResponse e reúne o estado/contrato descrito para este módulo. |
| [invoke](#L63) | Implementa invoke como parte do fluxo descrito para este arquivo. |
| [create_task](#L75) | Cria create_task, segundo o contrato e as verificações deste módulo. |
| [list_tasks](#L85) | Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| [update_task](#L98) | Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| [complete_task](#L109) | Implementa complete_task como parte do fluxo descrito para este arquivo. |
| [create_reminder](#L119) | Cria create_reminder, segundo o contrato e as verificações deste módulo. |
| [list_reminders](#L129) | Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| [update_reminder](#L142) | Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| [cancel_reminder](#L153) | Cancela cancel_reminder, segundo o contrato e as verificações deste módulo. |
| [create_call](#L163) | Cria create_call, segundo o contrato e as verificações deste módulo. |
| [list_calls](#L173) | Lista list_calls, segundo o contrato e as verificações deste módulo. |
| [cancel_call](#L186) | Cancela cancel_call, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from datetime import date, datetime</code> | Importa date, datetime de datetime. |
| <a id="L2"></a>2 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L3"></a>3 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L4"></a>4 | <code>from fastapi import APIRouter, Depends, HTTPException, Query</code> | Importa APIRouter, Depends, HTTPException, Query de fastapi. |
| <a id="L5"></a>5 | <code>from pydantic import AwareDatetime, BaseModel, ConfigDict, Field</code> | Importa AwareDatetime, BaseModel, ConfigDict, Field de pydantic. |
| <a id="L6"></a>6 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>from app.agent.action_parser import CallCreate, ReminderCreate, TaskCreate</code> | Importa CallCreate, ReminderCreate, TaskCreate de app.agent.action_parser. |
| <a id="L9"></a>9 | <code>from app.agent.errors import AgentError</code> | Importa AgentError de app.agent.errors. |
| <a id="L10"></a>10 | <code>from app.db.session import get_session</code> | Importa get_session de app.db.session. |
| <a id="L11"></a>11 | <code>from app.models import User</code> | Importa User de app.models. |
| <a id="L12"></a>12 | <code>from app.planning.service import PlanningService</code> | Importa PlanningService de app.planning.service. |
| <a id="L13"></a>13 | <code>from app.security import get_current_user</code> | Importa get_current_user de app.security. |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code>router = APIRouter(tags=[&quot;planning&quot;])</code> | Define router com APIRouter(tags=[&#x27;planning&#x27;]). Invoca APIRouter com os argumentos declarados nesta instrução. Argumentos: tags=[&#x27;planning&#x27;] |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L17"></a>17 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L18"></a>18 | <code># Documentação: Define o tipo TaskPatch e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo TaskPatch e reúne o estado/contrato descrito para este módulo. |
| <a id="L19"></a>19 | <code>class TaskPatch(BaseModel):</code> | Define o tipo TaskPatch e reúne o estado/contrato descrito para este módulo. |
| <a id="L20"></a>20 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L21"></a>21 | <code>    title: str &#124; None = Field(None, min_length=1, max_length=300)</code> | Define title com Field(None, min_length=1, max_length=300). Invoca Field com os argumentos declarados nesta instrução. Argumentos: None, min_length=1, max_length=300 |
| <a id="L22"></a>22 | <code>    description: str &#124; None = Field(None, max_length=2000)</code> | Define description com Field(None, max_length=2000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: None, max_length=2000 |
| <a id="L23"></a>23 | <code>    due_at: AwareDatetime &#124; None = None</code> | Define due_at com None. |
| <a id="L24"></a>24 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L26"></a>26 | <code># Documentação: Define o tipo ReminderPatch e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ReminderPatch e reúne o estado/contrato descrito para este módulo. |
| <a id="L27"></a>27 | <code>class ReminderPatch(BaseModel):</code> | Define o tipo ReminderPatch e reúne o estado/contrato descrito para este módulo. |
| <a id="L28"></a>28 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L29"></a>29 | <code>    text: str &#124; None = Field(None, min_length=1, max_length=1000)</code> | Define text com Field(None, min_length=1, max_length=1000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: None, min_length=1, max_length=1000 |
| <a id="L30"></a>30 | <code>    datetime: AwareDatetime &#124; None = None</code> | Define datetime com None. |
| <a id="L31"></a>31 | <code>    rrule: str &#124; None = Field(None, max_length=500)</code> | Define rrule com Field(None, max_length=500). Invoca Field com os argumentos declarados nesta instrução. Argumentos: None, max_length=500 |
| <a id="L32"></a>32 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L33"></a>33 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L34"></a>34 | <code># Documentação: Define o tipo TaskResponse e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo TaskResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L35"></a>35 | <code>class TaskResponse(BaseModel):</code> | Define o tipo TaskResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L36"></a>36 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L37"></a>37 | <code>    id: UUID</code> | Define id com None. |
| <a id="L38"></a>38 | <code>    title: str</code> | Define title com None. |
| <a id="L39"></a>39 | <code>    description: str &#124; None</code> | Define description com None. |
| <a id="L40"></a>40 | <code>    due_at: datetime &#124; None</code> | Define due_at com None. |
| <a id="L41"></a>41 | <code>    status: str</code> | Define status com None. |
| <a id="L42"></a>42 | <code>    created_at: datetime</code> | Define created_at com None. |
| <a id="L43"></a>43 | <code>    updated_at: datetime</code> | Define updated_at com None. |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L45"></a>45 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L46"></a>46 | <code># Documentação: Define o tipo ScheduleResponse e reúne o estado/contrato descrito para este</code> | Comentário: Documentação: Define o tipo ScheduleResponse e reúne o estado/contrato descrito para este |
| <a id="L47"></a>47 | <code># módulo.</code> | Comentário: módulo. |
| <a id="L48"></a>48 | <code>class ScheduleResponse(BaseModel):</code> | Define o tipo ScheduleResponse e reúne o estado/contrato descrito para este módulo. |
| <a id="L49"></a>49 | <code>    model_config = ConfigDict(from_attributes=True)</code> | Define model_config com ConfigDict(from_attributes=True). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: from_attributes=True |
| <a id="L50"></a>50 | <code>    id: UUID</code> | Define id com None. |
| <a id="L51"></a>51 | <code>    kind: str</code> | Define kind com None. |
| <a id="L52"></a>52 | <code>    text: str</code> | Define text com None. |
| <a id="L53"></a>53 | <code>    timezone: str</code> | Define timezone com None. |
| <a id="L54"></a>54 | <code>    start_at: datetime</code> | Define start_at com None. |
| <a id="L55"></a>55 | <code>    next_run_at: datetime &#124; None</code> | Define next_run_at com None. Próximo disparo UTC calculado conforme timezone/regra do agendamento. |
| <a id="L56"></a>56 | <code>    rrule: str &#124; None</code> | Define rrule com None. |
| <a id="L57"></a>57 | <code>    status: str</code> | Define status com None. |
| <a id="L58"></a>58 | <code>    version: int</code> | Define version com None. |
| <a id="L59"></a>59 | <code>    created_at: datetime</code> | Define created_at com None. |
| <a id="L60"></a>60 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L61"></a>61 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L62"></a>62 | <code># Documentação: Implementa invoke como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa invoke como parte do fluxo descrito para este arquivo. |
| <a id="L63"></a>63 | <code>def invoke(session, user, operation, *args):</code> | Implementa invoke como parte do fluxo descrito para este arquivo. |
| <a id="L64"></a>64 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L65"></a>65 | <code>        result = getattr(PlanningService(session, user.id), operation)(*args)</code> | Define result com getattr(PlanningService(session, user.id), operation)(*args). Invoca getattr(PlanningService(session, user.id), operation) com os argumentos declarados nesta instrução. Argumentos: *args |
| <a id="L66"></a>66 | <code>        session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L67"></a>67 | <code>        return result</code> | Retorna result ao chamador e encerra este caminho da função. |
| <a id="L68"></a>68 | <code>    except AgentError as error:</code> | Trata exceção AgentError como error. |
| <a id="L69"></a>69 | <code>        session.rollback()</code> | Desfaz a transação atual antes de tratar a falha. |
| <a id="L70"></a>70 | <code>        raise HTTPException(error.status_code, error.code) from None</code> | Interrompe este caminho lançando HTTPException(error.status_code, error.code). |
| <a id="L71"></a>71 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L72"></a>72 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L73"></a>73 | <code>@router.post(&quot;/tasks&quot;, response_model=TaskResponse, status_code=201)</code> | Aplica o decorator router.post(&quot;/tasks&quot;, response_model=TaskResponse, status_code=201) à definição que segue. |
| <a id="L74"></a>74 | <code># Documentação: Cria create_task, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cria create_task, segundo o contrato e as verificações deste módulo. |
| <a id="L75"></a>75 | <code>def create_task(</code> | Cria create_task, segundo o contrato e as verificações deste módulo. |
| <a id="L76"></a>76 | <code>    data: TaskCreate,</code> | Continua/fecha a instrução da linha 75. Cria create_task, segundo o contrato e as verificações deste módulo. |
| <a id="L77"></a>77 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 75. Cria create_task, segundo o contrato e as verificações deste módulo. |
| <a id="L78"></a>78 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 75. Cria create_task, segundo o contrato e as verificações deste módulo. |
| <a id="L79"></a>79 | <code>):</code> | Continua/fecha a instrução da linha 75. Cria create_task, segundo o contrato e as verificações deste módulo. |
| <a id="L80"></a>80 | <code>    return invoke(session, user, &quot;create_task&quot;, data.model_dump())</code> | Retorna invoke(session, user, &#x27;create_task&#x27;, data.model_dump()) ao chamador e encerra este caminho da função. |
| <a id="L81"></a>81 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L82"></a>82 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L83"></a>83 | <code>@router.get(&quot;/tasks&quot;, response_model=list[TaskResponse])</code> | Aplica o decorator router.get(&quot;/tasks&quot;, response_model=list[TaskResponse]) à definição que segue. |
| <a id="L84"></a>84 | <code># Documentação: Lista list_tasks, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L85"></a>85 | <code>def list_tasks(</code> | Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L86"></a>86 | <code>    day: date &#124; None = Query(None, alias=&quot;date&quot;),</code> | Continua/fecha a instrução da linha 85. Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L87"></a>87 | <code>    status: str &#124; None = Query(None, pattern=&quot;^(OPEN&#124;COMPLETED)$&quot;),</code> | Continua/fecha a instrução da linha 85. Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L88"></a>88 | <code>    limit: int = Query(50, ge=1, le=100),</code> | Continua/fecha a instrução da linha 85. Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L89"></a>89 | <code>    offset: int = Query(0, ge=0),</code> | Continua/fecha a instrução da linha 85. Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L90"></a>90 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 85. Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L91"></a>91 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 85. Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L92"></a>92 | <code>):</code> | Continua/fecha a instrução da linha 85. Lista list_tasks, segundo o contrato e as verificações deste módulo. |
| <a id="L93"></a>93 | <code>    return invoke(session, user, &quot;list_tasks&quot;, day, status, limit, offset)</code> | Retorna invoke(session, user, &#x27;list_tasks&#x27;, day, status, limit, offset) ao chamador e encerra este caminho da função. |
| <a id="L94"></a>94 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L95"></a>95 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L96"></a>96 | <code>@router.patch(&quot;/tasks/{identifier}&quot;, response_model=TaskResponse)</code> | Aplica o decorator router.patch(&quot;/tasks/{identifier}&quot;, response_model=TaskResponse) à definição que segue. |
| <a id="L97"></a>97 | <code># Documentação: Atualiza update_task, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| <a id="L98"></a>98 | <code>def update_task(</code> | Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| <a id="L99"></a>99 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 98. Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| <a id="L100"></a>100 | <code>    data: TaskPatch,</code> | Continua/fecha a instrução da linha 98. Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| <a id="L101"></a>101 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 98. Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| <a id="L102"></a>102 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 98. Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| <a id="L103"></a>103 | <code>):</code> | Continua/fecha a instrução da linha 98. Atualiza update_task, segundo o contrato e as verificações deste módulo. |
| <a id="L104"></a>104 | <code>    return invoke(session, user, &quot;update_task&quot;, identifier, data.model_dump(exclude_unset=True))</code> | Retorna invoke(session, user, &#x27;update_task&#x27;, identifier, data.model_dump(exclude_unset=True)) ao chamador e encerra este caminho da função. |
| <a id="L105"></a>105 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L106"></a>106 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L107"></a>107 | <code>@router.post(&quot;/tasks/{identifier}/complete&quot;, response_model=TaskResponse)</code> | Aplica o decorator router.post(&quot;/tasks/{identifier}/complete&quot;, response_model=TaskResponse) à definição que segue. |
| <a id="L108"></a>108 | <code># Documentação: Implementa complete_task como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa complete_task como parte do fluxo descrito para este arquivo. |
| <a id="L109"></a>109 | <code>def complete_task(</code> | Implementa complete_task como parte do fluxo descrito para este arquivo. |
| <a id="L110"></a>110 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 109. Implementa complete_task como parte do fluxo descrito para este arquivo. |
| <a id="L111"></a>111 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 109. Implementa complete_task como parte do fluxo descrito para este arquivo. |
| <a id="L112"></a>112 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 109. Implementa complete_task como parte do fluxo descrito para este arquivo. |
| <a id="L113"></a>113 | <code>):</code> | Continua/fecha a instrução da linha 109. Implementa complete_task como parte do fluxo descrito para este arquivo. |
| <a id="L114"></a>114 | <code>    return invoke(session, user, &quot;complete_task&quot;, identifier)</code> | Retorna invoke(session, user, &#x27;complete_task&#x27;, identifier) ao chamador e encerra este caminho da função. |
| <a id="L115"></a>115 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L116"></a>116 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L117"></a>117 | <code>@router.post(&quot;/reminders&quot;, response_model=ScheduleResponse, status_code=201)</code> | Aplica o decorator router.post(&quot;/reminders&quot;, response_model=ScheduleResponse, status_code=201) à definição que segue. |
| <a id="L118"></a>118 | <code># Documentação: Cria create_reminder, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cria create_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L119"></a>119 | <code>def create_reminder(</code> | Cria create_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L120"></a>120 | <code>    data: ReminderCreate,</code> | Continua/fecha a instrução da linha 119. Cria create_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L121"></a>121 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 119. Cria create_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L122"></a>122 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 119. Cria create_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L123"></a>123 | <code>):</code> | Continua/fecha a instrução da linha 119. Cria create_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L124"></a>124 | <code>    return invoke(session, user, &quot;create_schedule&quot;, &quot;REMINDER&quot;, data.model_dump())</code> | Retorna invoke(session, user, &#x27;create_schedule&#x27;, &#x27;REMINDER&#x27;, data.model_dump()) ao chamador e encerra este caminho da função. |
| <a id="L125"></a>125 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L126"></a>126 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L127"></a>127 | <code>@router.get(&quot;/reminders&quot;, response_model=list[ScheduleResponse])</code> | Aplica o decorator router.get(&quot;/reminders&quot;, response_model=list[ScheduleResponse]) à definição que segue. |
| <a id="L128"></a>128 | <code># Documentação: Lista list_reminders, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L129"></a>129 | <code>def list_reminders(</code> | Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L130"></a>130 | <code>    day: date &#124; None = Query(None, alias=&quot;date&quot;),</code> | Continua/fecha a instrução da linha 129. Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L131"></a>131 | <code>    status: str &#124; None = Query(None, pattern=&quot;^(SCHEDULED&#124;CANCELLED&#124;COMPLETED)$&quot;),</code> | Continua/fecha a instrução da linha 129. Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L132"></a>132 | <code>    limit: int = Query(50, ge=1, le=100),</code> | Continua/fecha a instrução da linha 129. Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L133"></a>133 | <code>    offset: int = Query(0, ge=0),</code> | Continua/fecha a instrução da linha 129. Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L134"></a>134 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 129. Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L135"></a>135 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 129. Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L136"></a>136 | <code>):</code> | Continua/fecha a instrução da linha 129. Lista list_reminders, segundo o contrato e as verificações deste módulo. |
| <a id="L137"></a>137 | <code>    return invoke(session, user, &quot;list_schedules&quot;, &quot;REMINDER&quot;, day, status, limit, offset)</code> | Retorna invoke(session, user, &#x27;list_schedules&#x27;, &#x27;REMINDER&#x27;, day, status, limit, offset) ao chamador e encerra este caminho da função. |
| <a id="L138"></a>138 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L139"></a>139 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L140"></a>140 | <code>@router.patch(&quot;/reminders/{identifier}&quot;, response_model=ScheduleResponse)</code> | Aplica o decorator router.patch(&quot;/reminders/{identifier}&quot;, response_model=ScheduleResponse) à definição que segue. |
| <a id="L141"></a>141 | <code># Documentação: Atualiza update_reminder, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L142"></a>142 | <code>def update_reminder(</code> | Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L143"></a>143 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 142. Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L144"></a>144 | <code>    data: ReminderPatch,</code> | Continua/fecha a instrução da linha 142. Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L145"></a>145 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 142. Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L146"></a>146 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 142. Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L147"></a>147 | <code>):</code> | Continua/fecha a instrução da linha 142. Atualiza update_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L148"></a>148 | <code>    return invoke(session, user, &quot;update_schedule&quot;, identifier, data.model_dump(exclude_unset=True))</code> | Retorna invoke(session, user, &#x27;update_schedule&#x27;, identifier, data.model_dump(exclude_unset=True)) ao chamador e encerra este caminho da função. |
| <a id="L149"></a>149 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L150"></a>150 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L151"></a>151 | <code>@router.delete(&quot;/reminders/{identifier}&quot;, response_model=ScheduleResponse)</code> | Aplica o decorator router.delete(&quot;/reminders/{identifier}&quot;, response_model=ScheduleResponse) à definição que segue. |
| <a id="L152"></a>152 | <code># Documentação: Cancela cancel_reminder, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cancela cancel_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L153"></a>153 | <code>def cancel_reminder(</code> | Cancela cancel_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L154"></a>154 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 153. Cancela cancel_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L155"></a>155 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 153. Cancela cancel_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L156"></a>156 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 153. Cancela cancel_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L157"></a>157 | <code>):</code> | Continua/fecha a instrução da linha 153. Cancela cancel_reminder, segundo o contrato e as verificações deste módulo. |
| <a id="L158"></a>158 | <code>    return invoke(session, user, &quot;cancel_schedule&quot;, identifier, &quot;REMINDER&quot;)</code> | Retorna invoke(session, user, &#x27;cancel_schedule&#x27;, identifier, &#x27;REMINDER&#x27;) ao chamador e encerra este caminho da função. |
| <a id="L159"></a>159 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L160"></a>160 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L161"></a>161 | <code>@router.post(&quot;/scheduled-calls&quot;, response_model=ScheduleResponse, status_code=201)</code> | Aplica o decorator router.post(&quot;/scheduled-calls&quot;, response_model=ScheduleResponse, status_code=201) à definição que segue. |
| <a id="L162"></a>162 | <code># Documentação: Cria create_call, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cria create_call, segundo o contrato e as verificações deste módulo. |
| <a id="L163"></a>163 | <code>def create_call(</code> | Cria create_call, segundo o contrato e as verificações deste módulo. |
| <a id="L164"></a>164 | <code>    data: CallCreate,</code> | Continua/fecha a instrução da linha 163. Cria create_call, segundo o contrato e as verificações deste módulo. |
| <a id="L165"></a>165 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 163. Cria create_call, segundo o contrato e as verificações deste módulo. |
| <a id="L166"></a>166 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 163. Cria create_call, segundo o contrato e as verificações deste módulo. |
| <a id="L167"></a>167 | <code>):</code> | Continua/fecha a instrução da linha 163. Cria create_call, segundo o contrato e as verificações deste módulo. |
| <a id="L168"></a>168 | <code>    return invoke(session, user, &quot;create_schedule&quot;, &quot;CALL&quot;, data.model_dump())</code> | Retorna invoke(session, user, &#x27;create_schedule&#x27;, &#x27;CALL&#x27;, data.model_dump()) ao chamador e encerra este caminho da função. |
| <a id="L169"></a>169 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L170"></a>170 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L171"></a>171 | <code>@router.get(&quot;/scheduled-calls&quot;, response_model=list[ScheduleResponse])</code> | Aplica o decorator router.get(&quot;/scheduled-calls&quot;, response_model=list[ScheduleResponse]) à definição que segue. |
| <a id="L172"></a>172 | <code># Documentação: Lista list_calls, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L173"></a>173 | <code>def list_calls(</code> | Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L174"></a>174 | <code>    day: date &#124; None = Query(None, alias=&quot;date&quot;),</code> | Continua/fecha a instrução da linha 173. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L175"></a>175 | <code>    status: str &#124; None = Query(None, pattern=&quot;^(SCHEDULED&#124;CANCELLED&#124;COMPLETED)$&quot;),</code> | Continua/fecha a instrução da linha 173. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L176"></a>176 | <code>    limit: int = Query(50, ge=1, le=100),</code> | Continua/fecha a instrução da linha 173. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L177"></a>177 | <code>    offset: int = Query(0, ge=0),</code> | Continua/fecha a instrução da linha 173. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L178"></a>178 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 173. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L179"></a>179 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 173. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L180"></a>180 | <code>):</code> | Continua/fecha a instrução da linha 173. Lista list_calls, segundo o contrato e as verificações deste módulo. |
| <a id="L181"></a>181 | <code>    return invoke(session, user, &quot;list_schedules&quot;, &quot;CALL&quot;, day, status, limit, offset)</code> | Retorna invoke(session, user, &#x27;list_schedules&#x27;, &#x27;CALL&#x27;, day, status, limit, offset) ao chamador e encerra este caminho da função. |
| <a id="L182"></a>182 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L183"></a>183 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L184"></a>184 | <code>@router.delete(&quot;/scheduled-calls/{identifier}&quot;, response_model=ScheduleResponse)</code> | Aplica o decorator router.delete(&quot;/scheduled-calls/{identifier}&quot;, response_model=ScheduleResponse) à definição que segue. |
| <a id="L185"></a>185 | <code># Documentação: Cancela cancel_call, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Cancela cancel_call, segundo o contrato e as verificações deste módulo. |
| <a id="L186"></a>186 | <code>def cancel_call(</code> | Cancela cancel_call, segundo o contrato e as verificações deste módulo. |
| <a id="L187"></a>187 | <code>    identifier: UUID,</code> | Continua/fecha a instrução da linha 186. Cancela cancel_call, segundo o contrato e as verificações deste módulo. |
| <a id="L188"></a>188 | <code>    user: User = Depends(get_current_user),</code> | Continua/fecha a instrução da linha 186. Cancela cancel_call, segundo o contrato e as verificações deste módulo. |
| <a id="L189"></a>189 | <code>    session: Session = Depends(get_session),</code> | Continua/fecha a instrução da linha 186. Cancela cancel_call, segundo o contrato e as verificações deste módulo. |
| <a id="L190"></a>190 | <code>):</code> | Continua/fecha a instrução da linha 186. Cancela cancel_call, segundo o contrato e as verificações deste módulo. |
| <a id="L191"></a>191 | <code>    return invoke(session, user, &quot;cancel_schedule&quot;, identifier, &quot;CALL&quot;)</code> | Retorna invoke(session, user, &#x27;cancel_schedule&#x27;, identifier, &#x27;CALL&#x27;) ao chamador e encerra este caminho da função. |
