# Conexão, proxies e proteção de dados

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/

Autenticação, conjuntos automáticos de proxies, modos de IP, política de fallback, solicitações externas e armazenamento de segredos.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Este documento descreve o comportamento do TgWitness 0.8.0 e suas limitações. A autenticação, o acesso à fonte, a conectividade de rede e a integridade da captura são estados distintos. Para etapas de login, formatos de arquivo e contas múltiplas, comece por [“Contas e formatos de sessão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/)”. Para políticas de eventos e comportamento de reinício, consulte [“Como funciona a coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/)”.

## Configuração guiada da conexão

Em **Conexão**, o administrador pode escolher **Esta conta**, **Um grupo de contas** ou **Todas as contas** e, em seguida, selecionar uma rota. **Revisar seleção** lista as contas afetadas. **Preparar e verificar** testa a rota proposta sem alterar a rota salva. **Aplicar conexão verificada** verifica novamente, pausa a observação se necessário, salva a rota e retoma a observação que já estava em andamento. Nunca inicia a coleta em uma conta que estava ociosa anteriormente. Os downloads do histórico permanecem pausados e podem ser retomados separadamente. Pause as exportações ativas antes de alternar.

Alterações em grupos mantêm as contas em suas respectivas rotas por padrão. Desmarque essa opção somente quando a visualização listar as alterações desejadas. O aplicativo relata o resultado de cada conta; não se trata de uma transação do tipo “tudo ou nada” entre bancos de dados. Uma mudança malsucedida restaura as configurações anteriores daquela conta. Uma falha na retomada é exibida explicitamente. As visualizações expiram após dez minutos e alterações nas configurações de conexão ou na participação em grupos exigem uma nova verificação.

| Rota | O que o TgWitness gerencia |
| --- | --- |
| Direto | Conexões a partir do host; uma VPN de host externo não é detectada nem imposta. |
| VPN | Um perfil WireGuard de túnel completo por conta, executado por um processo SOCKS5 no espaço do usuário local. Nenhuma interface de host ou driver é instalado. |
| Meu proxy | Credenciais SOCKS5, HTTP CONNECT ou MTProxy. Um URL pode preencher os campos SOCKS5/HTTP. Ao selecionar várias contas, esse proxy inserido é compartilhado. |
| MTProto público | O pool existente atribui rotas Telegram. As solicitações externas ficam desativadas até que um proxy externo adequado seja configurado nas configurações avançadas. |
| WARP | Um túnel local separado para cada conta selecionada, com registro no WARP e um perfil do WireGuard mantido no cofre dessa conta. |

A verificação da rota atual utiliza um transporte Telegram novo e não autenticado, e não a sessão da conta. Para rotas compatíveis com HTTP, ela também solicita o rastreamento HTTPS da Cloudflare por essa rota e exibe o IP de saída relatado, o país, o estado do WARP e a hora da verificação. A latência medida é o tempo de estabelecimento da conexão Telegram, não um ping ICMP. A preparação do WARP falha, a menos que o rastreamento indique que o WARP está ativo. Essas verificações estabelecem a conectividade, não a autenticidade ou integridade das mensagens capturadas. Um processo local em execução, por si só, não constitui uma verificação de saída bem-sucedida.

### WARP e WireGuard portáteis

Esta é uma integração não oficial do WARP **** utilizando [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) e [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3). O administrador aceita explicitamente a configuração antes do primeiro download ou do registro no WARP. Essas conexões de configuração vão diretamente para o GitHub e o Cloudflare e revelam o IP da máquina. O tráfego normal da conta mantém sua rota existente até o aplicativo. O Cloudflare escolhe o endereço de saída e o país; túneis separados podem compartilhar um endereço de saída. A seleção de país, a rotação periódica de IP e um kill switch de VPN para todo o host não são fornecidos por esse recurso.

