# Contexto e memória — Fase 3

O PostgreSQL guarda conversas e mensagens completas. O modelo recebe um contexto novo em cada request, construído pelo Core; não há dependência de estado interno da LLM.

## Fluxo de um turno

1. JWT identifica o usuário. `client_message_id` UUID é obrigatório e deve ser reutilizado em reenvios da mesma mensagem.
2. Uma transação curta grava a mensagem `PENDING` e reserva a conversa com uma lease durável. O lock transacional termina antes da inferência.
3. Quando necessário, o Summarizer gera um resumo estruturado das mensagens antigas. Uma falha de resumo é auditada e o turno continua com a janela recente.
4. Context Builder combina system prompt, usuário/timezone, relógio UTC/local, resumo, memórias relevantes, capacidades e últimas mensagens. Tarefas/lembretes/jobs estão explicitamente indisponíveis nesta fase.
5. Router chama a LLM local; a política técnica da Fase 2 controla eventual fallback. JSON inválido não dispara fallback.
6. Pydantic valida resposta, candidatos e ações. Em uma nova transação, o Core verifica que ainda possui a lease e grava resposta, candidatos, ações e auditoria juntos.

Uma mensagem já concluída retorna a resposta persistida, com `replayed=true`, sem chamar novamente a LLM ou duplicar propostas. Reutilizar o UUID com texto/conversa diferente retorna 409. Outro turno na mesma conversa ocupada retorna `conversation_busy` (409), permitindo ao cliente tentar posteriormente.

Uma falha de inferência/JSON mantém a mensagem original `FAILED` e libera a lease. O mesmo UUID permite tentar de novo quando esse for o último turno da conversa. Após um crash, a lease expira; o próximo request pode recuperar a conversa e marcar o turno abandonado. Uma execução antiga não pode finalizar ou liberar a lease de outra execução. Esta recuperação é acionada por requests; não há processamento em background nesta fase.

## Orçamento

- `CONTEXT_RECENT_MESSAGES=8`: até oito mensagens concluídas recentes, com recorte de até 1400 caracteres por mensagem enviado à LLM.
- `CONTEXT_MAX_CHARS=12000`: limite total de caracteres enviados por turno, incluindo a mensagem atual completa (máximo 4000). É um orçamento de caracteres, não contagem exata do tokenizer do modelo.
- `SUMMARY_TRIGGER_MESSAGES=16`: resumo quando há dezesseis mensagens concluídas ainda não cobertas; a janela recente é preservada.
- Mensagem system tem até 8000 caracteres. Primeiro são retiradas memórias de menor relevância, depois itens acessórios do resumo; se necessário, o resumo é omitido naquele request.

Resumos incrementais incluem `summary`, `facts` e `open_topics`, com limites de tamanho e cobertura `through_sequence`. O resumo anterior alimenta o seguinte. As mensagens originais continuam intactas. Arquivar uma conversa oculta-a da listagem padrão e impede novos turnos; permite consultar seu histórico.

Datas persistidas são UTC; o relógio local usa a timezone IANA do usuário (`America/Sao_Paulo` por padrão). Datas em ações precisam incluir offset e são normalizadas para UTC.

## Política de memória

`memory_candidates` é uma proposta da LLM; `memories` contém somente conteúdo autorizado pelo Core ou criado explicitamente pela API autenticada.

Aceitação automática exige os três critérios: pedido/preferência explícita no início da mensagem (`Lembre que`, `Guarde que`, `Memorize que`, `Prefiro`), conteúdo literal presente na mensagem atual e confiança mínima de 0,9. Se a LLM mudar o verbo ou inferir um fato, o candidato fica `PENDING`. A API permite aceitar ou rejeitar a proposta. Formatos reconhecidos de chaves/senhas/tokens são recusados e o texto sensível é substituído no candidato; isso é uma heurística, não um detector universal de segredos.

Hash do conteúdo normalizado evita memórias duplicadas por usuário. Desativar uma memória exclui-a da seleção de contexto; não apaga histórico antigo. Reaceitar um candidato cuja memória foi desativada não a reativa. A criação explícita do mesmo conteúdo pela API pode reativá-la.

A busca inicial compara palavras das últimas cem memórias ativas do usuário, prioriza preferências e envia até cinco resultados. Não há embeddings/pgvector nesta fase; fatos sem correspondência lexical podem ficar fora do contexto. Cada query usa o usuário autenticado; IDs de outro usuário retornam 404.

## Ações e inferência

Há schemas enumerados para tarefas, lembretes, chamadas e workers, com UUIDs e argumentos limitados. Tipos desconhecidos, shell, caminhos no lugar de IDs e campos extras são rejeitados. Ações válidas são registradas `UNSUPPORTED` nesta fase; não executam nada e a resposta informa a indisponibilidade.

Os requests JSON do llama.cpp desativam thinking por `reasoning_effort=none`/`enable_thinking=false`, mantendo o orçamento para o JSON final. Essa opção é específica do provider local; não é enviada ao Groq. Referência: [API do llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md).

Auditoria de inferência e operações contém IDs/metadados, sem cópia de prompts/respostas. As tabelas de mensagens e resumos contêm o conteúdo da conversa conforme a persistência solicitada e devem ser protegidas junto com os backups.
