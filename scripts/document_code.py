#!/usr/bin/env python3
"""Build a deterministic, numbered reference without reading ignored private files."""

import argparse
import ast
import hashlib
import html
import io
import json
import os
import re
import subprocess
import textwrap
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts/code_reference_catalog.json"
OUTPUT = Path("docs/code")
MARKER = "Documentação:"


# Documentação: Implementa module_purpose como parte do fluxo descrito para este arquivo.
def module_purpose(path, catalog):
    if path in catalog["modules"]:
        return catalog["modules"][path]
    if path.endswith("/__init__.py"):
        return "Marca o pacote Python e, quando há imports, expõe os símbolos públicos indicados."
    if "/migrations/versions/" in path:
        return (
            "Revisão Alembic " + Path(path).stem + ". upgrade aplica o schema; downgrade reverte "
            "as alterações dessa revisão. Operações de banco exigem o papel de migrations."
        )
    if "test" in path.lower():
        return (
            "Conjunto de validações de " + Path(path).stem + ". Fixtures preparam o ambiente; "
            "asserts verificam o comportamento observado, e cleanup remove os recursos de teste."
        )
    if path.endswith("requirements.txt") or path.endswith("requirements-dev.txt"):
        return (
            "Declara dependências Python e versões instaladas por pip"
            " no runtime ou ambiente de testes."
        )
    if path.endswith("conftest.py"):
        return "Fornece fixtures pytest compartilhadas e isolamento dos dados usados pelos testes."
    return "Arquivo textual de configuração ou apoio do componente " + path.split("/")[0] + "."


# Documentação: Implementa symbol_purpose como parte do fluxo descrito para este arquivo.
def symbol_purpose(path, qualified, catalog, is_class=False):
    name = qualified.rsplit(".", 1)[-1]
    description = catalog["functions"].get(qualified) or catalog["functions"].get(name)
    if description:
        return description
    if is_class:
        return (
            "Define o tipo " + qualified + " e reúne o estado/contrato descrito para este módulo."
        )
    if name == "__init__":
        return (
            "Inicializa "
            + qualified.rsplit(".", 1)[0]
            + " com as dependências e estado declarados."
        )
    if name.startswith("test"):
        return (
            "Verifica o cenário "
            + name
            + "; as condições e resultados esperados aparecem nos asserts."
        )
    if name == "upgrade":
        return "Aplica tabelas, campos, índices e constraints desta revisão Alembic."
    if name == "downgrade":
        return "Reverte os elementos de schema criados por esta revisão, respeitando dependências."
    if name == "main":
        return "Coordena a entrada de linha de comando deste arquivo: " + module_purpose(
            path, catalog
        )
    verbs = {
        "validate": "Valida",
        "list": "Lista",
        "create": "Cria",
        "update": "Atualiza",
        "cancel": "Cancela",
        "get": "Obtém",
        "save": "Persiste",
        "load": "Carrega",
        "delete": "Remove",
        "clear": "Limpa",
        "close": "Libera",
        "start": "Inicia",
        "stop": "Interrompe",
        "register": "Registra",
        "revoke": "Revoga",
        "check": "Confere",
        "request": "Executa a requisição de",
        "build": "Monta",
        "import": "Importa",
        "enqueue": "Enfileira",
        "retry": "Tenta novamente",
        "refresh": "Atualiza",
        "toggle": "Alterna",
        "on": "Trata o callback de",
        "ensure": "Garante a preparação de",
    }
    first = re.split(r"_|(?=[A-Z])", name)[0]
    if first in verbs:
        return (
            verbs[first] + " " + qualified + ", segundo o contrato e as verificações deste módulo."
        )
    return "Implementa " + qualified + " como parte do fluxo descrito para este arquivo."


# Documentação: Implementa python_symbols como parte do fluxo descrito para este arquivo.
def python_symbols(tree):
    result = []

    # Documentação: Implementa python_symbols.visit como parte do fluxo descrito para este
    # arquivo.
    def visit(node, parents):
        for child in ast.iter_child_nodes(node):
            nested = parents
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = ".".join([*parents, child.name])
                result.append((child, name))
                nested = [*parents, child.name]
            visit(child, nested)

    visit(tree, [])
    return result


# Documentação: Implementa kotlin_mask como parte do fluxo descrito para este arquivo.
def kotlin_mask(text):
    """Blank comments/literals for classification; retain literals in semantic comparison."""
    pattern = re.compile(
        r'/\*.*?\*/|//[^\n]*|""".*?"""|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
        re.DOTALL,
    )
    masked, semantic, end = [], [], 0
    for match in pattern.finditer(text):
        ordinary = text[end : match.start()]
        masked.append(ordinary)
        semantic.append(re.sub(r"\s+", "", ordinary))
        token = match.group()
        masked.append("".join("\n" if char == "\n" else " " for char in token))
        if not token.startswith(("//", "/*")):
            semantic.append(token)
        end = match.end()
    masked.append(text[end:])
    semantic.append(re.sub(r"\s+", "", text[end:]))
    return "".join(masked), "".join(semantic)


