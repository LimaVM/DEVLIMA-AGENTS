# backend/app/cli.py

Administra usuários pela linha de comando do ambiente operacional. Solicita senha sem eco, valida identidade/fuso e audita criação ou redefinição.

[Arquivo fonte](../../../../backend/app/cli.py) · 73 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Símbolos e responsabilidades

| Símbolo | Finalidade |
| --- | --- |
| [read_password](#L16) | Implementa read_password como parte do fluxo descrito para este arquivo. |
| [main](#L27) | Coordena a entrada de linha de comando deste arquivo: Administra usuários pela linha de comando do ambiente operacional. Solicita senha sem eco, valida identidade/fuso e audita criação ou redefinição. |

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>import argparse</code> | Importa módulo(s) argparse. |
| <a id="L2"></a>2 | <code>import getpass</code> | Importa módulo(s) getpass. |
| <a id="L3"></a>3 | <code>import re</code> | Importa módulo(s) re. |
| <a id="L4"></a>4 | <code>from zoneinfo import ZoneInfo</code> | Importa ZoneInfo de zoneinfo. |
| <a id="L5"></a>5 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L6"></a>6 | <code>from sqlalchemy import select</code> | Importa select de sqlalchemy. |
| <a id="L7"></a>7 | <code>from sqlalchemy.orm import Session</code> | Importa Session de sqlalchemy.orm. |
| <a id="L8"></a>8 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L9"></a>9 | <code>from app.config import get_settings</code> | Importa get_settings de app.config. |
| <a id="L10"></a>10 | <code>from app.db.session import get_engine</code> | Importa get_engine de app.db.session. |
| <a id="L11"></a>11 | <code>from app.models import AuditLog, User</code> | Importa AuditLog, User de app.models. |
| <a id="L12"></a>12 | <code>from app.security import hash_password</code> | Importa hash_password de app.security. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L14"></a>14 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L15"></a>15 | <code># Documentação: Implementa read_password como parte do fluxo descrito para este arquivo.</code> | Comentário: Documentação: Implementa read_password como parte do fluxo descrito para este arquivo. |
| <a id="L16"></a>16 | <code>def read_password() -&gt; str:</code> | Implementa read_password como parte do fluxo descrito para este arquivo. |
| <a id="L17"></a>17 | <code>    first = getpass.getpass(&quot;Senha (mínimo 12 caracteres): &quot;)</code> | Define first com getpass.getpass(&#x27;Senha (mínimo 12 caracteres): &#x27;). Invoca getpass.getpass com os argumentos declarados nesta instrução. Argumentos: &#x27;Senha (mínimo 12 caracteres): &#x27; |
| <a id="L18"></a>18 | <code>    second = getpass.getpass(&quot;Confirmar senha: &quot;)</code> | Define second com getpass.getpass(&#x27;Confirmar senha: &#x27;). Invoca getpass.getpass com os argumentos declarados nesta instrução. Argumentos: &#x27;Confirmar senha: &#x27; |
| <a id="L19"></a>19 | <code>    if first != second:</code> | Executa este ramo somente se first != second; caso contrário, segue o ramo alternativo. |
| <a id="L20"></a>20 | <code>        raise ValueError(&quot;As senhas não coincidem&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;As senhas não coincidem&#x27;). |
| <a id="L21"></a>21 | <code>    return first</code> | Retorna first ao chamador e encerra este caminho da função. |
| <a id="L22"></a>22 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L23"></a>23 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L24"></a>24 | <code># Documentação: Coordena a entrada de linha de comando deste arquivo: Administra usuários pela</code> | Comentário: Documentação: Coordena a entrada de linha de comando deste arquivo: Administra usuários pela |
| <a id="L25"></a>25 | <code># linha de comando do ambiente operacional. Solicita senha sem eco, valida identidade/fuso e</code> | Comentário: linha de comando do ambiente operacional. Solicita senha sem eco, valida identidade/fuso e |
| <a id="L26"></a>26 | <code># audita criação ou redefinição.</code> | Comentário: audita criação ou redefinição. |
| <a id="L27"></a>27 | <code>def main() -&gt; None:</code> | Coordena a entrada de linha de comando deste arquivo: Administra usuários pela linha de comando do ambiente operacional. Solicita senha sem eco, valida identidade/fuso e audita criação ou redefinição. |
| <a id="L28"></a>28 | <code>    parser = argparse.ArgumentParser(description=&quot;Administração DEVLIMA AGENT&quot;)</code> | Define parser com argparse.ArgumentParser(description=&#x27;Administração DEVLIMA AGENT&#x27;). Invoca argparse.ArgumentParser com os argumentos declarados nesta instrução. Argumentos: description=&#x27;Administração DEVLIMA AGENT&#x27; |
| <a id="L29"></a>29 | <code>    commands = parser.add_subparsers(dest=&quot;command&quot;, required=True)</code> | Define commands com parser.add_subparsers(dest=&#x27;command&#x27;, required=True). Invoca parser.add_subparsers com os argumentos declarados nesta instrução. Argumentos: dest=&#x27;command&#x27;, required=True |
| <a id="L30"></a>30 | <code>    create = commands.add_parser(&quot;create-user&quot;)</code> | Define create com commands.add_parser(&#x27;create-user&#x27;). Invoca commands.add_parser com os argumentos declarados nesta instrução. Argumentos: &#x27;create-user&#x27; |
| <a id="L31"></a>31 | <code>    create.add_argument(&quot;username&quot;)</code> | Invoca create.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;username&#x27; |
| <a id="L32"></a>32 | <code>    create.add_argument(&quot;--timezone&quot;, default=get_settings().default_timezone)</code> | Invoca create.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;--timezone&#x27;, default=get_settings().default_timezone |
| <a id="L33"></a>33 | <code>    reset = commands.add_parser(&quot;reset-password&quot;)</code> | Define reset com commands.add_parser(&#x27;reset-password&#x27;). Invoca commands.add_parser com os argumentos declarados nesta instrução. Argumentos: &#x27;reset-password&#x27; |
| <a id="L34"></a>34 | <code>    reset.add_argument(&quot;username&quot;)</code> | Invoca reset.add_argument com os argumentos declarados nesta instrução. Argumentos: &#x27;username&#x27; |
| <a id="L35"></a>35 | <code>    commands.add_parser(&quot;list-users&quot;)</code> | Invoca commands.add_parser com os argumentos declarados nesta instrução. Argumentos: &#x27;list-users&#x27; |
| <a id="L36"></a>36 | <code>    args = parser.parse_args()</code> | Define args com parser.parse_args(). Invoca parser.parse_args com os argumentos declarados nesta instrução. |
| <a id="L37"></a>37 | <code>    try:</code> | Delimita operações cujas falhas são tratadas pelos except/finally abaixo. |
| <a id="L38"></a>38 | <code>        with Session(get_engine()) as session:</code> | Abre contexto(s) Session(get_engine()); a saída do bloco executa a liberação/fechamento definidos por cada contexto. |
| <a id="L39"></a>39 | <code>            if args.command == &quot;list-users&quot;:</code> | Executa este ramo somente se args.command == &#x27;list-users&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L40"></a>40 | <code>                for user in session.scalars(select(User).order_by(User.username)):</code> | Percorre session.scalars(select(User).order_by(User.username)), atribuindo cada elemento a user. |
| <a id="L41"></a>41 | <code>                    print(f&quot;{user.id} {user.username} {user.timezone} active={user.is_active}&quot;)</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: f&#x27;{user.id} {user.username} {user.timezone} active={user.is_active}&#x27; |
| <a id="L42"></a>42 | <code>                return</code> | Retorna None ao chamador e encerra este caminho da função. |
| <a id="L43"></a>43 | <code>            username = args.username.lower()</code> | Define username com args.username.lower(). Invoca args.username.lower com os argumentos declarados nesta instrução. |
| <a id="L44"></a>44 | <code>            if not re.fullmatch(r&quot;[a-z0-9_.-]{1,80}&quot;, username):</code> | Executa este ramo somente se not re.fullmatch(&#x27;[a-z0-9_.-]{1,80}&#x27;, username); caso contrário, segue o ramo alternativo. |
| <a id="L45"></a>45 | <code>                raise ValueError(&quot;Nome de usuário inválido&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Nome de usuário inválido&#x27;). |
| <a id="L46"></a>46 | <code>            user = session.scalar(select(User).where(User.username == username))</code> | Define user com session.scalar(select(User).where(User.username == username)). Invoca session.scalar com os argumentos declarados nesta instrução. Argumentos: select(User).where(User.username == username) |
| <a id="L47"></a>47 | <code>            if args.command == &quot;create-user&quot;:</code> | Executa este ramo somente se args.command == &#x27;create-user&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L48"></a>48 | <code>                if user:</code> | Executa este ramo somente se user; caso contrário, segue o ramo alternativo. |
| <a id="L49"></a>49 | <code>                    raise ValueError(&quot;Usuário já existe&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Usuário já existe&#x27;). |
| <a id="L50"></a>50 | <code>                ZoneInfo(args.timezone)</code> | Invoca ZoneInfo com os argumentos declarados nesta instrução. Argumentos: args.timezone |
| <a id="L51"></a>51 | <code>                user = User(</code> | Define user com User(username=username, timezone=args.timezone, password_hash=hash_password(read_password())). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=username, timezone=args.timezone, password_hash=hash_password(read_password()) |
| <a id="L52"></a>52 | <code>                    username=username,</code> | Continua/fecha a instrução da linha 51. Define user com User(username=username, timezone=args.timezone, password_hash=hash_password(read_password())). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=username, timezone=args.timezone, password_hash=hash_password(read_password()) |
| <a id="L53"></a>53 | <code>                    timezone=args.timezone,</code> | Continua/fecha a instrução da linha 51. Define user com User(username=username, timezone=args.timezone, password_hash=hash_password(read_password())). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=username, timezone=args.timezone, password_hash=hash_password(read_password()) |
| <a id="L54"></a>54 | <code>                    password_hash=hash_password(read_password()),</code> | Continua/fecha a instrução da linha 51. Define user com User(username=username, timezone=args.timezone, password_hash=hash_password(read_password())). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=username, timezone=args.timezone, password_hash=hash_password(read_password()) |
| <a id="L55"></a>55 | <code>                )</code> | Continua/fecha a instrução da linha 51. Define user com User(username=username, timezone=args.timezone, password_hash=hash_password(read_password())). Invoca User com os argumentos declarados nesta instrução. Argumentos: username=username, timezone=args.timezone, password_hash=hash_password(read_password()) |
| <a id="L56"></a>56 | <code>                session.add(user)</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: user |
| <a id="L57"></a>57 | <code>                session.flush()</code> | Envia alterações pendentes ao banco sem confirmar a transação. |
| <a id="L58"></a>58 | <code>                event = &quot;admin.user_created&quot;</code> | Define event com &#x27;admin.user_created&#x27;. |
| <a id="L59"></a>59 | <code>            else:</code> | Ramo alternativo quando a condição anterior não é satisfeita. |
| <a id="L60"></a>60 | <code>                if user is None:</code> | Executa este ramo somente se user is None; caso contrário, segue o ramo alternativo. |
| <a id="L61"></a>61 | <code>                    raise ValueError(&quot;Usuário não existe&quot;)</code> | Interrompe este caminho lançando ValueError(&#x27;Usuário não existe&#x27;). |
| <a id="L62"></a>62 | <code>                user.password_hash = hash_password(read_password())</code> | Define user.password_hash com hash_password(read_password()). Armazena verificador Argon2; não é a senha original do usuário. Invoca hash_password com os argumentos declarados nesta instrução. Argumentos: read_password() |
| <a id="L63"></a>63 | <code>                user.token_version += 1</code> | Atualiza user.token_version com 1. Contador de revogação comparado com o JWT para invalidar tokens antigos. |
| <a id="L64"></a>64 | <code>                event = &quot;admin.password_reset&quot;</code> | Define event com &#x27;admin.password_reset&#x27;. |
| <a id="L65"></a>65 | <code>            session.add(AuditLog(user_id=user.id, event=event, details={&quot;source&quot;: &quot;cli&quot;}))</code> | Invoca session.add com os argumentos declarados nesta instrução. Argumentos: AuditLog(user_id=user.id, event=event, details={&#x27;source&#x27;: &#x27;cli&#x27;}) |
| <a id="L66"></a>66 | <code>            session.commit()</code> | Confirma a transação e torna suas alterações persistentes. |
| <a id="L67"></a>67 | <code>            print(f&quot;Operação concluída: {event}, usuário {username}&quot;)</code> | Invoca print com os argumentos declarados nesta instrução. Argumentos: f&#x27;Operação concluída: {event}, usuário {username}&#x27; |
| <a id="L68"></a>68 | <code>    except ValueError as error:</code> | Trata exceção ValueError como error. |
| <a id="L69"></a>69 | <code>        parser.exit(1, f&quot;Erro: {error}\n&quot;)</code> | Invoca parser.exit com os argumentos declarados nesta instrução. Argumentos: 1, f&#x27;Erro: {error}\n&#x27; |
| <a id="L70"></a>70 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L71"></a>71 | <code>∅</code> | Linha em branco que separa trechos; não acrescenta operação ao programa. |
| <a id="L72"></a>72 | <code>if __name__ == &quot;__main__&quot;:</code> | Executa este ramo somente se __name__ == &#x27;__main__&#x27;; caso contrário, segue o ramo alternativo. |
| <a id="L73"></a>73 | <code>    main()</code> | Invoca main com os argumentos declarados nesta instrução. |
