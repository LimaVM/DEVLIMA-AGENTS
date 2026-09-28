# backend/tests/test_foundation.py

Conjunto de validações de test_foundation. Fixtures preparam o ambiente; asserts verificam o comportamento observado, e cleanup remove os recursos de teste.

[Arquivo fonte](../../../../backend/tests/test_foundation.py) · 252 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [test_health_and_request_id](#L23) | Verifica o cenário test_health_and_request_id; as condições e resultados esperados aparecem nos asserts. |
| [test_docs_disabled](#L34) | Verifica o cenário test_docs_disabled; as condições e resultados esperados aparecem nos asserts. |
| [test_database_error_does_not_expose_secrets](#L41) | Verifica o cenário test_database_error_does_not_expose_secrets; as condições e resultados esperados aparecem nos asserts. |
| [test_database_error_does_not_expose_secrets.fail](#L44) | Implementa test_database_error_does_not_expose_secrets.fail como parte do fluxo descrito para este arquivo. |
| [test_short_secrets_refused](#L57) | Verifica o cenário test_short_secrets_refused; as condições e resultados esperados aparecem nos asserts. |
| [test_invalid_timezone_refused](#L64) | Verifica o cenário test_invalid_timezone_refused; as condições e resultados esperados aparecem nos asserts. |
| [test_password_hash_and_wrong_password](#L71) | Verifica o cenário test_password_hash_and_wrong_password; as condições e resultados esperados aparecem nos asserts. |
| [test_password_length_policy](#L82) | Verifica o cenário test_password_length_policy; as condições e resultados esperados aparecem nos asserts. |
| [test_authentication_and_audit](#L89) | Verifica o cenário test_authentication_and_audit; as condições e resultados esperados aparecem nos asserts. |
| [test_invalid_login_indistinguishable](#L110) | Verifica o cenário test_invalid_login_indistinguishable; as condições e resultados esperados aparecem nos asserts. |
| [test_missing_or_invalid_auth](#L118) | Verifica o cenário test_missing_or_invalid_auth; as condições e resultados esperados aparecem nos asserts. |
| [test_validation_does_not_echo_password](#L125) | Verifica o cenário test_validation_does_not_echo_password; as condições e resultados esperados aparecem nos asserts. |
| [test_token_signature_audience_and_expiration](#L140) | Verifica o cenário test_token_signature_audience_and_expiration; as condições e resultados esperados aparecem nos asserts. |
| [test_reset_password_revokes_existing_tokens](#L158) | Verifica o cenário test_reset_password_revokes_existing_tokens; as condições e resultados esperados aparecem nos asserts. |
| [test_inactive_user_cannot_login_or_use_token](#L167) | Verifica o cenário test_inactive_user_cannot_login_or_use_token; as condições e resultados esperados aparecem nos asserts. |
| [test_login_limit_persists_across_sessions](#L182) | Verifica o cenário test_login_limit_persists_across_sessions; as condições e resultados esperados aparecem nos asserts. |
| [test_login_limit_atomic_under_concurrency](#L200) | Verifica o cenário test_login_limit_atomic_under_concurrency; as condições e resultados esperados aparecem nos asserts. |
| [test_login_limit_atomic_under_concurrency.attempt](#L205) | Implementa test_login_limit_atomic_under_concurrency.attempt como parte do fluxo descrito para este arquivo. |
| [test_expired_login_window_resets](#L223) | Verifica o cenário test_expired_login_window_resets; as condições e resultados esperados aparecem nos asserts. |
| [test_cli_create_list_reset](#L238) | Verifica o cenário test_cli_create_list_reset; as condições e resultados esperados aparecem nos asserts. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from concurrent.futures import ThreadPoolExecutor</code> | Importa ThreadPoolExecutor de concurrent.futures. |
| <a id="L2"></a>2 | <code>from datetime import UTC, datetime, timedelta</code> | Importa UTC, datetime, timedelta de datetime. |
| <a id="L3"></a>3 | <code>from uuid import UUID, uuid4</code> | Importa UUID, uuid4 de uuid. |
| <a id="L4"></a>4 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L5"></a>5 | <code>import jwt</code> | Importa módulo(s) jwt. |
| <a id="L6"></a>6 | <code>import pytest</code> | Importa módulo(s) pytest. |
| <a id="L7"></a>7 | <code>from fastapi import HTTPException</code> | Importa HTTPException de fastapi. |
| <a id="L8"></a>8 | <code>from pydantic import ValidationError</code> | Importa ValidationError de pydantic. |
| <a id="L9"></a>9 | <code>from sqlalchemy import func, select</code> | Importa func, select de sqlalchemy. |
| <a id="L10"></a>10 | <code>from sqlalchemy.exc import OperationalError</code> | Importa OperationalError de sqlalchemy.exc. |
| <a id="L11"></a>11 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L12"></a>12 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L13"></a>13 | <code>from app import cli</code> | Importa cli de app. |
| <a id="L14"></a>14 | <code>from app.api.auth import consume_login_attempt</code> | Importa consume_login_attempt de app.api.auth. |
| <a id="L15"></a>15 | <code>from app.config import Settings, get_settings</code> | Importa Settings, get_settings de app.config. |
| <a id="L16"></a>16 | <code>from app.db.session import get_engine</code> | Importa get_engine de app.db.session. |
| <a id="L17"></a>17 | <code>from app.models import AuditLog, LoginThrottle, User</code> | Importa AuditLog, LoginThrottle, User de app.models. |
| <a id="L18"></a>18 | <code>from app.security import create_token, decode_token, hash_password, verify_password</code> | Importa create_token, decode_token, hash_password, verify_password de app.security. |
| <a id="L19"></a>19 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L20"></a>20 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L21"></a>21 | <code># Documentação: Verifica o cenário test_health_and_request_id; as condições e resultados esperados</code> | Comentário: Documentação: Verifica o cenário test_health_and_request_id; as condições e resultados esperados |
| <a id="L22"></a>22 | <code># aparecem nos asserts.</code> | Comentário: aparecem nos asserts. |
| <a id="L23"></a>23 | <code>def test_health_and_request_id(client):</code> | Verifica o cenário test_health_and_request_id; as condições e resultados esperados aparecem nos asserts. |
| <a id="L24"></a>24 | <code>    response = client.get(&quot;/health/ready&quot;)</code> | Define response com client.get(&#x27;/health/ready&#x27;). Invoca client.get com os argumentos declarados nesta instrução. Argumentos: &#x27;/health/ready&#x27; |
| <a id="L25"></a>25 | <code>    assert response.status_code == 200</code> | Exige que response.status_code == 200 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L26"></a>26 | <code>    assert response.json()[&quot;schema&quot;] == &quot;0007_calls&quot;</code> | Exige que response.json()[&#x27;schema&#x27;] == &#x27;0007_calls&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L27"></a>27 | <code>    assert UUID(response.headers[&quot;X-Request-ID&quot;])</code> | Exige que UUID(response.headers[&#x27;X-Request-ID&#x27;]) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L28"></a>28 | <code>    assert response.headers[&quot;Cache-Control&quot;] == &quot;no-store&quot;</code> | Exige que response.headers[&#x27;Cache-Control&#x27;] == &#x27;no-store&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L29"></a>29 | <code>    assert client.get(&quot;/health/live&quot;).json()[&quot;status&quot;] == &quot;ok&quot;</code> | Exige que client.get(&#x27;/health/live&#x27;).json()[&#x27;status&#x27;] == &#x27;ok&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L30"></a>30 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L31"></a>31 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L32"></a>32 | <code># Documentação: Verifica o cenário test_docs_disabled; as condições e resultados esperados</code> | Comentário: Documentação: Verifica o cenário test_docs_disabled; as condições e resultados esperados |
| <a id="L33"></a>33 | <code># aparecem nos asserts.</code> | Comentário: aparecem nos asserts. |
| <a id="L34"></a>34 | <code>def test_docs_disabled(client):</code> | Verifica o cenário test_docs_disabled; as condições e resultados esperados aparecem nos asserts. |
| <a id="L35"></a>35 | <code>    assert client.get(&quot;/docs&quot;).status_code == 404</code> | Exige que client.get(&#x27;/docs&#x27;).status_code == 404 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L36"></a>36 | <code>    assert client.get(&quot;/openapi.json&quot;).status_code == 404</code> | Exige que client.get(&#x27;/openapi.json&#x27;).status_code == 404 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L37"></a>37 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L38"></a>38 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L39"></a>39 | <code># Documentação: Verifica o cenário test_database_error_does_not_expose_secrets; as condições e</code> | Comentário: Documentação: Verifica o cenário test_database_error_does_not_expose_secrets; as condições e |
| <a id="L40"></a>40 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L41"></a>41 | <code>def test_database_error_does_not_expose_secrets(client, monkeypatch):</code> | Verifica o cenário test_database_error_does_not_expose_secrets; as condições e resultados esperados aparecem nos asserts. |
| <a id="L42"></a>42 | <code>    # Documentação: Implementa test_database_error_does_not_expose_secrets.fail como parte do</code> | Comentário: Documentação: Implementa test_database_error_does_not_expose_secrets.fail como parte do |
| <a id="L43"></a>43 | <code>    # fluxo descrito para este arquivo.</code> | Comentário: fluxo descrito para este arquivo. |
| <a id="L44"></a>44 | <code>    def fail():</code> | Implementa test_database_error_does_not_expose_secrets.fail como parte do fluxo descrito para este arquivo. |
| <a id="L45"></a>45 | <code>        raise OperationalError(&quot;secret-query&quot;, {&quot;password&quot;: &quot;sensitive&quot;}, Exception(&quot;secret&quot;))</code> | Interrompe este caminho lançando OperationalError(&#x27;secret-query&#x27;, {&#x27;password&#x27;: &#x27;sensitive&#x27;}, Exception(&#x27;secret&#x27;)). |
| <a id="L46"></a>46 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L47"></a>47 | <code>    monkeypatch.setattr(&quot;app.main.get_engine&quot;, fail)</code> | Invoca monkeypatch.setattr com os argumentos declarados nesta instrução. Argumentos: &#x27;app.main.get_engine&#x27;, fail |
| <a id="L48"></a>48 | <code>    response = client.get(&quot;/health/ready&quot;)</code> | Define response com client.get(&#x27;/health/ready&#x27;). Invoca client.get com os argumentos declarados nesta instrução. Argumentos: &#x27;/health/ready&#x27; |
| <a id="L49"></a>49 | <code>    assert response.status_code == 503</code> | Exige que response.status_code == 503 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L50"></a>50 | <code>    assert &quot;secret&quot; not in response.text</code> | Exige que &#x27;secret&#x27; not in response.text seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L51"></a>51 | <code>    assert &quot;sensitive&quot; not in response.text</code> | Exige que &#x27;sensitive&#x27; not in response.text seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L52"></a>52 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L53"></a>53 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L54"></a>54 | <code>@pytest.mark.parametrize(&quot;name,value&quot;, [(&quot;jwt_secret&quot;, &quot;short&quot;), (&quot;postgres_password&quot;, &quot;short&quot;)])</code> | Aplica o decorator pytest.mark.parametrize(&quot;name,value&quot;, [(&quot;jwt_secret&quot;, &quot;short&quot;), (&quot;postgres_password&quot;, &quot;short&quot;)]) à definição que segue. |
| <a id="L55"></a>55 | <code># Documentação: Verifica o cenário test_short_secrets_refused; as condições e resultados esperados</code> | Comentário: Documentação: Verifica o cenário test_short_secrets_refused; as condições e resultados esperados |
| <a id="L56"></a>56 | <code># aparecem nos asserts.</code> | Comentário: aparecem nos asserts. |
| <a id="L57"></a>57 | <code>def test_short_secrets_refused(name, value):</code> | Verifica o cenário test_short_secrets_refused; as condições e resultados esperados aparecem nos asserts. |
| <a id="L58"></a>58 | <code>    with pytest.raises(ValidationError):</code> | Abre contexto(s) pytest.raises(ValidationError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L59"></a>59 | <code>        Settings(**{name: value})</code> | Invoca Settings com os argumentos declarados nesta instrução. Argumentos: **={name: value} |
| <a id="L60"></a>60 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L61"></a>61 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L62"></a>62 | <code># Documentação: Verifica o cenário test_invalid_timezone_refused; as condições e resultados</code> | Comentário: Documentação: Verifica o cenário test_invalid_timezone_refused; as condições e resultados |
| <a id="L63"></a>63 | <code># esperados aparecem nos asserts.</code> | Comentário: esperados aparecem nos asserts. |
| <a id="L64"></a>64 | <code>def test_invalid_timezone_refused():</code> | Verifica o cenário test_invalid_timezone_refused; as condições e resultados esperados aparecem nos asserts. |
| <a id="L65"></a>65 | <code>    with pytest.raises(ValidationError):</code> | Abre contexto(s) pytest.raises(ValidationError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L66"></a>66 | <code>        Settings(default_timezone=&quot;not/a/timezone&quot;)</code> | Invoca Settings com os argumentos declarados nesta instrução. Argumentos: default_timezone=&#x27;not/a/timezone&#x27; |
| <a id="L67"></a>67 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L68"></a>68 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L69"></a>69 | <code># Documentação: Verifica o cenário test_password_hash_and_wrong_password; as condições e</code> | Comentário: Documentação: Verifica o cenário test_password_hash_and_wrong_password; as condições e |
| <a id="L70"></a>70 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L71"></a>71 | <code>def test_password_hash_and_wrong_password():</code> | Verifica o cenário test_password_hash_and_wrong_password; as condições e resultados esperados aparecem nos asserts. |
| <a id="L72"></a>72 | <code>    hashed = hash_password(&quot;test-password-only&quot;)</code> | Define hashed com hash_password(&#x27;test-password-only&#x27;). Invoca hash_password com os argumentos declarados nesta instrução. Argumentos: &#x27;test-password-only&#x27; |
| <a id="L73"></a>73 | <code>    assert hashed.startswith(&quot;$argon2id$&quot;)</code> | Exige que hashed.startswith(&#x27;$argon2id$&#x27;) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L74"></a>74 | <code>    assert verify_password(hashed, &quot;test-password-only&quot;)</code> | Exige que verify_password(hashed, &#x27;test-password-only&#x27;) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L75"></a>75 | <code>    assert not verify_password(hashed, &quot;incorrect&quot;)</code> | Exige que not verify_password(hashed, &#x27;incorrect&#x27;) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L76"></a>76 | <code>    assert not verify_password(&quot;not-a-hash&quot;, &quot;incorrect&quot;)</code> | Exige que not verify_password(&#x27;not-a-hash&#x27;, &#x27;incorrect&#x27;) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L77"></a>77 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L78"></a>78 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L79"></a>79 | <code>@pytest.mark.parametrize(&quot;password&quot;, [&quot;short&quot;, &quot;a&quot; * 1025])</code> | Aplica o decorator pytest.mark.parametrize(&quot;password&quot;, [&quot;short&quot;, &quot;a&quot; * 1025]) à definição que segue. |
| <a id="L80"></a>80 | <code># Documentação: Verifica o cenário test_password_length_policy; as condições e resultados</code> | Comentário: Documentação: Verifica o cenário test_password_length_policy; as condições e resultados |
| <a id="L81"></a>81 | <code># esperados aparecem nos asserts.</code> | Comentário: esperados aparecem nos asserts. |
| <a id="L82"></a>82 | <code>def test_password_length_policy(password):</code> | Verifica o cenário test_password_length_policy; as condições e resultados esperados aparecem nos asserts. |
| <a id="L83"></a>83 | <code>    with pytest.raises(ValueError):</code> | Abre contexto(s) pytest.raises(ValueError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L84"></a>84 | <code>        hash_password(password)</code> | Invoca hash_password com os argumentos declarados nesta instrução. Argumentos: password |
| <a id="L85"></a>85 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L86"></a>86 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L87"></a>87 | <code># Documentação: Verifica o cenário test_authentication_and_audit; as condições e resultados</code> | Comentário: Documentação: Verifica o cenário test_authentication_and_audit; as condições e resultados |
| <a id="L88"></a>88 | <code># esperados aparecem nos asserts.</code> | Comentário: esperados aparecem nos asserts. |
| <a id="L89"></a>89 | <code>def test_authentication_and_audit(client, user, session):</code> | Verifica o cenário test_authentication_and_audit; as condições e resultados esperados aparecem nos asserts. |
| <a id="L90"></a>90 | <code>    response = client.post(</code> | Define response com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;TESTUSER&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;TESTUSER&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;} |
| <a id="L91"></a>91 | <code>        &quot;/auth/login&quot;, json={&quot;username&quot;: &quot;TESTUSER&quot;, &quot;password&quot;: &quot;test-password-only&quot;}</code> | Continua/fecha a instrução da linha 90. Define response com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;TESTUSER&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;TESTUSER&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;} |
| <a id="L92"></a>92 | <code>    )</code> | Continua/fecha a instrução da linha 90. Define response com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;TESTUSER&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;TESTUSER&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;} |
| <a id="L93"></a>93 | <code>    assert response.status_code == 200</code> | Exige que response.status_code == 200 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L94"></a>94 | <code>    assert response.json()[&quot;expires_in&quot;] == 1800</code> | Exige que response.json()[&#x27;expires_in&#x27;] == 1800 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L95"></a>95 | <code>    token = response.json()[&quot;access_token&quot;]</code> | Define token com response.json()[&#x27;access_token&#x27;]. |
| <a id="L96"></a>96 | <code>    me = client.get(&quot;/auth/me&quot;, headers={&quot;Authorization&quot;: f&quot;Bearer {token}&quot;})</code> | Define me com client.get(&#x27;/auth/me&#x27;, headers={&#x27;Authorization&#x27;: f&#x27;Bearer {token}&#x27;}). Invoca client.get com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/me&#x27;, headers={&#x27;Authorization&#x27;: f&#x27;Bearer {token}&#x27;} |
| <a id="L97"></a>97 | <code>    assert me.status_code == 200</code> | Exige que me.status_code == 200 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L98"></a>98 | <code>    assert me.json()[&quot;id&quot;] == str(user.id)</code> | Exige que me.json()[&#x27;id&#x27;] == str(user.id) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L99"></a>99 | <code>    assert me.json()[&quot;timezone&quot;] == &quot;America/Sao_Paulo&quot;</code> | Exige que me.json()[&#x27;timezone&#x27;] == &#x27;America/Sao_Paulo&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L100"></a>100 | <code>    assert &quot;password&quot; not in me.text</code> | Exige que &#x27;password&#x27; not in me.text seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L101"></a>101 | <code>    audit = session.scalar(select(AuditLog).where(AuditLog.event == &quot;auth.login_success&quot;))</code> | Define audit com session.scalar(select(AuditLog).where(AuditLog.event == &#x27;auth.login_success&#x27;)). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(AuditLog).where(AuditLog.event == &#x27;auth.login_success&#x27;) |
| <a id="L102"></a>102 | <code>    assert audit.user_id == user.id</code> | Exige que audit.user_id == user.id seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L103"></a>103 | <code>    assert audit.request_id == response.headers[&quot;X-Request-ID&quot;]</code> | Exige que audit.request_id == response.headers[&#x27;X-Request-ID&#x27;] seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L104"></a>104 | <code>    assert &quot;password&quot; not in str(audit.details)</code> | Exige que &#x27;password&#x27; not in str(audit.details) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L105"></a>105 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L106"></a>106 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L107"></a>107 | <code>@pytest.mark.parametrize(&quot;username&quot;, [&quot;testuser&quot;, &quot;unknown&quot;])</code> | Aplica o decorator pytest.mark.parametrize(&quot;username&quot;, [&quot;testuser&quot;, &quot;unknown&quot;]) à definição que segue. |
| <a id="L108"></a>108 | <code># Documentação: Verifica o cenário test_invalid_login_indistinguishable; as condições e resultados</code> | Comentário: Documentação: Verifica o cenário test_invalid_login_indistinguishable; as condições e resultados |
| <a id="L109"></a>109 | <code># esperados aparecem nos asserts.</code> | Comentário: esperados aparecem nos asserts. |
| <a id="L110"></a>110 | <code>def test_invalid_login_indistinguishable(client, user, username):</code> | Verifica o cenário test_invalid_login_indistinguishable; as condições e resultados esperados aparecem nos asserts. |
| <a id="L111"></a>111 | <code>    response = client.post(&quot;/auth/login&quot;, json={&quot;username&quot;: username, &quot;password&quot;: &quot;incorrect&quot;})</code> | Define response com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: username, &#x27;password&#x27;: &#x27;incorrect&#x27;}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: username, &#x27;password&#x27;: &#x27;incorrect&#x27;} |
| <a id="L112"></a>112 | <code>    assert response.status_code == 401</code> | Exige que response.status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L113"></a>113 | <code>    assert response.json() == {&quot;detail&quot;: &quot;Usuário ou senha inválidos&quot;}</code> | Exige que response.json() == {&#x27;detail&#x27;: &#x27;Usuário ou senha inválidos&#x27;} seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L114"></a>114 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L115"></a>115 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L116"></a>116 | <code># Documentação: Verifica o cenário test_missing_or_invalid_auth; as condições e resultados</code> | Comentário: Documentação: Verifica o cenário test_missing_or_invalid_auth; as condições e resultados |
| <a id="L117"></a>117 | <code># esperados aparecem nos asserts.</code> | Comentário: esperados aparecem nos asserts. |
| <a id="L118"></a>118 | <code>def test_missing_or_invalid_auth(client):</code> | Verifica o cenário test_missing_or_invalid_auth; as condições e resultados esperados aparecem nos asserts. |
| <a id="L119"></a>119 | <code>    assert client.get(&quot;/auth/me&quot;).status_code == 401</code> | Exige que client.get(&#x27;/auth/me&#x27;).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L120"></a>120 | <code>    assert client.get(&quot;/auth/me&quot;, headers={&quot;Authorization&quot;: &quot;Bearer invalid&quot;}).status_code == 401</code> | Exige que client.get(&#x27;/auth/me&#x27;, headers={&#x27;Authorization&#x27;: &#x27;Bearer invalid&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L121"></a>121 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L122"></a>122 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L123"></a>123 | <code># Documentação: Verifica o cenário test_validation_does_not_echo_password; as condições e</code> | Comentário: Documentação: Verifica o cenário test_validation_does_not_echo_password; as condições e |
| <a id="L124"></a>124 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L125"></a>125 | <code>def test_validation_does_not_echo_password(client):</code> | Verifica o cenário test_validation_does_not_echo_password; as condições e resultados esperados aparecem nos asserts. |
| <a id="L126"></a>126 | <code>    secret = &quot;sensitive-input-must-not-be-echoed&quot;</code> | Define secret com &#x27;sensitive-input-must-not-be-echoed&#x27;. |
| <a id="L127"></a>127 | <code>    response = client.post(&quot;/auth/login&quot;, json={&quot;username&quot;: &quot;invalid name&quot;, &quot;password&quot;: secret})</code> | Define response com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;invalid name&#x27;, &#x27;password&#x27;: secret}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;invalid name&#x27;, &#x27;password&#x27;: secret} |
| <a id="L128"></a>128 | <code>    assert response.status_code == 422</code> | Exige que response.status_code == 422 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L129"></a>129 | <code>    assert secret not in response.text</code> | Exige que secret not in response.text seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L130"></a>130 | <code>    assert &quot;input&quot; not in response.json()[&quot;detail&quot;][0]</code> | Exige que &#x27;input&#x27; not in response.json()[&#x27;detail&#x27;][0] seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L131"></a>131 | <code>    extra = client.post(</code> | Define extra com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;user&#x27;, &#x27;password&#x27;: &#x27;valid&#x27;, &#x27;token&#x27;: secret}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;user&#x27;, &#x27;password&#x27;: &#x27;valid&#x27;, &#x27;token&#x27;: secret} |
| <a id="L132"></a>132 | <code>        &quot;/auth/login&quot;, json={&quot;username&quot;: &quot;user&quot;, &quot;password&quot;: &quot;valid&quot;, &quot;token&quot;: secret}</code> | Continua/fecha a instrução da linha 131. Define extra com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;user&#x27;, &#x27;password&#x27;: &#x27;valid&#x27;, &#x27;token&#x27;: secret}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;user&#x27;, &#x27;password&#x27;: &#x27;valid&#x27;, &#x27;token&#x27;: secret} |
| <a id="L133"></a>133 | <code>    )</code> | Continua/fecha a instrução da linha 131. Define extra com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;user&#x27;, &#x27;password&#x27;: &#x27;valid&#x27;, &#x27;token&#x27;: secret}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;user&#x27;, &#x27;password&#x27;: &#x27;valid&#x27;, &#x27;token&#x27;: secret} |
| <a id="L134"></a>134 | <code>    assert extra.status_code == 422</code> | Exige que extra.status_code == 422 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L135"></a>135 | <code>    assert secret not in extra.text</code> | Exige que secret not in extra.text seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L136"></a>136 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L137"></a>137 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L138"></a>138 | <code># Documentação: Verifica o cenário test_token_signature_audience_and_expiration; as condições e</code> | Comentário: Documentação: Verifica o cenário test_token_signature_audience_and_expiration; as condições e |
| <a id="L139"></a>139 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L140"></a>140 | <code>def test_token_signature_audience_and_expiration(user):</code> | Verifica o cenário test_token_signature_audience_and_expiration; as condições e resultados esperados aparecem nos asserts. |
| <a id="L141"></a>141 | <code>    settings = get_settings()</code> | Define settings com get_settings(). Invoca get_settings com os argumentos declarados nesta instrução. |
| <a id="L142"></a>142 | <code>    token = create_token(user, settings)</code> | Define token com create_token(user, settings). Invoca create_token com os argumentos declarados nesta instrução. Argumentos: user, settings |
| <a id="L143"></a>143 | <code>    claims = decode_token(token, settings)</code> | Define claims com decode_token(token, settings). Invoca decode_token com os argumentos declarados nesta instrução. Argumentos: token, settings |
| <a id="L144"></a>144 | <code>    assert claims[&quot;sub&quot;] == str(user.id)</code> | Exige que claims[&#x27;sub&#x27;] == str(user.id) seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L145"></a>145 | <code>    for mutation in ({&quot;aud&quot;: &quot;wrong&quot;}, {&quot;exp&quot;: datetime.now(UTC) - timedelta(seconds=1)}):</code> | Percorre ({&#x27;aud&#x27;: &#x27;wrong&#x27;}, {&#x27;exp&#x27;: datetime.now(UTC) - timedelta(seconds=1)}), atribuindo cada elemento a mutation. |
| <a id="L146"></a>146 | <code>        bad = jwt.encode(</code> | Define bad com jwt.encode(claims &#124; mutation, settings.jwt_secret.get_secret_value(), algorithm=&#x27;HS256&#x27;). Invoca jwt.encode com os argumentos declarados nesta instrução. Argumentos: claims &#124; mutation, settings.jwt_secret.get_secret_value(), algorithm=&#x27;HS256&#x27; |
| <a id="L147"></a>147 | <code>            claims &#124; mutation, settings.jwt_secret.get_secret_value(), algorithm=&quot;HS256&quot;</code> | Continua/fecha a instrução da linha 146. Define bad com jwt.encode(claims &#124; mutation, settings.jwt_secret.get_secret_value(), algorithm=&#x27;HS256&#x27;). Invoca jwt.encode com os argumentos declarados nesta instrução. Argumentos: claims &#124; mutation, settings.jwt_secret.get_secret_value(), algorithm=&#x27;HS256&#x27; |
| <a id="L148"></a>148 | <code>        )</code> | Continua/fecha a instrução da linha 146. Define bad com jwt.encode(claims &#124; mutation, settings.jwt_secret.get_secret_value(), algorithm=&#x27;HS256&#x27;). Invoca jwt.encode com os argumentos declarados nesta instrução. Argumentos: claims &#124; mutation, settings.jwt_secret.get_secret_value(), algorithm=&#x27;HS256&#x27; |
| <a id="L149"></a>149 | <code>        with pytest.raises(jwt.InvalidTokenError):</code> | Abre contexto(s) pytest.raises(jwt.InvalidTokenError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L150"></a>150 | <code>            decode_token(bad, settings)</code> | Invoca decode_token com os argumentos declarados nesta instrução. Argumentos: bad, settings |
| <a id="L151"></a>151 | <code>    forged = jwt.encode(claims, &quot;wrong-secret-that-is-long-enough-1234&quot;, algorithm=&quot;HS256&quot;)</code> | Define forged com jwt.encode(claims, &#x27;wrong-secret-that-is-long-enough-1234&#x27;, algorithm=&#x27;HS256&#x27;). Invoca jwt.encode com os argumentos declarados nesta instrução. Argumentos: claims, &#x27;wrong-secret-that-is-long-enough-1234&#x27;, algorithm=&#x27;HS256&#x27; |
| <a id="L152"></a>152 | <code>    with pytest.raises(jwt.InvalidTokenError):</code> | Abre contexto(s) pytest.raises(jwt.InvalidTokenError); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L153"></a>153 | <code>        decode_token(forged, settings)</code> | Invoca decode_token com os argumentos declarados nesta instrução. Argumentos: forged, settings |
| <a id="L154"></a>154 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L155"></a>155 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L156"></a>156 | <code># Documentação: Verifica o cenário test_reset_password_revokes_existing_tokens; as condições e</code> | Comentário: Documentação: Verifica o cenário test_reset_password_revokes_existing_tokens; as condições e |
| <a id="L157"></a>157 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L158"></a>158 | <code>def test_reset_password_revokes_existing_tokens(client, user, session):</code> | Verifica o cenário test_reset_password_revokes_existing_tokens; as condições e resultados esperados aparecem nos asserts. |
| <a id="L159"></a>159 | <code>    token = create_token(user, get_settings())</code> | Define token com create_token(user, get_settings()). Invoca create_token com os argumentos declarados nesta instrução. Argumentos: user, get_settings() |
| <a id="L160"></a>160 | <code>    user.token_version += 1</code> | Atualiza user.token_version com 1. Contador de revogação comparado com o JWT para invalidar tokens antigos. |
| <a id="L161"></a>161 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L162"></a>162 | <code>    assert client.get(&quot;/auth/me&quot;, headers={&quot;Authorization&quot;: f&quot;Bearer {token}&quot;}).status_code == 401</code> | Exige que client.get(&#x27;/auth/me&#x27;, headers={&#x27;Authorization&#x27;: f&#x27;Bearer {token}&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L163"></a>163 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L164"></a>164 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L165"></a>165 | <code># Documentação: Verifica o cenário test_inactive_user_cannot_login_or_use_token; as condições e</code> | Comentário: Documentação: Verifica o cenário test_inactive_user_cannot_login_or_use_token; as condições e |
| <a id="L166"></a>166 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L167"></a>167 | <code>def test_inactive_user_cannot_login_or_use_token(client, user, session):</code> | Verifica o cenário test_inactive_user_cannot_login_or_use_token; as condições e resultados esperados aparecem nos asserts. |
| <a id="L168"></a>168 | <code>    token = create_token(user, get_settings())</code> | Define token com create_token(user, get_settings()). Invoca create_token com os argumentos declarados nesta instrução. Argumentos: user, get_settings() |
| <a id="L169"></a>169 | <code>    user.is_active = False</code> | Define user.is_active com False. |
| <a id="L170"></a>170 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L171"></a>171 | <code>    assert client.get(&quot;/auth/me&quot;, headers={&quot;Authorization&quot;: f&quot;Bearer {token}&quot;}).status_code == 401</code> | Exige que client.get(&#x27;/auth/me&#x27;, headers={&#x27;Authorization&#x27;: f&#x27;Bearer {token}&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L172"></a>172 | <code>    assert (</code> | Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;testuser&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L173"></a>173 | <code>        client.post(</code> | Continua/fecha a instrução da linha 172. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;testuser&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L174"></a>174 | <code>            &quot;/auth/login&quot;, json={&quot;username&quot;: &quot;testuser&quot;, &quot;password&quot;: &quot;test-password-only&quot;}</code> | Continua/fecha a instrução da linha 172. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;testuser&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L175"></a>175 | <code>        ).status_code</code> | Continua/fecha a instrução da linha 172. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;testuser&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L176"></a>176 | <code>        == 401</code> | Continua/fecha a instrução da linha 172. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;testuser&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L177"></a>177 | <code>    )</code> | Continua/fecha a instrução da linha 172. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;testuser&#x27;, &#x27;password&#x27;: &#x27;test-password-only&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L178"></a>178 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L179"></a>179 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L180"></a>180 | <code># Documentação: Verifica o cenário test_login_limit_persists_across_sessions; as condições e</code> | Comentário: Documentação: Verifica o cenário test_login_limit_persists_across_sessions; as condições e |
| <a id="L181"></a>181 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L182"></a>182 | <code>def test_login_limit_persists_across_sessions(client, session):</code> | Verifica o cenário test_login_limit_persists_across_sessions; as condições e resultados esperados aparecem nos asserts. |
| <a id="L183"></a>183 | <code>    for _ in range(5):</code> | Percorre range(5), atribuindo cada elemento a _. |
| <a id="L184"></a>184 | <code>        assert (</code> | Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L185"></a>185 | <code>            client.post(</code> | Continua/fecha a instrução da linha 184. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L186"></a>186 | <code>                &quot;/auth/login&quot;, json={&quot;username&quot;: &quot;unknown&quot;, &quot;password&quot;: &quot;wrong&quot;}</code> | Continua/fecha a instrução da linha 184. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L187"></a>187 | <code>            ).status_code</code> | Continua/fecha a instrução da linha 184. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L188"></a>188 | <code>            == 401</code> | Continua/fecha a instrução da linha 184. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L189"></a>189 | <code>        )</code> | Continua/fecha a instrução da linha 184. Exige que client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;}).status_code == 401 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L190"></a>190 | <code>    response = client.post(&quot;/auth/login&quot;, json={&quot;username&quot;: &quot;unknown&quot;, &quot;password&quot;: &quot;wrong&quot;})</code> | Define response com client.post(&#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;}). Invoca client.post com os argumentos declarados nesta instrução. Argumentos: &#x27;/auth/login&#x27;, json={&#x27;username&#x27;: &#x27;unknown&#x27;, &#x27;password&#x27;: &#x27;wrong&#x27;} |
| <a id="L191"></a>191 | <code>    assert response.status_code == 429</code> | Exige que response.status_code == 429 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L192"></a>192 | <code>    assert response.headers[&quot;Retry-After&quot;] == &quot;900&quot;</code> | Exige que response.headers[&#x27;Retry-After&#x27;] == &#x27;900&#x27; seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L193"></a>193 | <code>    with Session(get_engine()) as independent:</code> | Abre contexto(s) Session(get_engine()); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L194"></a>194 | <code>        assert independent.scalar(select(LoginThrottle.attempts)) == 6</code> | Exige que independent.scalar(select(LoginThrottle.attempts)) == 6 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L195"></a>195 | <code>    assert session.scalar(select(func.count()).select_from(AuditLog)) == 5</code> | Exige que session.scalar(select(func.count()).select_from(AuditLog)) == 5 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L196"></a>196 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L197"></a>197 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L198"></a>198 | <code># Documentação: Verifica o cenário test_login_limit_atomic_under_concurrency; as condições e</code> | Comentário: Documentação: Verifica o cenário test_login_limit_atomic_under_concurrency; as condições e |
| <a id="L199"></a>199 | <code># resultados esperados aparecem nos asserts.</code> | Comentário: resultados esperados aparecem nos asserts. |
| <a id="L200"></a>200 | <code>def test_login_limit_atomic_under_concurrency():</code> | Verifica o cenário test_login_limit_atomic_under_concurrency; as condições e resultados esperados aparecem nos asserts. |
| <a id="L201"></a>201 | <code>    bucket = str(uuid4())</code> | Define bucket com str(uuid4()). Invoca str com os argumentos declarados nesta instrução. Argumentos: uuid4() |
| <a id="L202"></a>202 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L203"></a>203 | <code>    # Documentação: Implementa test_login_limit_atomic_under_concurrency.attempt como parte do</code> | Comentário: Documentação: Implementa test_login_limit_atomic_under_concurrency.attempt como parte do |
| <a id="L204"></a>204 | <code>    # fluxo descrito para este arquivo.</code> | Comentário: fluxo descrito para este arquivo. |
| <a id="L205"></a>205 | <code>    def attempt(_):</code> | Implementa test_login_limit_atomic_under_concurrency.attempt como parte do fluxo descrito para este arquivo. |
| <a id="L206"></a>206 | <code>        with Session(get_engine()) as db:</code> | Abre contexto(s) Session(get_engine()); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L207"></a>207 | <code>            try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L208"></a>208 | <code>                consume_login_attempt(db, bucket, get_settings())</code> | Invoca consume_login_attempt com os argumentos declarados nesta instrução. Argumentos: db, bucket, get_settings() |
| <a id="L209"></a>209 | <code>                return 200</code> | Retorna 200 ao chamador e encerra este caminho da função. |
| <a id="L210"></a>210 | <code>            except HTTPException as error:</code> | Trata exceção HTTPException como error. |
| <a id="L211"></a>211 | <code>                return error.status_code</code> | Retorna error.status_code ao chamador e encerra este caminho da função. |
| <a id="L212"></a>212 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L213"></a>213 | <code>    with ThreadPoolExecutor(max_workers=10) as pool:</code> | Abre contexto(s) ThreadPoolExecutor(max_workers=10); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L214"></a>214 | <code>        statuses = list(pool.map(attempt, range(10)))</code> | Define statuses com list(pool.map(attempt, range(10))). Invoca list com os argumentos declarados nesta instrução. Argumentos: pool.map(attempt, range(10)) |
| <a id="L215"></a>215 | <code>    assert statuses.count(200) == 5</code> | Exige que statuses.count(200) == 5 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L216"></a>216 | <code>    assert statuses.count(429) == 5</code> | Exige que statuses.count(429) == 5 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L217"></a>217 | <code>    with Session(get_engine()) as db:</code> | Abre contexto(s) Session(get_engine()); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L218"></a>218 | <code>        assert db.get(LoginThrottle, bucket).attempts == 10</code> | Exige que db.get(LoginThrottle, bucket).attempts == 10 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L219"></a>219 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L220"></a>220 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L221"></a>221 | <code># Documentação: Verifica o cenário test_expired_login_window_resets; as condições e resultados</code> | Comentário: Documentação: Verifica o cenário test_expired_login_window_resets; as condições e resultados |
| <a id="L222"></a>222 | <code># esperados aparecem nos asserts.</code> | Comentário: esperados aparecem nos asserts. |
| <a id="L223"></a>223 | <code>def test_expired_login_window_resets(session):</code> | Verifica o cenário test_expired_login_window_resets; as condições e resultados esperados aparecem nos asserts. |
| <a id="L224"></a>224 | <code>    bucket = &quot;old-window&quot;</code> | Define bucket com &#x27;old-window&#x27;. |
| <a id="L225"></a>225 | <code>    session.add(</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: LoginThrottle(bucket=bucket, attempts=99, window_started_at=datetime.now(UTC) - timedelta(hours=1)) |
| <a id="L226"></a>226 | <code>        LoginThrottle(</code> | Continua/fecha a instrução da linha 225. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: LoginThrottle(bucket=bucket, attempts=99, window_started_at=datetime.now(UTC) - timedelta(hours=1)) |
| <a id="L227"></a>227 | <code>            bucket=bucket, attempts=99, window_started_at=datetime.now(UTC) - timedelta(hours=1)</code> | Continua/fecha a instrução da linha 225. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: LoginThrottle(bucket=bucket, attempts=99, window_started_at=datetime.now(UTC) - timedelta(hours=1)) |
| <a id="L228"></a>228 | <code>        )</code> | Continua/fecha a instrução da linha 225. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: LoginThrottle(bucket=bucket, attempts=99, window_started_at=datetime.now(UTC) - timedelta(hours=1)) |
| <a id="L229"></a>229 | <code>    )</code> | Continua/fecha a instrução da linha 225. Invoca session.add com os argumentos declarados nesta instrução. Argumentos: LoginThrottle(bucket=bucket, attempts=99, window_started_at=datetime.now(UTC) - timedelta(hours=1)) |
| <a id="L230"></a>230 | <code>    session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L231"></a>231 | <code>    consume_login_attempt(session, bucket, get_settings())</code> | Invoca consume_login_attempt com os argumentos declarados nesta instrução. Argumentos: session, bucket, get_settings() |
| <a id="L232"></a>232 | <code>    session.expire_all()</code> | Invoca session.expire_all com os argumentos declarados nesta instrução. |
| <a id="L233"></a>233 | <code>    assert session.get(LoginThrottle, bucket).attempts == 1</code> | Exige que session.get(LoginThrottle, bucket).attempts == 1 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L234"></a>234 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L235"></a>235 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L236"></a>236 | <code># Documentação: Verifica o cenário test_cli_create_list_reset; as condições e resultados esperados</code> | Comentário: Documentação: Verifica o cenário test_cli_create_list_reset; as condições e resultados esperados |
| <a id="L237"></a>237 | <code># aparecem nos asserts.</code> | Comentário: aparecem nos asserts. |
| <a id="L238"></a>238 | <code>def test_cli_create_list_reset(monkeypatch, capsys, session):</code> | Verifica o cenário test_cli_create_list_reset; as condições e resultados esperados aparecem nos asserts. |
| <a id="L239"></a>239 | <code>    monkeypatch.setattr(&quot;sys.argv&quot;, [&quot;cli&quot;, &quot;create-user&quot;, &quot;owner&quot;])</code> | Invoca monkeypatch.setattr com os argumentos declarados nesta instrução. Argumentos: &#x27;sys.argv&#x27;, [&#x27;cli&#x27;, &#x27;create-user&#x27;, &#x27;owner&#x27;] |
| <a id="L240"></a>240 | <code>    monkeypatch.setattr(&quot;getpass.getpass&quot;, lambda prompt: &quot;test-password-only&quot;)</code> | Invoca monkeypatch.setattr com os argumentos declarados nesta instrução. Argumentos: &#x27;getpass.getpass&#x27;, lambda prompt: &#x27;test-password-only&#x27; |
| <a id="L241"></a>241 | <code>    cli.main()</code> | Invoca cli.main com os argumentos declarados nesta instrução. |
| <a id="L242"></a>242 | <code>    user = session.scalar(select(User).where(User.username == &quot;owner&quot;))</code> | Define user com session.scalar(select(User).where(User.username == &#x27;owner&#x27;)). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(User).where(User.username == &#x27;owner&#x27;) |
| <a id="L243"></a>243 | <code>    assert user is not None</code> | Exige que user is not None seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L244"></a>244 | <code>    assert user.token_version == 0</code> | Exige que user.token_version == 0 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L245"></a>245 | <code>    monkeypatch.setattr(&quot;sys.argv&quot;, [&quot;cli&quot;, &quot;list-users&quot;])</code> | Invoca monkeypatch.setattr com os argumentos declarados nesta instrução. Argumentos: &#x27;sys.argv&#x27;, [&#x27;cli&#x27;, &#x27;list-users&#x27;] |
| <a id="L246"></a>246 | <code>    cli.main()</code> | Invoca cli.main com os argumentos declarados nesta instrução. |
| <a id="L247"></a>247 | <code>    assert &quot;owner&quot; in capsys.readouterr().out</code> | Exige que &#x27;owner&#x27; in capsys.readouterr().out seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L248"></a>248 | <code>    monkeypatch.setattr(&quot;sys.argv&quot;, [&quot;cli&quot;, &quot;reset-password&quot;, &quot;owner&quot;])</code> | Invoca monkeypatch.setattr com os argumentos declarados nesta instrução. Argumentos: &#x27;sys.argv&#x27;, [&#x27;cli&#x27;, &#x27;reset-password&#x27;, &#x27;owner&#x27;] |
| <a id="L249"></a>249 | <code>    cli.main()</code> | Invoca cli.main com os argumentos declarados nesta instrução. |
| <a id="L250"></a>250 | <code>    session.refresh(user)</code> | Invoca session.refresh com os argumentos declarados nesta instrução. Argumentos: user |
| <a id="L251"></a>251 | <code>    assert user.token_version == 1</code> | Exige que user.token_version == 1 seja verdadeiro; caso contrário, falha com AssertionError. |
| <a id="L252"></a>252 | <code>    assert session.scalar(select(func.count()).select_from(AuditLog)) == 2</code> | Exige que session.scalar(select(func.count()).select_from(AuditLog)) == 2 seja verdadeiro; caso contrário, falha com AssertionError. |