# Documentação: Implementa kotlin_symbols como parte do fluxo descrito para este arquivo.
def kotlin_symbols(text):
    masked, _ = kotlin_mask(text)
    result = []
    owners = []
    depth = 0
    pending = None
    for number, line in enumerate(masked.splitlines(), 1):
        declaration = re.match(
            r"\s*(?:(?:private|public|internal|open|data|sealed|abstract|override|suspend|"
            r"protected|inline|tailrec|operator|infix|external)\s+)*"
            r"(class|object|interface|fun)\s+(?:<[^>]+>\s*)?([\w.]+)",
            line,
        )
        if declaration:
            kind, name = declaration.groups()
            qualified = ".".join([*[owner for _, owner in owners], name])
            result.append((number, qualified, kind))
            pending = name if kind != "fun" else None
        for brace in re.findall(r"[{}]", line):
            if brace == "{":
                depth += 1
                if pending:
                    owners.append((depth, pending))
                    pending = None
            else:
                depth -= 1
                owners = [(level, name) for level, name in owners if level <= depth]
    return result


# Documentação: Implementa annotation_lines como parte do fluxo descrito para este arquivo.
def annotation_lines(prefix, indent, description):
    width = max(20, 98 - len(indent) - len(prefix) - 1)
    wrapped = textwrap.wrap(MARKER + " " + description, width=width)
    return [indent + prefix + " " + part + "\n" for part in wrapped]


# Documentação: Implementa annotate_text como parte do fluxo descrito para este arquivo.
def annotate_text(path, text, catalog):
    if not path.endswith((".py", ".kt")):
        return text, 0
    lines = text.splitlines(keepends=True)
    additions = {}
    prefix = "#" if path.endswith(".py") else "//"
    if path.endswith(".py"):
        before = ast.parse(text)
        symbols = [
            (node.lineno, name, isinstance(node, ast.ClassDef))
            for node, name in python_symbols(before)
        ]
    else:
        symbols = [(number, name, kind != "fun") for number, name, kind in kotlin_symbols(text)]
    for number, name, is_class in symbols:
        previous = number - 2
        preceding = []
        while previous >= 0 and lines[previous].lstrip().startswith(prefix):
            preceding.append(lines[previous])
            previous -= 1
        if any(MARKER in line for line in preceding):
            continue
        indent = re.match(r"\s*", lines[number - 1]).group().replace("\n", "")
        additions[number - 1] = annotation_lines(
            prefix, indent, symbol_purpose(path, name, catalog, is_class)
        )
    output = []
    for position, line in enumerate(lines):
        output.extend(additions.get(position, []))
        output.append(line)
    updated = "".join(output)
    if path.endswith(".py"):
        if ast.dump(before, include_attributes=False) != ast.dump(
            ast.parse(updated), include_attributes=False
        ):
            raise ValueError("Annotations changed Python semantics: " + path)
    elif kotlin_mask(text)[1] != kotlin_mask(updated)[1]:
        raise ValueError("Annotations changed Kotlin tokens: " + path)
    return updated, len(additions)


# Documentação: Implementa brief como parte do fluxo descrito para este arquivo.
def brief(node):
    value = ast.unparse(node).replace("\n", " ") if node is not None else "None"
    return value if len(value) <= 180 else value[:177] + "..."


# Documentação: Implementa call_description como parte do fluxo descrito para este arquivo.
def call_description(node):
    name = brief(node.func)
    tail = name.rsplit(".", 1)[-1]
    meanings = {
        "commit": "Confirma a transação e torna suas alterações persistentes.",
        "rollback": "Desfaz a transação atual antes de tratar a falha.",
        "flush": "Envia alterações pendentes ao banco sem confirmar a transação.",
        "with_for_update": (
            "Solicita lock de linha; skip_locked, se presente, evita disputar linha ocupada."
        ),
        "begin_nested": (
            "Abre savepoint para isolar a falha deste trecho dentro da transação externa."
        ),
        "execute": (
            "Invoca execute; o receptor e os argumentos abaixo determ"
            "inam SQL ou operação permitida."
        ),
        "select": (
            "Constrói seleção SQLAlchemy; condições posteriores delimitam os registros consultados."
        ),
        "where": "Acrescenta predicado que filtra os registros da consulta.",
        "order_by": "Define a ordenação dos registros retornados pela consulta.",
        "limit": "Limita o número de registros retornados.",
        "model_dump": "Serializa o modelo validado para os campos do contrato de saída.",
        "model_validate": "Valida dados de entrada contra o contrato do modelo.",
        "json": "Decodifica a resposta como JSON; o chamador ainda deve conferir formato/campos.",
        "get_secret_value": "Obtém valor secreto apenas no ponto em que a operação precisa dele.",
        "compare_digest": "Compara valores usando a primitiva de comparação de tempo constante.",
        "uuid4": "Gera UUID aleatório para identificar registro ou operação.",
        "sha256": "Calcula digest SHA-256 para identificação/integridade conforme o contexto.",
        "token_urlsafe": "Gera material aleatório com secrets para uso operacional externo.",
        "encrypt": "Cifra/autentica conteúdo usando o componente de armazenamento indicado.",
        "decrypt": "Autentica/decifra conteúdo antes de disponibilizá-lo ao restante do fluxo.",
        "run": "Invoca run com os argumentos declarados; o receptor determina processo/runner.",
        "unlink": "Remove exclusivamente o caminho de arquivo indicado.",
        "mkdir": "Prepara diretório conforme permissões e opções declaradas.",
        "chmod": "Aplica as permissões de arquivo declaradas no argumento.",
        "raise_for_status": (
            "Converte resposta HTTP de erro em exceção para o tratamento do chamador."
        ),
    }
    result = meanings.get(tail, "Invoca " + name + " com os argumentos declarados nesta instrução.")
    if node.args or node.keywords:
        arguments = [brief(arg) for arg in node.args]
        arguments.extend((arg.arg or "**") + "=" + brief(arg.value) for arg in node.keywords)
        argument_text = ", ".join(arguments)
        result += (
            " Argumentos: " + argument_text[:220] + ("..." if len(argument_text) > 220 else "")
        )
    return result


