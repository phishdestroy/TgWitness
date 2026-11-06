# O que foi testado

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/

O teste ao vivo no Telegram, as verificações automatizadas, as verificações no navegador e o que ainda não foi verificado.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidências e verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)

![Evidências e verificação](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Atualizado em 6 de novembro de 2026.** Os resultados estão vinculados à revisão, ao ambiente e à carga de trabalho registrados para cada execução. [Os recursos atuais](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) descrevem os fluxos de trabalho disponíveis; esta página registra o que foi efetivamente verificado.

[Gráficos de desempenho](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Auditoria em inglês com linguagem de sinais](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Medidas disponíveis para download](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Evidências mais recentes | Resultado | Escopo |
| --- | --- | --- |
| Auditoria de lançamento · 6, novembro | Testes do núcleo 1,461 aprovados; a plataforma 37 foi ignorada | Fonte `92e539af40d8`; conclusões em aberto mantidas |
| Exportações recentes · 6, novembro | 127.713 e 141.781 registros/s, ciclo completo | Duas contas por servidor; texto e metadados via WARP |
| Arquivos mantidos · 6, novembro | Arquivos 48; registros 3,598,381 verificados | Arquivos existentes verificados em relação às chaves fixadas do espaço de trabalho |
| Trusted Live · 5 de novembro | Gravação protegida da CPU e verificações WARP | O login oficial no Desktop e a exportação nativa permanecem sem restrições |
| Phala / Intel TDX · 4 de novembro | Todas as verificações do verificador 16 foram aprovadas em execuções posteriores | Implantação histórica; sem conta no Telegram no CVM |

**Nesta página**

- [Auditoria de lançamento e novas exportações · 6 de novembro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu e WARP · 5 de novembro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Implantação ao vivo do Phala Cloud · 4 de novembro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Inventário do diário do servidor ativo · 1 de novembro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Verificações recentes offline e com injeção de falhas · 1 de novembro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Teste ao vivo do Telegram, conta completa · 29 de outubro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Exportação protegida por senha aberta com libarchive · 29 de outubro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Teste ao vivo do Telegram · 27 a 29 de outubro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Medição sintética da capacidade local](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Pesquisa de texto completo em um milhão de mensagens · 5 de novembro de 2026](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Qualificação restante](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/#remaining-qualification)

## Auditoria de lançamento e novas exportações · 6 de novembro de 2026

A auditoria utilizou a versão v0.9.1 na fonte `92e539af40d8368d198ff5e040f1d876f2c1310e`, versão `92e539af40d8-83e41104669e`. Os testes de verificação de pacotes instalados foram aprovados em três servidores. O relatório assinado mantém o estado observado naquele momento.

[![Taxas de aquisição e exportação completa para duas novas cargas de trabalho](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Carga de trabalho | Registros | Aquisição | Ciclo completo | Taxa de ciclo completo |
| --- | --- | --- | --- | --- |
| Servidor A · duas contas | 27,030 | 189.043s | 211.647s | 127.713 registros/s |
| Servidor B · duas contas | 29,299 | 182.513s | 206.650s | 141.781 registros/s |

Ambas as exportações começaram sem retomada, excluíram anexos e avatares e terminaram sem nenhum registro duplicado ou reutilizado. O ciclo completo inclui preparação, aquisição, seleção, empacotamento e verificação do arquivo. O servidor A também executou uma verificação de leitura de bate-papos protegidos. Quatro eventos FloodWait no servidor A e três no servidor B foram respeitados. Essas observações não estabelecem uma garantia geral de taxa de transferência.

| Verificar | Resultado | Qualificação |
| --- | --- | --- |
| Núcleo pytest | 1,461 aprovado | A plataforma 37 ignora |
| Navegador / experiência do usuário do navegador / evidências / site | 102 / 66 / 15 / 9 aprovados | Esses programas se sobrepõem a outros testes; as contagens não são cumulativas |
| Complemento de captura | 124 aprovado | Três verificações oficiais da Web bloqueadas pela sandbox do Chromium exigida |
| Autorização da API | Rotas 269; solicitações 538 aprovadas | Credenciais ausentes e acesso revogado |
| Arquivos mantidos | 48 de 48 verificado | Registros 3,598,381; chaves fixadas no espaço de trabalho |
| Verificações de leitura em tempo real da frota | 24 dos perfis 40 foram aprovados | As rotas WARP 16 não foram aprovadas na qualificação; esses perfis não estavam conectados |

O relatório [assinado](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) registra todas as descobertas, incluindo três defeitos em um instantâneo de bate-papo secreto não publicado, ausente da versão principal auditada. A qualificação anterior [do histórico público](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) utilizou uma revisão e carga de trabalho diferentes; suas taxas não devem ser combinadas com esta comparação.

Verifique o relatório original usando a chave [fixada e o verificador](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Sua assinatura protege o relatório do operador contra alterações. Não se trata de um atestado independente, prova de autoria do Telegram ou certificação do GDPR.

## Trusted Live CPU Ubuntu e WARP · 5 de novembro de 2026

A execução de integração mantida utilizou um convidado Ubuntu 24.04.5 apenas com CPU (vCPU 4, 8 GiB) no QEMU dentro de um host RunPod com CPU. O coletor utilizou `14e642a5`; a verificação utilizou `02072461`. As correções finais foram mescladas no [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) como `755f78f6`, cuja árvore correspondia à cabeça do PR testado. Este não era um TEE.

- Um WARP Connector real foi relatado como em bom estado; o HTTPS por proxy indicou que o WARP e o Gateway estavam habilitados. Três sondas detectaram o mesmo endereço de saída, o que não garante um IP fixo.
- A desconexão do WARP fez com que a solicitação por proxy falhasse. O HTTPS direto do serviço de gateway foi rejeitado. No namespace do gravador, o IPv4/IPv6 direto, o DNS externo e o resolvedor UDP embutido do Docker foram bloqueados.
- Um token de provedor de escopo restrito e somente leitura podia ler os parâmetros de integridade/conexões, mas não podia ler o token de cadastro do conector. As observações assinadas do provedor incluíam amostras explicitamente indisponíveis. O witness era executado no host do operador; portanto, isso demonstra o registro e a retenção, e não a custódia por terceiros independentes.
- O Official Desktop chegou à tela de boas-vindas sem autenticação. A entrada de teclado protegida foi rejeitada durante a captura. Três segmentos de exibição H.264 foram decodificados e sua sobreposição de relógio foi inspecionada. O arquivo de pré-verificação do evento 18 foi verificado em relação à chave fixada do gravador e ao ponto de verificação retido.
- Os testes finais de captura foram aprovados nos casos 114 nas infraestruturas de integração contínua (CI) do Windows e do Linux, com versões reais do Chromium/FFmpeg. Cinco testes de referência e verificações de avisos de dependência foram aprovados.

Uma inicialização inicial com vCPU 2/4 GiB atingiu o tempo limite sob carga simultânea de construção de imagem e foi interrompida pelo mecanismo de proteção; isso não é considerado um sucesso. O login manual na conta de teste, a exportação nativa do chat, a comparação híbrida real e o logout pelo Telegram permanecem pendentes. Nenhuma sessão do Telethon fornecida foi importada. Anexos, OCR automático, verificação local de drand BLS e atestado Trusted Live TDX não foram qualificados.

## Implantação ao vivo na Phala Cloud · 4 de novembro de 2026

**Resultado histórico: as implantações posteriores** passaram em todas as verificações do verificador 16, incluindo o Intel TDX e o túnel rápido. As evidências de reinicialização, a descoberta de endereços assinados e os carimbos de data/hora dos relatórios foram verificados separadamente. Cada CVM de teste foi removido após sua execução.

| Configuração | Valor registrado |
| --- | --- |
| Provedor | Phala Cloud · `tdx.small` · US-WEST-1 |
| Implantação | `--provider phala --quick-tunnel`: espaço de trabalho inicialmente vazio |
| Coletor inicial | `df7d860c` · v0.8.1 |
| Coletor com todas as correções | `53a0f7e9` |
| Convidado de produção | `dstack-0.5.12`; acesso via SSH desativado |
| Serviços externos | ntfy.sh, GitHub e Intel PCS |
| Custo observado | Sete CVMs, totalizando cerca de 1.9 centavos de dólar; preços históricos de testes |

A sequência abaixo separa falhas iniciais, correções e verificações concluídas. Nenhuma conta do Telegram estava conectada a esses CVMs.

**Implantações 1–2 · diferenças entre provedores e verificações de regressão**

As duas primeiras implantações identificaram cinco diferenças em relação à Phala Cloud simulada. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) agora reproduz cada uma delas e falha sem a respectiva correção:

| No Phala Cloud | Antes da correção | Correção |
| --- | --- | --- |
| É necessário o `compose_file.name` | HTTP 422, nada foi criado | A configuração do Docker Compose contém o nome da CVM |
| A menos que seja fornecido um vazio, o Phala adiciona seu próprio script de pré-inicialização ao app-compose medido (v0.0.20: login no Docker, `docker compose pull`, senha de root, chaves SSH de `user_config`) | O `tdx_compose` falha: código fora da configuração publicada do Docker Compose | O app-compose define `pre_launch_script` como `""`; o Phala, então, o omite |
| Sem o `image`, o Phala seleciona o `dstack-dev-0.5.12`, a versão de desenvolvimento, com acesso SSH habilitado | O `server_state` falha. Apenas o registro de atestado de hardware foi aprovado nesta imagem; somente o registro do provedor e o `tdx_os` o apresentam | A implantação solicita a versão de produção do lançamento atual do Phala, `dstack-0.5.12` |
| Com o gateway dstack desativado, os detalhes da CVM nunca recebem um `instance_id` | A implantação aguarda 30 minutos e falha | O ID da instância é lido a partir do estado da CVM |
| Reinicializações, paradas e inicializações são operações do CVM, não revisões do aplicativo | O `provider_actions` não listou reinicializações | As operações de leitura também foram realizadas |

**Implantação 3 · atestado, verificações de acesso e evidências de reinicialização**

- A CVM executou o `dstack-0.5.12` com o acesso SSH desativado. O coletor publicou seu endereço assinado cerca de 1,5 minuto após a criação. A implantação foi então aprovada para o `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, registro de atestado de hardware v4, FMSPC `20a06f000000`, sem modo de depuração, não migrável, com suporte a dados de verificação criptográfica obtidos da Intel), `tdx_compose_hash`, `tdx_compose` (byte a byte) e `tdx_identity` (chaves KMS).
- O painel no endereço trycloudflare.com respondeu com código 401 sem um token ou com um token incorreto, e com código 200 com o token do painel.
- `verify` com `--source` definido para o arquivo do commit no GitHub e a impressão digital aprovada separadamente: servidor, `server_state`, firewall (sem gateway, sem endpoint público), log do provedor, extrato, impressão digital, hash de origem, inicialização e as cinco verificações `tdx_*` foram aprovadas. O Cloudflare e o `tdx_os` estavam indisponíveis, portanto, o resultado foi INCOMPLETO.
- Duas reinicializações por meio da API do Phala: em cada uma delas, a CVM voltou a funcionar em menos de dois minutos com a mesma chave de coletor, um novo endereço assinado e o antigo respondendo com o código 530. O `verify` relatou a nova inicialização e ambas as reinicializações como REVIEW. Com o `--evidence`, foram confirmadas as assinaturas do diário e três inicializações, cada uma com seu próprio registro de atestado de hardware Intel TDX proveniente do mesmo CVM.
- O `destroy` removeu apenas essa CVM. O espaço de trabalho ficou então vazio, e o endereço do painel deixou de responder.
- A verificação de preço do assistente do painel indicou `tdx.small` a US$ 0,058 por hora. Uma chave incorreta gerou uma mensagem simples “não aceitou a chave da API”.

**Correções subsequentes · descoberta de endereços assinados e medições do sistema operacional**

- Sem a chave de endereço, o `verify` seguiu a postagem mais recente e bem formada sobre o tópico de endereço, que está impressa na configuração publicada do Docker Compose. Uma postagem falsificada o enviou para um host que não existe, e o `statement` falhou: um falsificador não conseguiu se passar pelo coletor, mas conseguiu bloquear a verificação de terceiros por até 12 horas com um carimbo de data/hora futuro falsificado. O coletor agora também publica seu endereço assinado com sua própria chave; o `verify` aceita apenas essas publicações quando o coletor as faz, e as publicações são ordenadas pela hora de recebimento do ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) reproduz as postagens falsificadas. Um CVM executa isso apenas a partir de um commit que o contenha; portanto, o coletor desta execução ainda não assinou seu endereço e o `verify` indicou isso.
- O `tdx_os` não pôde ser executado sem o `dstack-mr`, cuja versão atual possui o `measure-os` em vez do `measure --json` mencionado na documentação. O verificador agora calcula o MRTD e o RTMR0-2 por conta própria a partir da imagem publicada e da configuração da VM, incluindo as tabelas ACPI.

**Implantação 4 · todas as verificações 16, selos de relatório e verificação de reinicialização**

- A implantação baixou o `dstack-0.5.12` publicado uma vez, comparou-o com o hash da imagem do SO que a CVM relatou, e o `tdx_os` foi aprovado: MRTD, RTMR0, RTMR1 e RTMR2 são iguais aos valores calculados para o QEMU 8.2.2, 1 vCPU e 2 GiB. O mesmo cálculo resultou em um RTMR0 diferente para os valores declarados de 4 GiB, 2 vCPUs, QEMU 9.2.1 ou uma segunda placa de rede, e falhou para um kernel, firmware ou linha de comando alterados e para a imagem de desenvolvimento.
- O `verify` foi aprovado em todas as suas 16 verificações, incluindo o conector do túnel rápido, portanto, o resultado foi APROVADO. Ele gerou o certificado em HTML e PDF, selado digitalmente com assinaturas e carimbos de data e hora, incluindo um carimbo de data e hora qualificado pelo eIDAS proveniente da unidade de carimbo de data e hora do governo belga, a TSU 202301 (status concedido na lista de confiança da Bélgica ), um carimbo de data e hora FreeTSA e a assinatura do verificador; o `check-report` confirmou todos eles e a assinatura do PDF.
- Após uma reinicialização, o `verify --evidence` confirmou duas inicializações, cada uma acompanhada por uma atestação de hardware gerada dentro da CVM e cada uma inicializada a partir do `dstack-0.5.12` publicado; a reinicialização e a nova inicialização foram classificadas como REVIEW.
- O `destroy` deixou o espaço de trabalho vazio.

**Implantação 5 · descoberta assinada pelo coletor e rejeição de postagens falsificadas**

O coletor foi executado a partir do commit `53a0f7e9`, que inclui as correções acima.

- O coletor publicou seu endereço assinado com sua própria chave, ao lado da publicação HMAC do operador. Duas publicações falsificadas foram então adicionadas ao tópico, uma com um HMAC zerado e outra assinada por outra chave Ed25519, ambas alegando uma data no ano de 2096. O `verify` utilizou o endereço assinado pela chave do coletor e passou em todas as 16 verificações; o selo trazia novamente o carimbo de data e hora belga qualificado, o carimbo de data e hora do FreeTSA e a assinatura do verificador, e o `check-report` confirmou esses elementos.
- Após uma reinicialização, o coletor publicou o novo endereço assinado: `verify` o encontrou imediatamente; o operador **localizou o endereço atual** 27 segundos depois a partir da publicação HMAC, e ambos ignoraram as publicações falsificadas. `verify --evidence` confirmou duas inicializações a partir de `dstack-0.5.12`.
- A implantação exibiu o valor que a Phala cobra pela CVM, incluindo o disco: US$ 0,06078 por hora.

### Assistente de painéis e escopo restante

O assistente do painel foi executado no Phala Cloud duas vezes: uma vez por meio de sua API de tarefas e outra vez por meio do navegador com um Chromium real: a verificação de preço, a criação com o commit sob **Advanced**, todas as seis verificações de atestado foram aprovadas, a lista de servidores exibindo o preço faturado (44,37 dólares por mês), **Find o endereço atual**, o download da configuração do Docker Compose medida e a exclusão. O navegador não detectou erros de página. Em ambas as ocasiões, o espaço de trabalho ficou vazio posteriormente.

Não incluídos: um domínio da Cloudflare no Phala, uma conta do Telegram no CVM e a imagem `dstack-0.6.1` . O preço do assistente antes da criação é apenas o preço de computação do Phala, já que sua API indica o preço do disco apenas para um CVM existente; a lista de servidores mostra o preço faturado após a criação. Todos os preços nesta seção foram observados em 4 de novembro de 2026.

## Inventário do diário do servidor em tempo real · 1 de novembro de 2026

Aproximadamente às 19:15 UTC, consultas SQLite `query_only` sequenciais somente para leitura contaram eventos em dez bancos de dados de áreas de trabalho em um servidor em execução. A coleta continuou durante as consultas; portanto, este não é um instantâneo atômico entre as áreas de trabalho.

| Observado nas dez bases de dados de espaços de trabalho | Contagem |
| --- | --- |
| Espaços de trabalho com pelo menos um evento `message.new` | 8 |
| Registros do diário, incluindo eventos operacionais | 1,610,818 |
| Eventos `message.new` | 900,232 |
| Eventos `message.edited` | 80,683 |
| Eventos `message.deleted` | 400,536 |
| Eventos `message.recovered` | 53,403 |
| Eventos `message.snapshot` | 2,183 |
| Eventos `media.saved` | 50,418 |
| Eventos `media.failed` | 5,575 |
| Eventos `coverage.gap` | 11 |
| Bytes do banco de dados, excluindo arquivos WAL e mídia | 7,909,003,264 |

Trata-se de **contagens de eventos**, não de mensagens, pessoas ou arquivos de mídia únicos. A mesma mensagem pode aparecer em mais de um espaço de trabalho, e uma edição ou exclusão pode gerar outro evento no diário. `media.failed` conta eventos históricos de falha, não a fila de mídia atual. As consultas **não** verificaram novamente as assinaturas nem a cadeia de hash completa de todos os 1,610,818 registros, não mediram a entrega ou a taxa de transferência, nem estabeleceram que todos os eventos do Telegram foram capturados. Nenhum conteúdo de mensagem, IDs de conta ou de chat, rótulos de espaço de trabalho, credenciais ou arquivos privados são publicados aqui.

Nesta revisão, o monitor público configurado separadamente abrangeu três fontes: uma resposta de captura estava OK e duas relataram `no_response`. Esse monitor não é um resumo de integridade de dez espaços de trabalho. `no_response` significa que o observador não conseguiu obter uma resposta naquela verificação; isso não indica perda de mensagem. O teste menor de 29 de outubro abaixo possui sua própria assinatura explícita e verificação de cadeia de hash.

## Verificações recentes offline e com injeção de falhas · 1 de novembro de 2026

Essas verificações utilizam dados fictícios e arquivos locais; elas fornecem evidências de regressão para a fonte atual, e não para outra medição de entrega do Telegram em tempo real:

| Verificar | O que foi testado |
| --- | --- |
| [Arquivo-fonte](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Duas compilações com bytes de código-fonte idênticos, mas com horários de arquivo alterados, produziram o mesmo ZIP e a mesma soma de verificação. Os bytes exatos do arquivo compactado e os hashes dos arquivos corresponderam; os arquivos de teste privados permaneceram excluídos. Uma falha simulada de gravação deixou o arquivo compactado e a soma de verificação anteriores intactos. |
| [Recuperação de exportação de conta](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Um erro simulado no disco no segundo membro do ZIP não resultou em nenhum ZIP publicado ou parcial. A retomada manteve todos os recibos assinados idênticos em cada byte, produziu um arquivo verificável de forma independente usando a impressão digital de assinatura esperada e reteve a lacuna de cobertura sintética como um resultado parcial. As asserções de escala protegem contra varreduras repetidas de tarefas e recibos à medida que os históricos crescem. |
| [Privacidade com divulgação minimizada](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Nomes e aliases Unicode sintéticos, metadados aninhados, remetentes desconhecidos e campos de mídia foram verificados nos três modos de identidade e com omissão de texto. Uma falha no limite de mascaramento não enfraqueceu silenciosamente a expurgação; a exportação original da conta assinada permaneceu inalterada. |
| [Decodificador de mídia para Linux e OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | Uma [verificação de CI do Docker no Linux](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) no commit `5a9e0814` foi aprovada com entradas geradas nos formatos Ogg/Opus, MP3, M4A, MP4 com vídeo, WAV e FLAC; controles de duração falsificada e referência a arquivos secundários; e 48 fixtures de analisador mutantes (34 rejeitados, 14 decodificados dentro dos limites). O OCR real do Tesseract foi executado com os bytes originais inalterados. O decodificador e o OCR foram executados em contêineres isolados da rede, sem um modelo do Whisper. |

As verificações são executadas nos fluxos de trabalho [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) e [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml). Elas testam esses limites de falha, não todas as possíveis falhas de armazenamento nem se uma divulgação é automaticamente segura para publicação. A verificação de mídia não mede a precisão do reconhecimento de fala nem a entrega pelo Telegram. Revise cada derivado antes de compartilhar.

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

As verificações do Docker/Compose e de instalação são registradas na CI; a implantação real do Phala e a verificação externa de carimbos de data/hora são descritas acima. Elas não estabelecem carga elevada sustentada, uma matriz completa de plataforma/função em tempo real, revisão de segurança independente, validação de arquivamento de longo prazo ou certificação forense. O estado salvo do MTProto e a atualização estão implementados; a reprodução atômica sem perdas em tempo real permanece por estabelecer. O backfill mais recente confirma mensagens e cursores de forma atômica e preserva as Ações Recentes disponíveis, mas sua cobertura sintética é distinta da qualificação em tempo real. Consulte [aceitação em tempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) para a matriz de qualificação controlada.

O diretório de auditoria pública  contém apenas o relatório assinado e as medições agregadas. Recibos operacionais detalhados, capturas brutas e material da conta permanecem privados. As capturas de tela do aplicativo em `docs/assets/` utilizam dados fictícios de demonstração.
