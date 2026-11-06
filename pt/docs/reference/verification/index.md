# O que foi testado

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/

O teste ao vivo no Telegram, as verificações automatizadas, as verificações no navegador e o que ainda não foi verificado.

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Implantação ao vivo na Phala Cloud · 4 de novembro de 2026

O `--provider phala --quick-tunnel` foi executado no **Phala Cloud** real (`tdx.small`, região US-WEST-1) com uma chave de API do Phala Cloud de um espaço de trabalho vazio, o ntfy.sh real, GitHub e Intel PCS. A CVM instalou o commit `df7d860c` (v0.8.1); as etapas de implantação, verificação e destruição foram executadas a partir da linha de comando com as correções abaixo. Sete CVMs custaram, no total, cerca de 1,9 centavos de dólar.

As duas primeiras implantações identificaram cinco diferenças em relação à Phala Cloud simulada. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) agora reproduz cada uma delas e falha sem a respectiva correção:

| No Phala Cloud | Antes da correção | Correção |
| --- | --- | --- |
| É necessário o `compose_file.name` | HTTP 422, nada foi criado | A configuração do Docker Compose contém o nome da CVM |
| A menos que seja fornecido um vazio, o Phala adiciona seu próprio script de pré-inicialização ao app-compose medido (v0.0.20: login no Docker, `docker compose pull`, senha de root, chaves SSH de `user_config`) | O `tdx_compose` falha: código fora da configuração publicada do Docker Compose | O app-compose define `pre_launch_script` como `""`; o Phala, então, o omite |
| Sem o `image`, o Phala seleciona o `dstack-dev-0.5.12`, a versão de desenvolvimento, com acesso SSH habilitado | O `server_state` falha. Apenas o registro de atestado de hardware foi aprovado nesta imagem; somente o registro do provedor e o `tdx_os` o apresentam | A implantação solicita a versão de produção do lançamento atual do Phala, `dstack-0.5.12` |
| Com o gateway dstack desativado, os detalhes da CVM nunca recebem um `instance_id` | A implantação aguarda 30 minutos e falha | O ID da instância é lido a partir do estado da CVM |
| Reinicializações, paradas e inicializações são operações do CVM, não revisões do aplicativo | O `provider_actions` não listou reinicializações | As operações de leitura também foram realizadas |

A terceira implantação:

