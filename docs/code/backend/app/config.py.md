# backend/app/config.py

Carrega configuração por variáveis de ambiente e valida limites, timezone, segredo JWT, senha de banco e endereço privado da LLM local. SecretStr oculta valores na representação dos objetos.

[Arquivo fonte](../../../../backend/app/config.py) · 175 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [Settings](#L12) | Define o tipo Settings e reúne o estado/contrato descrito para este módulo. |
| [Settings.validate_context_limits](#L48) | Valida Settings.validate_context_limits, segundo o contrato e as verificações deste módulo. |
| [Settings.validate_local_url](#L63) | Valida Settings.validate_local_url, segundo o contrato e as verificações deste módulo. |
| [Settings.validate_timeout](#L106) | Valida Settings.validate_timeout, segundo o contrato e as verificações deste módulo. |
| [Settings.validate_model](#L115) | Valida Settings.validate_model, segundo o contrato e as verificações deste módulo. |
| [Settings.validate_jwt_secret](#L124) | Valida Settings.validate_jwt_secret, segundo o contrato e as verificações deste módulo. |
| [Settings.validate_db_password](#L133) | Valida Settings.validate_db_password, segundo o contrato e as verificações deste módulo. |
| [Settings.validate_timezone](#L142) | Valida Settings.validate_timezone, segundo o contrato e as verificações deste módulo. |
| [Settings.validate_positive](#L153) | Valida Settings.validate_positive, segundo o contrato e as verificações deste módulo. |
| [Settings.database_url](#L161) | Implementa Settings.database_url como parte do fluxo descrito para este arquivo. |
| [get_settings](#L174) | Obtém get_settings, segundo o contrato e as verificações deste módulo. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>from functools import lru_cache</code> | Importa lru_cache de functools. |
| <a id="L2"></a>2 | <code>from ipaddress import ip_address, ip_network</code> | Importa ip_address, ip_network de ipaddress. |
| <a id="L3"></a>3 | <code>from urllib.parse import urlsplit</code> | Importa urlsplit de urllib.parse. |
| <a id="L4"></a>4 | <code>from zoneinfo import ZoneInfo, ZoneInfoNotFoundError</code> | Importa ZoneInfo, ZoneInfoNotFoundError de zoneinfo. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>from pydantic import SecretStr, field_validator, model_validator</code> | Importa SecretStr, field_validator, model_validator de pydantic. |
| <a id="L7"></a>7 | <code>from pydantic_settings import BaseSettings, SettingsConfigDict</code> | Importa BaseSettings, SettingsConfigDict de pydantic_settings. |
| <a id="L8"></a>8 | <code>from sqlalchemy import URL</code> | Importa URL de sqlalchemy. |
| <a id="L9"></a>9 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L10"></a>10 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L11"></a>11 | <code># Documentação: Define o tipo Settings e reúne o estado/contrato descrito para este módulo.</code> | Comentário: Documentação: Define o tipo Settings e reúne o estado/contrato descrito para este módulo. |
| <a id="L12"></a>12 | <code>class Settings(BaseSettings):</code> | Define o tipo Settings e reúne o estado/contrato descrito para este módulo. |
| <a id="L13"></a>13 | <code>    model_config = SettingsConfigDict(env_file=&quot;.env&quot;, extra=&quot;ignore&quot;, hide_input_in_errors=True)</code> | Define model_config com SettingsConfigDict(env_file=&#x27;.env&#x27;, extra=&#x27;ignore&#x27;, hide_input_in_errors=True). Invoca SettingsConfigDict com os argumentos declarados nesta instrução. Argumentos: env_file=&#x27;.env&#x27;, extra=&#x27;ignore&#x27;, hide_input_in_errors=True |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code>    app_name: str = &quot;DEVLIMA AGENT&quot;</code> | Define app_name com &#x27;DEVLIMA AGENT&#x27;. |
| <a id="L16"></a>16 | <code>    app_environment: str = &quot;production&quot;</code> | Define app_environment com &#x27;production&#x27;. |
| <a id="L17"></a>17 | <code>    enable_api_docs: bool = False</code> | Define enable_api_docs com False. |
| <a id="L18"></a>18 | <code>    postgres_host: str = &quot;postgres&quot;</code> | Define postgres_host com &#x27;postgres&#x27;. |
| <a id="L19"></a>19 | <code>    postgres_port: int = 5432</code> | Define postgres_port com 5432. |
| <a id="L20"></a>20 | <code>    postgres_db: str = &quot;devlima_agent&quot;</code> | Define postgres_db com &#x27;devlima_agent&#x27;. |
| <a id="L21"></a>21 | <code>    postgres_user: str = &quot;agent&quot;</code> | Define postgres_user com &#x27;agent&#x27;. |
| <a id="L22"></a>22 | <code>    postgres_password: SecretStr</code> | Define postgres_password com None. |
| <a id="L23"></a>23 | <code>    jwt_secret: SecretStr</code> | Define jwt_secret com None. |
| <a id="L24"></a>24 | <code>    jwt_issuer: str = &quot;devlima-agent&quot;</code> | Define jwt_issuer com &#x27;devlima-agent&#x27;. |
| <a id="L25"></a>25 | <code>    jwt_audience: str = &quot;devlima-android&quot;</code> | Define jwt_audience com &#x27;devlima-android&#x27;. |
| <a id="L26"></a>26 | <code>    jwt_ttl_minutes: int = 30</code> | Define jwt_ttl_minutes com 30. |
| <a id="L27"></a>27 | <code>    default_timezone: str = &quot;America/Sao_Paulo&quot;</code> | Define default_timezone com &#x27;America/Sao_Paulo&#x27;. |
| <a id="L28"></a>28 | <code>    login_max_attempts: int = 5</code> | Define login_max_attempts com 5. |
| <a id="L29"></a>29 | <code>    login_window_seconds: int = 900</code> | Define login_window_seconds com 900. |
| <a id="L30"></a>30 | <code>    local_llm_base_url: str = &quot;&quot;</code> | Define local_llm_base_url com &#x27;&#x27;. |
| <a id="L31"></a>31 | <code>    local_llm_model: str = &quot;&quot;</code> | Define local_llm_model com &#x27;&#x27;. |
| <a id="L32"></a>32 | <code>    local_llm_timeout: float = 30</code> | Define local_llm_timeout com 30. |
| <a id="L33"></a>33 | <code>    groq_api_key: SecretStr = SecretStr(&quot;&quot;)</code> | Define groq_api_key com SecretStr(&#x27;&#x27;). Invoca SecretStr com os argumentos declarados nesta instrução. Argumentos: &#x27;&#x27; |
| <a id="L34"></a>34 | <code>    groq_model: str = &quot;openai/gpt-oss-120b&quot;</code> | Define groq_model com &#x27;openai/gpt-oss-120b&#x27;. |
| <a id="L35"></a>35 | <code>    groq_timeout: float = 30</code> | Define groq_timeout com 30. |
| <a id="L36"></a>36 | <code>    llm_health_timeout: float = 5</code> | Define llm_health_timeout com 5. |
| <a id="L37"></a>37 | <code>    allow_cloud_fallback: bool = True</code> | Define allow_cloud_fallback com True. |
| <a id="L38"></a>38 | <code>    scheduler_poll_seconds: int = 5</code> | Define scheduler_poll_seconds com 5. |
| <a id="L39"></a>39 | <code>    vm_manager_socket: str = &quot;/run/vm-manager/api.sock&quot;</code> | Define vm_manager_socket com &#x27;/run/vm-manager/api.sock&#x27;. |
| <a id="L40"></a>40 | <code>    vm_manager_token: SecretStr = SecretStr(&quot;&quot;)</code> | Define vm_manager_token com SecretStr(&#x27;&#x27;). Invoca SecretStr com os argumentos declarados nesta instrução. Argumentos: &#x27;&#x27; |
| <a id="L41"></a>41 | <code>    context_recent_messages: int = 8</code> | Define context_recent_messages com 8. |
| <a id="L42"></a>42 | <code>    context_max_chars: int = 12000</code> | Define context_max_chars com 12000. |
| <a id="L43"></a>43 | <code>    summary_trigger_messages: int = 16</code> | Define summary_trigger_messages com 16. |
| <a id="L44"></a>44 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L45"></a>45 | <code>    @model_validator(mode=&quot;after&quot;)</code> | Aplica o decorator model_validator(mode=&quot;after&quot;) à definição que segue. |
| <a id="L46"></a>46 | <code>    # Documentação: Valida Settings.validate_context_limits, segundo o contrato e as verificações</code> | Comentário: Documentação: Valida Settings.validate_context_limits, segundo o contrato e as verificações |
| <a id="L47"></a>47 | <code>    # deste módulo.</code> | Comentário: deste módulo. |
| <a id="L48"></a>48 | <code>    def validate_context_limits(self):</code> | Valida Settings.validate_context_limits, segundo o contrato e as verificações deste módulo. |
| <a id="L49"></a>49 | <code>        if not 1 &lt;= self.scheduler_poll_seconds &lt;= 60:</code> | Executa este ramo somente se not 1 &lt;= self.scheduler_poll_seconds &lt;= 60; caso contrário, segue o ramo alternativo. |
| <a id="L50"></a>50 | <code>            raise ValueError(&quot;Scheduler poll deve ser entre 1 e 60 segundos&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Scheduler poll deve ser entre 1 e 60 segundos&#x27;). |
| <a id="L51"></a>51 | <code>        if not 2 &lt;= self.context_recent_messages &lt;= 16:</code> | Executa este ramo somente se not 2 &lt;= self.context_recent_messages &lt;= 16; caso contrário, segue o ramo alternativo. |
| <a id="L52"></a>52 | <code>            raise ValueError(&quot;Janela de contexto deve ter entre 2 e 16 mensagens&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Janela de contexto deve ter entre 2 e 16 mensagens&#x27;). |
| <a id="L53"></a>53 | <code>        if not 10000 &lt;= self.context_max_chars &lt;= 16000:</code> | Executa este ramo somente se not 10000 &lt;= self.context_max_chars &lt;= 16000; caso contrário, segue o ramo alternativo. |
| <a id="L54"></a>54 | <code>            raise ValueError(&quot;Contexto deve ter entre 10000 e 16000 caracteres&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Contexto deve ter entre 10000 e 16000 caracteres&#x27;). |
| <a id="L55"></a>55 | <code>        if not self.context_recent_messages &lt; self.summary_trigger_messages &lt;= 100:</code> | Executa este ramo somente se not self.context_recent_messages &lt; self.summary_trigger_messages &lt;= 100; caso contrário, segue o ramo alternativo. |
| <a id="L56"></a>56 | <code>            raise ValueError(&quot;Trigger de resumo deve exceder a janela recente e ser até 100&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Trigger de resumo deve exceder a janela recente e ser até 100&#x27;). |
| <a id="L57"></a>57 | <code>        return self</code> | Retorna self ao chamador e encerra este caminho da função. |
| <a id="L58"></a>58 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L59"></a>59 | <code>    @field_validator(&quot;local_llm_base_url&quot;)</code> | Aplica o decorator field_validator(&quot;local_llm_base_url&quot;) à definição que segue. |
| <a id="L60"></a>60 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L61"></a>61 | <code>    # Documentação: Valida Settings.validate_local_url, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Valida Settings.validate_local_url, segundo o contrato e as verificações deste |
| <a id="L62"></a>62 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L63"></a>63 | <code>    def validate_local_url(cls, value: str) -&gt; str:</code> | Valida Settings.validate_local_url, segundo o contrato e as verificações deste módulo. |
| <a id="L64"></a>64 | <code>        if not value:</code> | Executa este ramo somente se not value; caso contrário, segue o ramo alternativo. |
| <a id="L65"></a>65 | <code>            return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L66"></a>66 | <code>        parsed = urlsplit(value)</code> | Define parsed com urlsplit(value). Invoca urlsplit com os argumentos declarados nesta instrução. Argumentos: value |
| <a id="L67"></a>67 | <code>        if (</code> | Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L68"></a>68 | <code>            parsed.scheme not in {&quot;http&quot;, &quot;https&quot;}</code> | Continua/fecha a instrução da linha 67. Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L69"></a>69 | <code>            or not parsed.hostname</code> | Continua/fecha a instrução da linha 67. Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L70"></a>70 | <code>            or parsed.username</code> | Continua/fecha a instrução da linha 67. Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L71"></a>71 | <code>            or parsed.password</code> | Continua/fecha a instrução da linha 67. Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L72"></a>72 | <code>            or parsed.query</code> | Continua/fecha a instrução da linha 67. Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L73"></a>73 | <code>            or parsed.fragment</code> | Continua/fecha a instrução da linha 67. Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L74"></a>74 | <code>        ):</code> | Continua/fecha a instrução da linha 67. Executa este ramo somente se parsed.scheme not in {&#x27;http&#x27;, &#x27;https&#x27;} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment; caso contrário, segue o ramo alternativo. |
| <a id="L75"></a>75 | <code>            raise ValueError(&quot;LOCAL_LLM_BASE_URL deve ser uma URL privada sem credenciais&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;LOCAL_LLM_BASE_URL deve ser uma URL privada sem credenciais&#x27;). |
| <a id="L76"></a>76 | <code>        try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L77"></a>77 | <code>            if parsed.port is not None and not 1 &lt;= parsed.port &lt;= 65535:</code> | Executa este ramo somente se parsed.port is not None and (not 1 &lt;= parsed.port &lt;= 65535); caso contrário, segue o ramo alternativo. |
| <a id="L78"></a>78 | <code>                raise ValueError(&quot;Porta inválida&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Porta inválida&#x27;). |
| <a id="L79"></a>79 | <code>        except ValueError:</code> | Trata exceção ValueError. |
| <a id="L80"></a>80 | <code>            raise ValueError(&quot;Porta da LLM inválida&quot;) from None</code> | Interrompe este caminho lançando ValueError(&#x27;Porta da LLM inválida&#x27;). |
| <a id="L81"></a>81 | <code>        try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L82"></a>82 | <code>            address = ip_address(parsed.hostname)</code> | Define address com ip_address(parsed.hostname). Invoca ip_address com os argumentos declarados nesta instrução. Argumentos: parsed.hostname |
| <a id="L83"></a>83 | <code>        except ValueError:</code> | Trata exceção ValueError. |
| <a id="L84"></a>84 | <code>            if parsed.hostname != &quot;localhost&quot; and not parsed.hostname.endswith(&quot;.ts.net&quot;):</code> | Executa este ramo somente se parsed.hostname != &#x27;localhost&#x27; and (not parsed.hostname.endswith(&#x27;.ts.net&#x27;)); caso contrário, segue o ramo alternativo. |
| <a id="L85"></a>85 | <code>                raise ValueError(</code> | Interrompe este caminho lançando ValueError(&#x27;Use IP privado, localhost ou hostname Tailscale .ts.net&#x27;). |
| <a id="L86"></a>86 | <code>                    &quot;Use IP privado, localhost ou hostname Tailscale .ts.net&quot;</code> | Continua/fecha a instrução da linha 85. Interrompe este caminho lançando ValueError(&#x27;Use IP privado, localhost ou hostname Tailscale .ts.net&#x27;). |
| <a id="L87"></a>87 | <code>                ) from None</code> | Continua/fecha a instrução da linha 85. Interrompe este caminho lançando ValueError(&#x27;Use IP privado, localhost ou hostname Tailscale .ts.net&#x27;). |
| <a id="L88"></a>88 | <code>        else:</code> | Ramo alternativo quando a condição anterior não é satisfeita. |
| <a id="L89"></a>89 | <code>            private_networks = (</code> | Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L90"></a>90 | <code>                &quot;10.0.0.0/8&quot;,</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L91"></a>91 | <code>                &quot;172.16.0.0/12&quot;,</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L92"></a>92 | <code>                &quot;192.168.0.0/16&quot;,</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L93"></a>93 | <code>                &quot;100.64.0.0/10&quot;,</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L94"></a>94 | <code>                &quot;127.0.0.0/8&quot;,</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L95"></a>95 | <code>                &quot;::1/128&quot;,</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L96"></a>96 | <code>                &quot;fc00::/7&quot;,</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L97"></a>97 | <code>            )</code> | Continua/fecha a instrução da linha 89. Define private_networks com (&#x27;10.0.0.0/8&#x27;, &#x27;172.16.0.0/12&#x27;, &#x27;192.168.0.0/16&#x27;, &#x27;100.64.0.0/10&#x27;, &#x27;127.0.0.0/8&#x27;, &#x27;::1/128&#x27;, &#x27;fc00::/7&#x27;). |
| <a id="L98"></a>98 | <code>            if not any(address in ip_network(network) for network in private_networks):</code> | Executa este ramo somente se not any((address in ip_network(network) for network in private_networks)); caso contrário, segue o ramo alternativo. |
| <a id="L99"></a>99 | <code>                raise ValueError(&quot;A LLM primária deve usar endereço privado&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;A LLM primária deve usar endereço privado&#x27;). |
| <a id="L100"></a>100 | <code>        return value.rstrip(&quot;/&quot;)</code> | Retorna value.rstrip(&#x27;/&#x27;) ao chamador e encerra este caminho da função. |
| <a id="L101"></a>101 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L102"></a>102 | <code>    @field_validator(&quot;local_llm_timeout&quot;, &quot;groq_timeout&quot;, &quot;llm_health_timeout&quot;)</code> | Aplica o decorator field_validator(&quot;local_llm_timeout&quot;, &quot;groq_timeout&quot;, &quot;llm_health_timeout&quot;) à definição que segue. |
| <a id="L103"></a>103 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L104"></a>104 | <code>    # Documentação: Valida Settings.validate_timeout, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Valida Settings.validate_timeout, segundo o contrato e as verificações deste |
| <a id="L105"></a>105 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L106"></a>106 | <code>    def validate_timeout(cls, value: float) -&gt; float:</code> | Valida Settings.validate_timeout, segundo o contrato e as verificações deste módulo. |
| <a id="L107"></a>107 | <code>        if not 0 &lt; value &lt;= 120:</code> | Executa este ramo somente se not 0 &lt; value &lt;= 120; caso contrário, segue o ramo alternativo. |
| <a id="L108"></a>108 | <code>            raise ValueError(&quot;Timeout deve estar entre 0 e 120 segundos&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Timeout deve estar entre 0 e 120 segundos&#x27;). |
| <a id="L109"></a>109 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L110"></a>110 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L111"></a>111 | <code>    @field_validator(&quot;local_llm_model&quot;, &quot;groq_model&quot;)</code> | Aplica o decorator field_validator(&quot;local_llm_model&quot;, &quot;groq_model&quot;) à definição que segue. |
| <a id="L112"></a>112 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L113"></a>113 | <code>    # Documentação: Valida Settings.validate_model, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Valida Settings.validate_model, segundo o contrato e as verificações deste |
| <a id="L114"></a>114 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L115"></a>115 | <code>    def validate_model(cls, value: str) -&gt; str:</code> | Valida Settings.validate_model, segundo o contrato e as verificações deste módulo. |
| <a id="L116"></a>116 | <code>        if len(value) &gt; 512 or &quot;\n&quot; in value or &quot;\r&quot; in value:</code> | Executa este ramo somente se len(value) &gt; 512 or &#x27;\n&#x27; in value or &#x27;\r&#x27; in value; caso contrário, segue o ramo alternativo. |
| <a id="L117"></a>117 | <code>            raise ValueError(&quot;Identificador de modelo inválido&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Identificador de modelo inválido&#x27;). |
| <a id="L118"></a>118 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L119"></a>119 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L120"></a>120 | <code>    @field_validator(&quot;jwt_secret&quot;)</code> | Aplica o decorator field_validator(&quot;jwt_secret&quot;) à definição que segue. |
| <a id="L121"></a>121 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L122"></a>122 | <code>    # Documentação: Valida Settings.validate_jwt_secret, segundo o contrato e as verificações</code> | Comentário: Documentação: Valida Settings.validate_jwt_secret, segundo o contrato e as verificações |
| <a id="L123"></a>123 | <code>    # deste módulo.</code> | Comentário: deste módulo. |
| <a id="L124"></a>124 | <code>    def validate_jwt_secret(cls, value: SecretStr) -&gt; SecretStr:</code> | Valida Settings.validate_jwt_secret, segundo o contrato e as verificações deste módulo. |
| <a id="L125"></a>125 | <code>        if len(value.get_secret_value()) &lt; 32:</code> | Executa este ramo somente se len(value.get_secret_value()) &lt; 32; caso contrário, segue o ramo alternativo. |
| <a id="L126"></a>126 | <code>            raise ValueError(&quot;JWT_SECRET deve ter pelo menos 32 caracteres&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;JWT_SECRET deve ter pelo menos 32 caracteres&#x27;). |
| <a id="L127"></a>127 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L128"></a>128 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L129"></a>129 | <code>    @field_validator(&quot;postgres_password&quot;)</code> | Aplica o decorator field_validator(&quot;postgres_password&quot;) à definição que segue. |
| <a id="L130"></a>130 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L131"></a>131 | <code>    # Documentação: Valida Settings.validate_db_password, segundo o contrato e as verificações</code> | Comentário: Documentação: Valida Settings.validate_db_password, segundo o contrato e as verificações |
| <a id="L132"></a>132 | <code>    # deste módulo.</code> | Comentário: deste módulo. |
| <a id="L133"></a>133 | <code>    def validate_db_password(cls, value: SecretStr) -&gt; SecretStr:</code> | Valida Settings.validate_db_password, segundo o contrato e as verificações deste módulo. |
| <a id="L134"></a>134 | <code>        if len(value.get_secret_value()) &lt; 16:</code> | Executa este ramo somente se len(value.get_secret_value()) &lt; 16; caso contrário, segue o ramo alternativo. |
| <a id="L135"></a>135 | <code>            raise ValueError(&quot;POSTGRES_PASSWORD deve ter pelo menos 16 caracteres&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;POSTGRES_PASSWORD deve ter pelo menos 16 caracteres&#x27;). |
| <a id="L136"></a>136 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L137"></a>137 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L138"></a>138 | <code>    @field_validator(&quot;default_timezone&quot;)</code> | Aplica o decorator field_validator(&quot;default_timezone&quot;) à definição que segue. |
| <a id="L139"></a>139 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L140"></a>140 | <code>    # Documentação: Valida Settings.validate_timezone, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Valida Settings.validate_timezone, segundo o contrato e as verificações deste |
| <a id="L141"></a>141 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L142"></a>142 | <code>    def validate_timezone(cls, value: str) -&gt; str:</code> | Valida Settings.validate_timezone, segundo o contrato e as verificações deste módulo. |
| <a id="L143"></a>143 | <code>        try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L144"></a>144 | <code>            ZoneInfo(value)</code> | Invoca ZoneInfo com os argumentos declarados nesta instrução. Argumentos: value |
| <a id="L145"></a>145 | <code>        except ZoneInfoNotFoundError as exc:</code> | Trata exceção ZoneInfoNotFoundError como exc. |
| <a id="L146"></a>146 | <code>            raise ValueError(&quot;Timezone IANA inválido&quot;) from exc</code> | Interrompe este caminho lançando ValueError(&#x27;Timezone IANA inválido&#x27;). |
| <a id="L147"></a>147 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L148"></a>148 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L149"></a>149 | <code>    @field_validator(&quot;jwt_ttl_minutes&quot;, &quot;login_max_attempts&quot;, &quot;login_window_seconds&quot;)</code> | Aplica o decorator field_validator(&quot;jwt_ttl_minutes&quot;, &quot;login_max_attempts&quot;, &quot;login_window_seconds&quot;) à definição que segue. |
| <a id="L150"></a>150 | <code>    @classmethod</code> | Aplica o decorator classmethod à definição que segue. |
| <a id="L151"></a>151 | <code>    # Documentação: Valida Settings.validate_positive, segundo o contrato e as verificações deste</code> | Comentário: Documentação: Valida Settings.validate_positive, segundo o contrato e as verificações deste |
| <a id="L152"></a>152 | <code>    # módulo.</code> | Comentário: módulo. |
| <a id="L153"></a>153 | <code>    def validate_positive(cls, value: int) -&gt; int:</code> | Valida Settings.validate_positive, segundo o contrato e as verificações deste módulo. |
| <a id="L154"></a>154 | <code>        if value &lt; 1:</code> | Executa este ramo somente se value &lt; 1; caso contrário, segue o ramo alternativo. |
| <a id="L155"></a>155 | <code>            raise ValueError(&quot;Valor deve ser positivo&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Valor deve ser positivo&#x27;). |
| <a id="L156"></a>156 | <code>        return value</code> | Retorna value ao chamador e encerra este caminho da função. |
| <a id="L157"></a>157 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L158"></a>158 | <code>    @property</code> | Aplica o decorator property à definição que segue. |
| <a id="L159"></a>159 | <code>    # Documentação: Implementa Settings.database_url como parte do fluxo descrito para este</code> | Comentário: Documentação: Implementa Settings.database_url como parte do fluxo descrito para este |
| <a id="L160"></a>160 | <code>    # arquivo.</code> | Comentário: arquivo. |
| <a id="L161"></a>161 | <code>    def database_url(self) -&gt; URL:</code> | Implementa Settings.database_url como parte do fluxo descrito para este arquivo. |
| <a id="L162"></a>162 | <code>        return URL.create(</code> | Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L163"></a>163 | <code>            &quot;postgresql+psycopg&quot;,</code> | Continua/fecha a instrução da linha 162. Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L164"></a>164 | <code>            username=self.postgres_user,</code> | Continua/fecha a instrução da linha 162. Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L165"></a>165 | <code>            password=self.postgres_password.get_secret_value(),</code> | Continua/fecha a instrução da linha 162. Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L166"></a>166 | <code>            host=self.postgres_host,</code> | Continua/fecha a instrução da linha 162. Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L167"></a>167 | <code>            port=self.postgres_port,</code> | Continua/fecha a instrução da linha 162. Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L168"></a>168 | <code>            database=self.postgres_db,</code> | Continua/fecha a instrução da linha 162. Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L169"></a>169 | <code>        )</code> | Continua/fecha a instrução da linha 162. Retorna URL.create(&#x27;postgresql+psycopg&#x27;, username=self.postgres_user, password=self.postgres_password.get_secret_value(), host=self.postgres_host, port=self.postgres_port, database=self... ao chamador e encerra este caminho da função. |
| <a id="L170"></a>170 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L171"></a>171 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L172"></a>172 | <code>@lru_cache</code> | Aplica o decorator lru_cache à definição que segue. |
| <a id="L173"></a>173 | <code># Documentação: Obtém get_settings, segundo o contrato e as verificações deste módulo.</code> | Comentário: Documentação: Obtém get_settings, segundo o contrato e as verificações deste módulo. |
| <a id="L174"></a>174 | <code>def get_settings() -&gt; Settings:</code> | Obtém get_settings, segundo o contrato e as verificações deste módulo. |
| <a id="L175"></a>175 | <code>    return Settings()</code> | Retorna Settings() ao chamador e encerra este caminho da função. |