# Documentação: Implementa statement_description como parte do fluxo descrito para este arquivo.
def statement_description(node, path, names, catalog):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        qualified = names[id(node)]
        return symbol_purpose(path, qualified, catalog, isinstance(node, ast.ClassDef))
    if isinstance(node, ast.Import):
        return "Importa módulo(s) " + ", ".join(alias.name for alias in node.names) + "."
    if isinstance(node, ast.ImportFrom):
        return (
            "Importa "
            + ", ".join(alias.name for alias in node.names)
            + " de "
            + ("." * node.level + (node.module or ""))
            + "."
        )
    if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        target = ", ".join(brief(item) for item in targets)
        verb = "Atualiza" if isinstance(node, ast.AugAssign) else "Define"
        result = verb + " " + target + " com " + brief(node.value) + "."
        for field, description in catalog["fields"].items():
            if any(brief(item).rsplit(".", 1)[-1] == field for item in targets):
                result += " " + description
        if isinstance(node.value, ast.Call):
            result += " " + call_description(node.value)
        return result
    if isinstance(node, ast.Return):
        return "Retorna " + brief(node.value) + " ao chamador e encerra este caminho da função."
    if isinstance(node, ast.Raise):
        return "Interrompe este caminho lançando " + brief(node.exc) + "."
    if isinstance(node, ast.Assert):
        return (
            "Exige que "
            + brief(node.test)
            + " seja verdadeiro; caso contrário, falha com AssertionError."
        )
    if isinstance(node, ast.If):
        return (
            "Executa este ramo somente se "
            + brief(node.test)
            + "; caso contrário, segue o ramo alternativo."
        )
    if isinstance(node, (ast.For, ast.AsyncFor)):
        return (
            "Percorre "
            + brief(node.iter)
            + ", atribuindo cada elemento a "
            + brief(node.target)
            + "."
        )
    if isinstance(node, ast.While):
        return "Repete este bloco enquanto " + brief(node.test) + " permanecer verdadeiro."
    if isinstance(node, (ast.With, ast.AsyncWith)):
        return (
            "Abre contexto(s) "
            + ", ".join(brief(i.context_expr) for i in node.items)
            + ("; a saída do bloco executa a liberação/fechamento definidos por cada contexto.")
        )
    if isinstance(node, (ast.Try, getattr(ast, "TryStar", ast.Try))):
        return "Delimita operações cujas falhas são tratadas pelos except/finally abaixo."
    if isinstance(node, ast.ExceptHandler):
        return (
            "Trata exceção " + brief(node.type) + (" como " + node.name if node.name else "") + "."
        )
    if isinstance(node, ast.Expr):
        if isinstance(node.value, ast.Call):
            return call_description(node.value)
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return (
                "Define documentação ou conteúdo literal; o texto não é e"
                "xecutado como instrução Python."
            )
        return "Avalia a expressão " + brief(node.value) + "."
    if isinstance(node, ast.Continue):
        return "Encerra esta iteração e passa ao próximo elemento do loop."
    if isinstance(node, ast.Break):
        return "Sai do loop atual; o processamento continua após seu bloco."
    if isinstance(node, ast.Pass):
        return "Mantém o bloco sem operação adicional, inclusive quando uma exceção é ignorada."
    if isinstance(node, ast.Delete):
        return "Remove a referência/elemento " + ", ".join(brief(i) for i in node.targets) + "."
    if isinstance(node, (ast.Global, ast.Nonlocal)):
        return "Vincula nomes ao escopo " + type(node).__name__ + ": " + ", ".join(node.names) + "."
    return "Integra a instrução " + type(node).__name__ + " no fluxo deste bloco."


