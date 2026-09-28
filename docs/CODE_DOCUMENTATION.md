# Como ler e manter a documentação do código

A [referência por arquivo](code/README.md) cobre cada linha física do código textual versionado: produção, testes, migrations, infraestrutura e build. A tabela de cada arquivo conserva número, código original e explicação; linhas em branco, comentários, literais e delimitadores também estão incluídos. Os símbolos possuem uma descrição de responsabilidade, e funções/classes Python e Kotlin recebem comentários de manutenção no próprio fonte.

O [catálogo editorial](../scripts/code_reference_catalog.json) descreve contratos dos módulos, pontos críticos e campos. O [gerador](../scripts/document_code.py) combina esse contexto com AST Python e análise lexical de Kotlin/configuração para produzir as explicações de cada instrução. Explicações automáticas de sintaxe não substituem a leitura dos contratos ou a revisão técnica; cobertura de documentação não comprova execução ou homologação de uma funcionalidade.

Markdown já existente é documentação e não é documentado recursivamente. JARs/imagens são assets binários sem linhas textuais: o índice e o manifesto registram essa distinção. Arquivos privados ignorados — `.env`, chaves, senhas, dados e backups — não entram no inventário do gerador. A configuração externa está descrita em [CONFIGURATION_SECRETS.md](CONFIGURATION_SECRETS.md).

## Atualizar

Requer Python 3.12 e Git no ambiente de desenvolvimento da VPS. O gerador usa apenas biblioteca padrão, não importa módulos de runtime e não executa o código documentado.

```sh
cd /srv/devlima-agent
# O inventário usa git ls-files: adicione novos fontes ao índice antes de gerar.
git add caminho/do/novo/fonte.py
python3 scripts/document_code.py --annotate
python3 scripts/document_code.py --check
```

`--annotate` adiciona comentários às definições Python/Kotlin. Antes de escrever, compara a AST Python sem posições e a sequência lexical Kotlin sem comentários/espaços externos aos literais. Se houver diferença, interrompe a alteração desse arquivo. Reexecutar não adiciona comentários duplicados. Arquivos de fornecedor, como o Gradle wrapper, recebem guia externo e são conservados no formato original.

Quando uma responsabilidade mudar, atualize também o catálogo e o comentário existente no fonte. A ferramenta não reescreve automaticamente um comentário anterior que pode conter contexto humano. Para mudanças apenas no guia/catálogo, gere novamente sem `--annotate`.

```sh
python3 scripts/document_code.py
python3 scripts/document_code.py --check
python3 -m unittest discover -s tests -p test_code_reference.py -v
```

## Verificar e publicar

O manifesto contém SHA-256 e contagem de linhas de cada fonte. `--check` gera a referência esperada em memória e compara todos os guias, índice e manifesto existentes, incluindo explicações. Um fonte novo ou alterado, um guia modificado ou um catálogo desatualizado faz a verificação falhar. Não use essa opção para recuperar texto perdido sem antes conferir a alteração no catálogo.

Antes do commit, execute a verificação, `git diff --check` e os checks apropriados para os fontes alterados. Comentários não autorizam mudanças de comportamento. O workflow inclui a verificação da referência; a falha de inicialização da CI hospedada registrada anteriormente continua sendo uma limitação operacional separada.

## Limites da interpretação

As descrições de módulo/função/campo são contexto editorial; as linhas são interpretadas estaticamente. A ferramenta não prova ownership, idempotência, isolamento ou sucesso de uma chamada só por encontrar seu nome. Cadeias de chamadas, estruturas Compose e continuação de argumentos são explicadas conforme a sintaxe, junto aos símbolos e ao contexto do arquivo. Resultados reais permanecem nos relatórios de fases, testes e validação física.

## Verificação desta entrega — 2026-09-28

- Referência conferida por hash, conteúdo e sequência completa de anchors, incluindo linhas em branco.
- Comentários em 788 funções/classes; comparação de AST em 86 arquivos Python existentes e de tokens em 25 Kotlin existentes sem diferença de estrutura.
- Treze testes das ferramentas/documentação/backup/configuração passaram; Ruff em backend, migrations, testes, scripts e manager sem erros.
- Android debug/AndroidTest compilados na VPS, quatro unitários e lint sem erros. Nenhum teste físico foi executado nesta alteração; chamadas bloqueadas/Doze da pré-release continuam pendentes.
- Alteração documental conservada separadamente dos resultados históricos da V1; imagens de backend e APK já publicado não foram substituídos.
