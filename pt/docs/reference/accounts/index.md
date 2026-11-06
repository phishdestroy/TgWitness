# Formatos de contas e sessões

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/

Faça login por telefone, código QR ou chave de autenticação, importe sessões do Telethon, Pyrogram ou Telegram Desktop e gerencie várias contas.

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

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

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

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Os arquivos são convertidos **na memória** do seu servidor TgWitness. Os arquivos enviados não são armazenados, os arquivos ZIP não são extraídos para o disco e nenhum serviço externo é acionado.
- A sessão resultante é então verificada com o Telegram. Se um arquivo indicar um ID de usuário, ele deverá corresponder à conta informada pelo Telegram.
- Arquivos que descrevem contas diferentes ou credenciais de API diferentes são rejeitados em vez de selecionar apenas uma.
- O campo **“Senha ou texto da sessão”** contém o campo de senha local do TData, um campo para colar um StringSession e **ler arquivos sem fazer login** (preenche o formulário sem entrar em contato com o Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

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
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData é a pasta `tdata` do aplicativo Telegram Desktop (o aplicativo multiplataforma disponível em desktop.telegram.org).

| Sistema | Localização padrão do `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portátil: ao lado do `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Para importá-lo:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
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
| `string_session` (`session_string`, `session_str`; legacy `session`) | Texto da StringSession do Telethon, não um nome de arquivo |
| `auth_key` (`auth_key_hex`) + `dc_id` | Chave de autenticação completa de 512 caracteres e DC 1–5 |
| `user_id` (`id`) | Opcional; verificado no Telegram antes que a autorização seja salva |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

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