# Documentação: Implementa python_rows como parte do fluxo descrito para este arquivo.
def python_rows(path, text, catalog):
    tree = ast.parse(text)
    symbols = python_symbols(tree)
    names = {id(node): name for node, name in symbols}
    candidates = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.stmt, ast.ExceptHandler)) and hasattr(node, "lineno")
    ]
    literal_lines, comment_lines = set(), {}
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type == tokenize.STRING:
            literal_lines.update(range(token.start[0] + 1, token.end[0] + 1))
        elif token.type == tokenize.COMMENT:
            comment_lines[token.start[0]] = token.string.lstrip("# ")
    rows = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if number in literal_lines:
            explanation = (
                "Continua o literal iniciado acima, preservando texto/SQL/prompt como dados."
            )
        elif not stripped:
            explanation = "Linha em branco que separa trechos; não acrescenta operação ao programa."
        elif stripped.startswith("#"):
            explanation = "Comentário: " + comment_lines.get(number, stripped.lstrip("# "))
        elif stripped.startswith("@"):
            explanation = "Aplica o decorator " + stripped[1:] + " à definição que segue."
        elif stripped in {"else:", "finally:"}:
            explanation = (
                "Ramo alternativo quando a condição anterior não é satisfeita."
                if stripped == "else:"
                else "Bloco de finalização executado mesmo quando a operação anterior falha."
            )
        else:
            applicable = [node for node in candidates if node.lineno <= number <= node.end_lineno]
            node = min(applicable, key=lambda n: (n.end_lineno - n.lineno, -n.lineno), default=None)
            if node is not None:
                explanation = statement_description(node, path, names, catalog)
                if number != node.lineno:
                    explanation = (
                        "Continua/fecha a instrução da linha "
                        + str(node.lineno)
                        + ". "
                        + explanation
                    )
            else:
                explanation = "Componente da expressão/estrutura Python declarada neste trecho."
        rows.append((number, line, explanation))
    return rows, [
        (node.lineno, name, symbol_purpose(path, name, catalog, isinstance(node, ast.ClassDef)))
        for node, name in symbols
    ]


