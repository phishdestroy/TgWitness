# Linha de comando

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/cli/

Pesquise, leia o contexto, conte atividades e exporte mensagens salvas a partir de scripts e agentes, com saída no formato --json, códigos de saída estáveis e tokens de leitura exclusiva com escopo definido.

[MCP somente leitura](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/) · [Pesquisa de texto completo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Pré-visualização.** `tgwitness search`, `context`, `messages`, `stats` e `export` ler observações salvas para scripts e agentes de IA. Eles não podem enviar nada para o Telegram, alterar configurações nem modificar o diário assinado.

Com `--json`, a saída padrão (stdout) contém exatamente um documento JSON (`export` grava linhas JSON). O progresso, as dicas e os erros são direcionados para o stderr. Os códigos de saída são estáveis:

| Código | Significado |
| --- | --- |
| `0` | Sucesso, incluindo um resultado vazio |
| `1` | Falha: painel inacessível, dados ilegíveis, exportação interrompida |
| `2` | Erro de uso ou solicitação inválida: data incorreta, opção desconhecida, índice de pesquisa desativado |
| `3` | Indisponível no momento: o espaço de trabalho está aberto em um painel em execução, ou o painel solicita que se tente novamente mais tarde (limite de taxa, tempo limite) |
| `4` | Acesso negado: token ausente, expirado ou revogado; um chat fora do escopo; uma ferramenta que não permite |

## Duas maneiras de ler

**Por meio do painel (`--url`).** O comando utiliza a mesma API de arquivo com escopo que o MCP. Crie uma conexão em **Integrações → MCP**: escolha espaços de trabalho e chats, ferramentas e um prazo de validade; em seguida, copie o token uma vez. A conexão é somente para leitura, limitada a esses chats, com restrição de taxa de 60 solicitações por minuto e pode ser revogada ou renovada a qualquer momento. Os tokens de login do painel e as credenciais do Telegram não funcionam aqui.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Um painel remoto requer HTTPS; o HTTP simples é aceito apenas para `127.0.0.1`, `localhost` e `::1`. Variáveis de ambiente de proxy são ignoradas e redirecionamentos são recusados, de modo que o token chegue apenas ao endereço que você fornecer.

**Diretamente de um espaço de trabalho parado (`--data-dir`).** Lê o diretório de dados com acesso local total, sem um token. Use-o em uma cópia de um diretório de dados ou enquanto a coleta estiver parada. Registros assinados nunca são alterados; assim como no painel, abrir um espaço de trabalho pode atualizar seus índices derivados. Quando o painel tem o espaço de trabalho aberto, o comando sai com código `3`; leia pelo painel, em vez disso. Sem `--data-dir`, `TGWITNESS_DATA`, `./data/live` ou o diretório de dados da instalação que está executando o comando é utilizado.

`--workspace ID` seleciona um espaço de trabalho (padrão `default`). `tgwitness messages
--workspaces` lista aqueles que você pode ler.

## Comandos

| Comando | Resultado |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Melhores correspondências primeiro, incluindo formas de palavras, frases exatas entre aspas, domínios e `@username` ([sintaxe](https://phishdestroy.github.io/TgWitness/pt/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Texto exato, do mais recente ao mais antigo, sem o índice |
| `tgwitness context CHAT_ID MESSAGE_ID` | Mensagens salvas dentro de dez IDs de mensagem de cada lado |
| `tgwitness messages` | Conversas que você pode ler |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Mensagens salvas do chat, com as mais recentes em primeiro lugar |
| `tgwitness messages CHAT_ID --message ID` | Cada versão salva e registro de exclusão de uma mensagem |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Estatísticas de atividade, abaixo |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Observações salvas como linhas JSON na ordem do registro |

As datas são `2026-10-01` (meia-noite UTC) ou horários ISO com fuso horário, `2026-10-01T09:00+03:00`. Para `search`, `messages` e `export` eles selecionam a hora da observação. As páginas comportam até 50 registros: siga `next_offset` (`--offset`) para busca por classificação e `next_before` (`--before`) em outros lugares.

Ranked search stops at 1,000 results. The final page may be shorter than `--limit`; narrow the query, chat or period when more matching observations exist.

Cada resultado de mensagem contém `untrusted_content: true`os IDs do espaço de trabalho, do chat e da mensagem, a sequência do diário, o hash do registro salvo e um link para o painel. Edições, notificações de exclusão e `missing_on_recheck` são registros separados. A ausência de um registro não prova que um evento nunca tenha ocorrido.

### Estatísticas de atividade

`stats` Conta as observações salvas para um chat, um remetente ou todos os chats no escopo:

- mensagens por hora UTC e por dia da semana (começando pela segunda-feira), horários e dias de maior movimento;
- editados, excluídos e `missing_on_recheck` compartilhamentos;
- remetentes com contagem de mensagens e horários da primeira e da última mensagem;
- os domínios mais frequentes e `@handles`, contados uma vez por mensagem em todas as suas versões salvas;
- cobertura: `coverage.gap` registros e, para acesso a todo o espaço de trabalho, períodos sem um sinal de vida do coletor conectado (`collector_liveness`).

O período seleciona **a hora da mensagem informada pelo Telegram**. As contagens de horas e dias da semana podem ajudar a estimar o fuso horário do remetente; elas não o determinam. Os números são calculados mediante solicitação a partir do diário e não são armazenados. Cada resultado indica o cabeçalho do diário que abrange quando seu acesso abrange toda a área de trabalho. A leitura é interrompida após cinco segundos no painel ou `--timeout` segundos localmente (padrão: 30); então `complete` é falso e `partial` indica o primeiro registro que não foi lido. Nesse caso, apenas os registros mais recentes são contados.

### Exportar

`export` grava um objeto JSON por observação salva (novas mensagens, capturas de tela, edições, mensagens recuperadas, avisos de exclusão, `missing_on_recheck` e registros de mídia salvos) na ordem do diário. Cada linha possui os mesmos campos dos demais resultados, com o texto completo. Com `--output`, o arquivo é gravado com um `.partial` nome e é renomeado somente após o registro de conclusão do painel; uma exportação interrompida não deixa nenhum arquivo e encerra com o código `1`. `--output` nunca sobrescreve um arquivo existente. Com `--output` e `--json`, a saída padrão (stdout) exibe um resumo: contagem de registros, última sequência do diário e, para acesso a toda a área de trabalho, o cabeçalho do diário.

A exportação pelo painel requer uma conexão que permita **a exportação de mensagens (somente por linha de comando)**; essa opção não está selecionada por padrão. Este arquivo é uma cópia de trabalho, não uma prova: para uma transferência verificável, use a exportação assinada em **“Exportações”**, que `python -m tgwitness.verify`é verificada.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Habilidade do agente

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) explica a um agente como usar esses comandos, como citar registros e como tratar o texto capturado. Agentes que leem `.agents/skills` carregam-no a partir de um checkout do repositório. Para o Claude Code, copie a `tgwitness-cli` pasta para `.claude/skills/` dentro do seu projeto ou `~/.claude/skills/`.

## MCP e a linha de comando

Ambos utilizam as mesmas conexões, verificações de escopo e limites. Os resultados do MCP estão limitados a uma página de 64 KiB; portanto, o MCP não oferece exportação em massa; a linha de comando transmite os dados em fluxo contínuo. `get_activity_stats` está disponível para ambos.
