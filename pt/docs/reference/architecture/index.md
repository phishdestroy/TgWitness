# Arquitetura

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/architecture/

Componentes do coletor, do painel, do diário, dos workers e do witness, e como os dados circulam entre eles.

Um processo em Python hospeda o painel FastAPI e um número ilimitado de espaços de trabalho isolados, cada um com um cliente de conta de usuário do Telethon. O SQLite armazena um diário de eventos assinado, no modo “somente acréscimo”, e configurações operacionais mutáveis. Um cofre criptografado armazena as credenciais da API, a StringSession e a chave de assinatura. O front-end é composto por HTML/CSS/JavaScript simples e empacotados: não são necessárias compilações em Node, CDNs nem downloads de front-end em tempo de execução.

| Módulo | Responsabilidade |
| --- | --- |
| collector.py | Autorização, seleção de diálogos, atualizações, instantâneos, fila de mídia, monitoramento de conexão |
| interactions.py / telegram_client.py | Ações explícitas do painel, recibos assinados, IDs de solicitação persistentes e política de retentativas de callback/participação local à tarefa |
| message_content.py | Comparação observável de mensagens, excluindo metadados de acesso de transporte |
| workers.py | Aguarde a conclusão dos processos de exportação de arquivos antes de iniciar a limpeza de cancelamentos |
| store.py | Transações WAL, cadeia de eventos ordenada, filtros de consulta, configurações operacionais |
| security.py | Criação de arquivos privados, cofre criptografado, assinatura Ed25519, bloqueio de processo único |
| evidence.py | Exportação do diário completo, derivados, pontos de verificação, verificação de anexos |
| verify.py | Verificador autônomo e somente de leitura (biblioteca padrão + criptografia): arquivos, cobertura, registros de testemunho e publicações em canais, arquivos de perfil |
| app.py | API autenticada, ciclo de vida, validação de solicitações, painel estático |
| profiles.py | Coletores de múltiplas contas, controlador de acesso compartilhado, ciclo de vida por espaço de trabalho |
| access.py | Autorizações restritas, verificações de permissão, restrições de IP, limites de sessão e console de administrador |
| proxy_catalog.py | Instantâneos de feeds públicos, verificações de transporte, conjunto de proxies compartilhados e seleção com base na integridade |
| provenance.py | Medições assinadas de identidade, código e dependências durante a execução da aquisição |
| network.py | Rotas validadas por espaço de trabalho; status e evidências censurados; opções de transporte do Telethon |
| sessions.py | Conversão offline, somente para leitura, dos esquemas SQLite revisados do Telethon |
| account_import.py | Detecção e normalização em memória de arquivos de contas compatíveis e JSON |
| tdata.py | Leitor ZIP TData moderno e limitado, validação de checksum/descriptografia, sem extração |
| doctor.py | Verificações de prontidão local sem coleta de dados, login ou instalação de pacotes |
| download.py | Download de exportação de streaming autenticado, com leituras limitadas e sem sobrescritas |
| monitoring.py | Política de eventos validada por espaço de trabalho e regras de anexos por tipo, compartilhadas por responsáveis, status e recibos assinados |
| scope.py | Âmbito de observação (conversas selecionadas, pasta do Telegram, conta inteira), tipos de fontes, exclusões, níveis de verificação |
| dossier.py | Perfis de usuários por conversa criados a partir de registros salvos: fatos com referências aos registros, SHA-256/pHash do avatar, extração de menções |
| witness_api.py | Tokens de testemunha somente para leitura e o cabeçalho assinado do registro que eles podem obter |
| witness.py | Processo de testemunho independente: chave e registro próprios, verificações de integridade, publicações assinadas no canal, exportação |
| alerts.py | Notificações do Apprise e a lista de notificações do painel |
| logging_config.py | Registro de console e diagnósticos rotativos do servidor para execuções sem janela |
| static/ | Interface responsiva, porta de acesso local, filtros, detalhes, exportações, configuração de conta |
| demo.py | Registro sintético claramente identificado, isolado da coleta real |