# Documentação: Implementa kotlin_rows como parte do fluxo descrito para este arquivo.
def kotlin_rows(path, text, catalog):
    masked, _ = kotlin_mask(text)
    mask_lines = masked.splitlines()
    symbols = kotlin_symbols(text)
    definitions = {number: (name, kind) for number, name, kind in symbols}
    rows = []
    block_comment = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        code = mask_lines[number - 1].strip() if number <= len(mask_lines) else ""
        if not stripped:
            explanation = "Linha em branco para separar declarações/blocos; não executa uma ação."
        elif block_comment or stripped.startswith(("//", "/*", "*")):
            explanation = "Comentário de manutenção/documentação: " + stripped.lstrip("/* ")
            block_comment = "*/" not in stripped and (block_comment or stripped.startswith("/*"))
        elif number in definitions:
            name, kind = definitions[number]
            explanation = symbol_purpose(path, name, catalog, kind != "fun")
        elif stripped.startswith("import "):
            explanation = (
                "Disponibiliza o símbolo Kotlin/Android " + stripped[7:] + " neste arquivo."
            )
        elif stripped.startswith("package "):
            explanation = "Associa as declarações ao namespace " + stripped[8:] + "."
        elif stripped.startswith("@"):
            explanation = "Aplica a anotação " + stripped + " à declaração seguinte."
        elif not code:
            explanation = (
                "Conteúdo literal usado como texto/SQL/argumento; não é u"
                "ma instrução Kotlin independente."
            )
        elif re.fullmatch(r"[)}\],;]+", code):
            explanation = (
                "Fecha delimitador de bloco, chamada, coleção ou lista de"
                " argumentos iniciada acima."
            )
        elif re.match(r"(?:private\s+|val\s+|var\s+|const\s+|lateinit\s+)+", code):
            explanation = (
                "Declara/inicializa estado, propriedade ou argumento com o tipo/valor indicado."
            )
        elif re.match(r"(?:else\s+)?if\b", code):
            explanation = "Escolhe este caminho somente quando a condição indicada é satisfeita."
        elif code.startswith(("else", "catch", "finally")):
            explanation = (
                "Define caminho alternativo, tratamento de erro ou libera"
                "ção de recursos do bloco anterior."
            )
        elif code.startswith(("for ", "while ")):
            explanation = (
                "Percorre elementos ou repete o bloco enquanto a condição declarada permitir."
            )
        elif code.startswith("return"):
            explanation = "Encerra este caminho e devolve o resultado ao chamador/label indicado."
        elif code.startswith(("throw ", "require(", "check(", "assert")):
            explanation = "Exige a condição/invariante indicada ou interrompe o fluxo com erro."
        elif code.startswith("when"):
            explanation = "Despacha o valor/condição para os ramos declarados abaixo."
        else:
            call = re.search(r"\b([\w.]+)\s*\(", code)
            named = re.match(r"(\w+)\s*=\s*(.*)", stripped)
            if call:
                explanation = "Invoca/continua " + call.group(1) + " com os argumentos declarados."
            elif named:
                explanation = (
                    "Fornece o valor de " + named.group(1) + " no contexto desta expressão."
                )
            else:
                explanation = "Fornece a expressão " + stripped + " ao bloco/chamada em construção."
        meanings = {
            "Text": "Renderiza texto/estado com estilo e conteúdo declarados.",
            "Column": "Organiza componentes filhos verticalmente no layout.",
            "Row": "Organiza componentes filhos horizontalmente no layout.",
            "Button": "Cria controle que executa onClick quando habilitado e acionado.",
            "OutlinedButton": "Cria controle com contorno e a ação onClick declarada.",
            "TextButton": "Cria ação textual com a condição enabled declarada.",
            "OutlinedTextField": "Liga entrada de texto ao valor e callback de alteração.",
            "Dialog": "Apresenta conteúdo modal segundo propriedades e callback de fechamento.",
            "AlertDialog": "Apresenta confirmação/recusa com os botões e mensagens declarados.",
            "Surface": "Define superfície visual usando cor/forma e componentes filhos.",
            "Scaffold": "Reserva áreas para navegação/conteúdo e entrega padding ao layout.",
            "NavigationBarItem": "Cria destino de navegação com seleção e callback onClick.",
            "Switch": "Liga opção booleana ao estado/callback de alteração.",
            "MaterialTheme": "Disponibiliza cores/tipografia ao conteúdo Compose.",
            "padding": "Aplica espaço interno ao componente segundo os valores declarados.",
            "fillMaxSize": "Solicita ocupar o tamanho disponível no layout pai.",
            "fillMaxWidth": "Solicita ocupar a largura disponível no layout pai.",
            "JSONObject": "Monta/interpreta objeto JSON usado pelo contrato do Core/cache.",
            "put": "Adiciona ou atualiza campo/chave com o valor declarado.",
            "getString": "Lê o campo textual indicado; campo ausente/incompatível pode falhar.",
            "optString": "Lê texto opcional, aplicando fallback declarado quando necessário.",
            "setAction": "Define a ação que distingue este Intent/PendingIntent.",
            "putExtra": "Acrescenta argumento ao Intent, validado pelo componente destino.",
            "getStringExtra": "Lê argumento textual do Intent para o fluxo indicado.",
            "setContentIntent": "Define destino aberto ao acionar o corpo da notificação.",
            "setVisibility": "Define a privacidade da notificação na tela bloqueada.",
            "setSound": "Configura som do canal, respeitando alterações do usuário.",
            "setOngoing": "Indica notificação associada a atividade/chamada em andamento.",
            "setOnlyAlertOnce": "Evita novo alerta sonoro ao atualizar a mesma notificação.",
            "setFullScreenIntent": "Solicita tela de chamada quando o sistema autorizar.",
            "cancel": "Solicita cancelamento do recurso/notificação identificado.",
            "checkSelfPermission": "Confere autorização; declaração no manifesto não basta.",
            "stopService": "Solicita encerrar somente o componente de serviço indicado.",
            "stopSelf": "Encerra este serviço conforme seu ciclo de vida Android.",
            "registerDefaultNetworkCallback": "Observa rede para acordar a reconexão.",
            "trySend": "Tenta publicar no canal sem suspender; o resultado indica aceitação.",
            "refreshEvents": "Publica o estado persistido para os observadores da interface.",
            "enqueueVoice": "Grava transcrição na fila durável vinculada à chamada.",
            "sendText": "Encaminha texto pela fila/contrato da chamada ativa.",
            "toggleMute": "Alterna silêncio e interrupção da voz conforme o controlador.",
            "toggleSpeaker": "Alterna saída solicitada entre alto-falante e auricular.",
            "newWebSocket": "Abre WSS com listener; autenticação ocorre nos frames.",
            "setTransactionSuccessful": "Marca transação SQLite para confirmar no encerramento.",
            "beginTransaction": "Abre transação SQLite para alterações associadas.",
            "endTransaction": "Finaliza transação SQLite, confirmando se marcada como válida.",
            "startForeground": (
                "Publica notificação obrigatória e promove o serviço ao tipo declarado."
            ),
            "startForegroundService": (
                "Solicita início do serviço; as restrições de background "
                "do Android continuam valendo."
            ),
            "canUseFullScreenIntent": (
                "Confere a autorização de tela cheia antes de solicitar apresentação da chamada."
            ),
            "requestDismissKeyguard": (
                "Pede ao Android desbloqueio; não contorna PIN/biometria do usuário."
            ),
            "setShowWhenLocked": (
                "Autoriza esta janela a ser mostrada sobre bloqueio, sem desbloquear o aparelho."
            ),
            "setTurnScreenOn": (
                "Solicita ligar a tela para apresentar a chamada, sujeito às regras do sistema."
            ),
            "FLAG_INSISTENT": (
                "Solicita repetição do toque até cancelamento/timeout da notificação."
            ),
            "setTimeoutAfter": "Limita permanência da notificação ao tempo indicado.",
            "collectAsStateWithLifecycle": (
                "Observa StateFlow de acordo com o lifecycle para atualizar a interface."
            ),
            "remember": "Conserva valor/estado entre recomposições do trecho Compose.",
            "LaunchedEffect": (
                "Executa coroutine vinculada às chaves e à presença do trecho na composição."
            ),
            "withLock": (
                "Serializa esta seção para impedir renovação/alteração concorrente do estado."
            ),
            "withContext": (
                "Executa trabalho no dispatcher declarado sem bloquear o chamador de UI."
            ),
            "launch": (
                "Inicia coroutine no escopo declarado; cancelamento segue a duração desse escopo."
            ),
            "use": "Garante fechamento do recurso ao terminar este bloco, incluindo falha.",
            "abandonAudioFocusRequest": (
                "Libera foco de áudio do app para não disputar a captura com o reconhecedor."
            ),
            "startListening": (
                "Solicita captura ao serviço SpeechRecognizer; depende de"
                " permissão/estado do sistema."
            ),
            "Cipher": (
                "Usa primitiva criptográfica; modo, IV e AAD são configurados nas linhas próximas."
            ),
            "updateAAD": "Vincula autenticação GCM ao applicationId declarado.",
            "execSQL": (
                "Executa SQL local; placeholders são preenchidos pelos argumentos declarados."
            ),
            "rawQuery": (
                "Abre cursor de consulta SQLite que deve ser fechado ao concluir a leitura."
            ),
            "assert": (
                "Verifica comportamento esperado pelo teste; não constitu"
                "i funcionalidade de produção."
            ),
            "getSharedPreferences": (
                "Acessa preferências privadas do aplicativo para conservar escolha/estado."
            ),
        }
        if not stripped.startswith(("//", "/*", "*")) and code:
            for word, meaning in meanings.items():
                if re.search(r"\b" + word + (r"\w*\b" if word == "assert" else r"\b"), code):
                    explanation += " " + meaning
                    break
            for field, meaning in catalog["fields"].items():
                if re.search(r"\b" + field + r"\b", line):
                    explanation += " " + meaning
                    break
        rows.append((number, line, explanation))
    return rows, [
        (number, name, symbol_purpose(path, name, catalog, kind != "fun"))
        for number, name, kind in symbols
    ]


