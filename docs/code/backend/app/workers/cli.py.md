# backend/app/workers/cli.py

Executa smoke Core/runner/manager com usuário isolado e operações de worker restritas ao contrato do sistema.

[Arquivo fonte](../../../../../backend/app/workers/cli.py) · 65 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [main](#L19) | Coordena a entrada de linha de comando deste arquivo: Executa smoke Core/runner/manager com usuário isolado e operações de worker restritas ao contrato do sistema. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>&quot;&quot;&quot;Real manager/queue smoke; restricted to the isolated test database.&quot;&quot;&quot;</code> | Define documentação ou conteúdo literal; o texto não é executado como instrução Python. |
| <a id="L2"></a>2 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L3"></a>3 | <code>import json</code> | Importa módulo(s) json. |
| <a id="L4"></a>4 | <code>from uuid import uuid4</code> | Importa uuid4 de uuid. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L7"></a>7 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L8"></a>8 | <code>from app.config import get_settings</code> | Importa get_settings de app.config. |
| <a id="L9"></a>9 | <code>from app.db.session import get_engine</code> | Importa get_engine de app.db.session. |
| <a id="L10"></a>10 | <code>from app.models import User</code> | Importa User de app.models. |
| <a id="L11"></a>11 | <code>from app.security import hash_password</code> | Importa hash_password de app.security. |
| <a id="L12"></a>12 | <code>from app.workers.client import ManagerClient</code> | Importa ManagerClient de app.workers.client. |
| <a id="L13"></a>13 | <code>from app.workers.runner import execute_one</code> | Importa execute_one de app.workers.runner. |
| <a id="L14"></a>14 | <code>from app.workers.service import WorkerService</code> | Importa WorkerService de app.workers.service. |
| <a id="L15"></a>15 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L16"></a>16 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L17"></a>17 | <code># Documentação: Coordena a entrada de linha de comando deste arquivo: Executa smoke</code> | Comentário: Documentação: Coordena a entrada de linha de comando deste arquivo: Executa smoke |
| <a id="L18"></a>18 | <code># Core/runner/manager com usuário isolado e operações de worker restritas ao contrato do sistema.</code> | Comentário: Core/runner/manager com usuário isolado e operações de worker restritas ao contrato do sistema. |
| <a id="L19"></a>19 | <code>def main():</code> | Coordena a entrada de linha de comando deste arquivo: Executa smoke Core/runner/manager com usuário isolado e operações de worker restritas ao contrato do sistema. |
| <a id="L20"></a>20 | <code>    settings = get_settings()</code> | Define settings com get_settings(). Invoca get_settings com os argumentos declarados nesta instrução. |
| <a id="L21"></a>21 | <code>    if settings.postgres_host != &quot;postgres-test&quot; or settings.postgres_db != &quot;devlima_agent_test&quot;:</code> | Executa este ramo somente se settings.postgres_host != &#x27;postgres-test&#x27; or settings.postgres_db != &#x27;devlima_agent_test&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L22"></a>22 | <code>        raise SystemExit(&quot;Smoke requires the isolated test database&quot;)</code> | Interrompe este caminho lançando SystemExit(&#x27;Smoke requires the isolated test database&#x27;). |
| <a id="L23"></a>23 | <code>    manager = ManagerClient(settings)</code> | Define manager com ManagerClient(settings). Invoca ManagerClient com os argumentos declarados nesta instrução. Argumentos: settings |
| <a id="L24"></a>24 | <code>    assert manager.request(&quot;GET&quot;, &quot;/health&quot;)[&quot;status&quot;] == &quot;ok&quot;</code> | Exige que manager.request(&#x27;GET&#x27;, &#x27;/health&#x27;)[&#x27;status&#x27;] == &#x27;ok&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L25"></a>25 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L26"></a>26 | <code>        with Session(get_engine(), expire_on_commit=False) as session:</code> | Abre contexto(s) Session(get_engine(), expire_on_commit=False); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L27"></a>27 | <code>            user = User(</code> | Define user com User(username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27;). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27; |
| <a id="L28"></a>28 | <code>                username=&quot;worker-smoke-&quot; + uuid4().hex[:12],</code> | Continua/fecha a instrução da linha 27. Define user com User(username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27;). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27; |
| <a id="L29"></a>29 | <code>                password_hash=hash_password(uuid4().hex),</code> | Continua/fecha a instrução da linha 27. Define user com User(username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27;). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27; |
| <a id="L30"></a>30 | <code>                timezone=&quot;America/Sao_Paulo&quot;,</code> | Continua/fecha a instrução da linha 27. Define user com User(username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27;). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27; |
| <a id="L31"></a>31 | <code>            )</code> | Continua/fecha a instrução da linha 27. Define user com User(username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27;). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=&#x27;worker-smoke-&#x27; + uuid4().hex[:12], password_hash=hash_password(uuid4().hex), timezone=&#x27;America/Sao_Paulo&#x27; |
| <a id="L32"></a>32 | <code>            session.add(user)</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: user |
| <a id="L33"></a>33 | <code>            session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L34"></a>34 | <code>            service = WorkerService(session, user.id)</code> | Define service com WorkerService(session, user.id). Invoca WorkerService com os argumentos declarados nesta instrução. Argumentos: session, user.id |
| <a id="L35"></a>35 | <code>            create = service.queue(</code> | Define create com service.queue(&#x27;CREATE&#x27;, {&#x27;name&#x27;: &#x27;core-queue-smoke&#x27;, &#x27;vcpu&#x27;: 1, &#x27;ram_mb&#x27;: 1024, &#x27;disk_gb&#x27;: 10}). Invoca service.queue com os argumentos declarados nesta instrução. Argumentos: &#x27;CREATE&#x27;, {&#x27;name&#x27;: &#x27;core-queue-smoke&#x27;, &#x27;vcpu&#x27;: 1, &#x27;ram_mb&#x27;: 1024, &#x27;disk_gb&#x27;: 10} |
| <a id="L36"></a>36 | <code>                &quot;CREATE&quot;, {&quot;name&quot;: &quot;core-queue-smoke&quot;, &quot;vcpu&quot;: 1, &quot;ram_mb&quot;: 1024, &quot;disk_gb&quot;: 10}</code> | Continua/fecha a instrução da linha 35. Define create com service.queue(&#x27;CREATE&#x27;, {&#x27;name&#x27;: &#x27;core-queue-smoke&#x27;, &#x27;vcpu&#x27;: 1, &#x27;ram_mb&#x27;: 1024, &#x27;disk_gb&#x27;: 10}). Invoca service.queue com os argumentos declarados nesta instrução. Argumentos: &#x27;CREATE&#x27;, {&#x27;name&#x27;: &#x27;core-queue-smoke&#x27;, &#x27;vcpu&#x27;: 1, &#x27;ram_mb&#x27;: 1024, &#x27;disk_gb&#x27;: 10} |
| <a id="L37"></a>37 | <code>            )</code> | Continua/fecha a instrução da linha 35. Define create com service.queue(&#x27;CREATE&#x27;, {&#x27;name&#x27;: &#x27;core-queue-smoke&#x27;, &#x27;vcpu&#x27;: 1, &#x27;ram_mb&#x27;: 1024, &#x27;disk_gb&#x27;: 10}). Invoca service.queue com os argumentos declarados nesta instrução. Argumentos: &#x27;CREATE&#x27;, {&#x27;name&#x27;: &#x27;core-queue-smoke&#x27;, &#x27;vcpu&#x27;: 1, &#x27;ram_mb&#x27;: 1024, &#x27;disk_gb&#x27;: 10} |
| <a id="L38"></a>38 | <code>            session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L39"></a>39 | <code>            try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L40"></a>40 | <code>                assert execute_one(session, manager, create.id)</code> | Exige que execute_one(session, manager, create.id) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L41"></a>41 | <code>                assert create.status == &quot;SUCCEEDED&quot;, create.error_code</code> | Exige que create.status == &#x27;SUCCEEDED&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L42"></a>42 | <code>                assert service.worker(create.worker_id).status == &quot;BOOTING&quot;</code> | Exige que service.worker(create.worker_id).status == &#x27;BOOTING&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L43"></a>43 | <code>            finally:</code> | Bloco de finalização executado mesmo quando a operação anterior falha. |
| <a id="L44"></a>44 | <code>                if create.status != &quot;PENDING&quot;:</code> | Executa este ramo somente se create.status != &#x27;PENDING&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L45"></a>45 | <code>                    destroy = service.queue(&quot;DESTROY&quot;, {}, worker_id=create.worker_id)</code> | Define destroy com service.queue(&#x27;DESTROY&#x27;, {}, worker_id=create.worker_id). Invoca service.queue com os argumentos declarados nesta instrução. Argumentos: &#x27;DESTROY&#x27;, {}, worker_id=create.worker_id |
| <a id="L46"></a>46 | <code>                    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L47"></a>47 | <code>                    assert execute_one(session, manager, destroy.id)</code> | Exige que execute_one(session, manager, destroy.id) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L48"></a>48 | <code>                    assert destroy.status == &quot;SUCCEEDED&quot;, destroy.error_code</code> | Exige que destroy.status == &#x27;SUCCEEDED&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L49"></a>49 | <code>                    assert service.worker(create.worker_id).status == &quot;DESTROYED&quot;</code> | Exige que service.worker(create.worker_id).status == &#x27;DESTROYED&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L50"></a>50 | <code>            print(</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L51"></a>51 | <code>                json.dumps(</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L52"></a>52 | <code>                    {</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L53"></a>53 | <code>                        &quot;result&quot;: &quot;passed&quot;,</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L54"></a>54 | <code>                        &quot;core_queue&quot;: True,</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L55"></a>55 | <code>                        &quot;manager_uid&quot;: 10001,</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L56"></a>56 | <code>                        &quot;worker_id&quot;: str(create.worker_id),</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L57"></a>57 | <code>                    }</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L58"></a>58 | <code>                )</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L59"></a>59 | <code>            )</code> | Continua/fecha a instrução da linha 50. Invoca print com os argumentos declarados nesta instrução. Argumentos: json.dumps({&#x27;result&#x27;: &#x27;passed&#x27;, &#x27;core_queue&#x27;: True, &#x27;manager_uid&#x27;: 10001, &#x27;worker_id&#x27;: str(create.worker_id)}) |
| <a id="L60"></a>60 | <code>    finally:</code> | Bloco de finalização executado mesmo quando a operação anterior falha. |
| <a id="L61"></a>61 | <code>        manager.close()</code> | Invoca manager.close com os argumentos declarados nesta instrução. |
| <a id="L62"></a>62 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L63"></a>63 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L64"></a>64 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L65"></a>65 | <code>    main()</code> | Invoca main com os argumentos declarados nesta instrução. |
