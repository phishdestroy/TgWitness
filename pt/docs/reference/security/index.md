# Segurança e tratamento de dados

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/

Modelo de ameaças, modelo de acesso, dados confidenciais em repouso, exposição de rede, importação de sessões e como relatar uma vulnerabilidade.

O TgWitness é executado no seu próprio computador ou servidor. As conexões de contas, a manutenção da lista pública de proxies e os serviços externos opcionais possuem políticas de roteamento explícitas. Notificações, registros de data e hora, cópias externas e uma testemunha são configuradas separadamente. Esta página lista o que é protegido, como e o que fica a cargo do operador.

| Área | Em resumo |
| --- | --- |
| Acesso | Chave de administrador, além de acesso restrito a contas/chats, sete permissões e sessões revogáveis; localhost por padrão |
| Segredos em repouso | As configurações de sessão, par de API, chave de assinatura e proxy são criptografadas com Fernet |
| Mensagens e arquivos de mídia | Armazenado sem criptografia: utilize criptografia de disco e permissões rigorosas |
| Integridade | Cadeia de hash SHA-256 e uma assinatura Ed25519 em cada registro |
| Não abordado | Um administrador de máquina, um token de painel vazado, integridade da captura |

Para relatórios de vulnerabilidades, consulte a [política de segurança](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Modelo de acesso

O token do painel principal concede controle total. Outras pessoas podem receber seu próprio [acesso restrito](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/): espaços de trabalho e chats selecionados, permissões, prazo de validade, restrições de IP, limites de login e sessões revogáveis. Um acesso restrito a um chat não pode realizar operações em todo o espaço de trabalho, mesmo que sua permissão esteja marcada. Os espaços de trabalho compartilham um processo e não isolam os dados do administrador do servidor.

O painel escuta no localhost por padrão. O login no navegador troca um token de acesso por uma credencial de sessão; o navegador o envia como um token de portador. Ele é mantido no sessionStorage, em vez de em um cookie de autenticação. Bloquear/sair limpa a sessão do navegador. Fechar o navegador ou encerrar uma sessão não interrompe a coleta.

Os tokens emitidos e as credenciais de sessão são mantidos como hashes no cofre criptografado. A revogação encerra as sessões associadas; alterações de permissão afetam as solicitações subsequentes. Arquivos baixados não podem ser recuperados. O administrador também pode limitar suas próprias sessões de navegador, mas scripts que utilizam diretamente o token do painel principal mantêm acesso total e contornam esses limites de sessão do navegador.

A autenticação malsucedida é limitada por taxa por endereço do cliente. As restrições de IP utilizam o endereço percebido pelo aplicativo; verifique o comportamento do proxy reverso antes de confiar nele. As credenciais do Witness permanecem separadas como credenciais de verificação de integridade/ponto de verificação, apenas para leitura.

### Acesso à demonstração

`/api/demo-access` é um bootstrap deliberadamente não autenticado para uma demonstração sintética isolada e iniciada explicitamente. Ele emite uma capacidade válida apenas durante a vida útil do processo, nunca o token real do painel nem uma substituição do TGWITNESS_TOKEN. A emissão e o uso exigem um par de loopback e um Host, sem cabeçalhos encaminhados e sem solicitações entre origens. Espaços de trabalho adicionais ou uma sessão autorizada desativam esse caminho. Espaços de trabalho ativos nunca emitem essa capacidade. A demonstração não pode conectar contas nem alterar configurações de coleta.

## Conteúdo dos painéis e exportações

O painel não utiliza fontes externas, ferramentas de análise, recursos de CDN nem mídia remota incorporada. O texto proveniente do Telegram é inserido como texto, não como HTML. Os anexos baixados são fornecidos como anexos binários. As exportações em JSONL preservam as cadeias de caracteres originais; o HTML as escapa; as células CSV que poderiam se tornar fórmulas recebem um apóstrofo como prefixo.

As exportações excluem segredos de autenticação e assinatura, mas contêm deliberadamente metadados de origem coletados, identificadores e, possivelmente, conteúdo pessoal ou confidencial. Hashes de acesso ao Telegram e referências a arquivos podem estar presentes nos metadados de origem brutos.

## Segredos em repouso

As credenciais da API do Telegram, o StringSession e a chave privada Ed25519 são criptografadas usando o Fernet. Por padrão, sua chave é armazenada no mesmo diretório de dados protegidos. Isso reduz a exposição acidental de texto não criptografado; não se trata de proteção contra um invasor capaz de ler todo o diretório. O conteúdo das mensagens e as mídias **não** são **criptografados** pelo TgWitness. Utilize criptografia de disco e permissões restritivas do sistema operacional. Os arquivos de chave privada do Unix são criados com o modo 0600; os diretórios de dados recém-criados utilizam o modo 0700. As permissões existentes dos diretórios não são alteradas. O Windows herda as ACLs dos diretórios: restrinja-as à conta de serviço e aos administradores autorizados.

### Chave mestra externa

Para um novo diretório de dados, o TGWITNESS_VAULT_KEY_FILE pode fornecer uma chave mestra aleatória externa. O HKDF-SHA256 e um salt aleatório separado geram uma chave Fernet diferente para cada espaço de trabalho. O arquivo vault.external.json deve ser mantido para recuperação. Chaves-mestras ausentes ou incorretas resultam em falha. Cofres locais existentes não são migrados automaticamente. O processo em execução pode acessar a chave; não se trata de isolamento HSM. O painel informa o modo selecionado e declara explicitamente que o armazenamento de mensagens/mídia não é criptografado pelo aplicativo. Consulte [conexão, proxies e proteção de dados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) para obter o modelo de ameaças completo.

## Proxies e rotas de rede

A configuração do proxy é criptografada no cofre. Senhas e segredos do MTProxy não são retornados pela API nem registrados nos registros de evidências. Cada espaço de trabalho escolhe sua rota do Telegram e um [modo de IP](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes).

O modo “Ocultar IP” recusa o fallback direto do Telegram e requer um proxy para solicitações HTTP externas. O modo de fallback explicitamente selecionado permite o acesso direto ao Telegram após um certo atraso; o modo “túnel/VPN” permite rotas diretas. A escolha do modo de túnel não instala nem verifica uma VPN. Essas configurações não controlam todo o tráfego da máquina, navegadores, gerenciadores de pacotes ou a resolução de DNS do host do proxy local.

O MTProxy transporta apenas o tráfego do Telegram. Solicitações externas podem utilizar um proxy SOCKS5/HTTP separado, a rota SOCKS5/HTTP do espaço de trabalho ou uma rota direta permitida; elas também podem ser desativadas. A testemunha independente possui suas próprias configurações de transporte. A autenticação CONNECT padrão do SOCKS5/HTTP não é criptografada por esses próprios protocolos de proxy. Segredos TLS falsos do MTProxy continuam sem suporte.

## Início de sessão e importação de sessões

Os arquivos .tgwitness-session convertidos contêm um segredo de autorização em texto simples até que sejam carregados e armazenados no cofre. A CLI offline aceita esquemas Telethon revisados. A importação pelo painel aceita, além disso, Pyrogram SQLite, o moderno TData ZIP de conta única e entradas JSON documentadas. Ela é autenticada, limitada a quatro arquivos / 8 MiB, e processa os envios na memória sem extração do arquivo compactado nem salvamento dos arquivos originais. As credenciais normalizadas são retornadas apenas ao navegador autenticado solicitante; elas são salvas no cofre criptografado após a autorização bem-sucedida do Telegram. Proteja os arquivos originais e os convertidos e evite que clientes simultâneos clonem uma autorização.

O processamento de dados verifica somas de verificação de contêineres, hashes de descriptografia local e comprimentos de estrutura. Uma senha local fornecida para o Desktop é utilizada temporariamente e não é armazenada. Este analisador limitado não garante que todas as versões do Desktop sejam compatíveis. As imagens de QR são geradas localmente, contêm tokens de login do Telegram de curta duração e nunca são enviadas a um serviço de renderização externo. O bloqueio, a troca de área de trabalho, um novo login e alterações de rota cancelam as tentativas de QR pendentes. Recarregar ou fechar uma aba pode deixar uma tentativa pendente até o vencimento. Um login por QR bem-sucedido ainda impõe a vinculação da conta. Os corpos de API comuns permanecem limitados a 16 KiB; a rota de importação autenticada aceita até 12 MiB de JSON codificado, impondo separadamente o limite menor para o arquivo decodificado.

Códigos de login e senhas de verificação em duas etapas do Telegram não são armazenados. O estado do número de telefone/hash do código é mantido na memória durante a autorização. As sessões do Telegram concedem acesso à conta; nunca faça upload de um diretório de dados, sessão, token, chave do cofre ou chave de assinatura privada para o GitHub.

## Registros e transporte

A resposta padrão de validação da API é substituída para que não repita os valores das credenciais. O registro de acesso ao aplicativo está desativado. Não configure um proxy reverso para registrar cabeçalhos de autorização ou corpos de solicitação. O HTTP transmite tokens e segredos de login em texto simples: utilize HTTPS ou um túnel SSH sempre que sair do localhost.

## Limites de integridade

A cadeia de hashes, os gatilhos do banco de dados e as assinaturas detectam determinadas modificações; eles não impedem que um administrador local reescreva e assine novamente o registro. Mantenha pontos de verificação assinados e a impressão digital da chave pública em um sistema separado. O modo de evidência e a cópia externa (ambos desativados por padrão) enviam hashes de pontos de verificação para serviços de registro de data e hora e cópias criptografadas para armazenamento compatível com S3; consulte o [formato de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/). Registros de transparência, assinatura respaldada por HSM e certificação formal da cadeia de custódia não estão implementados.

## Caso suspeite de algum problema

Mantenha o diretório de dados original e utilize uma cópia separada para análise. Não inclua dados privados do Telegram nem credenciais em uma publicação pública. Não é reivindicada nenhuma certificação de segurança independente.