# Documentação: Implementa configuration_rows como parte do fluxo descrito para este arquivo.
def configuration_rows(path, text, catalog):
    rows = []
    for number, line in enumerate(text.splitlines(), 1):
        value = line.strip()
        if not value:
            explanation = "Linha em branco que separa entradas de configuração."
        elif value.startswith(("#", "//", "<!--", "rem ", "@rem")):
            explanation = "Comentário/orientação do arquivo; não acrescenta uma configuração ativa."
        elif path.endswith((".xml", ".plist")):
            explanation = (
                "Declara elemento/atributo XML conforme o schema do compo"
                "nente indicado no contexto."
            )
        elif path.endswith((".service", ".timer")):
            explanation = (
                "Abre seção " + value + " do systemd."
                if value.startswith("[")
                else "Define diretiva systemd "
                + value.partition("=")[0]
                + " com o valor declarado."
            )
        elif path.endswith((".toml", ".ini", ".properties")):
            explanation = (
                "Abre seção/tabela " + value + "."
                if value.startswith("[")
                else "Define a opção "
                + re.split(r"[=:]", value, maxsplit=1)[0].strip()
                + " do build/ferramenta."
            )
        elif path == ".env.example":
            explanation = (
                "Exemplifica a variável "
                + value.partition("=")[0]
                + "; implantação usa valor externo próprio."
            )
        elif path.endswith("ignore"):
            explanation = (
                "Regra de inclusão/exclusão do contexto Git/Docker para o padrão declarado."
            )
        elif "requirements" in path:
            explanation = "Declara dependência pip, respeitando a versão/restrição indicada."
        elif path.endswith((".yml", ".yaml", ".json")):
            match = re.match(r'[- ]*["\']?([\w.-]+)["\']?\s*:\s*(.*)', value)
            explanation = (
                "Configura " + match.group(1) + " com " + (match.group(2) or "o bloco abaixo") + "."
                if match
                else "Item/fechamento da lista ou objeto de configuração em construção."
            )
        elif Path(path).name == "Dockerfile":
            explanation = (
                "Diretiva Dockerfile " + value.split()[0] + " para configurar a etapa da imagem."
            )
        elif "Caddyfile" in path:
            explanation = "Diretiva/bloco Caddy para endereço, TLS ou encaminhamento ao backend."
        elif path.endswith(".mako"):
            explanation = (
                "Trecho do template Alembic; placeholders são preenchidos ao gerar uma revisão."
            )
        else:
            explanation = (
                "Comando/estrutura do wrapper de ferramenta; o contexto a"
                "cima identifica seu executor."
            )
        directives = {
            "image:": "Seleciona imagem/versionamento; digest fixa seu conteúdo.",
            "build:": "Define como construir a imagem a partir do contexto local.",
            "context:": "Seleciona diretório de build; .dockerignore limita o conteúdo.",
            "target:": "Seleciona etapa do Dockerfile, como produção ou testes.",
            "environment:": "Injeta variáveis no serviço em vez de gravá-las na imagem.",
            "restart:": "Define quando Docker deve reiniciar este container.",
            "profiles:": "Habilita o serviço somente nos perfis de execução indicados.",
            "command:": "Substitui comando com executável/argumentos explícitos.",
            "volumes:": "Define dados persistentes ou bind mounts e acesso.",
            "ports:": "Publica portas no endereço do host declarado.",
            "networks:": "Associa serviços aos domínios de comunicação definidos.",
            "tmpfs:": "Fornece área temporária em memória sem gravar na imagem.",
            "mem_limit:": "Limita memória do container para proteger o host.",
            "cpus:": "Limita capacidade de CPU disponível ao container.",
            "pids_limit:": "Limita quantidade de processos/threads no container.",
            "interval:": "Define intervalo entre verificações operacionais.",
            "timeout:": "Define prazo máximo da verificação/chamada indicada.",
            "retries:": "Define falhas toleradas antes do estado de erro.",
            "start_period:": "Reserva tempo inicial para o serviço ficar pronto.",
            "stop_grace_period:": "Reserva tempo de encerramento antes do término forçado.",
            "<<:": "Reutiliza âncora YAML e permite overrides explícitos.",
            "branches:": "Limita branches que acionam o evento da CI.",
            "permissions:": "Delimita acesso do token da execução GitHub.",
            "runs-on:": "Seleciona o ambiente do runner de CI.",
            "timeout-minutes:": "Limita duração do job de CI.",
            "run:": "Executa script no runner sob o contexto/ambiente do passo.",
            "if:": "Condiciona execução do passo à expressão declarada.",
            "WorkingDirectory": "Define base para caminhos relativos do serviço.",
            "EnvironmentFile": "Carrega variáveis externas sem embutir valores na unidade.",
            "Type=oneshot": "Termina após o comando, sem manter processo servidor.",
            "PrivateTmp": "Isola diretórios temporários do serviço.",
            "ProtectSystem": "Restringe escrita nos diretórios do sistema.",
            "ReadWritePaths": "Permite escrita nos paths declarados sob as restrições da unidade.",
            "RandomizedDelaySec": "Distribui disparos por atraso aleatório.",
            "WantedBy": "Define alvo systemd utilizado ao habilitar unidade/timer.",
            "ExecStart": "Comando executado pela unidade; argumentos/caminho são explícitos.",
            "User=": "Define a identidade que executa o serviço.",
            "OnCalendar": "Define calendário de disparo do timer.",
            "Persistent=": (
                "Controla recuperação de disparos do timer perdidos durante desligamento."
            ),
            "read_only": (
                "Monta filesystem do container como somente leitura; volu"
                "mes/tmpfs são exceções declaradas."
            ),
            "internal:": "Controla isolamento da rede Docker em relação ao tráfego externo.",
            "cap_drop": "Remove capabilities Linux do container.",
            "no-new-privileges": "Impede adquirir privilégios adicionais por exec no container.",
            "healthcheck": "Define teste de saúde operacional, distinto de presença do processo.",
            "depends_on": "Estabelece dependência/condição de partida entre serviços.",
            "reverse_proxy": "Encaminha HTTP e upgrades WSS para o backend indicado.",
            "uses:": "Seleciona ação GitHub; o hash fixa sua revisão.",
            "android:exported": "Delimita se outros aplicativos podem invocar este componente.",
            "uses-permission": (
                "Declara permissão solicitável; declaração não equivale a autorização do usuário."
            ),
            "foregroundServiceType": "Declara os tipos Android autorizados para este serviço.",
            "POST_NOTIFICATIONS": "Avisos exigem aprovação em runtime no Android moderno.",
            "RECORD_AUDIO": "Captura de microfone exige aprovação do usuário.",
            "USE_FULL_SCREEN_INTENT": "Apresentação urgente de chamada é controlada pelo sistema.",
            "RECEIVE_BOOT_COMPLETED": "Permite receber boot após disponibilidade do app.",
            "INTERNET": "Autoriza acesso de rede para HTTPS/WSS do Core.",
            "ACCESS_NETWORK_STATE": "Permite observar conectividade, sem ler conteúdo de rede.",
            "android:stopWithTask": "Controla se remover a tarefa encerra o serviço.",
            "android:excludeFromRecents": "Controla presença da Activity nos recentes.",
            "android:allowBackup": "Controla backup automático dos dados do app.",
            "android:usesCleartextTraffic": "Controla tráfego HTTP sem TLS.",
        }
        for key, meaning in directives.items():
            if key in value:
                explanation += " " + meaning
        if "${" in value:
            explanation += (
                " ${...} é substituição do ambiente/template, não uma credencial literal."
            )
        rows.append((number, line, explanation))
    return rows, []


