# backend/app/agent/action_parser.py

Define o contrato JSON da resposta do agente. Recusa campos extras, chaves duplicadas, argumentos incompatíveis e propostas fora dos limites antes de qualquer execução.

[Arquivo fonte](../../../../../backend/app/agent/action_parser.py) · 201 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [StrictModel](#L20) | Define o tipo StrictModel e reúne o estado/contrato descrito para este módulo. |
| [TaskCreate](#L25) | Define o tipo TaskCreate e reúne o estado/contrato descrito para este módulo. |
| [IdArguments](#L32) | Define o tipo IdArguments e reúne o estado/contrato descrito para este módulo. |
| [TaskUpdate](#L37) | Define o tipo TaskUpdate e reúne o estado/contrato descrito para este módulo. |
| [ReminderCreate](#L44) | Define o tipo ReminderCreate e reúne o estado/contrato descrito para este módulo. |
| [ReminderUpdate](#L51) | Define o tipo ReminderUpdate e reúne o estado/contrato descrito para este módulo. |
| [CallCreate](#L57) | Define o tipo CallCreate e reúne o estado/contrato descrito para este módulo. |
| [ListArguments](#L64) | Define o tipo ListArguments e reúne o estado/contrato descrito para este módulo. |
| [EmptyArguments](#L69) | Define o tipo EmptyArguments e reúne o estado/contrato descrito para este módulo. |
| [WorkerCreate](#L74) | Define o tipo WorkerCreate e reúne o estado/contrato descrito para este módulo. |
| [WorkerArguments](#L82) | Define o tipo WorkerArguments e reúne o estado/contrato descrito para este módulo. |
| [WorkerRestore](#L87) | Define o tipo WorkerRestore e reúne o estado/contrato descrito para este módulo. |
| [WorkerJob](#L92) | Define o tipo WorkerJob e reúne o estado/contrato descrito para este módulo. |
| [ActionProposal](#L123) | Define o tipo ActionProposal e reúne o estado/contrato descrito para este módulo. |
| [ActionProposal.validate_arguments](#L129) | Confere argumentos contra o schema específico da ação antes do despacho. |
| [MemoryProposal](#L143) | Define o tipo MemoryProposal e reúne o estado/contrato descrito para este módulo. |
| [AgentEnvelope](#L150) | Define o tipo AgentEnvelope e reúne o estado/contrato descrito para este módulo. |
| [AgentEnvelope.not_blank](#L159) | Implementa AgentEnvelope.not_blank como parte do fluxo descrito para este arquivo. |
| [SummaryEnvelope](#L166) | Define o tipo SummaryEnvelope e reúne o estado/contrato descrito para este módulo. |
| [SummaryEnvelope.bound_items](#L174) | Implementa SummaryEnvelope.bound_items como parte do fluxo descrito para este arquivo. |
| [reject_duplicate_keys](#L184) | Recusa objetos JSON que reutilizam a mesma chave, evitando interpretações divergentes. |
| [parse_response](#L194) | Valida envelope JSON estruturado da LLM e recusa resposta fora do contrato. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>import json</code> | Importa módulo(s) json. |
| <a id="L2"></a>2 | <code>from datetime import UTC</code> | Importa UTC de datetime. |
| <a id="L3"></a>3 | <code>from typing import Literal</code> | Importa Literal de typing. |
| <a id="L4"></a>4 | <code>from uuid import UUID</code> | Importa UUID de uuid. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>from pydantic import (</code> | Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L7"></a>7 | <code>    AwareDatetime,</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L8"></a>8 | <code>    BaseModel,</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L9"></a>9 | <code>    ConfigDict,</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L10"></a>10 | <code>    Field,</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L11"></a>11 | <code>    ValidationError,</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L12"></a>12 | <code>    field_validator,</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L13"></a>13 | <code>    model_validator,</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L14"></a>14 | <code>)</code> | Continua/fecha a instrução da linha 6. Importa AwareDatetime, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator de pydantic. |
| <a id="L15"></a>15 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L16"></a>16 | <code>from app.agent.errors import InvalidAgentResponse</code> | Importa InvalidAgentResponse de app.agent.errors. |
| <a id="L17"></a>17 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L18"></a>18 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L19"></a>19 | <code># Documentação: Define o tipo StrictModel e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo StrictModel e reúne o estado/contrato descrito para este módulo. |
| <a id="L20"></a>20 | <code>class StrictModel(BaseModel):</code> | Define o tipo StrictModel e reúne o estado/contrato descrito para este módulo. |
| <a id="L21"></a>21 | <code>    model_config = ConfigDict(extra=&quot;forbid&quot;)</code> | Define model_config com ConfigDict(extra=&#x27;forbid&#x27;). Invoca ConfigDict com os argumentos declarados nesta instrução. Argumentos: extra=&#x27;forbid&#x27; |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code># Documentação: Define o tipo TaskCreate e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo TaskCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L25"></a>25 | <code>class TaskCreate(StrictModel):</code> | Define o tipo TaskCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L26"></a>26 | <code>    title: str = Field(min_length=1, max_length=300)</code> | Define title com Field(min_length=1, max_length=300). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=300 |
| <a id="L27"></a>27 | <code>    description: str &#124; None = Field(default=None, max_length=2000)</code> | Define description com Field(default=None, max_length=2000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, max_length=2000 |
| <a id="L28"></a>28 | <code>    due_at: AwareDatetime &#124; None = None</code> | Define due_at com None. |
| <a id="L29"></a>29 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L30"></a>30 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L31"></a>31 | <code># Documentação: Define o tipo IdArguments e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo IdArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L32"></a>32 | <code>class IdArguments(StrictModel):</code> | Define o tipo IdArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L33"></a>33 | <code>    id: UUID</code> | Define id com None. |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L35"></a>35 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L36"></a>36 | <code># Documentação: Define o tipo TaskUpdate e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo TaskUpdate e reúne o estado/contrato descrito para este módulo. |
| <a id="L37"></a>37 | <code>class TaskUpdate(IdArguments):</code> | Define o tipo TaskUpdate e reúne o estado/contrato descrito para este módulo. |
| <a id="L38"></a>38 | <code>    title: str &#124; None = Field(default=None, min_length=1, max_length=300)</code> | Define title com Field(default=None, min_length=1, max_length=300). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, min_length=1, max_length=300 |
| <a id="L39"></a>39 | <code>    description: str &#124; None = Field(default=None, max_length=2000)</code> | Define description com Field(default=None, max_length=2000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, max_length=2000 |
| <a id="L40"></a>40 | <code>    due_at: AwareDatetime &#124; None = None</code> | Define due_at com None. |
| <a id="L41"></a>41 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L42"></a>42 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L43"></a>43 | <code># Documentação: Define o tipo ReminderCreate e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ReminderCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L44"></a>44 | <code>class ReminderCreate(StrictModel):</code> | Define o tipo ReminderCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L45"></a>45 | <code>    text: str = Field(min_length=1, max_length=1000)</code> | Define text com Field(min_length=1, max_length=1000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=1000 |
| <a id="L46"></a>46 | <code>    datetime: AwareDatetime</code> | Define datetime com None. |
| <a id="L47"></a>47 | <code>    rrule: str &#124; None = Field(default=None, max_length=500)</code> | Define rrule com Field(default=None, max_length=500). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, max_length=500 |
| <a id="L48"></a>48 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L49"></a>49 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L50"></a>50 | <code># Documentação: Define o tipo ReminderUpdate e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ReminderUpdate e reúne o estado/contrato descrito para este módulo. |
| <a id="L51"></a>51 | <code>class ReminderUpdate(IdArguments):</code> | Define o tipo ReminderUpdate e reúne o estado/contrato descrito para este módulo. |
| <a id="L52"></a>52 | <code>    text: str &#124; None = Field(default=None, min_length=1, max_length=1000)</code> | Define text com Field(default=None, min_length=1, max_length=1000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, min_length=1, max_length=1000 |
| <a id="L53"></a>53 | <code>    datetime: AwareDatetime &#124; None = None</code> | Define datetime com None. |
| <a id="L54"></a>54 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L55"></a>55 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L56"></a>56 | <code># Documentação: Define o tipo CallCreate e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo CallCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L57"></a>57 | <code>class CallCreate(StrictModel):</code> | Define o tipo CallCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L58"></a>58 | <code>    datetime: AwareDatetime</code> | Define datetime com None. |
| <a id="L59"></a>59 | <code>    reason: str = Field(default=&quot;Conversar com o agente&quot;, max_length=500)</code> | Define reason com Field(default=&#x27;Conversar com o agente&#x27;, max_length=500). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=&#x27;Conversar com o agente&#x27;, max_length=500 |
| <a id="L60"></a>60 | <code>    rrule: str &#124; None = Field(default=None, max_length=500)</code> | Define rrule com Field(default=None, max_length=500). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, max_length=500 |
| <a id="L61"></a>61 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L62"></a>62 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L63"></a>63 | <code># Documentação: Define o tipo ListArguments e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ListArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L64"></a>64 | <code>class ListArguments(StrictModel):</code> | Define o tipo ListArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L65"></a>65 | <code>    date: str &#124; None = Field(default=None, pattern=r&quot;^\d{4}-\d{2}-\d{2}$&quot;)</code> | Define date com Field(default=None, pattern=&#x27;^\\d{4}-\\d{2}-\\d{2}$&#x27;). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, pattern=&#x27;^\\d{4}-\\d{2}-\\d{2}$&#x27; |
| <a id="L66"></a>66 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L67"></a>67 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L68"></a>68 | <code># Documentação: Define o tipo EmptyArguments e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo EmptyArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L69"></a>69 | <code>class EmptyArguments(StrictModel):</code> | Define o tipo EmptyArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L70"></a>70 | <code>    pass</code> | Mantém o bloco sem operação adicional, inclusive quando uma exceção é ignorada. |
| <a id="L71"></a>71 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L72"></a>72 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L73"></a>73 | <code># Documentação: Define o tipo WorkerCreate e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo WorkerCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L74"></a>74 | <code>class WorkerCreate(StrictModel):</code> | Define o tipo WorkerCreate e reúne o estado/contrato descrito para este módulo. |
| <a id="L75"></a>75 | <code>    name: str &#124; None = Field(default=None, min_length=1, max_length=64, pattern=r&quot;^[a-z0-9-]+$&quot;)</code> | Define name com Field(default=None, min_length=1, max_length=64, pattern=&#x27;^[a-z0-9-]+$&#x27;). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=None, min_length=1, max_length=64, pattern=&#x27;^[a-z0-9-]+$&#x27; |
| <a id="L76"></a>76 | <code>    vcpu: int = Field(default=2, ge=1, le=4)</code> | Define vcpu com Field(default=2, ge=1, le=4). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=2, ge=1, le=4 |
| <a id="L77"></a>77 | <code>    ram_mb: int = Field(default=2048, ge=512, le=8192)</code> | Define ram_mb com Field(default=2048, ge=512, le=8192). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=2048, ge=512, le=8192 |
| <a id="L78"></a>78 | <code>    disk_gb: int = Field(default=20, ge=10, le=80)</code> | Define disk_gb com Field(default=20, ge=10, le=80). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=20, ge=10, le=80 |
| <a id="L79"></a>79 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L80"></a>80 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L81"></a>81 | <code># Documentação: Define o tipo WorkerArguments e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo WorkerArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L82"></a>82 | <code>class WorkerArguments(StrictModel):</code> | Define o tipo WorkerArguments e reúne o estado/contrato descrito para este módulo. |
| <a id="L83"></a>83 | <code>    worker_id: UUID</code> | Define worker_id com None. |
| <a id="L84"></a>84 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L85"></a>85 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L86"></a>86 | <code># Documentação: Define o tipo WorkerRestore e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo WorkerRestore e reúne o estado/contrato descrito para este módulo. |
| <a id="L87"></a>87 | <code>class WorkerRestore(WorkerArguments):</code> | Define o tipo WorkerRestore e reúne o estado/contrato descrito para este módulo. |
| <a id="L88"></a>88 | <code>    snapshot_id: UUID</code> | Define snapshot_id com None. |
| <a id="L89"></a>89 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L90"></a>90 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L91"></a>91 | <code># Documentação: Define o tipo WorkerJob e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo WorkerJob e reúne o estado/contrato descrito para este módulo. |
| <a id="L92"></a>92 | <code>class WorkerJob(WorkerArguments):</code> | Define o tipo WorkerJob e reúne o estado/contrato descrito para este módulo. |
| <a id="L93"></a>93 | <code>    script: str = Field(min_length=1, max_length=8000)</code> | Define script com Field(min_length=1, max_length=8000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=8000 |
| <a id="L94"></a>94 | <code>    timeout: int = Field(default=120, ge=1, le=300)</code> | Define timeout com Field(default=120, ge=1, le=300). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default=120, ge=1, le=300 |
| <a id="L95"></a>95 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L96"></a>96 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L97"></a>97 | <code>ARGUMENT_SCHEMAS = {</code> | Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L98"></a>98 | <code>    &quot;create_task&quot;: TaskCreate,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L99"></a>99 | <code>    &quot;update_task&quot;: TaskUpdate,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L100"></a>100 | <code>    &quot;complete_task&quot;: IdArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L101"></a>101 | <code>    &quot;list_tasks&quot;: ListArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L102"></a>102 | <code>    &quot;create_reminder&quot;: ReminderCreate,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L103"></a>103 | <code>    &quot;update_reminder&quot;: ReminderUpdate,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L104"></a>104 | <code>    &quot;cancel_reminder&quot;: IdArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L105"></a>105 | <code>    &quot;list_reminders&quot;: ListArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L106"></a>106 | <code>    &quot;schedule_call&quot;: CallCreate,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L107"></a>107 | <code>    &quot;cancel_call&quot;: IdArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L108"></a>108 | <code>    &quot;list_scheduled_calls&quot;: ListArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L109"></a>109 | <code>    &quot;create_linux_worker&quot;: WorkerCreate,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L110"></a>110 | <code>    &quot;destroy_worker&quot;: WorkerArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L111"></a>111 | <code>    &quot;reset_worker&quot;: WorkerArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L112"></a>112 | <code>    &quot;snapshot_worker&quot;: WorkerArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L113"></a>113 | <code>    &quot;restore_worker&quot;: WorkerRestore,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L114"></a>114 | <code>    &quot;get_worker_status&quot;: WorkerArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L115"></a>115 | <code>    &quot;list_workers&quot;: EmptyArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L116"></a>116 | <code>    &quot;start_worker&quot;: WorkerArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L117"></a>117 | <code>    &quot;stop_worker&quot;: WorkerArguments,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L118"></a>118 | <code>    &quot;run_worker_job&quot;: WorkerJob,</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L119"></a>119 | <code>}</code> | Continua/fecha a instrução da linha 97. Define ARGUMENT_SCHEMAS com {&#x27;create_task&#x27;: TaskCreate, &#x27;update_task&#x27;: TaskUpdate, &#x27;complete_task&#x27;: IdArguments, &#x27;list_tasks&#x27;: ListArguments, &#x27;create_reminder&#x27;: ReminderCreate, &#x27;update_reminder&#x27;: ReminderU.... |
| <a id="L120"></a>120 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L121"></a>121 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L122"></a>122 | <code># Documentação: Define o tipo ActionProposal e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo ActionProposal e reúne o estado/contrato descrito para este módulo. |
| <a id="L123"></a>123 | <code>class ActionProposal(StrictModel):</code> | Define o tipo ActionProposal e reúne o estado/contrato descrito para este módulo. |
| <a id="L124"></a>124 | <code>    type: str</code> | Define type com None. |
| <a id="L125"></a>125 | <code>    arguments: dict</code> | Define arguments com None. |
| <a id="L126"></a>126 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L127"></a>127 | <code>    @model_validator(mode=&quot;after&quot;)</code> | Aplica o decorator model_validator(mode=&quot;after&quot;) à definição que segue. |
| <a id="L128"></a>128 | <code>    # Documentação: Confere argumentos contra o schema específico da ação antes do despacho.</code> | Comentário: Documentação: Confere argumentos contra o schema específico da ação antes do despacho. |
| <a id="L129"></a>129 | <code>    def validate_arguments(self):</code> | Confere argumentos contra o schema específico da ação antes do despacho. |
| <a id="L130"></a>130 | <code>        schema = ARGUMENT_SCHEMAS.get(self.type)</code> | Define schema com ARGUMENT_SCHEMAS.get(self.type). Invoca ARGUMENT_SCHEMAS.get com os argumentos declarados nesta instrução. Argumentos: self.type |
| <a id="L131"></a>131 | <code>        if schema is None:</code> | Executa este ramo somente se schema is None; caso contrário, segue o ramo alternativo. |
| <a id="L132"></a>132 | <code>            raise ValueError(&quot;Ação não permitida&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Ação não permitida&#x27;). |
| <a id="L133"></a>133 | <code>        parsed = schema.model_validate(self.arguments)</code> | Define parsed com schema.model_validate(self.arguments). Valida dados de entrada contra o contrato do modelo. Argumentos: self.arguments |
| <a id="L134"></a>134 | <code>        for name in (&quot;due_at&quot;, &quot;datetime&quot;):</code> | Percorre (&#x27;due_at&#x27;, &#x27;datetime&#x27;), atribuindo cada elemento a name. |
| <a id="L135"></a>135 | <code>            value = getattr(parsed, name, None)</code> | Define value com getattr(parsed, name, None). Invoca getattr com os argumentos declarados nesta instrução. Argumentos: parsed, name, None |
| <a id="L136"></a>136 | <code>            if value is not None:</code> | Executa este ramo somente se value is not None; caso contrário, segue o ramo alternativo. |
| <a id="L137"></a>137 | <code>                setattr(parsed, name, value.astimezone(UTC))</code> | Invoca setattr com os argumentos declarados nesta instrução. Argumentos: parsed, name, value.astimezone(UTC) |
| <a id="L138"></a>138 | <code>        self.arguments = parsed.model_dump(mode=&quot;json&quot;, exclude_none=True)</code> | Define self.arguments com parsed.model_dump(mode=&#x27;json&#x27;, exclude_none=True). Serializa o modelo validado para os campos do contrato de saída. Argumentos: mode=&#x27;json&#x27;, exclude_none=True |
| <a id="L139"></a>139 | <code>        return self</code> | Retorna self ao chamador e encerra este caminho da função. |
| <a id="L140"></a>140 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L141"></a>141 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L142"></a>142 | <code># Documentação: Define o tipo MemoryProposal e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo MemoryProposal e reúne o estado/contrato descrito para este módulo. |
| <a id="L143"></a>143 | <code>class MemoryProposal(StrictModel):</code> | Define o tipo MemoryProposal e reúne o estado/contrato descrito para este módulo. |
| <a id="L144"></a>144 | <code>    content: str = Field(min_length=1, max_length=1000)</code> | Define content com Field(min_length=1, max_length=1000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=1000 |
| <a id="L145"></a>145 | <code>    category: Literal[&quot;preference&quot;, &quot;fact&quot;]</code> | Define category com None. |
| <a id="L146"></a>146 | <code>    confidence: float = Field(ge=0, le=1)</code> | Define confidence com Field(ge=0, le=1). Invoca Field com os argumentos declarados nesta instrução. Argumentos: ge=0, le=1 |
| <a id="L147"></a>147 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L148"></a>148 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L149"></a>149 | <code># Documentação: Define o tipo AgentEnvelope e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo AgentEnvelope e reúne o estado/contrato descrito para este módulo. |
| <a id="L150"></a>150 | <code>class AgentEnvelope(StrictModel):</code> | Define o tipo AgentEnvelope e reúne o estado/contrato descrito para este módulo. |
| <a id="L151"></a>151 | <code>    reply: str = Field(min_length=1, max_length=4000)</code> | Define reply com Field(min_length=1, max_length=4000). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=4000 |
| <a id="L152"></a>152 | <code>    actions: list[ActionProposal] = Field(default_factory=list, max_length=8)</code> | Define actions com Field(default_factory=list, max_length=8). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default_factory=list, max_length=8 |
| <a id="L153"></a>153 | <code>    memory_candidates: list[MemoryProposal] = Field(default_factory=list, max_length=5)</code> | Define memory_candidates com Field(default_factory=list, max_length=5). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default_factory=list, max_length=5 |
| <a id="L154"></a>154 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L155"></a>155 | <code>    @field_validator(&quot;reply&quot;)</code> | Aplica o decorator field_validator(&quot;reply&quot;) à definição que segue. |
| <a id="L156"></a>156 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L157"></a>157 | <code>    # Documentação: Implementa AgentEnvelope.not_blank como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa AgentEnvelope.not_blank como parte do fluxo descrito para este |
| <a id="L158"></a>158 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L159"></a>159 | <code>    def not_blank(cls, value):</code> | Implementa AgentEnvelope.not_blank como parte do fluxo descrito para este arquivo. |
| <a id="L160"></a>160 | <code>        if not value.strip():</code> | Executa este ramo somente se not value.strip(); caso contrário, segue o ramo alternativo. |
| <a id="L161"></a>161 | <code>            raise ValueError(&quot;Resposta vazia&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Resposta vazia&#x27;). |
| <a id="L162"></a>162 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L163"></a>163 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L164"></a>164 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L165"></a>165 | <code># Documentação: Define o tipo SummaryEnvelope e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo SummaryEnvelope e reúne o estado/contrato descrito para este módulo. |
| <a id="L166"></a>166 | <code>class SummaryEnvelope(StrictModel):</code> | Define o tipo SummaryEnvelope e reúne o estado/contrato descrito para este módulo. |
| <a id="L167"></a>167 | <code>    summary: str = Field(min_length=1, max_length=1800)</code> | Define summary com Field(min_length=1, max_length=1800). Invoca Field com os argumentos declarados nesta instrução. Argumentos: min_length=1, max_length=1800 |
| <a id="L168"></a>168 | <code>    facts: list[str] = Field(default_factory=list, max_length=8)</code> | Define facts com Field(default_factory=list, max_length=8). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default_factory=list, max_length=8 |
| <a id="L169"></a>169 | <code>    open_topics: list[str] = Field(default_factory=list, max_length=8)</code> | Define open_topics com Field(default_factory=list, max_length=8). Invoca Field com os argumentos declarados nesta instrução. Argumentos: default_factory=list, max_length=8 |
| <a id="L170"></a>170 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L171"></a>171 | <code>    @model_validator(mode=&quot;after&quot;)</code> | Aplica o decorator model_validator(mode=&quot;after&quot;) à definição que segue. |
| <a id="L172"></a>172 | <code>    # Documentação: Implementa SummaryEnvelope.bound_items como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa SummaryEnvelope.bound_items como parte do fluxo descrito para este |
| <a id="L173"></a>173 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L174"></a>174 | <code>    def bound_items(self):</code> | Implementa SummaryEnvelope.bound_items como parte do fluxo descrito para este arquivo. |
| <a id="L175"></a>175 | <code>        if not self.summary.strip() or any(</code> | Executa este ramo somente se not self.summary.strip() or any((not item.strip() or len(item) &gt; 160 for item in self.facts + self.open_topics)); caso contrário, segue o ramo alternativo. |
| <a id="L176"></a>176 | <code>            not item.strip() or len(item) &gt; 160 for item in self.facts + self.open_topics</code> | Continua/fecha a instrução da linha 175. Executa este ramo somente se not self.summary.strip() or any((not item.strip() or len(item) &gt; 160 for item in self.facts + self.open_topics)); caso contrário, segue o ramo alternativo. |
| <a id="L177"></a>177 | <code>        ):</code> | Continua/fecha a instrução da linha 175. Executa este ramo somente se not self.summary.strip() or any((not item.strip() or len(item) &gt; 160 for item in self.facts + self.open_topics)); caso contrário, segue o ramo alternativo. |
| <a id="L178"></a>178 | <code>            raise ValueError(&quot;Resumo excede o limite&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Resumo excede o limite&#x27;). |
| <a id="L179"></a>179 | <code>        return self</code> | Retorna self ao chamador e encerra este caminho da função. |
| <a id="L180"></a>180 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L181"></a>181 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L182"></a>182 | <code># Documentação: Recusa objetos JSON que reutilizam a mesma chave, evitando interpretações</code> | Comentário: Documentação: Recusa objetos JSON que reutilizam a mesma chave, evitando interpretações |
| <a id="L183"></a>183 | <code># divergentes.</code> | Comentário: divergentes. |
| <a id="L184"></a>184 | <code>def reject_duplicate_keys(pairs):</code> | Recusa objetos JSON que reutilizam a mesma chave, evitando interpretações divergentes. |
| <a id="L185"></a>185 | <code>    result = {}</code> | Define result com {}. |
| <a id="L186"></a>186 | <code>    for key, value in pairs:</code> | Percorre pairs, atribuindo cada elemento a (key, value). |
| <a id="L187"></a>187 | <code>        if key in result:</code> | Executa este ramo somente se key in result; caso contrário, segue o ramo alternativo. |
| <a id="L188"></a>188 | <code>            raise ValueError(&quot;Chave duplicada&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Chave duplicada&#x27;). |
| <a id="L189"></a>189 | <code>        result[key] = value</code> | Define result[key] com value. |
| <a id="L190"></a>190 | <code>    return result</code> | Retorna result ao chamador e encerra este caminho da função. |
| <a id="L191"></a>191 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L192"></a>192 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L193"></a>193 | <code># Documentação: Valida envelope JSON estruturado da LLM e recusa resposta fora do contrato.</code> | Comentário: Documentação: Valida envelope JSON estruturado da LLM e recusa resposta fora do contrato. |
| <a id="L194"></a>194 | <code>def parse_response(raw: str, schema=AgentEnvelope):</code> | Valida envelope JSON estruturado da LLM e recusa resposta fora do contrato. |
| <a id="L195"></a>195 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L196"></a>196 | <code>        if len(raw) &gt; 20000:</code> | Executa este ramo somente se len(raw) &gt; 20000; caso contrário, segue o ramo alternativo. |
| <a id="L197"></a>197 | <code>            raise ValueError(&quot;Resposta muito grande&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Resposta muito grande&#x27;). |
| <a id="L198"></a>198 | <code>        data = json.loads(raw, object_pairs_hook=reject_duplicate_keys)</code> | Define data com json.loads(raw, object_pairs_hook=reject_duplicate_keys). Invoca json.loads com os argumentos declarados nesta instrução. Argumentos: raw, object_pairs_hook=reject_duplicate_keys |
| <a id="L199"></a>199 | <code>        return schema.model_validate(data)</code> | Retorna schema.model_validate(data) ao chamador e encerra este caminho da função. |
| <a id="L200"></a>200 | <code>    except (ValueError, TypeError, ValidationError, RecursionError):</code> | Trata exceção (ValueError, TypeError, ValidationError, RecursionError). |
| <a id="L201"></a>201 | <code>        raise InvalidAgentResponse() from None</code> | Interrompe este caminho lançando InvalidAgentResponse(). |