- A CVM executou o `dstack-0.5.12` com o acesso SSH desativado. O coletor publicou seu endereço assinado cerca de 1,5 minuto após a criação. A implantação foi então aprovada para o `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, registro de atestado de hardware v4, FMSPC `20a06f000000`, sem modo de depuração, não migrável, com suporte a dados de verificação criptográfica obtidos da Intel), `tdx_compose_hash`, `tdx_compose` (byte a byte) e `tdx_identity` (chaves KMS).
- O painel no endereço trycloudflare.com respondeu com código 401 sem um token ou com um token incorreto, e com código 200 com o token do painel.
- `verify` com `--source` definido para o arquivo do commit no GitHub e a impressão digital aprovada separadamente: servidor, `server_state`, firewall (sem gateway, sem endpoint público), log do provedor, extrato, impressão digital, hash de origem, inicialização e as cinco verificações `tdx_*` foram aprovadas. O Cloudflare e o `tdx_os` estavam indisponíveis, portanto, o resultado foi INCOMPLETO.
- Duas reinicializações por meio da API do Phala: em cada uma delas, a CVM voltou a funcionar em menos de dois minutos com a mesma chave de coletor, um novo endereço assinado e o antigo respondendo com o código 530. O `verify` relatou a nova inicialização e ambas as reinicializações como REVIEW. Com o `--evidence`, foram confirmadas as assinaturas do diário e três inicializações, cada uma com seu próprio registro de atestado de hardware Intel TDX proveniente do mesmo CVM.
- O `destroy` removeu apenas essa CVM. O espaço de trabalho ficou então vazio, e o endereço do painel deixou de responder.
- A verificação de preço do assistente do painel indicou `tdx.small` a US$ 0,058 por hora. Uma chave incorreta gerou uma mensagem simples “não aceitou a chave da API”.

Duas outras constatações, corrigidas posteriormente:

- Sem a chave de endereço, o `verify` seguiu a postagem mais recente e bem formada sobre o tópico de endereço, que está impressa na configuração publicada do Docker Compose. Uma postagem falsificada o enviou para um host que não existe, e o `statement` falhou: um falsificador não conseguiu se passar pelo coletor, mas conseguiu bloquear a verificação de terceiros por até 12 horas com um carimbo de data/hora futuro falsificado. O coletor agora também publica seu endereço assinado com sua própria chave; o `verify` aceita apenas essas publicações quando o coletor as faz, e as publicações são ordenadas pela hora de recebimento do ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) reproduz as postagens falsificadas. Um CVM executa isso apenas a partir de um commit que o contenha; portanto, o coletor desta execução ainda não assinou seu endereço e o `verify` indicou isso.
- O `tdx_os` não pôde ser executado sem o `dstack-mr`, cuja versão atual possui o `measure-os` em vez do `measure --json` mencionado na documentação. O verificador agora calcula o MRTD e o RTMR0-2 por conta própria a partir da imagem publicada e da configuração da VM, incluindo as tabelas ACPI.

A quarta implantação, com os seguintes elementos:

- A implantação baixou o `dstack-0.5.12` publicado uma vez, comparou-o com o hash da imagem do SO que a CVM relatou, e o `tdx_os` foi aprovado: MRTD, RTMR0, RTMR1 e RTMR2 são iguais aos valores calculados para o QEMU 8.2.2, 1 vCPU e 2 GiB. O mesmo cálculo resultou em um RTMR0 diferente para os valores declarados de 4 GiB, 2 vCPUs, QEMU 9.2.1 ou uma segunda placa de rede, e falhou para um kernel, firmware ou linha de comando alterados e para a imagem de desenvolvimento.
- O `verify` foi aprovado em todas as suas 16 verificações, incluindo o conector do túnel rápido, portanto, o resultado foi APROVADO. Ele gerou o certificado em HTML e PDF, selado digitalmente com assinaturas e carimbos de data e hora, incluindo um carimbo de data e hora qualificado pelo eIDAS proveniente da unidade de carimbo de data e hora do governo belga, a TSU 202301 (status concedido na lista de confiança da Bélgica ), um carimbo de data e hora FreeTSA e a assinatura do verificador; o `check-report` confirmou todos eles e a assinatura do PDF.
- Após uma reinicialização, o `verify --evidence` confirmou duas inicializações, cada uma acompanhada por uma atestação de hardware gerada dentro da CVM e cada uma inicializada a partir do `dstack-0.5.12` publicado; a reinicialização e a nova inicialização foram classificadas como REVIEW.
- O `destroy` deixou o espaço de trabalho vazio.

A quinta implantação executou o coletor a partir do commit `53a0f7e9`, que contém todos os itens acima:

- O coletor publicou seu endereço assinado com sua própria chave, ao lado da publicação HMAC do operador. Duas publicações falsificadas foram então adicionadas ao tópico, uma com um HMAC zerado e outra assinada por outra chave Ed25519, ambas alegando uma data no ano de 2096. O `verify` utilizou o endereço assinado pela chave do coletor e passou em todas as 16 verificações; o selo trazia novamente o carimbo de data e hora belga qualificado, o carimbo de data e hora do FreeTSA e a assinatura do verificador, e o `check-report` confirmou esses elementos.
- Após uma reinicialização, o coletor publicou o novo endereço assinado: `verify` o encontrou imediatamente; o operador **localizou o endereço atual** 27 segundos depois a partir da publicação HMAC, e ambos ignoraram as publicações falsificadas. `verify --evidence` confirmou duas inicializações a partir de `dstack-0.5.12`.
- A implantação exibiu o valor que a Phala cobra pela CVM, incluindo o disco: US$ 0,06078 por hora.

O assistente do painel foi executado no Phala Cloud duas vezes: uma vez por meio de sua API de tarefas e outra vez por meio do navegador com um Chromium real: a verificação de preço, a criação com o commit sob **Advanced**, todas as seis verificações de atestado foram aprovadas, a lista de servidores exibindo o preço faturado (44,37 dólares por mês), **Find o endereço atual**, o download da configuração do Docker Compose medida e a exclusão. O navegador não detectou erros de página. Em ambas as ocasiões, o espaço de trabalho ficou vazio posteriormente.

Não incluídos: um domínio do Cloudflare no Phala, uma conta do Telegram no CVM e a imagem `dstack-0.6.1` . O preço exibido pelo assistente antes da criação refere-se apenas ao custo de computação do Phala, uma vez que sua API indica o custo do disco apenas para um CVM já existente; a lista de servidores mostra o valor faturado após a criação.

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

## Pesquisa de texto completo em um milhão de mensagens · 5 de novembro de 2026

Comando: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Um diário assinado determinístico com 1.000.000 de mensagens sintéticas em 200 conversas (formas de palavras em russo, ucraniano, inglês, chinês, japonês, links e identificadores) foi indexado em 71 segundos; o índice ocupou 58 MiB, além de um diário de 1,50 GiB. As buscas de melhor correspondência levaram de 9 a 190 ms (mediana), contra 2,4 a 3,2 segundos para a busca por subcadeia anterior . Resultados completos, hardware e limites: [Busca de texto completo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/search/#benchmark). `tools/test_fulltext.py` também verifica um arquivo assinado criado antes da pesquisa de texto completo (`tools/fixtures/evidence-before-fulltext.zip`) com o verificador atual, e um arquivo atual com o próprio arquivo `verify.py`.

## Qualificação restante

O diário em tempo real mantido registra efetivamente a coleta, as edições, os avisos de exclusão, os anexos, as verificações posteriores e o tratamento de limites de taxa. Ele não registra a entrega exaustiva nem uma matriz controlada de visibilidade de funções, atores de reação, FloodWait prolongado, bloqueios de contas e recuperação de interrupções de rede/processo. A emissão de tokens QR permanece distinta da confirmação por QR móvel concluída.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

Os recibos locais detalhados e as capturas de tela estão na pasta test-results/ (ignorados pelo Git). A captura de tela pública em docs/assets/ contém apenas dados fictícios de demonstração.