Os manipuladores de observação são registrados antes da conexão. A coleta em tempo real é condicionada pela identidade do cliente ativo, pelo estado explícito de execução, pelas fontes habilitadas ou pelo escopo da observação (os modos de pasta ou conta inteira adicionam um novo chat como fonte na sua primeira atualização) e pela política de eventos. Clientes rejeitados ou substituídos não podem contribuir com atualizações em tempo real. Reações brutas e atualizações de associação preservam os limites de visibilidade. O conteúdo da mensagem recebida e sua tarefa de mídia durável são confirmados em conjunto. As tarefas preservam o descritor TL original e vinculam seu hash à observação da mensagem assinada. As semânticas de remetente/editor/executor de exclusão são separadas.

Cada espaço de trabalho aceita uma conta e possui seu próprio diretório e identidade de assinatura. O espaço de trabalho principal permanece na raiz por motivos de compatibilidade; espaços de trabalho adicionais ficam em profiles/<id>/. Um token de portador controla toda a instalação; os espaços de trabalho não são entidades de autorização separadas. Bloqueios de processo protegem os diretórios; bloqueios de banco de dados serializam a inserção de eventos. Cada adição é confirmada de forma síncrona no WAL do SQLite com o modo síncrono FULL. Gatilhos de atualização/exclusão de eventos impedem edições comuns por parte do aplicativo; os administradores do sistema de arquivos permanecem dentro do limite de confiança.

A autorização da API é um token de portador. As operações de login são serializadas e limitadas no tempo. Os uploads de contas utilizam um limite dedicado de 12 MiB para o corpo codificado e um limite de 8 MiB para o arquivo decodificado; as solicitações normais da API mantêm o limite de 16 KiB. A conversão é executada em uma thread de trabalho, mantém os uploads na memória e retorna a entrada normalizada ao navegador autenticado. O login por QR possui um candidato por espaço de trabalho, um identificador de curta duração, uma tarefa de espera e cancelamento explícito. Apenas a autorização aceita se torna o cliente ativo. O Telegram FloodWait é retornado com um valor Retry-After; credenciais e mensagens de erro RPC em formato bruto não são expostas nos erros da API. As exportações são executadas fora do loop de eventos assíncrono e são serializadas por espaço de trabalho. Elas transmitem um instantâneo de leitura estável e podem coexistir com gravações contínuas no WAL. Os coletores de espaço de trabalho compartilham o processo/ciclo de eventos.

Instantâneos do histórico atual e atualizações em tempo real podem se sobrepor. Ambos são observações distintas, identificadas pela fonte; as duplicatas não são ocultadas automaticamente. Não é implementada nenhuma inferência a partir de IDs ausentes, texto excluído fabricado, enumeração forçada de membros ou adesão automática a grupos. Não é implementada.

Para a explicação destinada aos operadores, consulte [como funciona a coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/) e [os formatos de contas e sessões](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/).

A configuração de rede fica armazenada no cofre criptografado. A aplicação de uma rota encerra os clientes antigos e cancela logins inacabados; conexões posteriores utilizam essa rota sem recurso alternativo direto. Uma nova instalação com chave externa deriva a chave Fernet de cada espaço de trabalho usando HKDF-SHA256 a partir de um arquivo de chave mestra e um salt aleatório armazenado. Isso protege os segredos separadamente do diretório de dados, e não o conteúdo do diário ou da mídia em texto simples.

A entrada de demonstração local utiliza uma capacidade de processo gerada separadamente, nunca o token de painel configurado. A emissão e a aceitação exigem o modo de demonstração explícito, uma raiz sintética sem espaços de trabalho adicionais ou uma sessão autorizada, par/host de loopback, sem cabeçalhos de encaminhamento de proxy e sem solicitação de navegador de origem cruzada. As APIs ativas mantêm a autenticação de portador e rejeitam alterações na coleta no modo de demonstração.
