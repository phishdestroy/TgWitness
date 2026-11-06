# Recursos e limitações

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/features/

O modelo atual de coleta, fluxos de trabalho com múltiplas contas, exportações e limites operacionais do TgWitness.

O TgWitness preserva conversas do Telegram acessíveis às contas conectadas, registra alterações observadas e prepara exportações verificáveis. Esta referência descreve o modelo de coleta, os fluxos de trabalho atuais e seus limites.

## Aplicativo independente

O TgWitness possui instalação, diretório de dados e ciclo de vida de versões próprios. A interface web integrada cuida da configuração e da revisão; os registros exportados podem ser utilizados de forma independente.

O operador conecta suas contas, escolhe as fontes visíveis para cada uma delas e obtém um registro de observações salvo. O painel exibe o conteúdo, as alterações salvas, a proveniência das observações e as lacunas conhecidas. Outro investigador pode verificar o material exportado.

O painel distingue entre autorização da conta, acesso a uma fonte, atividade do coletor e cobertura registrada. Analise esses estados em conjunto ao avaliar um intervalo com poucas mensagens ou um problema de conexão.

## Investigações compartilhadas

Um administrador pode emitir [tokens de acesso](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/) restritos a espaços de trabalho e chats individuais, com permissões por ação, restrições de IP, validade, limites de login e controle de sessão. Um revisor com acesso somente leitura pode inspecionar um caso sem receber a autorização do Telegram ou a chave do painel principal. O acesso restrito ao chat permanece separado das configurações gerais da conta e das exportações completas do diário.

O MTProxy automático mantém rotas funcionais do Telegram a partir de quatro fontes públicas ou de um catálogo de operadores. [Os modos de IP](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes) determinam se, em caso de falha, é necessário aguardar outro proxy ou se é possível utilizar uma rota direta explicitamente permitida. As solicitações HTTP externas possuem uma rota separada e um botão para desativá-las.

## Ferramentas de arquivamento