Downloads de auxiliares compatíveis: Linux e macOS x86-64/ARM64, e Windows x86-64. Os artefatos são verificados em relação aos hashes SHA-256 incluídos no código-fonte revisado, e os executáveis armazenados em cache são verificados novamente antes da execução. Nenhum auxiliar é adicionado ao PATH, instalado como serviço do sistema ou recebe um ouvinte público. Todos os arquivos ficam no diretório `portable-routes/` do espaço de trabalho e em entradas criptografadas do cofre. O ouvinte de loopback SOCKS5 requer credenciais geradas de forma independente.

Perfis privados e credenciais de conta WARP são criptografados com o cofre do espaço de trabalho existente. Durante a execução, o auxiliar precisa de uma configuração em texto simples exclusiva do proprietário; ela é removida em uma parada normal. Uma falha no host pode deixar esse arquivo para trás na pasta de dados exclusiva do proprietário. Isso não criptografa o disco nem protege contra o administrador. O supervisor fecha o túnel se o pipe pai do painel desaparecer. Um túnel com falha nunca habilita um fallback direto. A reinicialização do painel restaura um túnel selecionado; tentativas de inicialização com falha são repetidas com um atraso limitado. **Parar o túnel** também pausa a observação e mantém o estado de parada. **Iniciar o túnel** inicia o túnel; retome a observação separadamente quando estiver pronto.

Os perfis do WireGuard enviados devem conter uma interface e um par, rotas IPv4 e IPv6 completas, e não devem conter hooks, includes, substituições de ambiente ou listeners adicionais. Os endereços de endpoints públicos são resolvidos e fixados antes da inicialização. Utilize uma VPN externa ou o gateway SOCKS5 para OpenVPN/IPsec e endpoints privados.

## Métodos de autenticação

