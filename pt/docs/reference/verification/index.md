# O que foi testado

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/

O teste ao vivo no Telegram, as verificações automatizadas, as verificações no navegador e o que ainda não foi verificado.

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

As entradas mais antigas abaixo descrevem seus próprios testes; a maioria delas utilizou clientes de teste sintéticos. Os resultados automatizados mais recentes encontram-se abaixo.

## Listas públicas integradas do MTProxy · 29 de outubro de 2026

Este é o registro histórico de testes da versão original com seleção manual. Para os modos atuais de pool automático e IP, consulte [as configurações de conexão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes). As contagens e os recursos não suportados abaixo referem-se à revisão testada.

Adicionou-se um snapshot público integrado e uma atualização explícita via HTTPS a partir de SoliSpirit/mtproto e zakky8/mtproto-proxy-pro. Neste servidor, o programa de download do aplicativo obteve ambos os feeds com sucesso em 29 de outubro de 2026 às 12h58 UTC: **118 endpoints compatíveis únicos** após filtragem, deduplicação e o limite de 64 entradas por fonte. Isso verifica a recuperação da lista, não a conectividade ou a entrega de mensagens por meio desses pontos de extremidade. Nenhuma conta real foi conectada a um proxy listado durante este trabalho. [Guia do operador e do usuário](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Respostas de fonte com falha, vazias ou incompatíveis mantêm as entradas e datas anteriores. As atualizações não alteram a rota selecionada. Endereços públicos são validados e os IPs resolvidos são fixados na seleção; rotas operacionais/manuais permanecem separadas. O teste de conexão agora está disponível no painel antes do login na conta. TLS ee falso e seleção automática de proxy continuam sem suporte. O catálogo do operador substitui completamente as assinaturas.

- Conjunto completo de testes: **366 aprovados, 3 ignorados**, 287,94 segundos. Os avisos de dependências existentes e as omissões de plataforma permanecem. Regressão final da lista pública/localização: **36 aprovados**, incluindo a rejeição de portas inválidas de proxy de download; isso se sobrepõe ao conjunto completo de testes.
- Aceitação pelo navegador comprovada em inglês/russo, nos modos claro/escuro a 390/1440 pixels: opções integradas, sem busca externa ao abrir as configurações, atualização explícita, manutenção de rotas e cache durante falhas, verificação pré-login, isolamento da área de trabalho em caso de resposta tardia, detalhes da fonte e layout/contraste. Sem erros de JavaScript nem solicitações externas do navegador.
- A cobertura final da tradução estática foi aprovada para todas as 13 localizações; o novo texto foi traduzido para o russo, com versões em inglês explícitas em outras partes. O guia integrado atualizado foi aprovado nas verificações de layout e contraste em ambos os temas.
- Verificações preliminares e de publicação aprovadas (259 arquivos públicos, 1.354 links locais); atualizado O arquivo YAML de “Compose” e de CI foi analisado. O Docker e a CI remota não foram executados neste contexto.
- A roda reconstruída passou nos testes de instalação isolada, carregamento de lista de pacotes e verificação de exportação assinada . Todos os 69 recursos do pacote corresponderam ao espaço de trabalho; os hashes do código-fonte foram verificados.

Recibos: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` e `test-results/public-proxies-package.log`. Os dados de teste de navegador/conta/transporte são sintéticos; os dois downloads de feed acima são solicitações HTTPS reais.

## Apresentação de recursos opcionais · 29 de outubro de 2026

O antigo destino do bot Proof agora é **o Extras**: uma breve visão geral seguida por uma página de configuração separada para a opção selecionada. O formulário de testemunho possui três etapas, com gerenciamento de conexão, opções de rede e detalhes de implantação ocultados. O GitHub está explicitamente previsto e não possui formulário de credenciais. [Visão geral em russo](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- Foram aprovados 30 testes específicos para localização, configuração do TgWitness e verificações de publicação.
- A aceitação da configuração do Chromium foi aprovada em inglês/russo, nos modos claro/escuro, com resolução de 390/1.440 pixels: foco no teclado e tecla Enter, ausência de conexões implícitas ao selecionar recursos adicionais, retenção de rascunhos, downloads fixados de configurações/tokens, limpeza de tokens ao bloquear a tela e âncoras do guia local em funcionamento. Verificações de layout e contraste de texto em fundo sólido aprovadas.
- A aceitação da troca de área de trabalho foi aprovada, incluindo uma resposta de token atrasada que chega após a troca. A navegação rápida permite localizar os recursos adicionais por meio dos termos “bot”, “prova” e “GitHub”; seus testes existentes de 320/390/1440 pixels e de russo/RTL também foram aprovados.
- Não foram observados erros de JavaScript nem solicitações externas do navegador durante a execução da configuração. Trata-se de verificações sintéticas da interface do usuário, e não de novas evidências de publicações em tempo real no Telegram ou por bots.
- O carregamento final dos idiomas e a cobertura do dicionário foram aprovados para todas as 13 configurações regionais, preservando alternativas explícitas em inglês fora do russo. O guia de prova expandido também foi aprovado nas verificações de layout/contraste em 320/768/1440 pixels em ambos os temas.
- A versão reconstruída foi aprovada na verificação de instalação isolada e de exportação assinada. Todos os 67 recursos empacotados corresponderam ao espaço de trabalho; o arquivo-fonte contém 253 arquivos públicos. A verificação de fontes/links foi aprovada para 1.346 links de documentação locais.

Recibos: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` e `test-results/extras-artifacts.json`. As capturas de tela utilizam espaços de trabalho sintéticos.

## Auditoria da configuração do bot Witness e do proxy · 29 de outubro de 2026

A configuração do witness (agora **em Extras → Um bot no seu canal**) prepara um witness implantado de forma independente: chave coletora fixada, download de token com escopo definido, canal próprio, política de publicação, rota HTTP/SOCKS5 e API de bot personalizada. O token do bot permanece no host da testemunha. Seu novo `--check-config` valida a configuração e os arquivos sem abrir uma conexão de rede ou criar uma chave. Os caminhos dos arquivos JSON são resolvidos junto com a configuração. Todas as variantes da testemunha do Compose agora encaminham as configurações do proxy HTTP e da API do bot.

As configurações da conta oferecem suporte a um catálogo público do MTProxy gerenciado pelo operador, visualização personalizada de links de proxy do Telegram e aos campos manuais existentes. As respostas do catálogo omitem informações confidenciais; a seleção armazena a rota no cofre do espaço de trabalho. Catálogos ausentes ou com formato incorreto mantêm as rotas manuais disponíveis. Nenhum endereço de proxy do projeto ou serviço de testemunha hospedado é criado ou habilitado por padrão. Um exemplo do Caddy expõe apenas o endpoint head com escopo definido quando uma testemunha externa precisa acessar um coletor cujo painel permanece privado.

Validação:

- Conjunto completo: **348 aprovados, 3 ignorados**, 195,81 segundos. As limitações do Windows são responsáveis pelas omissões; os dois avisos de descontinuidade de dependências existentes permanecem.
- Execução final de regressão de testemunho/configuração/lançamento: **11 aprovados, 1 ignorado**. Isso abrange o conjunto completo de testes. Os testes incluem resolução de caminho, verificação prévia offline, assinatura/publicação por meio de um dispositivo real de API de bot HTTP em loopback, falha na entrega registrada, verificação de token de canal e exclusão de segredo de proxy.
- A aceitação da configuração do Chromium foi aprovada em inglês/russo com 390/1.440 pixels: configuração fixada e downloads de tokens, limpeza de tokens ao bloquear a tela, seleção de catálogo, visualização de links personalizados seguida de salvamento explícito, layout/contraste e ausência de erros de JavaScript ou solicitações externas do navegador. Corrigido o excesso de largura no cabeçalho da conta em russo e na guia de login.
- Aprovado nas verificações de Ruff, de fontes/links e na análise do YAML de composição/fluxo de trabalho.
- A versão reformulada passou pelas verificações de instalação isolada, de painéis/recursos estáticos e de autenticação via API, além de uma verificação independente de exportações sintéticas de 32 eventos, tanto diretas quanto transmitidas.

Comprovantes: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` e `setup-package.log`. Essas verificações utilizam contas sintéticas/proxies e um ambiente de teste local da API do Bot. Elas não pretendem simular uma publicação real do bot, um servidor MTProxy público em funcionamento, uma execução remota do CI ou uma implantação no Docker. O histórico real de observação do Telegram mantido acima permanece como uma prova separada. [Instruções de configuração](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Revisão da apresentação e da documentação · 29 de outubro de 2026

A página do produto, a tela de acesso, os arquivos README em inglês e russo e as imagens de apresentação agora compartilham um único estilo visual. As capturas de tela públicas utilizam dados de demonstração fictícios. A revisão também corrigiu as descrições desatualizadas sobre validação em tempo real e recuperação mencionadas acima.

- Localização direcionada, testes do site e de publicação: **33 aprovados, 1 ignorado**. O teste ignorado requer a criação de um link simbólico, o que não está disponível neste host.
- A aceitação geral do painel do Chromium foi aprovada, incluindo todos os catálogos de idiomas, layout RTL, temas claro/escuro, contraste sólido de texto e alternância de área de trabalho. A verificação de criação de perfil agora aguarda a resposta HTTP efetiva antes de verificar a área de trabalho selecionada.
- As telas de acesso em inglês/russo foram aprovadas nas verificações de layout e contraste em ambos os temas nas resoluções de 320, 390, 768, 850 e 1440 pixels; o botão de envio permanece na área de visualização inicial.
- A aceitação do site público foi aprovada em 320, 390, 768, 1024 e 1440 pixels, incluindo , ampliação de capturas de tela/tecla Escape/retorno ao foco, tabulação do teclado, rejeição da área de transferência, subcaminhos do projeto, movimento reduzido e o fallback sem JavaScript. Não foram observadas falhas em solicitações de recursos, solicitações externas ou erros de JavaScript.
- A versão reconstruída passou por uma verificação de instalação isolada: os recursos do painel e as configurações regionais são carregados, o acesso à API requer autenticação e as exportações diretas/por streaming verificam de forma independente todos os 32 eventos sintéticos. As verificações de Ruff e de fontes públicas/links foram aprovadas.

Recibos locais: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` e `design-package/install-receipt.json`. O conjunto completo de back-end não foi executado novamente para esta alteração na apresentação/documentação; seu resultado anterior permanece na auditoria pré-publicação.

## Versão 0.6.1

A versão 0.6.1 altera a apresentação do painel, os lançadores, a embalagem e a documentação; o código de coleta, armazenamento, assinatura e exportação permanece inalterado. No Windows 11 / Python 3.12.10 com o runtime fixado:

- O conjunto completo de testes foi aprovado em **137 testes,** com 2**omissões** e o aviso existente do Starlette. Os novos testes abrangem o tratamento do comando Ctrl+C pelo iniciador (o servidor dispõe de 30 segundos para uma parada ordenada) e falhas passíveis de ação nas etapas de configuração.
- O Chromium (shell sem interface gráfica 156) foi aprovado em todos **os 45 cenários gerais** e **nos 35 cenários de importação de conta/QR/chave de autenticação**, incluindo a verificação de contraste de texto sólido, ausência de transbordamento horizontal entre 320 e 1.440 px e campos de primeiro login visíveis em 320/390 px. Não foram observados erros de JavaScript na página nem solicitações externas.
- `python start.py --setup-only` reinstalou o pacote na versão 0.6.1 e `python start.py --check` informou que estava pronto. Um servidor `python -m tgwitness --demo` real retornou o painel, a folha de estilo, o script, o logotipo, o guia e a versão `/api/status` 0.6.1; o `workspace.css` removido retornou um erro 404.
- O `Start.cmd` encontrou uma instalação do Python fora do PATH. Na ausência de Python disponível, exibiu a oferta de instalação; ao recusar as instruções do manual impresso, encerrou a operação 1. A etapa de download no python.org baixou o instalador 3.12.10 e passou na verificação Authenticode da Python Software Foundation; o próprio instalador não foi executado neste host.
- `start.sh`, sem qualquer código Python, exibiu a dica de instalação e encerrou a execução. 1. `scripts\Docker.cmd` e `scripts/docker-start.sh` foram testados contra executáveis falsos do `docker`: sequência de chamadas correta, endereço do painel e saída do token, e nenhuma mensagem de sucesso após uma falha.
- O `python tools/build_portable.py` criou um pacote para Windows de 18,8 MiB após verificar a soma de verificação do embeddable-runtime fixado. Extraído para um caminho contendo espaços e iniciado com apenas diretórios `C:\Windows` no PATH, seu Python incorporado passou no teste `TgWitness-Check.cmd`, disponibilizou a demonstração (32 eventos) e um espaço de trabalho ativo, e o Chromium exibiu o diário e a aba de detalhes sem erros de JavaScript. Os dados foram gravados na pasta `data` do pacote.
- O `python tools/build_preview.py` produziu um arquivo-fonte com 110 arquivos. Um teste do `git add` listou os mesmos 110 arquivos, sem arquivos de sessão, chave, banco de dados, token, log ou exportação, sem caminhos absolutos locais e sem sequências de caracteres com formato de segredo.

Não foram executados nesta rodada específica de compilação de 27 de outubro: a instalação automática do Python em si, as verificações de compilação/Compose do Docker, as execuções no Linux/macOS ou um novo exercício com conta ativa . Evidências reais do Telegram estão registradas acima e nas verificações de conta anteriores abaixo. As definições de CI, por si só, não qualificam a execução da plataforma.

## Versão 0.6.0

O conjunto completo mais recente de testes de tempo de execução fixado no Windows 11 / Python 3.12.10 foi aprovado em **135 testes**, com **1 teste ignorado**, em 26,53 segundos e com o aviso existente do Starlette. A omissão requer permissões POSIX. Após adicionar o renderizador de QR às verificações de prontidão e medições de processo, 8 verificações de prontidão/espaço de trabalho afetadas também foram aprovadas.

A nova cobertura inclui esquemas do Telethon 7/8, esquemas do Pyrogram 2/3, chaves JSON completas e JSON apenas com metadados, arquivos de contas correspondentes/conflitantes, senhas do TData, adulteração de checksum e caminhos não seguros, conversão offline/autenticada na memória, verificações online de ID de conta, sucesso de QR/2FA/vencimento, cancelamento por expiração e isolamento de conta. Os fixtures do TData utilizam uma implementação separada do AES-IGE para criptografia.

O Chromium foi aprovado em **45 cenários gerais** e **35 cenários de importação de conta/QR/chave de autenticação**, sem que fossem observados erros de JavaScript na página ou solicitações externas. Novas verificações do navegador abrangem todos os quatro formatos de entrada em conjunto: TData protegido, metadados da API, renderização de QR, expiração/nova tentativa, 2FA, rejeição de conta incorreta, cancelamento de bloqueio/espaço de trabalho, layout responsivo e respostas de conversão tardias após a seleção de um arquivo mais recente.

Ambos os conjuntos de navegadores foram aprovados novamente após as alterações na entrada da conta. A configuração em tempo real abre o formulário de conta; o modo de demonstração abre seu diário de amostra. A página de demonstração da conta exibe instruções de inicialização em tempo real e oculta os campos de inserção de credenciais. Verificações específicas em 320, 390 e 1.440 pixels confirmaram que o campo numérico e o botão principal caberam na tela sem necessidade de rolagem, que os campos da API estão inicialmente recolhidos e que o contraste do texto permanece legível. Os controles de captura e verificação permanecem ocultos após a abertura de suas novas seções expansíveis.

O fluxo direto da Chave de Autenticação foi testado com credenciais sintéticas por meio dos pontos de extremidade reais de importação e autorização. As verificações abrangem chaves incompletas, DC ausente, IDs de usuário imprecisos, identidade de conta incompatível, credenciais de API salvas, progresso visível da solicitação, limpeza de segredos e respostas atrasadas após edições ou alterações de método. Todos os quatro métodos de login foram verificados em 320, 390 e 1.440 pixels. O seletor de arquivos precede as orientações de formato, e o botão “Conectar” se ajusta à janela de visualização inicial de 844 pixels com as configurações da API ocultas. Nenhuma autorização real com chave de autenticação foi tentada neste teste de aceitação da interface do usuário.

A atualização do painel foi verificada novamente com ambos os conjuntos de navegadores: não foram observados erros de JavaScript na página nem solicitações externas. O conjunto de contas agora abrange a inserção de um par de ID/hash da API, rejeitando pares malformados ou múltiplos sem substituir campos, orientações exclusivamente sobre metadados e ignorando respostas de importação desatualizadas após uma mudança no método de login ou edição manual de credenciais. Seis verificações adicionais específicas foram aprovadas para o guia de configuração, início/pausa explícitos, recuperação de pesquisa vazia e layout final da conexão/guia local, além de contraste de texto sólido em 320, 390 e 1.440 pixels. A atualização do login direto adiciona uma única operação de solicitação de telefone/código e reutiliza o par de API salvo no espaço de trabalho atual para login por telefone, QR e sessão. O conjunto completo de testes em Python acima inclui novos testes de persistência, rejeição de credenciais parciais e isolamento do espaço de trabalho . As verificações no navegador abrangem a entrada direta do número de telefone, a reutilização de credenciais salvas, o roteamento apenas por metadados, a autorização de arquivos com um único botão e a rejeição de contas duplicadas. Os formulários simplificados de token de painel e de telefone também foram verificados sem rolagem inicial em 320, 390 e 1.440 pixels. Uma verificação de compatibilidade confirmou que o formulário direto de telefone pode utilizar os endpoints de configuração/código anteriores enquanto um processo mais antigo ainda estiver em execução.

Uma conta fornecida pelo usuário foi verificada separadamente, fora dos ambientes de teste públicos. Suas entradas Telethon, Pyrogram e TData corresponderam à mesma autorização; o arquivo JSON associado forneceu as credenciais da API. Todos os quatro arquivos foram carregados por meio do painel 0.6.0 e o Telegram confirmou o ID numérico esperado da conta. Os arquivos de origem permaneceram inalterados. Nenhuma fonte foi selecionada e a observação permaneceu desativada. Isso constitui um exemplo de importação/login, não de coleta, recuperação ou capacidade em tempo real.

O Telegram também emitiu um token QR real, que foi cancelado sem ter sido escaneado. Os fluxos completos de confirmação por QR e 2FA foram testados com clientes sintéticos; a confirmação por dispositivo móvel em um aplicativo real do Telegram continua sendo uma etapa de aceitação separada. Nenhum identificador de conta real, senha ou captura de tela está incluído nos arquivos públicos.

A atualização do iniciador foi concluída; o código-fonte, os metadados instalados e o marcador de prontidão relatam a versão 0.6.0, com o código QR 8.2 e um `pip check` aprovado. O wheel instalado forneceu o painel e o guia, rejeitou solicitações de API não autenticadas e verificou de forma independente exportações sintéticas diretas e transmitidas de 32 eventos. O guia offline atualizado foi verificado em 320, 390 e 1.440 pixels. As capturas de tela públicas continuam sendo sintéticas.

A versão de código-fonte contém 107 arquivos incluídos na lista de permissões. Os links para a documentação local estão ativos. A execução via Docker/Caddy, a publicação remota de CI/pacotes, o ambiente de execução ARM64, a coleta contínua e a matriz completa de aceitação do Telegram em tempo real permanecem sem qualificação neste documento.

## Versão 0.5.1

No Windows 11 / Python 3.12.10, o conjunto completo do ambiente do projeto foi aprovado: **94 aprovados, 2 ignorados**, em 31,21 segundos, com o aviso existente do Starlette. As omissões exigem permissões POSIX e a criação de links simbólicos, indisponíveis neste host. O fixture HTTP de download exibiu um diagnóstico da thread de solicitação; todas as asserções foram aprovadas. Esta execução não confirma a ausência de problemas de transporte no host.

Novos exercícios de cobertura de regressão incluíram StringSession, alterações no código e na conta 2FA, cancelamento da pesquisa de identidade, cancelamento de login pendente e atualizações por meio de manipuladores registrados em clientes ativos, rejeitados, substituídos e de teste. Apenas o coletor ativo contribui com eventos; as credenciais salvas e o histórico assinado permanecem intactos. Outras novas verificações abrangem a pesquisa Unicode após a reabertura de um banco de dados, a inclusão de limites de política de monitoramento no Coverage e exclusões de pacotes de código aberto.

O projeto `pythonw.exe` lançou um painel sintético isolado, retornou HTTP 200 e reteve os diagnósticos de inicialização no `logs/server.log`. O log não conteve o token do painel gerado nem os registros de acesso HTTP. O teste encerrou apenas seu próprio processo sintético. Nenhuma tarefa do Agendador de Tarefas foi registrada; logon/logoff, suspensão e recuperação de serviço continuam sendo requisitos distintos.

A aceitação no Chromium foi aprovada em **45 cenários**, sem erros de JavaScript na página e sem solicitações externas observadas. Novas verificações abrangem datas e horários da linha do tempo em 601/768/850 pixels, rascunhos de anexos durante a atualização de status, edições mais recentes feitas durante o salvamento, resultados de verificação apagados na troca de conta, respostas de verificação atrasadas após sair e voltar da página, e limites explícitos de verificação quando novos eventos chegam. O espaçamento do ícone de pesquisa e do texto também foi corrigido, e o conjunto de navegadores foi executado novamente.

A execução no navegador utilizou o ambiente de execução fixado em `.venv` e o Playwright 1.62.0/Chromium fornecido pelo sistema, anexado após o ambiente do projeto no caminho de importação. A instalação opcional de uma dependência de desenvolvimento foi interrompida durante um download lento do Playwright; nenhuma nova versão da ferramenta de navegador foi qualificada. Um `python start.py --setup-only` normal concluiu a atualização do aplicativo. O código-fonte, os metadados instalados e o marcador do iniciador indicam a versão 0.5.1; o `pip check` foi aprovado. As verificações de prontidão foram aprovadas em um caminho novo e não utilizado, mantendo o aviso esperado sobre a chave do cofre local.

O pacote 0.5.1 foi instalado separadamente e submetido a testes de verificação básica: todos os recursos de painéis/guias foram disponibilizados, o acesso não autenticado à API foi rejeitado e os arquivos ZIP de evidências, tanto diretos quanto transmitidos, contendo 32 eventos, foram aprovados em verificação independente. Os arquivos do aplicativo no pacote instalado foram comparados com o código-fonte. O arquivo público do código-fonte utiliza uma lista de permissões explícita de tipos de arquivo e recusa arquivos-fonte vinculados; o material de tempo de execução colocado dentro dos diretórios de código-fonte é excluído pelos testes de regressão.

Durante a execução da correção de código, a seleção de código aberto e o conjunto de candidatos do Git continham 86 arquivos, sem diretórios de dados de tempo de execução incluídos. Uma varredura em busca de padrões reconhecíveis de chave privada, token do GitHub, token de bot do Telegram e StringSession não encontrou correspondências. Trata-se de uma verificação de padrões delimitada, não de uma auditoria abrangente de segredos. As sondagens de regras de ignorar abrangem doze artefatos comuns de conta/dados/exportação. O YAML de fluxo de trabalho/issue/Compose e o script de tarefa do Windows foram analisados com sucesso. Os links para a documentação local foram resolvidos.

Todas as sete conclusões da análise de 27 de outubro foram abordadas. A execução do fluxo de trabalho no GitHub, o ambiente de execução em Linux/macOS/Docker, o Telegram real, a interoperabilidade com proxies externos/TSA e a qualificação para carga sustentada permanecem fora desta execução local. Não foi realizada nenhuma publicação em repositório, registro de serviço ou coleta de contas reais. Não foi realizada nenhuma publicação em repositório, registro de serviço ou coleta de contas reais.

### Atualização da documentação em inglês

O arquivo README, a referência de conta/sessão, o fluxo de trabalho de coleta e o guia incluído agora descrevem as entradas suportadas, o comportamento da área de trabalho, as políticas de eventos e os formatos de exportação em inglês. As três capturas de tela públicas foram atualizadas utilizando dados sintéticos. Nesse momento, a seleção de código aberto continha 88 arquivos, incluindo os dois novos guias. Todos os 131 links locais em 23 documentos Markdown estão funcionando corretamente.

Após as edições na interface e no guia, a aceitação no Chromium voltou a ser aprovada em todos os 45 cenários, sem que fossem observados erros de JavaScript na página ou solicitações externas. O conjunto completo de testes em Python não foi executado novamente para esta atualização da documentação e da apresentação; o resultado de 94 aprovações acima refere-se à execução anterior de correção de código.

A roda reconstruída foi instalada em um novo alvo isolado. Seus componentes de painel e guia funcionaram com sucesso, o acesso não autenticado à API foi rejeitado e tanto as exportações diretas quanto as transmitidas foram aprovadas na verificação independente de 32 eventos sintéticos.

### Atualização sobre instalação e implantação

As verificações específicas do instalador, do pacote e da prontidão foram aprovadas **em 14 testes**, com uma omissão devido à impossibilidade de criação de um link simbólico. As verificações do wrapper nativo abrangem caminhos com espaços, encaminhamento de argumentos, modos de configuração/demonstração e propagação de saída diferente de zero. As verificações do Git Bash testam o auxiliar de shell do Docker com um daemon simulado, incluindo ausência do Docker, ausência do Compose, falha na espera de integridade e uma inicialização bem-sucedida em porta alternativa. Essas verificações simuladas não estabelecem a compatibilidade de tempo de execução do Docker.

Uma cópia completa de código aberto foi instalada em um novo diretório do Windows cujo caminho contém espaços. O `scripts\Setup.cmd` criou um novo ambiente e instalou o runtime fixado; o `Start.cmd --check --json` informou estar pronto sem criar seu diretório de dados de destino. O `pip check` foi aprovado. A roda reconstruída também foi aprovada na verificação do pacote instalado, incluindo exportações diretas e transmitidas de 32 eventos.

Sintaxe do Shell e cinco arquivos YAML de fluxo de trabalho/Compose analisados. As configurações de código-fonte e de imagem do Compose estão alinhadas quanto às definições de armazenamento e de tempo de execução. Nessa etapa, todos os 139 links locais em 23 documentos Markdown foram resolvidos. A seleção de código-fonte público contém 99 arquivos.

As definições de CI agora realizam uma nova configuração nativa no Windows/Linux/macOS, gerenciamento do Compose (integridade/controle de acesso/persistência) durante a recriação de contêineres e configuração do Caddy. O fluxo de trabalho de lançamento condiciona a publicação a essas verificações e adiciona um teste de funcionalidade emulado em ARM64. O Docker não está disponível neste host: a execução real do Compose/Caddy, a emissão de certificados, a execução em ARM64 e a publicação remota de fluxos de trabalho/pacotes continuam sem restrições localmente. O código do aplicativo/interface do usuário não sofreu alterações com esta atualização; os resultados completos anteriores em Python e no navegador não foram reexecutados.

## Versão 0.5.0

O conjunto completo de testes de tempo de execução fixados foi aprovado: **81 aprovados, 1 ignorado**, em 22,00 segundos, com o aviso existente do Starlette. A verificação de permissões POSIX é ignorada no Windows. Os novos testes de manipulador enviam mensagens, edições, exclusões com ou sem escopo, reações, atualizações de participantes e mensagens do serviço de associação por meio de diferentes políticas. Categorias desativadas não geram observações em tempo real correspondentes; diagnósticos de cobertura e instantâneos explícitos permanecem disponíveis. Os testes verificam a persistência da política, a separação de espaços de trabalho, registros de auditoria assinados antes e depois, o comportamento de política inalterada, a validação rigorosa e a inclusão no próximo recebimento do processo.

Os testes de acesso à demonstração verificam que sua funcionalidade difere do token do painel configurado, não permite a autorização de um espaço de trabalho ativo, não permite alterar as configurações de coleta e não é emitido nem aceito para solicitações remotas, encaminhadas, de origem cruzada ou com host inválido. Abrir uma demonstração armazenada sem o sinalizador explícito de demonstração não habilita o acesso automático.

A aceitação do Chromium foi aprovada **em 39 cenários**, incluindo acesso à demonstração local sem inserção de token, predefinições de monitoramento, a transição da seleção de fonte para a política, independência por conta e verificações de layout para desktop/320/390 pixels e contraste de texto. Não houve erros de JavaScript na página. As solicitações injetadas pelo AdGuard no host permanecem no registro. O teste HTTP de download registrou uma reinicialização da conexão após um cliente ter encerrado sua conexão; as verificações ainda foram aprovadas. Este não é um resultado de serviço em produção.

O lançador padrão atualizou o ambiente isolado para a versão 0.5.0; as versões do código-fonte e da versão instalada estão em conformidade e a verificação via pip foi aprovada. As verificações existentes de criptografia do cofre de segredos, rejeição de chaves incorretas ou ausentes e integridade de assinaturas e arquivos de mídia foram aprovadas no conjunto completo de testes. Não há indicação de nova criptografia do conteúdo das mensagens ou dos anexos pelo aplicativo.

A demonstração local é reiniciada para disponibilizar a interface de usuário atualizada. Os registros sintéticos existentes são mantidos; interromper o antigo processo de demonstração em segundo plano cria um limite offline na próxima inicialização. Nenhuma sessão real do Telegram é utilizada para essas verificações.

O painel em execução no localhost:8787 apresentou a versão 0.5.0, acesso automático à demonstração, os cinco controles de monitoramento e 33 eventos sintéticos retidos no diário. O wheel 0.5.0 instalado separadamente forneceu todos os recursos do painel/guia, rejeitou o acesso não autenticado à API e produziu um arquivo ZIP verificado com 32 eventos, tanto diretamente quanto por meio do auxiliar de download por streaming. As versões dos pacotes em tempo de execução permanecem fixadas conforme registrado para a versão 0.4.

## Versão 0.4.0

O conjunto completo de testes de tempo de execução fixado foi aprovado: **78 aprovados, 1 ignorado**, em 19,77 segundos. A verificação ignorada requer permissões POSIX; o aviso de descontinuação do Starlette TestClient no código-fonte original permanece. Novos testes abrangem download por stream e roteamento do espaço de trabalho, cabeçalhos de autorização, recusa em sobrescrever, redirecionamentos, respostas truncadas, limites de tamanho anunciados/reais, leituras delimitadas, limpeza, sistemas de arquivos sem links físicos, falhas de prontidão e modos de inicialização que não devem instalar pacotes. Os testes de exportação confirmam a existência de arquivos temporários locais no espaço de trabalho e a limpeza seletiva de arquivos órfãos.

A aceitação no Chromium foi aprovada em todos os 36 cenários listados, sem erros de JavaScript na página. A ferramenta simula login por telefone/código/2FA, sessões convertidas, dois espaços de trabalho e rotas/estados separados, observações, assinaturas, pontos de verificação e solicitações de carimbo de data/hora, além de:

- Layouts para desktop e de 320/390 pixels, sem transbordamento horizontal, navegação visível, e o primeiro campo de login dentro da janela de visualização inicial de 844 pixels.
- Contraste do texto em fundo sólido de acordo com os limites de texto da WCAG AA. Controles desativados, opacidade e fundos com imagens ou gradientes estão excluídos; esta não é uma auditoria completa da WCAG.
- Uma resposta real de exportação local gerada por meio de um simulador de seletor de arquivos do sistema operacional/gravável, seguida de verificação independente do ZIP; o cancelamento não envia nenhuma solicitação de exportação.
- Uma falha na gravação interrompe o envio para o destino; o mecanismo de fallback de 128 MiB rejeita uma resposta anunciada com tamanho excessivo sem alocar uma carga útil correspondente.
- O guia local em inglês para desktop e para ambas as larguras reduzidas.

A caixa de diálogo de salvamento do sistema operacional e as gravações reais no navegador, com vários gigabytes, não foram automatizadas nem qualificadas. Os testes de download em Python utilizam blocos delimitados e dispositivos de loopback. A aceitação total da implantação com o Telegram real permanece separada.

O instalador padrão atualizou o `.venv` para a versão 0.4.0. O código-fonte e os metadados instalados estão em conformidade; o `pip check` foi aprovado. O `python start.py --check --json` foi declarado pronto em um novo caminho sintético, sem criar o diretório de dados. Seu aviso sobre o armazenamento de chaves locais permanece válido: os registros e arquivos de mídia não são criptografados pelo aplicativo.

O pacote wheel 0.4.0 foi compilado e instalado em um diretório separado. Todos os 23 arquivos do aplicativo correspondem ao código-fonte byte a byte. O pacote instalado exibiu o painel e o guia/recursos em inglês, rejeitou o acesso não autenticado à API e exportou um arquivo ZIP sintético com 32 eventos que passou na verificação. Seu comando de download por streaming também obteve um arquivo ZIP verificado de forma independente a partir do aplicativo instalado em execução.

A documentação pública e o guia local estão em inglês; os links para a documentação local funcionam. O PowerShell analisou o modelo de tarefa do Windows e o Python analisou o arquivo plist do macOS. Trata-se de verificações de sintaxe, não de execução de serviço. Nenhuma tarefa/serviço foi registrado. A configuração de CI agora inclui verificações de prontidão, mas a CI remota não foi executada aqui.

A execução do navegador na versão 0.4 observou novamente a injeção do AdGuard pelo host e o erro OSError 10022 do Windows relacionado à limpeza de soquetes asíncronos. As verificações do navegador foram aprovadas; essas observações ambientais são mantidas, em vez de serem tratadas como comportamento fixo do aplicativo. As tentativas iniciais de sandbox do OpenSSL/navegador/pip falharam; as execuções qualificadas bem-sucedidas utilizaram execução aprovada fora da sandbox.

## A versão 0.3.1 concentrou-se em correções de preparação

As verificações do lançador, do armazenamento de evidências e da API foram aprovadas: **31 aprovadas, 1 ignorada**, um aviso do Starlette no código-fonte. A verificação ignorada verifica as permissões de diretório POSIX e não consegue estabelecer essas permissões neste host Windows. O teste com Python antigo simula o limite de versão/importação; nenhum interpretador Python 3.10 foi instalado ou qualificado. O conjunto de testes 0.3, que havia sido aprovado anteriormente, está registrado abaixo; o conjunto completo de testes e os cenários de navegador não foram executados novamente para essas alterações específicas.

O iniciador padrão atualizou o ambiente local para a versão 0.3.1; os metadados de origem e os instalados estão em conformidade, e a verificação do pip foi bem-sucedida. Um wheel 0.3.1 instalado separadamente serviu o painel/ativos, rejeitou o acesso não autenticado à API e produziu uma exportação sintética verificada de 32 eventos. O YAML do fluxo de trabalho foi analisado, mas a nova verificação de tempo de execução do contêiner não foi executada: não havia nenhum tempo de execução local utilizável do Docker/Podman/Linux disponível.

Consulte [as conclusões sobre a prontidão](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) para conhecer as lacunas remanescentes em termos de usabilidade, serviço ativo e plataforma. Esta correção não certifica sistemas operacionais adicionais.

## Versão 0.3.0

O conjunto completo de testes de tempo de execução fixados foi aprovado: **61 testes**, com um aviso de descontinuação do Starlette TestClient no código-fonte original. Os metadados de tempo de execução indicam TgWitness 0.3.0 e python-socks 2.8.2; a verificação do pip foi aprovada. A execução de aceitação no navegador foi aprovada sem erros de JavaScript na página.

O wheel 0.3.0 foi compilado e instalado em um diretório de pacotes separado. Ele forneceu o painel e os recursos, rejeitou uma solicitação de API não autenticada e exportou um registro sintético de 32 eventos que passou por verificação independente. Os links da documentação local funcionam. Após a correção da normalização de chave simples do MTProxy, todos os nove testes de conexão/segurança foram executados novamente com sucesso.

A nova cobertura inclui:

- Nome de usuário/senha SOCKS5 e HTTP CONNECT por meio de servidores de teste de loopback reais; um proxy configurado que não está funcionando falha, em vez de recorrer ao destino.
- Validação de proxy, seleção de transporte MTProxy, rejeição de segredos TLS falsos, persistência, isolamento do espaço de trabalho, rejeição de alterações durante a observação e exclusão de segredos do status da API e de eventos assinados.
- Conversão somente para leitura dos esquemas SQLite sintéticos 7 e 8 do Telethon; hash de origem inalterado; rejeição de outros formatos, visões SQL e de um arquivo WAL pendente.
- Chave-mestra externa do cofre: diferentes chaves derivadas do espaço de trabalho, reabertura bem-sucedida, rejeição em caso de chave incorreta ou ausente e nenhuma migração implícita de cofres locais existentes.
- Configurações de proxy do navegador, limpeza de credenciais, divulgação de proteção de armazenamento, página de conexão móvel, autorização de arquivos de sessão convertida, rotas separadas, e todos os cenários de coleta/exportação abordados anteriormente com um cliente falso do Telegram.

Durante o desenvolvimento, um teste de loopback aguardou indefinidamente pelo desligamento do par; outra execução observou uma reinicialização da conexão no Windows após o handshake. O fixture agora delimita toda a troca de dados e trata o EOF/reinicialização após um handshake concluído como encerramento da conexão. As asserções de handshake/autenticação continuam sendo necessárias. Isso não qualifica provedores de proxy reais nem implica em um defeito fixo no transporte do Telegram.

A observação sobre a solicitação do AdGuard descrita abaixo continua válida. Não foi utilizada nenhuma conta real do Telegram, proxy SOCKS/HTTP externo ou servidor MTProxy em produção. O MTProxy é experimental e suas opções selecionadas/validação de segredos foram verificadas, mas não a interoperabilidade em produção. Novos comandos de conversão de chaves externas e de sessão foram testados apenas com segredos sintéticos. Linux/macOS/Docker permanecem sem qualificação neste contexto.

A medição de taxa de transferência da versão 0.2 apresentada abaixo não foi repetida e não deve ser apresentada como um novo benchmark para múltiplas contas/proxy para a versão 0.3.

## Versão 0.2.0 de referência

Testado no Windows com Python 3.12.10. Nenhuma conta real do Telegram foi conectada.

| Verificar | Resultado |
| --- | --- |
| Conjunto de ferramentas em Python | 52 testes foram aprovados no ambiente de desenvolvimento e 52 foram aprovados com o runtime fixado; um aviso de obsolescência do Starlette TestClient do upstream em cada execução |
| Sintaxe do JavaScript | Aprovado com Node.js |
| Aceitação do Chromium | Aprovado; sem erros de JavaScript na página |
| Layout para desktop/dispositivos móveis | Verificado nas resoluções 1440 × 1060 e 390 × 844; sem transbordamento horizontal do documento |
| Conteúdo da mensagem no formato HTML | Exibido como texto; o script inserido não foi executado |
| Fluxo de exemplo de conta | Credenciais da API → telefone → código → 2FA → selecionar grupo → iniciar → captura de tela → pausar → recarregar |
| Evidências no navegador | Comparação de edições, conteúdo anterior após a exclusão, filtros, download em ZIP, ponto de verificação, recibo de processo assinado, download de solicitação conforme a RFC 3161 e vinculação de ponto de verificação |
| Múltiplas contas | Registros, chaves, fontes e estados em tempo real separados; a troca de navegador mantém o outro coletor em execução; os espaços de trabalho são reabertos após a reinicialização; contas duplicadas e reatribuições de contas são rejeitadas |
| Falhas criptográficas | Campos assinados alterados, campos não assinados adicionados, chave incorreta, membro do arquivo corrompido, mídia alterada/ausente, truncamento detectado pelo ponto de verificação rejeitado |
| Armazenamento | Adições simultâneas são verificadas; atualizações/exclusões acionam a rejeição; a inicialização recusa um registro alterado sem adição e libera seu bloqueio |
| Durabilidade dos meios de comunicação | Gravações atômicas de mensagens/tarefas; recuperação após reinicialização; descritores da versão original mantidos; substituição de fila e corrupção de arquivos existentes rejeitadas; FloodWait mantido; falhas na fonte isoladas |
| Transmissão | O prefixo estável é exportado à medida que novos registros são acrescentados; o ponto de verificação retido detecta registros truncados; a exportação não reproduz o fluxo completo de eventos |
| RFC 3161 | O OpenSSL 3.5.9 lê as solicitações geradas; respostas sintéticas de CA/TSA geradas localmente são aceitas; dados alterados, nonces e CAs incorretas são rejeitados; o ambiente de CA circundante não se sobrepõe à confiança explícita |
| Configuração local | start.py --setup-only atualizou o .venv isolado para a versão 0.2.0; o código-fonte e os metadados instalados estão em conformidade; a verificação do pip foi bem-sucedida |
| Wheel | A versão 0.2.0 foi compilada e instalada separadamente na pasta “test-results”; disponibilizou painéis/recursos, rejeitou chamadas à API não autenticadas, exportou e verificou um arquivo sintético com 32 eventos |

Os testes de código-fonte utilizaram FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 e Playwright 1.62.0. O ambiente de execução fixado utiliza FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 e criptografia 50.0.2. O arquivo deploy/constraints.txt registra as versões fixadas do ambiente de execução; os arquivos deploy/requirements.lock e deploy/build.lock incluem o SHA-256 de cada arquivo de pacote, e os servidores Docker e de alta segurança realizam a instalação exclusivamente a partir deles (pip --require-hashes). Nenhuma dessas informações constitui prova de compatibilidade em todas as plataformas de CI configuradas. A CI remota não foi executada.

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

## Observações ambientais

As restrições da sandbox do Windows bloquearam os diretórios temporários padrão do pytest/pip e o subprocesso do Playwright. O pytest utilizou um novo diretório temporário dentro do projeto; os processos de instalação e do navegador exigiram execução aprovada fora da sandbox.

O AdGuard instalado no computador injetou solicitações para local.adguard.org no navegador. O histórico do navegador mantém essas solicitações. Esta execução **não** constitui prova de ausência total de solicitações de saída em um ambiente de navegador não modificado; o próprio código-fonte do aplicativo não contém solicitações a recursos externos, CDNs ou serviços de análise. As configurações do AdGuard não foram alteradas.

A execução final no navegador também registrou um erro OSError 10022 relacionado à limpeza de soquetes asíncronos do Windows. Todas as verificações do navegador foram aprovadas e não ocorreram erros de JavaScript nas páginas. Sua causa não foi determinada e esta execução não demonstra a ausência de problemas de transporte do host.

O primeiro teste HTTP do pacote instalado, utilizando as solicitações de fechamento de conexão do urllib, encontrou reinicializações de conexão, tanto dentro quanto fora da sandbox e com ambos os conjuntos de dependências. O teste final utilizou conexões persistentes padrão HTTP/1.1 por meio do http.client e foi aprovado. As solicitações do navegador também foram aprovadas. A origem exata das reinicializações não foi determinada; elas não foram classificadas como um defeito fixo do aplicativo.

## Qualificação restante

O diário em tempo real mantido registra efetivamente a coleta, as edições, os avisos de exclusão, os anexos, as verificações posteriores e o tratamento de limites de taxa. Ele não registra a entrega exaustiva nem uma matriz controlada de visibilidade de funções, atores de reação, FloodWait prolongado, bloqueios de contas e recuperação de interrupções de rede/processo. A emissão de tokens QR permanece distinta da confirmação por QR móvel concluída.

A compilação/execução no Docker, a instalação no Linux/macOS, a capacidade de suportar alta carga sustentada, a revisão de segurança independente, uma resposta TSA verdadeiramente independente, a validação de revogação/arquivamento de certificados e a certificação forense permanecem fora da qualificação registrada. O estado salvo do MTProto e a recuperação de dados estão implementados; a reprodução atômica durável ainda não foi estabelecida. A coleta de logs de administração, listas adicionais de reatores e polling curto prioritário continuam sendo recursos separados. Consulte [a aceitação em tempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) para a matriz de qualificação controlada.

Os recibos locais detalhados e as capturas de tela estão na pasta test-results/ (ignorados pelo Git). A captura de tela pública em docs/assets/ contém apenas dados fictícios de demonstração.

## Preparação do site público e da publicação · 27 de outubro de 2026

A apresentação separada do `website/` e a compilação do Pages foram adicionadas após as verificações do painel mencionadas acima. Nenhuma configuração de conta ativa ou lógica de coleta foi alterada.

- O conjunto de aplicativos existente foi aprovado: 138 aprovados, 1 ignorado (exclusivamente POSIX) e um aviso de obsolescência do Starlette/httpx no código-fonte original. Os 11 testes de compilação do site adicionados foram aprovados de forma independente, incluindo a rejeição de saída inesperada e a rejeição de entrada vinculada.
- Ambos os scripts do navegador do aplicativo foram executados utilizando o project-venv Playwright e o Chromium headless shell 156. Não foram registrados erros de JavaScript nas páginas nem solicitações externas. Todos os cenários de conta utilizaram transporte falso e dados fictícios.
- O `tools/check_site.py` foi aprovado nas larguras 320, 390, 768, 1024 e 1440, com um subcaminho da URL do projeto, teclas de tabulação do teclado, acesso à área de transferência bem-sucedido/negado, movimento reduzido e JavaScript desativado. Não ocorreram falhas em solicitações de recursos nem em solicitações externas.
- `tools/build_site.py` gerou 10 arquivos públicos incluídos na lista de permissões, totalizando cerca de 460 KB. Capturas de tela do navegador e um comprovante estão no arquivo `test-results/site/`, que foi ignorado.
- O wheel foi gerado com sucesso após a instalação das ferramentas setuptools/wheel destinadas exclusivamente à compilação no ambiente do projeto. A instalação em um alvo isolado e a execução do comando ``tools/check_install.py`` foram bem-sucedidas: ativos estáticos, controle de acesso, uma exportação sintética assinada de 32 eventos e download por streaming verificado de forma independente.
- O `pip check` foi aprovado. Uma varredura de padrões em candidatos públicos selecionados pelo Git não encontrou blocos de chaves privadas reconhecíveis, tokens do GitHub/bot/AWS, atribuições de segredos literais longos ou marcadores de conflito de mesclagem. Isso não constitui prova de que todos os possíveis formatos de segredos estejam ausentes. As sondagens de dados de tempo de execução/sessão/chave foram ignoradas pelo Git.
- A autenticação do GitHub CLI estava inválida; nenhum remoto estava configurado e não havia nenhum commit inicial. Não foi realizado nenhum push, fluxo de trabalho hospedado, implantação do Pages ou lançamento. O Docker e a qualificação do Telegram/plataforma em ambiente de produção permanecem fora desta verificação.

Neste servidor, o bloqueio de download do Playwright falhou no sistema de arquivos da área de trabalho E:. A instalação do Chromium no `%LOCALAPPDATA%/tgwitness-playwright` e o uso desse mesmo `PLAYWRIGHT_BROWSERS_PATH` para as verificações foram bem-sucedidos. Trata-se de uma solução alternativa de ambiente, não de uma alteração nas dependências de tempo de execução do aplicativo.

## Documentação interativa e metadados do site · 29 de outubro de 2026

O site público é composto por 12 páginas HTML em inglês: uma página inicial, um índice de guias e dez guias. O artefato contém 28 arquivos de apresentação explicitamente listados, aproximadamente 1,85 MB, e nenhum dado de coleta. O site público está em inglês; as traduções do aplicativo e os guias traduzidos do repositório são separados.

- Testes do site, da publicação de origem e dos limites de lançamento: **18 aprovados, 2 ignorados**. As omissões dizem respeito à criação de links simbólicos neste sistema de arquivos do Windows. Os testes verificam metadados exclusivos das páginas, páginas públicas apenas em inglês, URLs canônicas, todas as entradas do mapa do site, recursos/âncoras locais, navegação estruturada e exclusão de arquivos privados.
- Tanto o `tools/check_site.py` quanto o `tools/check_docs_site.py` foram aprovados no Chromium em 320, 390, 768, 1024 e 1440 pixels sob um subcaminho da URL do projeto. As verificações do guia abrangem todas as 11 páginas da documentação, pesquisa e navegação por teclado, aceitação/rejeição da área de transferência e conteúdo legível sem JavaScript.
- Cinco exemplos interativos aprovados: reprodução/avanço/pausa/reinício de mensagens com movimento reduzido e suspensão fora da tela; cadeias de hash originais/alteradas/reconstruídas/truncadas; decisões de aceitação/reversão/bifurcação/ausência de resposta da testemunha; e cenários de entrega completa/atrasada/ausente; além de um mapa de investigação que vincula observações fictícias de conversas cruzadas por ID do remetente, destino e hash do anexo . Os controles de investigação foram aprovados em verificações de navegação por teclado e de fallback sem JavaScript . Os resultados do SHA-256 do navegador foram comparados de forma independente com o `hashlib` do Python e o JSON canônico. O exemplo de hash também manteve seu fallback legível quando o Web Crypto estava indisponível.
- As taxas de entrega e os marcadores dos gráficos foram alinhados à tabela acessível. Os rótulos do eixo para dispositivos móveis foram ampliados após revisão visual. Cada exemplo é identificado como ilustrativo ou sintético, e nenhum exemplo de navegador entra em contato com o Telegram.
- Não foram registradas solicitações externas, solicitações HTTP com falha ou erros de JavaScript. Capturas de tela e recibos de desktop/dispositivos móveis estão sob os códigos ignorados `test-results/site/` e `test-results/docs-site/`. O índice da documentação, exemplos de mensagens/hashes, layout do TgWitness, gráfico de entrega e mapa de investigação foram inspecionados nos formatos para desktop e dispositivos móveis.
- A verificação da publicação foi aprovada para 282 arquivos de código-fonte públicos e 1.426 links de documentação locais. O Ruff foi aprovado para as ferramentas e testes modificados do site em Python.
- O `docs/HOW-IT-WORKS.md` fornece um complemento Markdown do GitHub com diagramas e fórmulas do Mermaid . O `docs/INVESTIGATION.md` abrange o escopo de toda a conta, a aquisição do histórico por chat, perfis de pessoas, referências entre chats, linhas do tempo e uma transferência de caso verificada. Suas etapas e limites foram verificados em relação ao escopo atual, coleta, dossiê, exportação, verificador e código do painel. A renderização hospedada no GitHub não foi verificada.

Trata-se de uma verificação local do site/documentação. Ela não adiciona qualificação ativa do Telegram nem confirma a implantação de páginas hospedadas, o sucesso da CI remota ou a indexação em mecanismos de busca. Consulte [o procedimento de publicação](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) e [as notas sobre os metadados do site](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