# Documentação: Implementa reference_path como parte do fluxo descrito para este arquivo.
def reference_path(path):
    # Use a public guide name that is not excluded by the .env.* privacy rule.
    name = "environment-example.md" if path == ".env.example" else path + ".md"
    return OUTPUT / name


# Documentação: Implementa reference_page como parte do fluxo descrito para este arquivo.
def reference_page(path, text, catalog):
    if path.endswith(".py"):
        rows, symbols = python_rows(path, text, catalog)
    elif path.endswith((".kt", ".kts")):
        rows, symbols = kotlin_rows(path, text, catalog)
    else:
        rows, symbols = configuration_rows(path, text, catalog)
    target = reference_path(path)
    relative = os.path.relpath(path, target.parent).replace(os.sep, "/")
    page = [
        "# " + path,
        "",
        module_purpose(path, catalog),
        "",
        "[Arquivo fonte](" + relative + ") · " + str(len(rows)) + " linhas físicas.",
        "",
        "Referência gerada por `scripts/document_code.py`. O contexto editorial vem de "
        "`scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. "
        "O guia descreve a instrução e não comprova sua execução ou homologação.",
        "",
    ]
    if symbols:
        page.extend(
            ["## Símbolos e responsabilidades", "", "| Símbolo | Finalidade |", "| --- | --- |"]
        )
        for number, name, purpose in symbols:
            page.append(
                "| [" + name + "](#L" + str(number) + ") | " + purpose.replace("|", "\\|") + " |"
            )
        page.append("")
    page.extend(
        ["## Linha a linha", "", "| Linha | Código original | Explicação |", "| --- | --- | --- |"]
    )
    for number, line, explanation in rows:
        source = html.escape(line).replace("|", "&#124;") if line else "∅"
        detail = html.escape(explanation).replace("|", "&#124;")
        page.append(f'| <a id="L{number}"></a>{number} | <code>{source}</code> | {detail} |')
    return "\n".join(page) + "\n"