**O ID da API e o hash da API identificam um aplicativo; eles não substituem o login da conta.** Eles são opcionais no TgWitness. Prioridade: um par inserido no formulário, em seguida, um proveniente de um arquivo JSON de conta importado, depois o par salvo no espaço de trabalho e, por fim, o conjunto integrado de 50 pares públicos, testados em ordem aleatória com rotação automática quando o Telegram recusa um. Apenas o par do Telegram Desktop (2040) é enviado com uma descrição correspondente do cliente Telegram Desktop. Seu próprio par, obtido nas Ferramentas de Desenvolvimento de API em [my.telegram.org,](https://my.telegram.org) pode ser usado com todas as suas contas; cada conta continua tendo sua própria autorização.

| Método | Requisitos | Suporte ao TgWitness |
| --- | --- | --- |
| Telefone, código, autenticação de dois fatores (2FA) opcional | Acesso à conta; par de API opcional | Login no painel |
| Chave de autenticação HEX + ID DC | Chave completa de 512 caracteres e DC 1–5 | Guia **“Chave de autenticação** direta”; o ID do usuário opcional é verificado antes que a autorização seja salva |
| Telethon StringSession | Uma sequência de sessão válida | Login no painel |
| Telethon SQLite `.session` | Texto conciso e consistente | Importação direta de esquemas por meio de painel 7/8; CLI offline opcional |
| Pyrogram SQLite `.session` | Sessão de usuário de produção encerrada | Importação direta de esquemas por meio do painel 2/3 |
| Telegram Desktop TData ZIP | Uma conta moderna; senha local, caso esteja protegida | Conversão na memória com verificações de checksum e descriptografia |
| JSON da conta | Campos suportados de API/sessão/chave | Os metadados, por si só, preenchem as credenciais da API; ainda é necessário um login por sessão/chave ou por telefone/QR code |
| Login via QR | Confirmação de um aplicativo autorizado do Telegram | Geração local de QR, validade/nova tentativa, 2FA opcional |
| TDLib / Pyrogram StringSession | Outros formatos específicos de bibliotecas | Não suportado |
| Token do bot | Um bot com seu próprio modelo de acesso/atualização | Não utilizado por este coletor |

O Telegram opta pela entrega de códigos; o envio por SMS não é garantido. Um hash da API não pode restaurar uma sessão revogada nem substituir uma senha de 2FA esquecida. O TgWitness não armazena códigos de login nem a senha de 2FA do Telegram no disco.

Para uma fonte privada, a conta já deve ter acesso. Não é necessário um nome de usuário de grupo. Um proxy ou importação de sessão não concede nem qualificação de membro nem direitos de administrador. A qualificação atual de membro não garante acesso ao histórico anterior à adesão.

## Importar um arquivo de sessão do Telethon

O Telethon SQLite, o Pyrogram SQLite e o TData do Telegram Desktop utilizam formatos diferentes. O painel detecta e converte as estruturas compatíveis; renomear um arquivo não constitui conversão. Selecione uma sessão e seu JSON correspondente em **“Arquivos**” e, em seguida, pressione **“Conectar conta**”. São aceitos até quatro arquivos correspondentes e 8 MiB no total. Consulte [os limites de formato](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/) para obter detalhes sobre TData/JSON. Não há recuperação de senha. O login por telefone/2FA ou QR gera uma autorização separada.

O caminho opcional da linha de comando exclusivo para o Telethon continua disponível:

1. Encerre a sessão do cliente original e crie uma cópia consistente. O conversor rejeita arquivos com um WAL/diário incompleto. Feche o cliente original adequadamente, em vez de excluir esses arquivos para contornar a verificação.
2. No ambiente do TgWitness, execute:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. Em **“Adicionar conta” → “Arquivos”**, carregue o resultado ou cole sua sequência de caracteres e continue.
2. Verifique o ID numérico da conta exibido, selecione as fontes e inicie a observação.

**O arquivo convertido é uma senha de acesso à conta não criptografada.** Mantenha-o em um armazenamento protegido e nunca o envie para um serviço de conversão de terceiros. O TgWitness armazena a sessão autorizada em seu cofre criptografado. Copiar uma sessão não cria uma autorização separada: não execute clientes simultâneos com chaves de autenticação clonadas e não presuma que as atualizações sejam entregues de forma independente.

A conversão transfere a autorização, não as mensagens originais, o cache da entidade ou um cursor de atualização persistente. Ela não garante a recuperação das atualizações após reinicializações do processo.

## MTProto, Telethon e proxies

MTProto é o protocolo do Telegram. Telethon é a biblioteca cliente em Python utilizada pelo TgWitness. MTProxy é um proxy de transporte do Telegram; SOCKS5 e HTTP CONNECT fornecem túneis gerais. Nenhum deles substitui a autenticação da conta.

Salve a rota para cada espaço de trabalho em **Conta → Configurações → Configurações de conexão → Alterar rota de conexão** antes de fazer login. Os novos espaços de trabalho são configurados por padrão como **Automático MTProxy · listas públicas** com a opção **“Ocultar o endereço**”. Os espaços de trabalho existentes que usavam explicitamente o modo “Direto” mantêm um modo que permite isso.

## Modos de IP

A rota escolhe a conexão. O modo IP, **a proteção de IP** na seção “Conta” do painel, determina quando o endereço do servidor pode ser exposto. Esses controles não instalam uma VPN nem redirecionam todo o tráfego da máquina.

| Modo | Telegram | Solicitações externas |
| --- | --- | --- |
| Ocultar o endereço (`hide`) | Utilize um proxy; aguarde caso nenhum funcione. Não há alternativa direta. | Requer SOCKS5/HTTP; rejeita solicitações sem um proxy adequado. |
| Recorra ao Direct apenas como último recurso (`fallback`) | O MTProxy automático pode utilizar o Direct após o atraso configurado e, em seguida, retornar a um proxy em funcionamento. | Prefira um proxy externo configurado ou a rota SOCKS5/HTTP da conta; caso contrário, a conexão direta é permitida. |
| Servidor atrás de um túnel ou VPN (`tunnel`) | São permitidas rotas diretas e o recurso automático imediato ao pool de reserva. | O acesso direto é permitido quando não houver nenhum proxy configurado. |

O modo de túnel ou VPN pressupõe que você gerencie essa rede separadamente. Sem um túnel em funcionamento, os destinatários podem ver o endereço do próprio servidor. Selecione o modo de acordo com sua rede real, e não com o nome da opção.

### Escolha um caminho

| Rota | Configurações | Limites |
| --- | --- | --- |
| MTProxy automático | Listas integradas ou um catálogo de operadores | Mantém uma rota funcional do Telegram; o recurso alternativo direto depende do modo IP |
| Direto | Modo Tunnel ou VPN | O Telethon utiliza a rota de rede do anfitrião |
| SOCKS5 | Servidor, porta, nome de usuário/senha opcionais | python-socks, DNS de destino remoto habilitado |
| HTTP CONNECT | Servidor, porta, nome de usuário/senha opcionais | HTTP CONNECT simples; o TLS para o próprio proxy não está implementado |
| MTProxy | Servidor, porta, chave secreta | Transporte experimental do Telethon; 32 dígitos hexadecimais ou `dd` + 32 dígitos hexadecimais |

Segredos TLS falsos do tipo `ee` são rejeitados. A normalização do Telethon 1.45 pode remover um prefixo e um domínio, mas isso não implementa o TLS falso. Cole `tg://proxy?server=…&port=…&secret=…` ou `https://t.me/proxy?server=…&port=…&secret=…` e selecione **“Preencher campos a partir do link**”. Isso valida e preenche os campos sem se conectar ou salvar; revise e salve a rota separadamente. Os campos manuais permanecem disponíveis. Consulte [os links de proxy do Telegram](https://core.telegram.org/api/links#proxy-links).

### Proxies públicos fornecidos pela sua instalação

A lista integrada combina quatro fontes: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) e [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). O instantâneo incluído contém informações sobre os terminais, atribuição de fontes e datas de download. A inclusão de um provedor na lista não constitui prova de que o proxy funcione ou forneça todas as atualizações do Telegram.

**O MTProxy automático** verifica a conectividade de transporte do Telegram, mantém um proxy em funcionamento e alterna para outro quando este falha. Os espaços de trabalho preferem proxies diferentes quando há entradas funcionais suficientes disponíveis; um endereço de saída único não é garantido. Os proxies com falha permanecem inativos antes de uma nova tentativa. Se nenhum funcionar, o modo IP determina se a coleta deve aguardar ou se pode utilizar uma conexão direta. A troca de proxies não altera a conta nem apaga seu diário. As escolhas e alterações de rota são registradas no diário assinado.

Enquanto as rotas automáticas estiverem ativas, as listas são atualizadas a cada hora e as verificações de transporte são executadas a cada dez minutos por padrão. Esses intervalos são configuráveis. **A atualização de listas públicas** solicita uma atualização; a simples visualização da lista não altera uma rota manual salva.

**O tráfego do Telegram e as solicitações HTTPS utilizam rotas diferentes.** Os downloads de listas utilizam uma conexão HTTPS separada e a rota de solicitação externa fornecida. O `TGWITNESS_PROXY_FEED_PROXY` substitui explicitamente essa rota por um proxy HTTP/SOCKS5; ambas as variantes do coletor Compose a encaminham. O pool em segundo plano segue o espaço de trabalho principal. Nenhuma sessão do Telegram, credenciais de API, token de painel ou token de bot é enviada aos provedores de feed. Os nomes dos provedores, as datas dos instantâneos e a rota de download aparecem na seção **“De onde vem a lista**”.

Um MTProxy transporta apenas tráfego do Telegram. Operações HTTP do espaço de trabalho, como registros de data e hora, notificações, cópias externas e verificações de fonte, utilizam um proxy SOCKS5/HTTP separado quando configurado; caso contrário, utilizam a rota SOCKS5/HTTP da conta. Na ausência de ambos, a opção “Ocultar endereço” recusa a solicitação; os outros modos permitem a conexão direta. Solicitações externas podem ser desativadas. Um proxy de download de feed explicitamente configurado permanece como uma substituição separada do operador. O serviço de testemunha independente mantém sua própria rota.

Para serviços privados gerenciados por operadores, a configuração existente do ambiente de servidor `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` permite destinos privados e mantém a resolução do nome de host no lado do proxy. Ela não pode ser ativada a partir do painel. O modo somente público rejeita destinos `.onion` antes de consultar o resolvedor público; os serviços onion do Tor exigem essa configuração explícita de destino privado e um proxy adequado. Esse comportamento do DNS se aplica a operações HTTP externas, não ao transporte do Telegram. A Cloudflare documenta o [endpoint JSON do DNS](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/).

****Parâmetros automáticos do pool****

Under **Parameters → Automatic MTProxy**, configure the failure threshold, cooldown, planned rotation, proxy sharing and permitted fallback delay.

| Controle | Padrão |
| --- | --- |
| Disconnects before replacement | 3 within 10 minutes |
| Proxies tried per connection attempt | 3 |
| First / maximum rest after failure | 10 minutes / 6 hours |
| Planned rotation | Disabled; switch on failure |
| Accounts per proxy | 0: prefer separate entries, share when needed. Set 1 to wait for an exclusive entry. |
| Delay before permitted Direct fallback | 10 minutes; Hide the address still refuses Direct |
| Feed refresh / transport checks | 60 / 10 minutes; main workspace values apply to the shared pool |

Different proxies do not guarantee different exit addresses. These settings do not override Telegram limits or prove anonymity.

Para substituir a lista pública pelo seu próprio catálogo de operadoras, configure a substituição abaixo. Isso desativa totalmente as assinaturas externas, inclusive quando a matriz `proxies` estiver vazia.

Copie [o catálogo vazio](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) para `proxy-config/proxies.json` e adicione seus endpoints públicos implantados:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Os valores de exemplo devem ser substituídos. São aceitas até 32 entradas distintas. A lista autenticada retorna rótulos/hosts/portas sem segredos compartilhados; ao selecionar um, suas credenciais são salvas no cofre da área de trabalho. A disponibilidade permanece não testada até que seja realizado um teste de transporte explícito. Um catálogo malformado permite a configuração manual.

Execução nativa: defina `TGWITNESS_PROXY_CATALOG` como o caminho JSON local. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

A sobreposição é montada como `proxy-config` em modo somente leitura; os arquivos devem ser legíveis pelo UID 10001 do contêiner. Esse diretório está excluído do Git, do contexto de compilação do Docker e dos arquivos-fonte. Este catálogo configura as contas de coleta; [o bot testemunha](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/) utiliza sua própria rota HTTP/SOCKS5, e não o MTProxy.

O fallback direto é regido pelo modo IP descrito acima. Suspenda a observação antes de alterar uma rota. Ao salvar, os clientes antigos são desconectados e os logins inacabados são cancelados; um novo cliente utiliza a rota salva. A vinculação entre o diário e a sessão da conta permanece. As configurações substituem a rota anterior: digite novamente as credenciais do proxy ao editá-la.

As credenciais são criptografadas em `network.enc`. A API não retorna o nome de usuário, a senha ou o segredo. Os registros assinados contêm o tipo de rota e se as credenciais estão presentes, excluindo o endpoint e os segredos. O operador pode visualizar o endpoint no painel. Os campos de segredos são apagados após salvar, bloquear ou alternar entre espaços de trabalho.

**O teste de conexão com o Telegram**, também disponível antes do login, abre e fecha uma conexão temporária não autorizada com o Telegram por meio da rota. Ele não entra em contato com um site de verificação de IP. O sucesso do teste confirma a conectividade de transporte, não o acesso a grupos, a entrega completa ou o anonimato.

O proxy se aplica às conexões do cliente do Telegram, incluindo downloads de mídia dos servidores de dados (DC) do Telegram. O navegador, o pip, o SSH e as ferramentas TSA acionadas manualmente seguem rotas separadas. O nome do host do proxy pode ser resolvido localmente. O `rdns` afeta os nomes de host de destino; o Telegram frequentemente fornece endereços IP numéricos dos servidores de dados (DC).

O SOCKS5 e o HTTP CONNECT simples, por si só, não criptografam as credenciais do proxy nem o túnel cliente-proxy. O MTProto protege separadamente o tráfego do Telegram. Utilize um canal seguro apropriado para acessar o proxy em uma rede não confiável. Grupos privados são bate-papos na nuvem; o MTProto não os transforma em bate-papos secretos com criptografia de ponta a ponta.

## Criptografia e assinaturas

| Camada | Implementado | Responsabilidade do operador |
| --- | --- | --- |
| Tráfego do Telegram | Telethon MTProto | Confiança, rota e disponibilidade da plataforma |
| Painel da web | Token de portador, configuração padrão de loopback, limites de solicitações | HTTPS ou túnel SSH para acesso remoto |
| Segredos | Fernet para credenciais de API, sessão, credenciais de proxy e chave privada de assinatura | Proteja a chave de descriptografia e o servidor em execução |
| Chave do cofre | Chave local ou chave mestra externa para uma nova instalação | Armazenamento protegido e backup de chaves separados |
| Mensagens e anexos | Armazenamento de aplicativos em texto simples | Disco/volume criptografado |
| ZIP/JSONL/CSV/HTML | Verificações de integridade, sem criptografia de conteúdo | Proteja cópias exportadas e transferências |
| Proveniência e data | Registro assinado, comprovante de processo, ferramentas RFC 3161 | Chave confiável, pontos de verificação independentes/TSA e procedimento de custódia |

**A proteção de armazenamento** na seção “Conta” exibe esses estados. O token do painel é um segredo de acesso, não uma senha de criptografia. Ele concede acesso de administrador; [os tokens emitidos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/) podem ter seu escopo restrito a contas e chats. Os espaços de trabalho compartilham o processo anfitrião e não são locatários isolados.

O BitLocker, o LUKS, o FileVault ou um volume criptografado gerenciado podem proteger o armazenamento de acordo com seus respectivos modelos de ameaças. Um administrador de uma máquina em execução e desbloqueada ainda pode ler os dados. Inclua SQLite WAL/SHM, mídia, exportações temporárias, swap, backups e downloads do navegador no planejamento de armazenamento. Um volume do Docker não é criptografado simplesmente por ser um volume. O TgWitness não implementa o SQLCipher nem a criptografia de objetos.

## Chave mestra externa

Para uma **nova** instalação, coloque a chave mestra fora do diretório de dados. Isso não migra automaticamente um cofre de chaves local já existente. Prepare um diretório de chaves acessível apenas à identidade do serviço e, em seguida, execute:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, utilizando o ambiente de projeto instalado:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

No Docker, monte o arquivo como somente leitura fora de `/data`, por exemplo, em `/run/secrets/tgwitness-master.key`, e defina a variável de ambiente com esse caminho. O UID do serviço deve ter permissão de leitura. Transmita o caminho, e não os bytes da chave, por meio de arquivos de ambiente/configuração.

Cada espaço de trabalho recebe um “salt” público aleatório e sua própria chave Fernet, derivada por meio do HKDF-SHA256. O `vault.external.json` armazena os metadados de derivação, não a chave mestra. Uma chave ausente ou incorreta impede a inicialização, sem substituí-la silenciosamente. Guarde tanto os metadados do “salt” quanto a chave mestra para fins de recuperação.

Todos os espaços de trabalho derivam da mesma chave mestra; seu comprometimento afeta toda a instalação. O processo em execução pode descriptografar segredos. Trata-se de um HSM ou KDF de senha. Senhas definidas arbitrariamente por usuários não são aceitas no lugar de uma chave aleatória.

Mantenha a chave existente para instalações já em uso até que uma migração planejada seja implementada e verificada. A exclusão de `vault.key` ou a substituição de uma chave mestra pode comprometer o acesso a sessões/chaves de assinatura. Mantenha backups criptografados e chaves separadamente e teste a recuperação em uma instância isolada.
