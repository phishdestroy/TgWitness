# Formatos de contas e sessões

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/

Faça login por telefone, código QR ou chave de autenticação, importe sessões do Telethon, Pyrogram ou Telegram Desktop e gerencie várias contas.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Introdução](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/)

![Introdução](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

O TgWitness faz login como uma **conta de usuário do Telegram** (não como um bot) via MTProto, utilizando o Telethon. Cada conta ocupa seu próprio **espaço de trabalho** (denominado *“workspace*” na API e nas ferramentas de linha de comando) com sua própria sessão, fontes, registro e chave de assinatura.

Arquivos de sessão, strings de sessão e chaves de autenticação são **autorizações de conta**: quem possuir uma delas poderá agir em nome dessa conta. Eles não contêm histórico de mensagens.

> [!AVISO] **Não utilize nada que o senhor não possa se dar ao luxo de perder.** Recomendamos veementemente que não conecte contas pessoais ou de qualquer outra forma valiosas, nem crie um ID de API / hash de API em uma conta que o senhor valorize. Não se trata de o TgWitness não ter sido testado: o Telegram restringe e bane permanentemente contas de forma imprevisível — para volumes de solicitações que ele considere excessivos, independentemente do cliente ou da finalidade, sem documentação adequada. Muitos banimentos são irreversíveis. Utilize contas dedicadas. O bom andamento dos testes depende do Telegram, não do software, e não garante nada para o futuro.

- [Visão geral](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#at-a-glance)
- [Antes de começar: ID da API e hash da API](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Número de telefone](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#phone-number) · [Código QR](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#qr-code) · [Chave de Autenticação + ID do DC](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#auth-key--dc-id)
- [Arquivos de contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#pyrogram-session) · [Par de sessão + JSON](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#telethon-stringsession) · [JSON da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json)
- [Identifique o que o senhor possui](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#identify-what-you-have) · [Formatos não suportados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#unsupported-formats)
- [Várias contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#multiple-accounts) · [Mantendo os arquivos de contas em segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#keeping-account-files-safe) · [Solução de problemas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#troubleshooting)

## Visão geral

| O que o senhor tem | Guia em **“Adicionar conta”** | Você também precisará de |
| --- | --- | --- |
| O número de telefone e o acesso aos seus códigos de login | **Telefone** | Senha de autenticação de duas etapas (2FA), caso esteja ativada |
| Telegram aberto em outro dispositivo | **Código QR** | Senha de autenticação de duas etapas (2FA), caso esteja ativada |
| Um arquivo `.session` (Telethon ou Pyrogram) | **Arquivos** | Arquivo JSON complementar opcional para configurações do aplicativo |
| `.session` + `.json` com o mesmo nome | **Arquivos** (selecione ambos) | Normalmente, nada mais |
| Uma pasta “`tdata`” no Telegram Desktop | **Arquivos** (em formato ZIP) | A senha local do Desktop, caso tenha sido definida |
| Uma StringSession do Telethon (texto, `.txt`, `.tgwitness-session`) | **Arquivos** | Não é necessário um par de APIs separado |
| Um `.json` com uma sessão ou chave de autenticação | **Arquivos** | Não é necessário um par de APIs separado |
| Uma chave de autenticação (512 caracteres hexadecimais) e seu número DC | **Chave de autenticação** | ID de usuário opcional |

O TgWitness reconhece os arquivos pelo seu **conteúdo**, e não pelos nomes. Renomear um arquivo nunca o converte.

## Antes de começar: ID da API e hash da API

É possível fazer login sem criar um aplicativo da API do Telegram. Quando nenhum par é inserido, importado ou já está salvo no espaço de trabalho, o TgWitness seleciona um par de seu conjunto integrado de pares de API pública 50 (`tgwitness/api_pool.py`), dando preferência ao Telegram Desktop para um novo login e mantendo em primeiro lugar um par salvo; os candidatos restantes são embaralhados. Se o Telegram recusar um par (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), o próximo é testado, até um máximo de oito por login; os pares recusados são ignorados até a reinicialização. O par que efetuou o login é salvo com a conta e reutilizado para ela. Um ID **API** e um hash **API** identificam o aplicativo para o Telegram; eles não autorizam uma conta por si só.

Campos de conexão ausentes utilizam um par determinístico de dispositivo/SO dos catálogos [opentele2 2.0.0](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735) incluídos no pacote: Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834` e Web `2496`. O ID de compilação de código-fonte do Android `4` também utiliza o catálogo do Android, conforme identificado em [BuildVars do Telegram para Android](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). A Web usa A como padrão; um sufixo de versão do aplicativo `K` importado ou um pacote de idiomas `macos` seleciona K, e a versão `0.7.0` seleciona Webogram. IDs de aplicativos desconhecidos mantêm as configurações padrão do host do Telethon. Campos importados sempre prevalecem, incluindo uma versão mais antiga do aplicativo e um pacote de idiomas vazio. O catálogo nunca altera o ID/hash da API. Seu instantâneo de versão é revisado explicitamente, não obtido durante o login. Um perfil salvo permanece estável após atualizações.

O `account.getAuthorizations` relata os metadados de autorização salvos pelo Telegram; ele não é um eco de cada novo `initConnection`. Compare-o com o perfil realmente enviado. Conectar uma autorização existente não valida seu hash de API correspondente: o `initConnection` envia o ID da API, enquanto o hash é usado pelas solicitações de login.

Após a autorização de um novo celular ou QR, o TgWitness solicita a configuração, o DC mais próximo, o status online, os idiomas (quando o pacote de idiomas não estiver vazio), atualizações do aplicativo e atualizações dos termos de serviço, com intervalos de 0.3–1.5 segundos entre as solicitações. A atualização do status marca brevemente a conta como online. Essa sequência é executada uma vez após a conclusão do login, não em importações, reconexões ou reinicializações. A autorização é salva primeiro; uma solicitação com falha interrompe a sequência sem tentar novamente ou descartar o login. Os resultados são registrados como `account.initialized`, com nomes de erros em vez de corpos de resposta. A sequência não é uma garantia contra restrições à conta.

Para `tdesktop` , um `tz_offset` ausente utiliza o deslocamento UTC local do servidor, arredondado para 900 segundos usando o algoritmo [opentele2](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; licença em `tgwitness/client_profiles.LICENSE` ). Ele é atualizado a cada conexão para que as mudanças no horário de verão sejam refletidas. Um `tz_offset` importado tem precedência em todas as plataformas e é mantido exatamente como está, incluindo zero. Outras entradas `initConnection.params` são mantidas. O formulário de login HTTP aceita o fuso horário numérico retornado pela importação do arquivo; valores booleanos, frações e desvios fora do intervalo suportado são rejeitados.

As rotas diretas, SOCKS5 e HTTP CONNECT utilizam o `ConnectionTcpObfuscated` da Telethon (MTProto abreviado e ofuscado). O HTTPS CONNECT mantém o TLS até o proxy e utiliza o mesmo transporte ofuscado dentro do túnel. O MTProxy mantém seu transporte intermediário aleatório obrigatório e o tratamento de segredos. As mudanças de rota aplicam as mesmas opções. A ofuscação altera o enquadramento dos pacotes; ela não oculta a conta nem seus metadados de cliente do Telegram, nem implica imunidade a restrições.

Após conectar um cliente autorizado, o TgWitness verifica a configuração, o DC mais próximo, a autorização atual, a linha de base da camada revisada, os idiomas, as atualizações do aplicativo e as atualizações dos termos de serviço. Esses diagnósticos são executados uma vez por instância do cliente, antes da coleta, e são exibidos nos detalhes da conexão com a respectiva hora. O `account.connection_checked` registra o resultado sem hashes de sessão, IPs, tokens ou hashes de API. Ele nunca aceita termos nem instala atualizações. Uma falha na solicitação ou o FloodWait interrompe as solicitações subsequentes; um resultado ausente permanece desconhecido. As verificações locais ainda podem relatar seus resultados, enquanto as verificações de rede são ignoradas.

Os diagnósticos do FloodWait retêm o método TL com falha, quaisquer wrappers Takeout/range, a espera solicitada pelo servidor e o prazo efetivo em `telegram.backoff`. Os detalhes da conexão mostram o método e o prazo enquanto as solicitações estão em pausa. O diagnóstico inclui contadores de chamadas do cliente por método desde que esse cliente foi criado; eles contam a resolução de pares aninhados separadamente, mas não contam pacotes nem as tentativas internas de repetição do Telethon. Os contadores atuais também estão disponíveis como `collector.rpc_activity` na API de status. Nenhum argumento de solicitação, nome de usuário, hashes de acesso ou texto de exceção é incluído. O último diagnóstico e o prazo completo permanecem após a reinicialização. Esperas anteriores sem um registro de método não podem ser atribuídas retrospectivamente. Consulte [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) para a revisão da fonte e a distinção entre descoberta e aquisição de histórico.

`official_app=True` ou `False` é o sinalizador de autorização atual do Telegram. Nenhum dos valores determina se a conta está restrita, é confiável ou está sob observação. Os instantâneos `account.devices` existentes no modo de evidência continuam sendo o histórico de todos os dispositivos conectados; os diagnósticos de conexão retêm apenas a descrição do dispositivo atual.

Antes da conexão, verificações preventivas comparam a plataforma da API, o pacote de idiomas, os formatos de dispositivo/SO e versão do aplicativo, a localidade do sistema móvel e a camada de esquema real do Telethon com a linha de base do catálogo revisado. Avisos aparecem no log do servidor e nos metadados de status da conta; eles nunca substituem valores importados nem alteram a camada de esquema. Uma camada diferente é um sinal de revisão de compatibilidade, não uma prova de que a conta esteja com problemas ou restrita. Essas verificações e o código `official_app` não garantem que o Telegram considere a conta a salvo de restrições. O status de conta desconectada utiliza o perfil salvo em vez de gerar outra descrição do dispositivo.

Para utilizar seu próprio aplicativo (a conta que o registra é a que corre risco; consulte [“Por que um conjunto de APIs integrado?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)”):

1. Acesse [my.telegram.org](https://my.telegram.org) e faça login com qualquer número de telefone de sua propriedade. O código é enviado pelo aplicativo do Telegram, e não por SMS.
2. Escolha **as ferramentas de desenvolvimento de API**.
3. Crie um aplicativo: qualquer título e nome abreviado (5 a 32 letras), plataforma **Desktop**. O URL e a descrição podem ficar em branco.
4. Copie **o api_id do aplicativo** (um número) e **o api_hash do aplicativo** (32 caracteres hexadecimais).

No painel, os campos **“ID da API” e “Hash”** estão localizados abaixo do formulário de login. É possível colar um único par `api_id:api_hash` no campo **“ID da API”** e ambos os campos serão preenchidos. Um único par pode ser utilizado para todas as suas contas. Após um login bem-sucedido, ele é salvo, criptografado, exclusivamente nesse espaço de trabalho e nunca é enviado de volta ao navegador.

Estão envolvidas três credenciais diferentes:

| Secreto | Abrir | Onde está disponível |
| --- | --- | --- |
| Token do painel | O painel web do TgWitness | `panel-token.txt` no diretório de dados, ou `TGWITNESS_TOKEN` |
| ID da API + hash | Nada por si só; identifica o aplicativo | Emparelhamento integrado, configurações importadas ou seu próprio aplicativo em my.telegram.org |
| Autorização de conta | A conta no Telegram | Criado por meio de login por telefone/QR ou importado como uma sessão |

Caso seja necessário acessar o Telegram por meio de um proxy, configure-o primeiro em **Conta → Configurações → Configurações de conexão → Alterar rota de conexão**.

## Número de telefone

1. Abra **a conta**, acesse a guia **“Telefone”** e insira o número no formato internacional, por exemplo, `+44 7700 900123`. Espaços e traços são removidos automaticamente.
2. Clique em **“Continuar**”. Os campos “ID da API” e “Hash” podem permanecer em branco.
3. Insira o código enviado pelo Telegram (geralmente para o aplicativo do Telegram; o envio por SMS não é garantido).
4. Caso a conta possua verificação em duas etapas, digite essa senha. Não se trata do token do painel nem da senha do dispositivo.
5. Verifique o ID da conta exibido após o login e, em seguida, selecione as fontes.

Os códigos de login e a senha de autenticação de duas etapas (2FA) nunca são gravados no disco.

## Código QR

Utilize esta opção quando a conta já estiver conectada em um celular ou em outro computador.

1. Guia **“Código QR”** → **Mostrar código QR**. O campo “ID da API + Hash” pode permanecer em branco.
2. No dispositivo em que está conectado: **Configurações → Dispositivos → Vincular dispositivo de desktop**, escaneie o código e confirme.
3. Insira a senha de autenticação de duas etapas (2FA) no TgWitness caso o Telegram a solicite.

A imagem do QR é gerada localmente. Os códigos expiram; clique em **“Gerar outro código QR”** para tentar novamente. Bloquear o painel, alternar de área de trabalho ou iniciar outro login cancela um código pendente.

## Chave de Autenticação + ID do DC

Uma Chave de Autorização (Auth Key) é a autorização bruta de 256 bytes por trás de cada sessão do Telegram, representada por **512 caracteres hexadecimais**, juntamente com o número do centro de dados **DC 1–5**.

1. Guia **“Chave de autenticação**”. Cole a chave completa; uma chave abreviada que contenha “`…`” não funcionará.
2. Selecione o DC ID fornecido com a chave.
3. Opcionalmente, insira o **ID do usuário**. O TgWitness recusará a conexão caso o Telegram identifique uma conta diferente.
4. **Conta no** Press **Connect**.

Uma chave de autenticação (512 caracteres) não é um hash de API (32 caracteres). A mesma chave também pode ser importada como JSON; consulte [JSON da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json).

## Arquivos de contas

Abra **“Adicionar conta” → “Arquivos”** e selecione até **quatro arquivos pertencentes a uma conta**, totalizando **8 MiB**; em seguida, pressione **“Conectar conta**”.

Os formulários **Arquivos**, **Chave de autenticação** e de importação em massa exibem o aviso de sessão paralela antes da conexão. Por padrão, as autorizações importadas são reutilizadas. Mantenha o cliente original fechado enquanto sua chave estiver em uso aqui. **Arquivos** e **Chave de autenticação** também oferecem **Criar uma autorização independente**, descrita abaixo. A importação em massa ainda utiliza o modo direto. O login por telefone e o login interativo via QR criam autorizações separadas. O título do aviso permanece visível no formulário de importação; sua explicação completa é exibida automaticamente quando arquivos ou uma chave/sequência de sessão são fornecidos. Ele pode ser ocultado após a leitura, para que o seletor de arquivos e os controles de conexão continuem utilizáveis em um celular.

- Os arquivos são convertidos **na memória** do seu servidor TgWitness. Os arquivos enviados não são armazenados, os arquivos ZIP não são extraídos para o disco e nenhum serviço externo é acionado.
- A sessão resultante é então verificada com o Telegram. Se um arquivo indicar um ID de usuário, ele deverá corresponder à conta informada pelo Telegram.
- Arquivos que descrevem contas diferentes ou credenciais de API diferentes são rejeitados em vez de selecionar apenas uma.
- O campo **“Senha ou texto da sessão”** contém o campo de senha local do TData, um campo para colar um StringSession e **ler arquivos sem fazer login** (preenche o formulário sem entrar em contato com o Telegram).

### Criar uma autorização independente

Selecione **Criar uma autorização independente** antes de conectar arquivos importados ou uma chave de autorização. TgWitness conecta brevemente o doador importado, usa-o para aprovar o token de login QR do novo cliente e desconecta o doador imediatamente após a aprovação. O novo cliente possui sua própria chave de autorização e um perfil de desktop selecionado separadamente. As credenciais de API e o perfil de dispositivo fornecidos pelo doador são utilizados apenas para a conexão do doador. Nenhuma autorização existente é desconectada ou revogada.

**Mantenha o cliente original do doador totalmente fechado durante esta etapa.** A conexão inicial ainda usa sua chave copiada; portanto, este modo não pode eliminar esse risco inicial de uso paralelo. Assim que a nova autorização estiver conectada, o proprietário poderá reabrir o cliente original e usar ambos de forma independente. O login interativo **por código QR** permite que o cliente original aprove o login sem copiar ou conectar sua chave aqui.

Se o Telegram solicitar 2FA, este modo utiliza `twoFA` do JSON selecionado, quando presente, ou solicita a senha. Uma senha importada rejeitada retorna ao formulário de senha. As senhas não são salvas. A chave candidata é salva criptografada no `independent_login.enc`, incluindo alterações durante a migração do data center. Após uma interrupção, selecione o mesmo doador e esta opção para retomar a chave candidata salva. O espaço de trabalho permanece reservado para essa conta; a falha na conclusão não exclui o novo espaço de trabalho. Mantenha seu diretório de dados e a chave do cofre. As credenciais finais e o registro do diário `account.authorized` incluem o método de importação, os formatos de entrada e o ID da API do doador, sem a chave ou a senha do doador.

Em 5 de novembro de 2026, uma conta dedicada passou por verificações em tempo real com os doadores Telethon, Pyrogram e TData: conclusão da autenticação de 2 fatores (2FA), novas chaves de autorização distintas, acesso simultâneo pelo doador e pelo novo cliente, e leitura de um canal público. O caso da Telethon também retomou um candidato salvo após uma interrupção na etapa da senha. Cada nova autorização concluiu as seis solicitações de inicialização pós-login, e seu diário assinado foi verificado. A sessão original permaneceu utilizável em todos os quatro formatos fornecidos.

O banco de dados de erros [RPC do Telegram](https://core.telegram.org/api/errors.json) associa `FRESH_CHANGE_ADMINS_FORBIDDEN` à troca de administradores, `FRESH_CHANGE_PHONE_FORBIDDEN` à alteração do número de telefone e `FRESH_RESET_AUTHORISATION_FORBIDDEN` à revogação de outras sessões, à alteração de sua validade ou ao registro de uma senha de acesso. `SESSION_TOO_FRESH_*` e `PASSWORD_TOO_FRESH_*` dizem respeito a transferências de propriedade e retiradas de receita ou presentes. Essas não são operações de coleta; um novo login não implica uma proibição geral de leitura por 24 horas. A exportação pode retornar `TAKEOUT_INIT_DELAY_*` separadamente. TgWitness mantém as pausas solicitadas pelo servidor e não tenta novamente a aceitação do token automaticamente nem revoga sessões para contornar restrições.

### Telethon `.session`

|  |  |
| --- | --- |
| O que é | O banco de dados SQLite que as ferramentas baseadas no Telethon criam, por exemplo, `my_account.session` |
| Reconhecido por | Tabelas `sessions` (com `dc_id`, `server_address`, `port`, `auth_key`) e `version` = 7 ou 8 |
| Requisitos | Exatamente uma linha de sessão autorizada; um banco de dados fechado e completo |

Feche primeiro o programa que criou o arquivo. Se `my_account.session-journal` ou `my_account.session-wal` estiverem presentes ao lado dele, o banco de dados não está finalizado: abra e feche o cliente original corretamente. A exclusão desses arquivos sidecar pode deixar uma cópia corrompida.

### Pyrogram `.session`

|  |  |
| --- | --- |
| O que é | As ferramentas baseadas no Pyrogram criam um banco de dados SQLite |
| Reconhecido por | Tabela `sessions` com `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 ou 3 |
| Requisitos | Uma sessão **de usuário** autorizado na rede de produção. Sessões de bots e de servidores de dados de teste (DC) são rejeitadas |

O ID do usuário armazenado é verificado no Telegram durante o login.

### Par de sessão + JSON

As contas costumam ser distribuídas como dois arquivos com o mesmo nome, por exemplo, `447700900123.session` e `447700900123.json`. Selecione **ambos** de uma só vez.

- A partir do JSON, o TgWitness utiliza `app_id`/`api_id` e `app_hash`/`api_hash`, de modo que normalmente não é necessário digitar credenciais da API.
- O perfil de conexão utiliza `device_model` (também conhecido como `device`), `system_version` (também conhecido como `sdk`), `app_version`, `lang_code`, `system_lang_code` (também conhecido como `system_lang_pack`), `lang_pack` e `tz_offset` opcional (segundos em relação ao UTC, de -43200 a 50400). Os campos fornecidos têm prioridade sobre os padrões gerados e o idioma do painel/navegador . Aliases conflitantes são rejeitados. O perfil resolvido é salvo nas credenciais criptografadas da área de trabalho e reutilizado após a reinicialização, incluindo a versão do aplicativo.
- `phone`, configurações de proxy e tokens de dispositivo são **ignorados**. `twoFA` é somente leitura quando **Criar uma autorização independente** é selecionado; a importação direta o ignora.
- Um JSON sem um campo de autorização compatível é apenas metadados. Adicione seu arquivo de sessão ou continue com o login por telefone ou QR. Um JSON contendo uma sessão compatível ou chave de autenticação (Auth Key) pode autorizar por si só; consulte [Account JSON](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData é a pasta `tdata` do aplicativo Telegram Desktop (o aplicativo multiplataforma disponível em desktop.telegram.org).

| Sistema | Localização padrão do `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portátil: ao lado do `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Para importá-lo:

> **Aviso de sessão paralela.** A importação direta de TData reutiliza a chave de autorização do Telegram Desktop. Não utilize essa chave simultaneamente no Desktop e no TgWitness. O Telegram pode invalidar a autorização com o `AUTH_KEY_DUPLICATED`, tornando ambas as cópias inutilizáveis até um novo login.
>
>
>
> Feche completamente o Desktop, incluindo seu processo na bandeja, e mantenha essa cópia fechada enquanto o TgWitness usa a sessão importada. **Feche, não faça logout nem revogue a sessão:** a revogação também invalida a cópia importada. Se você precisar que ambos os clientes estejam em execução, selecione **Criar uma autorização independente** e mantenha o Desktop fechado até que o novo login seja bem-sucedido, ou faça login no TgWitness por telefone ou QR. Recomenda-se uma conta dedicada, mas isso não torna as chaves clonadas seguras para uso em paralelo.
>
>
>
> Isso também se aplica a arquivos importados `.session` , ao texto da StringSession e à chave de autenticação HEX. Outros clientes com suas próprias autorizações criadas de forma independente podem permanecer conectados. Consulte [a documentação do Telegram sobre AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Encerre completamente o Telegram Desktop.
2. Crie um arquivo ZIP contendo **apenas** estes dois itens do `tdata`:

   - `key_datas`
   - o arquivo de 16 caracteres que termina em `s` ao lado dele, geralmente `D877F783D5D3EF8Cs`

   Compactar a pasta inteira com seu cache de mídia geralmente excede os limites (512 entradas, 32 MiB descompactados). 3. Selecione o arquivo ZIP em **“Arquivos**”. Se o Telegram Desktop tiver uma **senha local**, insira-a primeiro no campo **“Senha” ou “Texto da sessão**”. Essa não é a senha da autenticação de dois fatores (2FA).

Compatível: uma conta por arquivo, armazenamento moderno `key_datas`/`key_data0`/`key_data1`, senha local. Não compatível: pastas com várias contas conectadas, layouts mais antigos da versão para desktop, arquivos ZIP protegidos por senha e o aplicativo nativo separado para macOS “Telegram para macOS”.

### Telethon StringSession

Uma única linha de texto, geralmente começando com `1` e com cerca de 350 caracteres. Carregue- a como um arquivo `.txt` ou `.tgwitness-session` (no máximo 4 KiB) ou cole-a em **“Código de acesso” ou “Texto da sessão**”. Apenas strings do Telethon são aceitas; as strings do Pyrogram e do TDLib utilizam formatos diferentes.

### JSON da conta

Um objeto JSON, com no máximo **64 KiB**, em um arquivo com extensão **`.json`**.

| Campo (pseudônimos) | Significado |
| --- | --- |
| `api_id` (`app_id`) | ID do aplicativo, um número positivo |
| `api_hash` (`app_hash`) | Hash do aplicativo, 32 caracteres hexadecimais |
| `string_session` (`session_string`, `session_str`; `session` legado) | Texto da StringSession do Telethon, não um nome de arquivo |
| `auth_key` (`auth_key_hex`) + `dc_id` | Chave de autenticação completa de 512 caracteres e DC 1–5 |
| `user_id` (`id`) | Opcional; verificado no Telegram antes que a autorização seja salva |
| `device_model` (`device`) | Descrição do dispositivo de conexão |
| `system_version` (`sdk`) | Versão do sistema operacional de conexão |
| `app_version` | Versão do aplicativo enviada ao Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Idioma do cliente, idioma do sistema e pacote de idiomas do cliente; um valor vazio para `lang_pack` é permitido |
| `tz_offset` | Desvio opcional em relação ao UTC em segundos, enviado em `initConnection.params`; string de número inteiro ou decimal |

Se houver um alias e o nome principal, eles devem coincidir. Campos explícitos de sessão do Telethon têm prioridade sobre um blob genérico `session` em outro formato. Se ambos contiverem sessões reconhecíveis do Telethon, devem descrever a mesma autorização. Sem um campo explícito, `session` deve ser uma StringSession válida do Telethon. Exemplos:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

O primeiro exemplo preenche apenas as credenciais da API; faça login por telefone ou QR, ou adicione um arquivo de sessão. Listas em massa (um array JSON de contas) não são aceitas.

## Identifique o que o senhor possui

| Como pode ver | Trata-se de | Utilização |
| --- | --- | --- |
| `*.session`; ao abri-lo em um editor de texto, aparece `SQLite format 3` na parte superior | Telethon ou Pyrogram SQLite | **Arquivos** (detectados automaticamente) |
| Uma pasta `tdata` contendo `key_datas` | Telegram Desktop TData | Compacte dois arquivos em ZIP e, em seguida, **Arquivos** |
| Uma linha de texto começando com `1`, cerca de 350 caracteres | Telethon StringSession | **Arquivos** |
| `*.json` com `app_id`/`app_hash` | Metadados complementares | **Arquivos**, juntamente com sua sessão |
| `*.json` com `auth_key` ou `string_session` | JSON da conta | **Arquivos** |
| 512 caracteres `0-9a-f` | Chave de autenticação | **Chave de autenticação** |
| 32 caracteres `0-9a-f` | Hash da API | **ID da API + Hash** |
| `td.binlog` ou `db.sqlite` de um aplicativo TDLib | Armazenamento TDLib | Não compatível |
| `123456789:AA…` | Token do bot | Não compatível |

## Formatos não suportados

| Formato | Alternativa |
| --- | --- |
| Armazenamento TDLib (`td.binlog`) e exportações TDLib | Faça login por telefone ou QR |
| **Sequências** de sessão do Pyrogram | Utilize o arquivo Pyrogram `.session`, ou o código QR/telefone |
| TData com várias contas conectadas | Faça logout das outras contas no Telegram Desktop ou utilize o arquivo de sessão específico de cada conta |
| Tokens de bot | Não suportado: o TgWitness atua como uma conta de usuário |
| Listas em CSV/JSON de diversas contas | Importe arquivos de sessão compatíveis em **Contas → Importar contas** ou entre por telefone/QR em espaços de trabalho separados |
| Sessões de teste no DC ou com bots | Utilize uma conta de usuário de produção |

## Várias contas

Pressione **+** ao lado do seletor de conta ou abra **Conta → Configurações → Configurações de conexão → Espaços de trabalho**, insira um nome e faça login.

- Qualquer número de espaços de trabalho, incluindo o principal. Cada um possui sua própria sessão, rota de proxy, fontes, política de captura, registro, chave de assinatura, pontos de verificação e exportações.
- A troca da área de trabalho exibida não interrompe as demais.
- Um diário permanece vinculado à conta que o criou. O login com uma conta diferente requer outro espaço de trabalho, e uma conta não pode ser atribuída a dois espaços de trabalho.
- O token do painel principal controla todas as áreas de trabalho. [O acesso concedido](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/) pode restringir o acesso de outras pessoas a contas e chats selecionados, com permissões e limites de sessão distintos.
- **A função “Contas”** renomeia um espaço de trabalho e exclui um espaço adicionado, juntamente com sua sessão, registro, fontes e chave de assinatura. O espaço de trabalho principal não pode ser excluído do painel.

### Importação em lote e grupos de contas

Use **Contas → Importar contas** para adicionar várias contas, emparelhar arquivos pelo nome base e visualizar o resultado de cada login. Cada conta recebe seu próprio espaço de trabalho.

Um grupo mantém contas relacionadas juntas sem mesclar suas sessões, chaves ou evidências. Clicar em **“Grupo aberto”** em **“Contas”** leva à página correspondente em `/groups/<id>`:

- **Contas:** rota de conexão, observações e última mensagem de cada membro, com **“Iniciar tudo”** e **“Pausar tudo**”.
- **Requer atenção:** contas que foram desconectadas, estão indisponíveis ou apresentam um problema de conexão, entrada, fonte ou mídia; cada nome leva ao respectivo cartão.
- **Nas conversas de várias contas, é possível ver:** fontes compartilhadas, as contas que as observam e interrupções no período de observação do espaço de trabalho disponível (até sete dias). **A exportação com N contas** divide a exportação de um canal ou supergrupo entre elas e assina um único arquivo.
- **Exportar grupo:** uma ZIP com a exportação assinada de cada conta em `accounts/` e `manifest.json` listando suas impressões digitais de SHA-256 e chaves, assinadas pelo espaço de trabalho principal em `manifest.signature.json`. Verifique cada arquivo de conta separadamente com `python -m tgwitness.verify` e a impressão digital confiável dessa conta.

Os membros compartilham as configurações do grupo; uma conta pode manter seus próprios valores. Consulte [as configurações compartilhadas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/settings/#account-groups), [o guia de importação e grupos](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) e [o painel de pool MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Sair

**Conta → Sair do Telegram** (com a observação pausada) solicita ao Telegram que encerre a sessão, de modo que ela também desapareça da seção **Configurações → Dispositivos** da conta e remova a sessão do cofre do espaço de trabalho. O registro, as fontes, as configurações e a chave de assinatura permanecem, e o registro registra o encerramento da sessão. O espaço de trabalho ainda pertence à sua conta: somente essa conta poderá se conectar a ele novamente. Se o Telegram não responder, a sessão ainda será removida aqui e o painel indicará isso; encerre-a no Telegram em **Configurações → Dispositivos**.

## Mantendo os arquivos de contas em segurança

- Trate cada `.session`, TData ZIP, StringSession, chave de autenticação e JSON de conta como uma senha. O TgWitness mantém a autorização importada em seu cofre criptografado; o(a) senhor(a) pode remover os arquivos originais posteriormente.
- Não execute a mesma autorização em dois programas ao mesmo tempo. O Telegram pode revogá-la (`AUTH_KEY_DUPLICATED`), e ambas as cópias deixarão de funcionar.
- Uma sessão expirada ou revogada não pode ser reativada por meio de conversão. Faça login novamente.

## Solução de problemas

| Mensagem ou sintoma | O que fazer |
| --- | --- |
| *Não é possível ler esta sessão. Feche o cliente original…* | O arquivo SQLite está aberto ou incompleto (sidecar `-journal`/`-wal`). Feche o programa original corretamente e copie o arquivo novamente. |
| *Esquemas SQLite do Telethon compatíveis: 7 e 8* / *Pyrogram … 2 e 3* | O arquivo foi criado por uma versão muito antiga ou desconhecida da biblioteca. Faça o login por telefone/QR em vez disso. |
| *Apenas sessões de usuários de produção autorizadas são suportadas* | O arquivo Pyrogram pertence a um bot ou à rede de testes. |
| *O arquivo TData ultrapassa 512 entradas ou 32 MiB* | Compacte apenas os arquivos `key_datas` e `D877F783D5D3EF8Cs`, e não a pasta inteira. |
| *Não é possível descriptografar o TData. Verifique a senha local do Desktop* | Insira a senha local do Telegram Desktop no campo **“Senha” ou “Texto da sessão**”. |
| *Importe uma conta do TData por vez* | O Telegram Desktop possuía várias contas; consulte [“Formatos não suportados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#unsupported-formats)”. |
| *Os arquivos selecionados descrevem diferentes contas ou credenciais de API* | Selecione arquivos de apenas uma conta. |
| *O JSON não contém credenciais ou autorizações de API compatíveis* | Verifique os nomes dos campos no [JSON da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json). |
| *Apenas metadados da API* | O JSON não possui sessão. Adicione o arquivo `.session` ou utilize o telefone/QR. |
| *A chave de autenticação HEX deve conter todos os 512 caracteres hexadecimais* | A chave está truncada ou contém “`…`”. |
| O ID da conta não corresponde à conta importada | O ID de usuário do arquivo difere do que o Telegram informa; o arquivo pertence a outra conta. |
| A conta já pertence a outro espaço de trabalho | Abra esse espaço de trabalho em vez de adicionar a conta duas vezes. |
| Conectado, mas falta um grupo privado na lista de bate-papos em **“Fontes”** | Verifique a adesão. O seletor analisa as primeiras 1.000 conversas; aumente o limite na seção **“Parâmetros**”. |
| Falha na conexão via proxy | Verifique a rota e o modo de IP. O modo automático MTProxy tenta outra entrada que esteja funcionando. O modo “Hide the address waits” (Ocultar as esperas de endereço); o modo “Direct” (Direto), como último recurso, pode se conectar diretamente após o atraso configurado. Consulte [os modos de roteamento](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes). |

Veja também: [conexão e segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) para proxies e criptografia, e [como funciona a coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/) do que é capturado após o login.
