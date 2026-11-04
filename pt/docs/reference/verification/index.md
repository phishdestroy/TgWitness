# O que foi testado

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/

O teste ao vivo no Telegram, as verificações automatizadas, as verificações no navegador e o que ainda não foi verificado.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Contagem |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Verificar | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Teste ao vivo no Telegram, conta completa · 29 de outubro de 2026

A mesma conta continuou em funcionamento após o teste abaixo. Em 29 de outubro, às 12h10 UTC, seu escopo foi alterado para toda a conta (canais, grupos, conversas privadas e bots); o painel solicitou confirmação e o registro assinado registrou a ação. Às 17h59 UTC, o registro continha:

| Registrado de 27 de outubro, às 21h36, até 29 de outubro, às 17h59 (UTC) | Contagem |
| --- | --- |
| Registros do diário | 9,968 |
| Novas mensagens | 5,308 |
| deles após a mudança para a conta completa | 3,878 |
| Exclusões | 784 |
| das quais foram excluídas após o TgWitness ter salvo a mensagem | 596 |
| Edições | 41 |
| Mensagens adicionadas após novas verificações | 2,273 |
| Mensagens que uma nova verificação não conseguiu mais localizar | 18 |
| Mensagens salvas por meio de instantâneos do histórico | 242 |
| Anexos salvos | 247 |
| O coletor é iniciado | 19 |
| O Telegram FloodWait fica em pausa | 26 |

- A verificação **“Verify”** do painel confirmou as assinaturas e a cadeia de hash de todos os 9.968 registros.
- As mensagens vieram de 2 grupos ou canais e de 3 conversas privadas e bots. Um botão de mensagem foi pressionado na **seção “Conversas”**; a solicitação e a resposta do Telegram constam no registro.
- Novos chats foram adicionados quando o coletor escaneou novamente a conta após uma reinicialização. O salvamento das mensagens anteriores dos novos chats estava desativado (`history = 0`), portanto, isso não é abordado aqui.

Não abrangido: reações, alterações na lista de membros, perfis de pessoas, envio de mensagens, adesão por convite, proxies, notificações, o bot “witness” e o uso simultâneo de várias contas. Os arquivos públicos contêm apenas contagens.

## Exportação protegida por senha aberta com o libarchive · 29 de outubro de 2026

Um arquivo criado pelo código de criptografia de exportação (WinZip AES-256, formato lido pelo 7-Zip e pelo WinRAR ) foi aberto no Windows `tar` (bsdtar 3.6.2, libarchive). Com a senha correta, o arquivo extraído apresentou SHA-256 idêntico ao original; uma senha incorreta foi rejeitada com a mensagem “Senha incorreta ”. Os próprios programas 7-Zip e WinRAR não foram executados.

## Teste ao vivo no Telegram · 27 a 29 de outubro de 2026

Uma conta real do Telegram, conectada por meio do conjunto de pares de API integrado, registrou um supergrupo das **21h36 UTC de 27 de outubro às 05h15 UTC de 29 de outubro**. O coletor foi iniciado 12 vezes nesse período.

| Registrado | Contagem |
| --- | --- |
| Registros do diário, incluindo heartbeats e registros de serviço | 2,385 |
| Novas mensagens | 1,291 |
| Exclusões | 472 |
| das quais foram excluídas após o TgWitness ter salvo o texto | 347 |
| Edições | 12 |
| Mensagens perdidas durante a interrupção, adicionadas pela nova verificação | 12 |
| Anexos salvos | 17 |
| Anexos não baixados (opção de download desativada ou nenhum arquivo para baixar) | 14 |
| O Telegram FloodWait faz pausas de 3 segundos cada durante as novas verificações | 8 |

- As assinaturas e a cadeia de hash de todos os 2.385 registros são verificadas em relação à chave pública do diário.
- Após uma reinicialização, o coletor retoma a partir do estado de atualização salvo (`pts`) e o Telethon se atualiza; a nova verificação, então, adiciona as mensagens que ainda estão faltando.
- A cada FloodWait, o coletor aguardava o tempo solicitado e continuava.
- A conta permaneceu conectada, e a mesma sessão se reconectou em 29 de outubro.

Não abrangido por este teste: várias contas simultaneamente, funções de administrador, proxies, interrupções de serviço com duração superior a algumas horas e o [procedimento completo de aceitação em tempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Os arquivos públicos contêm apenas esses dados: sem identificadores de contas ou chats, mensagens ou credenciais.

## Medição sintética da capacidade local

Comando: `python tools/check_capacity.py --events 10000 --chats 100`

| Métrica | Observado |
| --- | --- |
| Entrada | 10.000 eventos de mensagens sintéticas em 100 fontes sintéticas selecionadas |
| Texto da mensagem | 400 caracteres; sem mídia ou rede |
| Ingestão | 53,273 segundos; 187,7 eventos/segundo |
| Latência do manipulador | p50 4,162 ms; p95 7,784 ms; máximo 129,118 ms |
| Exportação em ZIP | 19,868 segundos com o tracemalloc ativado |
| Picos de alocações de exportação rastreadas em Python | 0,51 MiB; não processar RSS |
| Tamanho do arquivo ZIP | 4.610.962 bytes |
| Verificação independente | Todos os 10.000 eventos foram verificados |

Isso mede o caminho local de gravação/exportação em série neste host Windows. Não mede a entrega via MTProto, contas simultâneas, limitação do Telegram, mídia, uma carga de trabalho de longa duração ou um número garantido de conversas reais. A medição é anterior à ferramenta final de registro de data e hora offline, a qual não altera o caminho das mensagens medidas.

## Qualificação restante

O diário em tempo real mantido registra efetivamente a coleta, as edições, os avisos de exclusão, os anexos, as verificações posteriores e o tratamento de limites de taxa. Ele não registra a entrega exaustiva nem uma matriz controlada de visibilidade de funções, atores de reação, FloodWait prolongado, bloqueios de contas e recuperação de interrupções de rede/processo. A emissão de tokens QR permanece distinta da confirmação por QR móvel concluída.

A compilação/execução no Docker, a instalação no Linux/macOS, a capacidade de suportar alta carga sustentada, a revisão de segurança independente, uma resposta TSA verdadeiramente independente, a validação de revogação/arquivamento de certificados e a certificação forense permanecem fora da qualificação registrada. O estado salvo do MTProto e a recuperação de dados estão implementados; a reprodução atômica durável ainda não foi estabelecida. A coleta de logs de administração, listas adicionais de reatores e polling curto prioritário continuam sendo recursos separados. Consulte [a aceitação em tempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) para a matriz de qualificação controlada.

Os recibos locais detalhados e as capturas de tela estão na pasta test-results/ (ignorados pelo Git). A captura de tela pública em docs/assets/ contém apenas dados fictícios de demonstração.