[Aquisição de histórico](https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/), [pesquisa e análise de arquivos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/analysis/),[MCP somente leitura](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/), [OCR/transcrição local](https://phishdestroy.github.io/TgWitness/pt/docs/reference/media-analysis/) e[webhooks de saída](https://phishdestroy.github.io/TgWitness/pt/docs/reference/webhooks/) estão incluídos em 0.7.1. Relatórios analíticos e textos reconhecidos permanecem separados dos eventos capturados.

[O Case Board](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/) adiciona marcadores, citações, notas e coleções vinculadas às fontes dentro de um espaço de trabalho. O [construtor de relatórios](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/) seleciona o material, as seções e um dos oito modelos para exportações em HTML/PDF compatíveis.

## Recursos opcionais

A configuração diária é: conta → fontes → observação. **A seção “Extras”** é um destino separado com um bot de testemunho do Telegram e uma visualização de captura no GitHub. Cada um indica sua disponibilidade e requisitos antes de exibir as configurações. Ao selecionar um cartão, as instruções são exibidas; isso não inscreve nem inicia um serviço.

A configuração do bot ocorre em três etapas: criar acesso somente leitura, escolher as configurações de publicação e iniciar no host do witness. Opções de rede e publicação, conexões existentes e comandos de verificação são divulgados sob demanda. A configuração baixada é distinta de um witness em execução. A troca de extras mantém o rascunho; alterações na conta e o bloqueio apagam o token temporário e o formulário. O guia integrado inclui instruções de inicialização. [O GitHub Actions captura](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) e inicia um coletor fixado a partir do seu fork, captura um chat e produz uma transferência criptografada com a proveniência do fluxo de trabalho.

## Protocolo e fontes privadas

**MTProto é o protocolo do Telegram; Telethon é a biblioteca Python que o TgWitness utiliza para comunicar-se via MTProto.** Não se trata de métodos alternativos de conexão. A coleta utiliza o MTProto; a testemunha opcional publica verificações assinadas por meio da API do bot.

Cada espaço de trabalho possui seu próprio cliente autorizado e fluxo de atualizações da conta. O TgWitness seleciona observações a partir de fontes configuradas e realiza solicitações explícitas e separadas para funções como instantâneos do histórico e downloads de mídia.

Uma fonte privada não necessita de nome de usuário público. O tipo de par do Telegram e o ID numérico são os identificadores; títulos e nomes de usuário podem ser alterados. O acesso depende da adesão e das permissões existentes. O TgWitness não adiciona fontes automaticamente nem contorna a aprovação de adesão. Um hash de acesso proveniente de outra conta não constitui um token de acesso universal.

O modelo de coleta deve levar em conta o histórico oculto anterior à adesão, as funções dos participantes/administradores, a revogação de sessões, a remoção ou alteração de permissões, a migração de grupo para supergrupo, tópicos/fóruns, discussões vinculadas, identidades de canais e anexos indisponíveis. Nem todas as combinações foram testadas em ambiente real.

A visibilidade da fonte é verificada no início do coletor. A ausência de uma fonte no resultado do diálogo delimitado significa que **o acesso não foi confirmado**, e não que a remoção tenha sido comprovada. Uma fonte indisponível não impede a observação de outras fontes acessíveis. Nunca coloque links de convite ou sessões reais em recursos públicos.

## Várias contas

O painel suporta qualquer número de **espaços de trabalho**, cada um com:

- Autorização, cofre criptografado e rota de conexão.
- Diário em SQLite e identidade de assinatura Ed25519.
- Fontes selecionadas, fila de mídia e configurações de captura.
- Estado de observação, erros, pontos de verificação e exportações.

A troca do espaço de trabalho exibido não interrompe outro coletor. A autorização de conta duplicada entre espaços de trabalho é rejeitada. Um registro já vinculado a uma conta do Telegram não pode ser reatribuído a outra; é permitido reconectar a mesma conta. Isso preserva a identidade da conta e o escopo relevante do ID da mensagem.

O aplicativo não define um número fixo de espaços de trabalho. Cada espaço de trabalho executa suas próprias tarefas do coletor para monitoramento de conexão, downloads de mídia, novas verificações e captação de novos chats dentro de um processo Python compartilhado e de um loop de eventos. A taxa de processamento depende da carga de trabalho. Para isolamento de processos, use instalações, portas e diretórios de dados separados.

Atribua a cada conta as fontes às quais ela tem acesso. Contas diferentes podem observar o mesmo grupo, mas suas observações permanecem separadas e mantêm sua origem. Duas contas em uma máquina controlada por um único operador não constituem duas testemunhas independentes. **A exportação do grupo** agrupa os arquivos ZIP das áreas de trabalho assinados separadamente com uma lista de arquivos assinada contendo seus IDs de área de trabalho, hashes e impressões digitais das chaves de assinatura. Cada diário mantém seu próprio limite. Crie uma linha do tempo combinada entre espaços de trabalho em notas de caso ou ferramentas de análise, mantendo essas referências de fonte.

## Captura e atribuição

A seção “Fontes” oferece opções por conta para novas mensagens, edições, exclusões, reações e participação em grupos. As predefinições retêm todas as categorias ou apenas mensagens/edições/exclusões. A política se aplica aos grupos selecionados do espaço de trabalho, permanece válida após a reinicialização e é assinada com as alterações antes e depois. As configurações padrão preservam todas as categorias. Desativar uma categoria não remove registros antigos; reativá-la não reconstrói eventos perdidos. Registros operacionais, outros eventos de serviço do grupo e instantâneos explícitos do histórico são separados. Objetos do Telegram capturados podem reter metadados incorporados, independentemente das opções de atualização separada. Ainda não há substituições de categoria por grupo.

| Material | Capturado agora | Limites |
| --- | --- | --- |
| Mensagem | Texto, IDs de pares/mensagens, metadados do remetente, respostas e envelope de atualização original | Preservado como uma observação visível na conta, assinada pelo coletor |
| Editar | Nova versão observada e quaisquer versões salvas anteriormente | As edições intermediárias realizadas durante o tempo de inatividade podem ser perdidas; o remetente não é necessariamente o editor |
| Exclusão | Notificação e conteúdo capturado anteriormente, se houver | Normalmente, não há indicação de quem excluiu nem do horário exato da ação |
| Aviso de exclusão no nível da conta | Aviso original; os registros resolvidos incluem o chat salvo e o método de correlação | Requer exatamente uma correspondência de chat privado ou grupo comum previamente salva no escopo; outros IDs permanecem como “`deletion.unscoped`”. IDs de canais e supergrupos são excluídos dessa correlação |
| Reação | Contadores apresentados e identidades recentes visíveis | Uma lista completa dos reatores disponíveis requer consultas separadas; os canais podem ocultar identidades |
| Associação | Mensagens de serviço e atualizações enviadas aos participantes | A visibilidade depende da função e do tipo de conversa; eventos ausentes não implicam ausência |
| Ações do administrador | Atualizações relevantes entregues e um instantâneo do log de administração nas exportações de bate-papos de canais/supergrupos | A exportação lê o log quando este estiver disponível para a conta de administrador responsável pela exportação; a consulta contínua do log de administração está fora deste processo |
| Anexo | Descritor da versão original, bytes baixados/SHA-256 e resultados das tentativas | Um arquivo excluído pode ser irrecuperável; a versão mais recente não é substituída |
| Histórico | Captura de tela explícita das mensagens visíveis no momento | Não reconstrói todas as edições nem o conteúdo excluído |
| Processo do coletor | Iniciar/parar, heartbeat, erros, configurações, escopo e recibo de execução assinado | Inventário local; o GitHub e o TDX adicionam [verificações independentes do ambiente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) |

A interface identifica a conta fornecida no evento de origem e mantém os nomes e nomes de usuário observados. Quando o evento omite seu autor, o relatório deixa esse campo em branco.

## Capacidade e limites do Telegram

Não há um número universal de conversas que possam ser monitoradas com qualidade garantida. A capacidade depende do pico de eventos por segundo, do volume e do tamanho dos anexos, de RPCs adicionais, de contas ativas, da latência do disco/espaço livre, das condições da rede, dos limites do Telegram, do atraso aceitável e da profundidade da fila.

O Telegram distingue a entrega passiva da consulta ativa de curta duração. Sua documentação de atualização descreve chamadas `updates.getChannelDifference` adicionais para canais abertos/supergrupos e recomenda, no máximo, **dez fontes submetidas simultaneamente à consulta de curta duração**. Isso não constitui um limite de dez grupos selecionados nem uma garantia de exaustividade.

| Modo | Objetivo | Status |
| --- | --- | --- |
| Observação padrão | Registre as atualizações recebidas de fontes selecionadas | Implementado |
| Revisões prioritárias | As fontes marcadas com estrela utilizam seu próprio intervalo configurável e têm prioridade em cada etapa de verificação limitada | Implementado com consultas de histórico e mensagens |

A estrela de prioridade controla essas verificações adicionais. A consulta rápida adicional ``updates.getChannelDifference` ` não é disponibilizada como um modo de usuário separado.

A sondagem arbitrária de alta frequência, ignorando o FloodWait ou presumindo capacidade linear de contas adicionais, não constitui um modelo válido de dimensionamento. Os limites padrão são os primeiros 1.000 diálogos listados, até 500 mensagens por instantâneo do histórico, 1–2.000 MiB por arquivo coletado, por tipo, e 4 GiB de conteúdo ZIP assinado não compactado; cada um é alterado por espaço de trabalho na seção **“Parâmetros**”. As exportações não possuem limite fixo de contagem de eventos. O fallback do navegador está limitado a 128 MiB por padrão; a CLI de streaming possui um limite de transferência configurável, de 5 GiB por padrão.

## Confiabilidade e recuperação

O comportamento implementado inclui WAL do SQLite/transações síncronas; gravações atômicas de mensagens e tarefas de mídia; tarefas persistentes e atrasos de repetição; descritores da versão original; retentativas limitadas; FloodWait de mídia persistida; downloads de mídia fora da espera de rede do evento de texto; exportações com prefixo estável enquanto gravações posteriores continuam; configurações atômicas e registros de auditoria; preservação da autorização ativa após falha no login de substituição; isolamento de um espaço de trabalho adicional danificado; tentativas explícitas de reconexão; relatórios distintos de perda de autorização; e detecção de alterações no relógio de parede por meio de um relógio monotônico.

Os pontos pts/qts/seq de contas e canais são salvos e retomados após uma reinicialização, e os chats monitorados são verificados novamente periodicamente; consulte [o formato de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#durable-collection-and-process-receipts-02). Salvar a posição periodicamente não constitui uma confirmação atômica e sem perdas da aceitação do registro.

Cada início de processo registra o ponto inicial anterior e o limite offline. O histórico atual não é tratado como correção de lacunas. A retenção de diferenças do Telegram é finita; o `differenceTooLong` não pode reconstruir todo o conteúdo desaparecido. Lacunas irrecuperáveis devem permanecer explícitas, mesmo que um instantâneo posterior do histórico seja bem-sucedido.

## Modelo de evidências

Cada evento registra uma sequência, a hora de observação local em UTC, a hora da fonte (quando fornecida), o tipo, a fonte, o autor (quando fornecido), a carga útil original, o hash anterior e a assinatura. As observações de mensagens também retêm a conta do coletor e o contexto da execução.

O recibo de processo assinado contém um ID de execução aleatório; versões do TgWitness/Python/OS/dependências; valores SHA-256 dos arquivos-fonte e impressão digital agregada; conta inicial, escopo e configurações; leituras UTC/monotônicas; e o cabeçalho do registro anterior. Alterações nas configurações, início/parada e erros são registrados no mesmo diário. Os pontos de verificação são retidos na inicialização, a cada cinco minutos durante a observação (parâmetro alterável) e na parada ordenada. Um ponto de verificação local retido pode detectar um retrocesso para um prefixo de diário anterior.

| Mecanismo | O que ele estabelece |
| --- | --- |
| SHA-256 do arquivo | Os bytes correspondem a um resumo conhecido |
| Cadeia de hashes de eventos | Ordenação/associação de registros em relação a um limite conhecido |
| Ed25519 | Assinatura sob uma chave específica |
| Ponto de verificação mantido de forma independente | O material subsequente está de acordo com o limite estabelecido |
| Análise do arquivo do programa | Relatório do coletor sobre os arquivos medidos |
| Resposta válida e independente da TSA | Existência de bytes específicos no momento TSA sob pressupostos explícitos de confiança |

A preparação de solicitações conforme a RFC 3161 e a verificação de respostas pelo OpenSSL estão implementadas. O modo de evidência também envia hashes de pontos de verificação para serviços de carimbo de data/hora configurados. Mantenha e verifique a resposta da autoridade para estabelecer uma âncora de tempo independente. Consulte [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/).

Mantenha pontos de verificação de forma independente, controle o acesso às chaves de assinatura, mantenha registros de transferência e verifique as exportações com software confiável. O [escopo da verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) explica como essas verificações se complementam e quais pressupostos de confiança se aplicam.

## Exportação, implantação e transferência

Um arquivo ZIP assinado contém os arquivos originais em JSONL, CSV e HTML, anexos preservados, hashes, um manifesto assinado e um verificador de conveniência. Abrange um espaço de trabalho e um prefixo fixo completo para o registro. Os filtros de pesquisa do painel não removem registros silenciosamente. Chaves secretas, tokens e sessões do Telegram são excluídos; as observações originais ainda podem conter informações pessoais e metadados do Telegram.

Mantenha o resumo do ZIP, a impressão digital confiável, o ponto de verificação, o recibo de processamento e o registro de transferência separadamente. Utilize um verificador proveniente de uma instalação confiável, em vez de confiar no código executável apenas porque ele aparece no ZIP examinado.

A interface do navegador é fornecida localmente, sem Node.js, CDNs ou fontes externas. Um token de operador controla a instalação. O acesso remoto requer HTTPS ou um túnel SSH. São fornecidas definições nativas em Python e para contêineres, com exemplos de serviços na pasta [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); as verificações de plataforma executadas são listadas separadamente.

O espaço de trabalho padrão utiliza a raiz de dados; espaços de trabalho adicionais utilizam `profiles/<id>/`. O backup requer que o processo esteja parado e que o conjunto completo de dados/chaves esteja disponível. Os arquivos ZIP de evidências não são backups do aplicativo. Os segredos podem utilizar uma chave mestra externa para um novo diretório de dados; a criptografia do diário e da mídia é fornecida pelo disco/volume do operador. Consulte [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) e [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/operations/).

## Critérios de lançamento estável

Antes do lançamento de uma versão estável, especifique:

1. Grupos privados reais, supergrupos, fóruns e canais com funções de membro/administrador e histórico oculto/visível, incluindo login/autenticação de duas etapas (2FA), revogação e perda de acesso.
2. Edições, exclusões, reações, participação e mídia controladas em relação a ações conhecidas.
3. Falhas no processo/servidor, falhas no disco/disco cheio, referências a arquivos expirados, FloodWait, perda de conexão de rede, arquivos corrompidos e reversão do banco de dados.
4. Uso contínuo de múltiplas contas com atrasos, filas, memória e espaço em disco controlados, incluindo fontes silenciosas e ruidosas em conjunto.
5. Interrupção entre o avanço do estado do MTProto e a aceitação do registro.
6. Instalação limpa na matriz de sistemas operacionais/contêineres pretendida e restauração de backup verificada.
7. Análise independente de segurança, assinaturas e alegações de atribuição/evidência.

O acesso restrito ao painel é descrito em [“Acesso e permissões](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/)”. A versão 0.6 oferece suporte ao TData de conta única delimitada e à importação de arquivos de conta, conforme descrito em [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/). Revise os termos da API do Telegram antes da publicação. As referências de pesquisa e as conclusões sobre a plataforma estão em [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