# Documentação: Implementa inventory como parte do fluxo descrito para este arquivo.
def inventory(root):
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    sources, binaries = {}, []
    for name in sorted(filter(None, names)):
        if name.startswith(str(OUTPUT) + "/") or name.endswith(".md"):
            continue
        blob = (root / name).read_bytes()
        try:
            if b"\0" in blob:
                raise UnicodeError("binary")
            sources[name] = blob.decode("utf-8")
        except UnicodeError:
            binaries.append({"path": name, "reason": "Binário/asset sem linhas de código textual."})
    return sources, binaries


# Documentação: Implementa rendered_reference como parte do fluxo descrito para este arquivo.
def rendered_reference(sources, binaries, catalog):
    result, records = {}, []
    for path, text in sorted(sources.items()):
        target = str(reference_path(path))
        result[target] = reference_page(path, text, catalog)
        records.append(
            {
                "path": path,
                "reference": target,
                "sha256": hashlib.sha256(text.encode()).hexdigest(),
                "lines": len(text.splitlines()),
                "nonempty_lines": sum(bool(line.strip()) for line in text.splitlines()),
            }
        )
    total = sum(row["lines"] for row in records)
    manifest = {
        "format_version": 1,
        "source_files": len(records),
        "physical_lines": total,
        "files": records,
        "binary_assets": binaries,
    }
    result[str(OUTPUT / "manifest.json")] = (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    index = [
        "# Referência completa do código",
        "",
        f"{len(records)} arquivos textuais e {total} linhas físicas documentados.",
        "",
        "Inclui código de produção, testes, migrations, build e configuração, além de linhas "
        "em branco/comentários/delimitadores. Arquivos privados ignorados não são lidos; binários "
        "não têm linhas. Markdown existente é documentação; não entra no inventário de código.",
        "",
        "Cada guia traz contexto editorial, responsabilidades dos símbolos e tabela com "
        "código original/número/explicação. O conteúdo literal é identificado como dados. "
        "Explicações sintáticas automáticas devem ser lidas junto ao contexto do módulo; "
        "cobertura de linhas não equivale a testes aprovados.",
        "",
        "[Como atualizar e validar](../CODE_DOCUMENTATION.md) · [Manifesto](manifest.json)",
        "",
        "| Arquivo | Linhas | Referência |",
        "| --- | ---: | --- |",
    ]
    for row in records:
        index.append(
            "| "
            + row["path"]
            + " | "
            + str(row["lines"])
            + " | [Ler]("
            + str(Path(row["reference"]).relative_to(OUTPUT))
            + ") |"
        )
    index.extend(["", "## Assets binários", ""])
    index.extend("- `" + row["path"] + "`: " + row["reason"] for row in binaries)
    result[str(OUTPUT / "README.md")] = "\n".join(index) + "\n"
    return result, manifest


# Documentação: Implementa differences como parte do fluxo descrito para este arquivo.
def differences(root, rendered):
    return [
        path
        for path, expected in rendered.items()
        if not (root / path).exists() or (root / path).read_text() != expected
    ]


# Documentação: Coordena a entrada de linha de comando deste arquivo: Gera referência
# determinística linha a linha a partir de arquivos versionados, AST Python e análise lexical
# Kotlin/configuração; verifica cobertura e não lê arquivos privados ignorados.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--annotate",
        action="store_true",
        help="Add semantic-preserving comments to authored Python/Kotlin symbols",
    )
    parser.add_argument(
        "--check", action="store_true", help="Fail if any generated reference is stale"
    )
    args = parser.parse_args()
    if args.annotate and args.check:
        parser.error("--annotate mutates sources and cannot be combined with --check")
    root = args.root.resolve()
    catalog = json.loads((root / CATALOG.relative_to(ROOT)).read_text())
    sources, binaries = inventory(root)
    annotated = 0
    if args.annotate:
        for path, text in list(sources.items()):
            updated, count = annotate_text(path, text, catalog)
            if updated != text:
                (root / path).write_text(updated)
                sources[path] = updated
                annotated += count
    rendered, manifest = rendered_reference(sources, binaries, catalog)
    changed = differences(root, rendered)
    if args.check:
        if changed:
            print(json.dumps({"stale_references": changed}, ensure_ascii=False))
            return 1
    else:
        for path, content in rendered.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    print(
        json.dumps(
            {
                "source_files": manifest["source_files"],
                "documented_lines": manifest["physical_lines"],
                "annotated_symbols": annotated,
                "check": args.check,
                "up_to_date": not changed if args.check else True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
