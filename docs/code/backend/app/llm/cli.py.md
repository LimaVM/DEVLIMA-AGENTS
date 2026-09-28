# backend/app/llm/cli.py

Executa diagnóstico do router e dos providers configurados, observando a política de fallback e sem imprimir API keys.

[Arquivo fonte](../../../../../backend/app/llm/cli.py) · 40 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [main](#L13) | Coordena a entrada de linha de comando deste arquivo: Executa diagnóstico do router e dos providers configurados, observando a política de fallback e sem imprimir API keys. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>import argparse</code> | Importa módulo(s) argparse. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L4"></a>4 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L5"></a>5 | <code>from app.config import get_settings</code> | Importa get_settings de app.config. |
| <a id="L6"></a>6 | <code>from app.db.session import get_engine</code> | Importa get_engine de app.db.session. |
| <a id="L7"></a>7 | <code>from app.llm.base import LLMError, LLMMessage</code> | Importa LLMError, LLMMessage de app.llm.base. |
| <a id="L8"></a>8 | <code>from app.llm.service import build_router</code> | Importa build_router de app.llm.service. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L11"></a>11 | <code># Documentação: Coordena a entrada de linha de comando deste arquivo: Executa diagnóstico do</code> | Comentário: Documentação: Coordena a entrada de linha de comando deste arquivo: Executa diagnóstico do |
| <a id="L12"></a>12 | <code># router e dos providers configurados, observando a política de fallback e sem imprimir API keys.</code> | Comentário: router e dos providers configurados, observando a política de fallback e sem imprimir API keys. |
| <a id="L13"></a>13 | <code>def main() -&gt; None:</code> | Coordena a entrada de linha de comando deste arquivo: Executa diagnóstico do router e dos providers configurados, observando a política de fallback e sem imprimir API keys. |
| <a id="L14"></a>14 | <code>    parser = argparse.ArgumentParser(description=&quot;Diagnóstico LLM no host autorizado&quot;)</code> | Define parser com argparse.ArgumentParser(description=&#x27;Diagnóstico LLM no host autorizado&#x27;). Invoca argparse.ArgumentParser com os argumentos declarados nesta instrução. Argumentos: description=&#x27;Diagnóstico LLM no host autorizado&#x27; |
| <a id="L15"></a>15 | <code>    parser.add_argument(&quot;command&quot;, choices=[&quot;health&quot;, &quot;smoke&quot;])</code> | Invoca parser.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;command&#x27;, choices=[&#x27;health&#x27;, &#x27;smoke&#x27;] |
| <a id="L16"></a>16 | <code>    args = parser.parse_args()</code> | Define args com parser.parse_args(). Invoca parser.parse_args com os argumentos declarados nesta instrução. |
| <a id="L17"></a>17 | <code>    with Session(get_engine()) as session, build_router(get_settings(), session) as llm:</code> | Abre contexto(s) Session(get_engine()), build_router(get_settings(), session); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L18"></a>18 | <code>        if args.command == &quot;health&quot;:</code> | Executa este ramo somente se args.command == &#x27;health&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L19"></a>19 | <code>            print(llm.health_check())</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: llm.health_check() |
| <a id="L20"></a>20 | <code>            return</code> | Retorna None ao chamador e encerra este caminho da função. |
| <a id="L21"></a>21 | <code>        try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L22"></a>22 | <code>            result = llm.chat(</code> | Define result com llm.chat([LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: [LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256 |
| <a id="L23"></a>23 | <code>                [LLMMessage(role=&quot;user&quot;, content=&quot;Responda apenas: conexão confirmada.&quot;)],</code> | Continua/fecha a instrução da linha 22. Define result com llm.chat([LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: [LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256 |
| <a id="L24"></a>24 | <code>                max_tokens=256,</code> | Continua/fecha a instrução da linha 22. Define result com llm.chat([LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: [LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256 |
| <a id="L25"></a>25 | <code>            )</code> | Continua/fecha a instrução da linha 22. Define result com llm.chat([LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256). Invoca llm.chat com os argumentos declarados nesta instrução. Argumentos: [LLMMessage(role=&#x27;user&#x27;, content=&#x27;Responda apenas: conexão confirmada.&#x27;)], max_tokens=256 |
| <a id="L26"></a>26 | <code>        except LLMError as error:</code> | Trata exceção LLMError como error. |
| <a id="L27"></a>27 | <code>            parser.exit(1, f&quot;Provider indisponível: {error.code}\n&quot;)</code> | Invoca parser.exit com os argumentos declarados nesta instrução. Argumentos: 1, f&#x27;Provider indisponível: {error.code}\n&#x27; |
| <a id="L28"></a>28 | <code>        print(</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L29"></a>29 | <code>            {</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L30"></a>30 | <code>                &quot;provider&quot;: result.completion.provider,</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L31"></a>31 | <code>                &quot;fallback&quot;: result.fallback_used,</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L32"></a>32 | <code>                &quot;request_id&quot;: str(result.request_id),</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L33"></a>33 | <code>                &quot;latency_ms&quot;: result.latency_ms,</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L34"></a>34 | <code>                &quot;reply&quot;: result.completion.content,</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L35"></a>35 | <code>            }</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L36"></a>36 | <code>        )</code> | Continua/fecha a instrução da linha 28. Invoca print com os argumentos declarados nesta instrução. Argumentos: {&#x27;provider&#x27;: result.completion.provider, &#x27;fallback&#x27;: result.fallback_used, &#x27;request_id&#x27;: str(result.request_id), &#x27;latency_ms&#x27;: result.latency_ms, &#x27;reply&#x27;: result.completion.cont... |
| <a id="L37"></a>37 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L38"></a>38 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L39"></a>39 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L40"></a>40 | <code>    main()</code> | Invoca main com os argumentos declarados nesta instrução. |
