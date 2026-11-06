# Segurança e tratamento de dados

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/

Modelo de ameaças, modelo de acesso, dados confidenciais em repouso, exposição de rede, importação de sessões e como relatar uma vulnerabilidade.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Implantação e recuperação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/)

![Implantação e recuperação](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Esta página descreve o acesso, o armazenamento e a proteção de rede em um espaço de trabalho local ou no servidor. Para coleta em um GitHub Runner ou em uma VM confidencial do Intel TDX, consulte os [modos de verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope), que adicionam verificações do ambiente de coleta. Conexões de conta, notificações, carimbos de data/hora, cópias externas e testemunhas possuem suas próprias configurações de roteamento.

| Área | Em resumo |
| --- | --- |
| Acesso | Chave de administrador, além de acesso restrito a contas/chats, sete permissões e sessões revogáveis; localhost por padrão |
| Segredos em repouso | As configurações de sessão, par de API, chave de assinatura e proxy são criptografadas com Fernet |
| Mensagens e arquivos de mídia | Armazenado sem criptografia: utilize criptografia de disco e permissões rigorosas |
| Integridade | Cadeia de hash SHA-256 e uma assinatura Ed25519 em cada registro |
| Limite de confiança local | O administrador do host controla o espaço de trabalho e sua chave de assinatura; pontos de verificação independentes mantêm um limite anterior do diário |

Para relatórios de vulnerabilidades, consulte a [política de segurança](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

**Nesta página**

- [Modelo de acesso](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#access-model)
- [Conteúdo do painel e exportações](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#panel-content-and-exports)
- [Segredos em repouso](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#secrets-at-rest)
- [Proxies e rotas de rede](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#proxies-and-network-routes)
- [Login e importação de sessões](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#sign-in-and-session-imports)
- [Logs e transporte](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#logs-and-transport)
- [Limites de integridade](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#integrity-limits)
- [Se você suspeitar de um problema](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/#if-you-suspect-a-problem)

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

As credenciais da API do Telegram, a sessão e a chave de assinatura são criptografadas com Fernet. Para mensagens e mídias locais, a criptografia é fornecida pelo disco ou volume do host; o espaço de trabalho armazena arquivos comuns. As exportações podem usar um ZIP AES-256 protegido por senha, e as cópias externas usam AES-256-GCM.

A chave do cofre é, por padrão, o diretório de dados protegidos. Use um arquivo externo de chave-mestra abaixo para armazená-la separadamente. No Unix, novos arquivos de chave privada usam o modo 0600 e novos diretórios de dados usam 0700; no Windows, defina a ACL do diretório para a conta de serviço e os administradores autorizados. As permissões existentes do diretório são mantidas.

### Chave mestra externa

Para um novo diretório de dados, TGWITNESS_VAULT_KEY_FILE pode fornecer uma chave mestra aleatória externa. O HKDF-SHA256 e um salt aleatório separado geram uma chave Fernet diferente para cada espaço de trabalho. O arquivo vault.external.json deve ser mantido para recuperação. Chaves-mestras ausentes ou incorretas resultam em falha. Cofres locais existentes não são migrados silenciosamente. O painel exibe o modo de armazenamento de chaves selecionado. A criptografia de disco protege as mensagens e os arquivos de mídia locais em ambos os modos; consulte “ [conexão” e “](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/)proteção de dados” para detalhes de configuração.

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

A verificação local verifica as assinaturas dos registros, a cadeia de hash, os anexos e o manifesto de exportação. O administrador detém a chave de assinatura local e pode criar outro diário assinado; um ponto de verificação mantido de forma independente detecta a substituição do prefixo que ele abrange. Mantenha a impressão digital da chave e os pontos de verificação com o destinatário ou uma testemunha independente.

Para uma coleta verificada de forma independente, escolha [Captura via GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) ou [Implantação via Intel TDX](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Seus verificadores analisam a proveniência do fluxo de trabalho ou medições de hardware, além da integridade do arquivo. Carimbos de data/hora opcionais e cópias criptografadas em local externo fornecem âncoras temporais e cópias recuperáveis; o formato [de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) descreve as verificações para cada modo.

## Caso suspeite de algum problema

Preserve o diretório de dados original e utilize uma cópia separada para análise. Relate a versão afetada, a operação e as etapas reproduzíveis por meio da [política de segurança](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), mantendo os dados da conta e as credenciais em sigilo.
