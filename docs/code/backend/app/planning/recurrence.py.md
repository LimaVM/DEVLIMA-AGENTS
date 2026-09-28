# backend/app/planning/recurrence.py

Valida regras RRULE permitidas e calcula ocorrências com timezone, limites e cuidado com horários locais ambíguos/inexistentes.

[Arquivo fonte](../../../../../backend/app/planning/recurrence.py) · 68 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [rule](#L23) | Implementa rule como parte do fluxo descrito para este arquivo. |
| [first_occurrence](#L50) | Implementa first_occurrence como parte do fluxo descrito para este arquivo. |
| [next_occurrence](#L62) | Implementa next_occurrence como parte do fluxo descrito para este arquivo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>import re</code> | Importa módulo(s) re. |
| <a id="L2"></a>2 | <code>from datetime import UTC, datetime, timedelta</code> | Importa UTC, datetime, timedelta de datetime. |
| <a id="L3"></a>3 | <code>from zoneinfo import ZoneInfo</code> | Importa ZoneInfo de zoneinfo. |
| <a id="L4"></a>4 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L5"></a>5 | <code>from dateutil.rrule import rrulestr</code> | Importa rrulestr de dateutil.rrule. |
| <a id="L6"></a>6 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L7"></a>7 | <code>from app.agent.errors import AgentError</code> | Importa AgentError de app.agent.errors. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>ALLOWED_FIELDS = {</code> | Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L10"></a>10 | <code>    &quot;FREQ&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L11"></a>11 | <code>    &quot;INTERVAL&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L12"></a>12 | <code>    &quot;BYDAY&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L13"></a>13 | <code>    &quot;BYMONTHDAY&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L14"></a>14 | <code>    &quot;BYMONTH&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L15"></a>15 | <code>    &quot;BYHOUR&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L16"></a>16 | <code>    &quot;BYMINUTE&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L17"></a>17 | <code>    &quot;COUNT&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L18"></a>18 | <code>    &quot;UNTIL&quot;,</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L19"></a>19 | <code>}</code> | Continua/fecha a instrução da linha 9. Define ALLOWED_FIELDS com {&#x27;FREQ&#x27;, &#x27;INTERVAL&#x27;, &#x27;BYDAY&#x27;, &#x27;BYMONTHDAY&#x27;, &#x27;BYMONTH&#x27;, &#x27;BYHOUR&#x27;, &#x27;BYMINUTE&#x27;, &#x27;COUNT&#x27;, &#x27;UNTIL&#x27;}. |
| <a id="L20"></a>20 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L22"></a>22 | <code># Documentação: Implementa rule como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa rule como parte do fluxo descrito para este arquivo. |
| <a id="L23"></a>23 | <code>def rule(text: str, start: datetime, timezone: str):</code> | Implementa rule como parte do fluxo descrito para este arquivo. |
| <a id="L24"></a>24 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L25"></a>25 | <code>        parts = text.upper().removeprefix(&quot;RRULE:&quot;).split(&quot;;&quot;)</code> | Define parts com text.upper().removeprefix(&#x27;RRULE:&#x27;).split(&#x27;;&#x27;). Invoca text.upper().removeprefix(&#x27;RRULE:&#x27;).split com os argumentos declarados nesta instrução. Argumentos: &#x27;;&#x27; |
| <a id="L26"></a>26 | <code>        fields = {}</code> | Define fields com {}. |
| <a id="L27"></a>27 | <code>        for part in parts:</code> | Percorre parts, atribuindo cada elemento a part. |
| <a id="L28"></a>28 | <code>            key, value = part.split(&quot;=&quot;, 1)</code> | Define (key, value) com part.split(&#x27;=&#x27;, 1). Invoca part.split com os argumentos declarados nesta instrução. Argumentos: &#x27;=&#x27;, 1 |
| <a id="L29"></a>29 | <code>            if key not in ALLOWED_FIELDS or key in fields or len(value.split(&quot;,&quot;)) &gt; 8:</code> | Executa este ramo somente se key not in ALLOWED_FIELDS or key in fields or len(value.split(&#x27;,&#x27;)) &gt; 8; caso contrário, segue o ramo alternativo. |
| <a id="L30"></a>30 | <code>                raise ValueError()</code> | Interrompe este caminho lançando ValueError(). |
| <a id="L31"></a>31 | <code>            if not re.fullmatch(r&quot;[A-Z0-9,+-]+&quot;, value):</code> | Executa este ramo somente se not re.fullmatch(&#x27;[A-Z0-9,+-]+&#x27;, value); caso contrário, segue o ramo alternativo. |
| <a id="L32"></a>32 | <code>                raise ValueError()</code> | Interrompe este caminho lançando ValueError(). |
| <a id="L33"></a>33 | <code>            fields[key] = value</code> | Define fields[key] com value. |
| <a id="L34"></a>34 | <code>        if fields.get(&quot;FREQ&quot;) not in {&quot;DAILY&quot;, &quot;WEEKLY&quot;, &quot;MONTHLY&quot;, &quot;YEARLY&quot;}:</code> | Executa este ramo somente se fields.get(&#x27;FREQ&#x27;) not in {&#x27;DAILY&#x27;, &#x27;WEEKLY&#x27;, &#x27;MONTHLY&#x27;, &#x27;YEARLY&#x27;}; caso contrário, segue o ramo alternativo. |
| <a id="L35"></a>35 | <code>            raise ValueError()</code> | Interrompe este caminho lançando ValueError(). |
| <a id="L36"></a>36 | <code>        if &quot;COUNT&quot; in fields and (&quot;UNTIL&quot; in fields or not 1 &lt;= int(fields[&quot;COUNT&quot;]) &lt;= 10000):</code> | Executa este ramo somente se &#x27;COUNT&#x27; in fields and (&#x27;UNTIL&#x27; in fields or not 1 &lt;= int(fields[&#x27;COUNT&#x27;]) &lt;= 10000); caso contrário, segue o ramo alternativo. |
| <a id="L37"></a>37 | <code>            raise ValueError()</code> | Interrompe este caminho lançando ValueError(). |
| <a id="L38"></a>38 | <code>        if not 1 &lt;= int(fields.get(&quot;INTERVAL&quot;, 1)) &lt;= 100:</code> | Executa este ramo somente se not 1 &lt;= int(fields.get(&#x27;INTERVAL&#x27;, 1)) &lt;= 100; caso contrário, segue o ramo alternativo. |
| <a id="L39"></a>39 | <code>            raise ValueError()</code> | Interrompe este caminho lançando ValueError(). |
| <a id="L40"></a>40 | <code>        return rrulestr(</code> | Retorna rrulestr(&#x27;;&#x27;.join((f&#x27;{key}={value}&#x27; for key, value in fields.items())), dtstart=start.astimezone(ZoneInfo(timezone)), cache=False) ao chamador e encerra este caminho da função. |
| <a id="L41"></a>41 | <code>            &quot;;&quot;.join(f&quot;{key}={value}&quot; for key, value in fields.items()),</code> | Continua/fecha a instrução da linha 40. Retorna rrulestr(&#x27;;&#x27;.join((f&#x27;{key}={value}&#x27; for key, value in fields.items())), dtstart=start.astimezone(ZoneInfo(timezone)), cache=False) ao chamador e encerra este caminho da função. |
| <a id="L42"></a>42 | <code>            dtstart=start.astimezone(ZoneInfo(timezone)),</code> | Continua/fecha a instrução da linha 40. Retorna rrulestr(&#x27;;&#x27;.join((f&#x27;{key}={value}&#x27; for key, value in fields.items())), dtstart=start.astimezone(ZoneInfo(timezone)), cache=False) ao chamador e encerra este caminho da função. |
| <a id="L43"></a>43 | <code>            cache=False,</code> | Continua/fecha a instrução da linha 40. Retorna rrulestr(&#x27;;&#x27;.join((f&#x27;{key}={value}&#x27; for key, value in fields.items())), dtstart=start.astimezone(ZoneInfo(timezone)), cache=False) ao chamador e encerra este caminho da função. |
| <a id="L44"></a>44 | <code>        )</code> | Continua/fecha a instrução da linha 40. Retorna rrulestr(&#x27;;&#x27;.join((f&#x27;{key}={value}&#x27; for key, value in fields.items())), dtstart=start.astimezone(ZoneInfo(timezone)), cache=False) ao chamador e encerra este caminho da função. |
| <a id="L45"></a>45 | <code>    except (ValueError, TypeError, OverflowError, KeyError):</code> | Trata exceção (ValueError, TypeError, OverflowError, KeyError). |
| <a id="L46"></a>46 | <code>        raise AgentError(&quot;invalid_recurrence&quot;, 422) from None</code> | Interrompe este caminho lançando AgentError(&#x27;invalid_recurrence&#x27;, 422). |
| <a id="L47"></a>47 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L48"></a>48 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L49"></a>49 | <code># Documentação: Implementa first_occurrence como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa first_occurrence como parte do fluxo descrito para este arquivo. |
| <a id="L50"></a>50 | <code>def first_occurrence(text: str &#124; None, start: datetime, timezone: str) -&gt; datetime:</code> | Implementa first_occurrence como parte do fluxo descrito para este arquivo. |
| <a id="L51"></a>51 | <code>    if not text:</code> | Executa este ramo somente se not text; caso contrário, segue o ramo alternativo. |
| <a id="L52"></a>52 | <code>        return start.astimezone(UTC)</code> | Retorna start.astimezone(UTC) ao chamador e encerra este caminho da função. |
| <a id="L53"></a>53 | <code>    occurrence = rule(text, start, timezone).after(</code> | Define occurrence com rule(text, start, timezone).after(start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1)). Invoca rule(text, start, timezone).after com os argumentos declarados nesta instrução. Argumentos: start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1) |
| <a id="L54"></a>54 | <code>        start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1)</code> | Continua/fecha a instrução da linha 53. Define occurrence com rule(text, start, timezone).after(start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1)). Invoca rule(text, start, timezone).after com os argumentos declarados nesta instrução. Argumentos: start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1) |
| <a id="L55"></a>55 | <code>    )</code> | Continua/fecha a instrução da linha 53. Define occurrence com rule(text, start, timezone).after(start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1)). Invoca rule(text, start, timezone).after com os argumentos declarados nesta instrução. Argumentos: start.astimezone(ZoneInfo(timezone)) - timedelta(microseconds=1) |
| <a id="L56"></a>56 | <code>    if occurrence is None:</code> | Executa este ramo somente se occurrence is None; caso contrário, segue o ramo alternativo. |
| <a id="L57"></a>57 | <code>        raise AgentError(&quot;recurrence_has_no_occurrence&quot;, 422)</code> | Interrompe este caminho lançando AgentError(&#x27;recurrence_has_no_occurrence&#x27;, 422). |
| <a id="L58"></a>58 | <code>    return occurrence.astimezone(UTC)</code> | Retorna occurrence.astimezone(UTC) ao chamador e encerra este caminho da função. |
| <a id="L59"></a>59 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L60"></a>60 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L61"></a>61 | <code># Documentação: Implementa next_occurrence como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa next_occurrence como parte do fluxo descrito para este arquivo. |
| <a id="L62"></a>62 | <code>def next_occurrence(</code> | Implementa next_occurrence como parte do fluxo descrito para este arquivo. |
| <a id="L63"></a>63 | <code>    text: str &#124; None, start: datetime, timezone: str, after: datetime</code> | Continua/fecha a instrução da linha 62. Implementa next_occurrence como parte do fluxo descrito para este arquivo. |
| <a id="L64"></a>64 | <code>) -&gt; datetime &#124; None:</code> | Continua/fecha a instrução da linha 62. Implementa next_occurrence como parte do fluxo descrito para este arquivo. |
| <a id="L65"></a>65 | <code>    if not text:</code> | Executa este ramo somente se not text; caso contrário, segue o ramo alternativo. |
| <a id="L66"></a>66 | <code>        return None</code> | Retorna None ao chamador e encerra este caminho da função. |
| <a id="L67"></a>67 | <code>    result = rule(text, start, timezone).after(after.astimezone(ZoneInfo(timezone)))</code> | Define result com rule(text, start, timezone).after(after.astimezone(ZoneInfo(timezone))). Invoca rule(text, start, timezone).after com os argumentos declarados nesta instrução. Argumentos: after.astimezone(ZoneInfo(timezone)) |
| <a id="L68"></a>68 | <code>    return result.astimezone(UTC) if result else None</code> | Retorna result.astimezone(UTC) if result else None ao chamador e encerra este caminho da função. |
