# Segurança e tratamento de dados

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/

Modelo de ameaças, modelo de acesso, dados confidenciais em repouso, exposição de rede, importação de sessões e como relatar uma vulnerabilidade.

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| Área | Em resumo |
| --- | --- |
| Acesso | Chave de administrador, além de acesso restrito a contas/chats, sete permissões e sessões revogáveis; localhost por padrão |
| Segredos em repouso | As configurações de sessão, par de API, chave de assinatura e proxy são criptografadas com Fernet |
| Mensagens e arquivos de mídia | Armazenado sem criptografia: utilize criptografia de disco e permissões rigorosas |
| Integridade | Cadeia de hash SHA-256 e uma assinatura Ed25519 em cada registro |
| Limite de confiança local | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

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

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### Chave mestra externa

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) for setup details.

## Proxies e rotas de rede

A configuração do proxy é criptografada no cofre. Senhas e segredos do MTProxy não são retornados pela API nem registrados nos registros de evidências. Cada espaço de trabalho escolhe sua rota do Telegram e um [modo de IP](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes).

**A opção “Ocultar o endereço”** desativa o fallback direto do Telegram e exige um proxy para solicitações HTTP externas. O modo de fallback explicitamente selecionado permite o acesso direto ao Telegram após um atraso; o modo túnel/VPN permite rotas diretas. A escolha do modo túnel não instala nem verifica uma VPN. Essas configurações não controlam todo o tráfego da máquina, navegadores, gerenciadores de pacotes ou a resolução de DNS do proxy local.

O MTProxy transporta apenas o tráfego do Telegram. Solicitações externas podem utilizar um proxy SOCKS5/HTTP separado, a rota SOCKS5/HTTP do espaço de trabalho ou uma rota direta permitida; elas também podem ser desativadas. A testemunha independente possui suas próprias configurações de transporte. A autenticação CONNECT padrão do SOCKS5/HTTP não é criptografada por esses próprios protocolos de proxy. Segredos TLS falsos do MTProxy continuam sem suporte.

## Início de sessão e importação de sessões

Os arquivos .tgwitness-session convertidos contêm um segredo de autorização em texto simples até que sejam carregados e armazenados no cofre. A CLI offline aceita esquemas Telethon revisados. A importação pelo painel aceita, além disso, Pyrogram SQLite, o moderno TData ZIP de conta única e entradas JSON documentadas. Ela é autenticada, limitada a quatro arquivos / 8 MiB, e processa os envios na memória sem extração do arquivo compactado nem salvamento dos arquivos originais. As credenciais normalizadas são retornadas apenas ao navegador autenticado solicitante; elas são salvas no cofre criptografado após a autorização bem-sucedida do Telegram. Proteja os arquivos originais e os convertidos e evite que clientes simultâneos clonem uma autorização.

O processamento de dados verifica somas de verificação de contêineres, hashes de descriptografia local e comprimentos de estrutura. Uma senha local fornecida para o Desktop é utilizada temporariamente e não é armazenada. Este analisador limitado não garante que todas as versões do Desktop sejam compatíveis. As imagens de QR são geradas localmente, contêm tokens de login do Telegram de curta duração e nunca são enviadas a um serviço de renderização externo. O bloqueio, a troca de área de trabalho, um novo login e alterações de rota cancelam as tentativas de QR pendentes. Recarregar ou fechar uma aba pode deixar uma tentativa pendente até o vencimento. Um login por QR bem-sucedido ainda impõe a vinculação da conta. Os corpos de API comuns permanecem limitados a 16 KiB; a rota de importação autenticada aceita até 12 MiB de JSON codificado, impondo separadamente o limite menor para o arquivo decodificado.

Códigos de login e senhas de verificação em duas etapas do Telegram não são armazenados. O estado do número de telefone/hash do código é mantido na memória durante a autorização. As sessões do Telegram concedem acesso à conta; nunca faça upload de um diretório de dados, sessão, token, chave do cofre ou chave de assinatura privada para o GitHub.

## Registros e transporte

A resposta padrão de validação da API é substituída para que não repita os valores das credenciais. O registro de acesso ao aplicativo está desativado. Não configure um proxy reverso para registrar cabeçalhos de autorização ou corpos de solicitação. O HTTP transmite tokens e segredos de login em texto simples: utilize HTTPS ou um túnel SSH sempre que sair do localhost.

## Limites de integridade

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## Caso suspeite de algum problema

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
