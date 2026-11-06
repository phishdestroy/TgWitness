# アカウントとセッション形式

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/

電話番号、QRコード、または認証キーでログインし、Telethon、Pyrogram、またはTelegram Desktopのセッションをインポートして、複数のアカウントを運用できます。

TgWitnessは、Telethonを使用して、MTProto経由で**Telegramのユーザーアカウント**（ボットではありません）としてログインします。 各アカウントは、独自の**ワークスペース**（APIおよびコマンドラインツールでは「*ワークスペース*」と呼ばれます）内に存在し、 独自のセッション、ソース、ジャーナル、および署名鍵を持っています。

セッションファイル、セッション文字列、および認証キーは**アカウントの認証情報**です。これらを 所持している者は誰でも、そのアカウントとして行動することができます。これらにはメッセージ履歴は含まれていません。

> [!警告] **失っても構わないもの以外は使用しないでください。**個人用やその他の重要なアカウントを接続すること、および 大切なアカウントでAPI IDやAPIハッシュを作成することは、 強くお勧めしません。 これは、TgWitnessが未検証であるということではありません。Telegramは、 クライアントや目的を問わず、同サービスが「過剰」とみなすリクエスト量に対して、 予測不能な形でアカウントを制限・永久停止しており、適切なドキュメントも提供されていません。多くの停止措置は 取り消すことができません。 専用のアカウントをご利用ください。テストが円滑に進むかどうかは、ソフトウェアではなく Telegram次第であり、今後の動作については一切保証されません。

- [概要](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#at-a-glance)
- [ご利用開始前に：API ID および API ハッシュ](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [電話番号](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#phone-number) · [QRコード](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#qr-code) · [認証キー + DC ID](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#auth-key--dc-id)
- [アカウントファイル](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#pyrogram-session) · [セッションとJSONのペア](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#telethon-stringsession) · [アカウントのJSON](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#account-json)
- [お手持ちのものを特定する](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#identify-what-you-have) · [サポートされていない形式](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#unsupported-formats)
- [複数のアカウント](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#multiple-accounts) · [アカウントファイルの安全な保管](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#keeping-account-files-safe) · [トラブルシューティング](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#troubleshooting)

## 概要

| 現在お持ちのもの | 「**アカウントの追加**」タブ | また、以下も必要となります |
| --- | --- | --- |
| 電話番号およびログインコードへのアクセス | **電話** | 2FAが有効になっている場合のパスワード |
| 別のデバイスでTelegramが開かれている | **QRコード** | 2FAが有効になっている場合のパスワード |
| `.session`ファイル（TelethonまたはPyrogram） | **ファイル** | アプリ設定用のオプションのJSONファイル |
| `.session` + `.json`（同名） | **ファイル**（両方を選択してください） | 通常、これ以外の記載はありません |
| Telegram Desktopの`tdata`フォルダ | **ファイル**（ZIP形式） | デスクトップ版でローカルパスコードが設定されている場合 |
| Telethon StringSession（テキスト、`.txt`、`.tgwitness-session`） | **ファイル** | 別途APIペアは必要ありません |
| セッションまたは認証キーを持つ`.json` | **ファイル** | 別途APIペアは必要ありません |
| 認証キー（512 ヘックス文字）とその DC 番号 | **認証キー** | オプションのユーザーID |

TgWitnessは、ファイル名ではなく内容によってファイルを識別します。ファイル名を変更しても、 そのファイルが変換されることはありません。

## ご利用開始前に：API ID および API ハッシュ

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

代わりに独自のアプリケーションを使用する場合（登録したアカウントがリスクにさらされます。「 [なぜ組み込みのAPIプールなのか？](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)」をご参照ください）：

1. [my.telegram.org](https://my.telegram.org) を開き、ご自身が所有する任意の電話番号でログインしてください。 認証コードはSMSではなく、Telegramアプリに届きます。
2. **API開発ツール**をお選びください。
3. アプリケーションを作成します：タイトルと短縮名（5～32文字）を任意で指定し、プラットフォームは「**デスクトップ」を選択してください**。 URLと説明は空欄のままでも構いません。
4. **App api_id**（数値）と**App api_hash**（32文字の16進数）をコピーしてください。

パネル内のサインインフォームの下に、「**API ID + ハッシュ**」という項目があります。**API ID** に 1 組の `api_id:api_hash`ペアを貼り付けると、両方のフィールドに値が入力されます。1 組のペアを すべてのアカウントでご利用いただけます。ログインに成功すると、その情報は暗号化され、 そのワークスペース内にのみ保存され、ブラウザへ送信されることはありません。

これには3種類の認証情報が関係しています：

| Secret | 開く | 設置場所 |
| --- | --- | --- |
| パネルトークン | TgWitnessのウェブパネル | データディレクトリ内の`panel-token.txt`、または`TGWITNESS_TOKEN` |
| API ID + ハッシュ | これ単体では意味を成しません。アプリを特定するものです。 | my.telegram.org にて、組み込みのペア、インポートされた設定、またはご自身のアプリをご利用いただけます。 |
| アカウント認証 | Telegramアカウント | 電話またはQRコードによるログインで作成するか、セッションとして取り込むことができます。 |

Telegramにプロキシ経由で接続する必要がある場合は、まず「 **アカウント**」 **→「設定」→「接続設定」→「接続経路の変更」**で設定を行ってください。

## 電話番号

1. 「**アカウント**を開設」を選択し、「**電話」**タブで、国際形式の番号を入力してください。 例：`+44 7700 900123`。スペースやハイフンは自動的に削除されます。
2. **「続行」**をクリックしてください。API ID およびハッシュは空欄のままでも構いません。
3. Telegramから送信されるコードを入力してください（通常はTelegramアプリ宛てですが、SMSでの受信は保証されません）。
4. アカウントに二段階認証が設定されている場合は、そのパスワードを入力してください。これはパネル トークンでも、デバイスのパスコードでもありません。
5. ログイン後に表示されるアカウントIDを確認し、ソースを選択してください。

ログインコードおよび2段階認証（2FA）のパスワードは、ディスクに書き込まれることはありません。

## QRコード

この機能は、アカウントがすでにスマートフォンや別のコンピュータでログインされている場合に使用してください。

1. **「QRコード」**タブ → **QRコードを表示します**。API ID および ハッシュは空欄のままでも構いません。
2. ログイン済みのデバイスで：**[設定] → [デバイス] → [デスクトップデバイスをリンク]** を選択し、コードをスキャンして 確認してください。
3. Telegramから要求があった場合は、TgWitnessに2FAパスワードを入力してください。

QRコード画像はローカルで生成されます。コードには有効期限があります。**「別のQRコードを生成」** を押して、再試行してください。パネルをロックしたり、ワークスペースを切り替えたり、別のログインを開始したりすると、 生成中のコードはキャンセルされます。

## 認証キー + DC ID

認証キー（Auth Key）とは、すべてのTelegramセッションの基盤となる256バイトの認証情報であり、 512文字の16進数で表記され、データセンター番号DC 1～5が併記されています。

1. 「**Auth key**」タブ。キーをすべて貼り付けてください。「`…`」を含む短縮されたキーでは機能しません。
2. キーとともに提供されたDC IDを選択してください。
3. 必要に応じて**ユーザーID**を入力してください。Telegramが 異なるアカウントであると報告した場合、TgWitnessは接続を拒否します。
4. Press **Connectアカウント**。

認証キー（512文字）は、APIハッシュ（32文字）とは異なります。同じキーは JSON形式でもインポート可能です。「[アカウントJSON](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#account-json)」をご参照ください。

## アカウントファイル

**「アカウントを追加」→「ファイル」**を開き、**1つのアカウントに属するファイルを**最大4つ（合計8 **MiBまで**）選択し、「**アカウントを接続**」を押してください。

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- ファイルは、TgWitnessサーバー上の**メモリ内で**変換されます。アップロードされたデータは保存されず、 ZIPファイルはディスクに解凍されず、外部サービスへの接続も行われません。
- 生成されたセッションは、その後Telegramで照合されます。ファイルにユーザーIDが記載されている場合、 そのIDはTelegramが報告するアカウントと一致している必要があります。
- 異なるアカウントや異なるAPI認証情報を記述したファイルは、 いずれか1つを選択する代わりに、拒否されます。
- **「パスコード」または「セッションテキスト」**には、TDataのローカルパスコードフィールドがあり、ここに StringSessionを貼り付けたり、**ログインせずにファイルを読み**込んだりすることができます（Telegramに 接続することなくフォームに入力できます）。

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Telethon `.session`

|  |  |
| --- | --- |
| 概要 | Telethonベースのツールが作成するSQLiteデータベース。例：`my_account.session` |
| 以下の組織から認められています | テーブル `sessions`（`dc_id`、`server_address`、`port`、`auth_key` を含む）および `version` = 7 または 8 |
| 要件 | 認証済みセッションの行がちょうど1つ。閉じた、完全なデータベースです。 |

まず、そのファイルを作成したプログラムを閉じてください。その隣に「`my_account.session-journal`」または 「`my_account.session-wal`」が存在する場合、データベースは確定されていません。元のクライアントを 適切に開いてから閉じてください。これらのサイドカーファイルを削除すると、破損したコピーが残ってしまう可能性があります。

### Pyrogram `.session`

|  |  |
| --- | --- |
| 概要 | Pyrogram ベースのツールが生成する SQLite データベース |
| 以下の組織から認められています | テーブル`sessions`（`dc_id`、`auth_key`、`test_mode`、`user_id`、`is_bot`を含む）；`version` = 2 または 3 |
| 要件 | 本番ネットワーク上での認証済み**ユーザー**セッションは1つまでです。ボットおよびテスト用DCのセッションは拒否されます。 |

保存されたユーザーIDは、ログイン時にTelegramと照合されます。

### セッションとJSONのペア

アカウントは、多くの場合、 `447700900123.session`や`447700900123.json`のように、同じ名前の2つのファイルとして配布されます。**両方を**一度に選択してください。

- JSONから、TgWitnessは`app_id`/`api_id`および`app_hash`/`api_hash`を使用するため、 通常、APIの認証情報を入力する必要はありません。
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TDataとは、Telegram Desktopアプリケーション（desktop.telegram.orgから入手できるクロスプラットフォーム アプリ）の`tdata`フォルダのことです。

| システム | デフォルトの`tdata`の場所 |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata`（ポータブル版Telegram：`Telegram.exe`の隣） |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

インポートするには：

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> これは、インポートされた`.session`ファイル、StringSessionテキスト、およびAuth Key HEXにも適用されます。 独自に作成された認証情報を持つ他のクライアントは、ログイン状態を維持できます。 [Telegramの「AUTH_KEY_DUPLICATED」に関するドキュメント](https://core.telegram.org/api/errors#406-not-acceptable)をご参照ください。

1. Telegram Desktopを完全に終了してください。
2. `tdata` から、以下の 2 つの**項目のみ**を含む ZIP ファイルを作成してください：

   - `key_datas`
   - その隣にある、末尾が「`s`」で終わる16文字のファイル（通常は「`D877F783D5D3EF8Cs`」）

   メディアキャッシュを含むフォルダ全体をZIP形式で圧縮すると、通常、制限を超過してしまいます （512エントリ、解凍後32 MiB）。 3. 「**ファイル**」からZIPファイルを選択してください。Telegram Desktopに**ローカルパスコード**が設定されている場合は、 まず「**パスコード」または**「**セッションテキスト**」欄に入力してください。これは2FAのパスワードではありません。

対応機能：アーカイブごとに1つのアカウント、最新の`key_datas`/`key_data0`/`key_data1`ストレージ、 ローカルパスコード。非対応機能：複数のアカウントがログインしているフォルダ、旧式のデスクトップ レイアウト、パスワードで保護されたZIPファイル、および独立したmacOSネイティブアプリ「Telegram for macOS」。

### Telethon StringSession

通常、`1`で始まり、長さが約350文字の1行のテキストです。これを `.txt`または`.tgwitness-session`ファイル（最大4 KiB）として読み込むか、 **「パスコード」または「セッションテキスト」**欄に貼り付けてください。Telethon形式の文字列のみが受け入れられます。PyrogramおよびTDLibの 文字列は異なる形式を使用しています。

### アカウントのJSON

**`.json`** で終わるファイル内に、最大 **64 KiB** の JSON オブジェクトが 1 つ含まれています。

| フィールド（別名） | 意味 |
| --- | --- |
| `api_id` (`app_id`) | アプリケーションID（正の整数） |
| `api_hash` (`app_hash`) | アプリケーションハッシュ（32文字の16進数） |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Telethon StringSessionのテキストであり、ファイル名ではありません。 |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512文字の認証キー（Auth Key）およびDC 1～5をすべてご入力ください |
| `user_id` (`id`) | オプション：認証情報が保存される前に、Telegramとの照合が行われます |
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

最初の例では、API認証情報のみを入力します。電話番号またはQRコードでログインするか、セッション ファイルを追加してください。一括リスト（アカウントのJSON配列）は受け付けられません。

## お手持ちのものを特定する

| ご覧の通り | これは | 使用方法 |
| --- | --- | --- |
| `*.session`；テキストエディタで開くと、先頭に `SQLite format 3` と表示されます | Telethon または Pyrogram SQLite | **ファイル**（自動検出） |
| `tdata`フォルダには`key_datas`が含まれています | Telegram Desktop TData | 2つのファイルをZIP形式で圧縮し、次に「**ファイル」へ** |
| `1` で始まる 1 行のテキスト、約 350 文字 | Telethon StringSession | **ファイル** |
| `*.json`、`app_id`、`app_hash` | 関連メタデータ | **ファイル**およびそのセッション |
| `*.json` と `auth_key` または `string_session` | アカウントのJSON | **ファイル** |
| 512文字 `0-9a-f` | 認証キー | **認証キー** |
| 32文字 `0-9a-f` | APIハッシュ | **API ID + ハッシュ** |
| TDLibアプリからの`td.binlog`または`db.sqlite` | TDLib ストレージ | 未対応 |
| `123456789:AA…` | ボットトークン | 未対応 |

## サポートされていない形式

| フォーマット | 代替案 |
| --- | --- |
| TDLib ストレージ (`td.binlog`) および TDLib エクスポート | 電話番号またはQRコードでログインしてください |
| Pyrogramのセッション**文字列** | Pyrogramの`.session`ファイル、または携帯電話／QRコードをご利用ください。 |
| 複数のアカウントでログインした状態のTData | Telegram Desktopで他のアカウントからログアウトするか、各アカウント専用のセッションファイルをご利用ください |
| ボットトークン | 対応していない機能：TgWitnessはユーザーアカウントとして監視を行います |
| 多数のアカウントのCSV/JSONリスト | **アカウント → アカウントのインポート**からサポートされているセッションファイルをインポートするか、個別のワークスペースで電話番号やQRコードを使ってサインインします |
| Test-DC またはボットセッション | 本番環境のユーザーアカウントを使用してください |

## 複数のアカウント

アカウント選択ボタンの横にある「**+**」を押すか、 「**アカウント」→「設定」→「接続設定」→「ワークスペース」**を開き、ラベルを入力して サインインしてください。

- メインワークスペースを含め、ワークスペースの数に制限はありません。各ワークスペースには、独自のセッション、プロキシ ルート、情報源、キャプチャポリシー、ジャーナル、署名鍵、チェックポイント、およびエクスポート設定があります。
- 表示されているワークスペースを切り替えても、他のワークスペースは一時停止されません。
- ジャーナルは、それを作成したアカウントに紐付けられたままとなります。別の アカウントでログインするには別のワークスペースが必要となり、1つのアカウントを2つの ワークスペースに割り当てることはできません。
- メインパネルのトークンにより、すべてのワークスペースを管理します。[付与されたアクセス権限](https://phishdestroy.github.io/TgWitness/ja/docs/reference/access/)により、他のユーザーを特定のアカウントやチャットに限定し、個別の権限やセッション制限を設定することができます。
- **アカウントは**ワークスペースの名前を変更したり、追加されたワークスペースを、そのセッション、ジャーナル、 ソース、および署名鍵とともに削除したりします。メインのワークスペースはパネルから削除することはできません。

### 一括インポートとアカウントグループ

**「アカウント」→「アカウントのインポート」**を使用して複数のアカウントを追加し、ベース名でファイルを紐付け、 各ログイン結果を確認できます。各アカウントには独自のワークスペースが割り当てられます。

グループは、関連するアカウントをまとめて管理しますが、セッション、鍵、 証拠は統合されません。**「Accounts**」の**「グループ」を開くと**、そのページが表示されます。 `/groups/<id>`:

- **アカウント:**各メンバーの接続経路、観察内容、最後のメッセージが表示され、 「**すべて**開始」および「**すべて一時停止」**の機能があります。
- **要確認:**ログアウトされたアカウント、利用できないアカウント、または 接続、取り込み、ソース、メディアに問題があるアカウント。各名称をクリックすると、そのカードが表示されます。
- **複数のアカウントが閲覧できるチャットには、** 共有ソース、それらを閲覧しているアカウント、および 利用可能なワークスペースの閲覧期間（最大7日間）における中断が表示されます。**N個のアカウントでのエクスポートでは** 、チャンネルまたはスーパーグループのエクスポートが各アカウントに分割され、1つのアーカイブに署名されます。
- **グループのエクスポート:**各アカウントの署名付きエクスポートが以下に格納された1つのZIP `accounts/` 、 `manifest.json` 各アカウントのSHA-256およびキーのフィンガープリントを列挙し、メイン ワークスペースによって `manifest.signature.json`。各アカウントのアーカイブは、 `python -m tgwitness.verify` およびそのアカウントの信頼済みフィンガープリントを使用して、各アカウントのアーカイブを個別に検証してください。

メンバーはグループの設定を共有しますが、各アカウントは独自の設定値を保持することもできます。 [共有設定](https://phishdestroy.github.io/TgWitness/ja/docs/reference/settings/#account-groups)、 [インポートおよびグループのガイド](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings)、 ならびに[MTProxyプールダッシュボード](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources)をご覧ください。

## ログアウト

「アカウント」→「Telegramからログアウト（監視を一時停止）」を選択すると、Telegramにセッションの終了が要求されます。 これにより、アカウントの「設定」→「デバイス」からもそのセッションが消え、ワークスペースの保管庫からも セッションが削除されます。ジャーナル、ソース、設定、および署名鍵は残され、 ジャーナルにはログアウトの記録が残ります。 ワークスペースは引き続きそのアカウントに属しており、 そのアカウントのみが再度接続できます。Telegramから応答がない場合でも、セッションは ここから削除され、パネルにその旨が表示されます。Telegramの「設定」→「デバイス」からセッションを終了してください。

## アカウントファイルの安全な保管

- `.session`、TData ZIP、StringSession、認証キー、およびアカウントのJSONはすべて、 パスワードと同様に扱ってください。TgWitnessは、インポートされた認証情報を暗号化された保管庫に保存します。そのため、 その後、元のファイルを削除しても問題ありません。
- 同じ認証情報を2つのプログラムで同時に実行しないでください。Telegramによって認証情報が無効化される可能性があります （`AUTH_KEY_DUPLICATED`）、その結果、両方のプログラムが動作しなくなります。
- 有効期限が切れた、または取り消されたセッションは、変換によって復活させることはできません。再度ログインしてください。

## トラブルシューティング

| メッセージまたは現象 | 手順 |
| --- | --- |
| *このセッションを読み取ることができません。元のクライアントを閉じてください…* | SQLiteファイルが開かれているか、未完了の状態です（`-journal`／`-wal`サイドカー）。元のプログラムを正常に終了させてから、ファイルを再度コピーしてください。 |
| *対応しているTelethon SQLiteスキーマ：7および8* / *Pyrogram … 2 および 3* | このファイルは、非常に古い、あるいは不明なライブラリのバージョンで作成されました。代わりに、電話またはQRコードでログインしてください。 |
| *サポート対象となるのは、承認された本番環境のユーザーセッションのみです。* | このPyrogramファイルは、ボットまたはテストネットワークに属するものです。 |
| *TDataアーカイブのエントリ数が512件、または32 MiBを超えています* | ZIPファイルは`key_datas`および`D877F783D5D3EF8Cs`のみとし、フォルダ全体は含めないでください。 |
| *TDataを復号できません。デスクトップのローカルパスコードをご確認ください。* | 「**パスコード」または「セッションテキスト」**の欄に、Telegram Desktopのローカルパスコードを入力してください。 |
| *TDataアカウントは一度に1つずつインポートしてください* | Telegram Desktopには複数のアカウントがありました。「[サポートされていない形式」](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#unsupported-formats)をご覧ください。 |
| *選択されたファイルには、さまざまなアカウントやAPI認証情報が記載されています。* | 1つのアカウントのファイルのみを選択してください。 |
| *JSONには、サポートされているAPIの認証情報や承認情報が含まれていません* | [アカウントのJSON](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#account-json)内のフィールド名をご確認ください。 |
| *APIメタデータのみ* | このJSONにはセッションが含まれていません。「`.session`」ファイルを追加するか、電話番号またはQRコードをご利用ください。 |
| *Auth Key HEXには、512文字の16進数文字すべてが含まれている必要があります* | キーが切り詰められているか、`…`が含まれています。 |
| アカウントIDがインポートされたアカウントと一致しません | このファイルのユーザーIDは、Telegramが報告しているものとは異なります。このファイルは別のアカウントのものです。 |
| このアカウントはすでに別のワークスペースに属しています | アカウントを2回追加するのではなく、そのワークスペースを開いてください。 |
| 接続されていますが、「**ソース**」のチャットリストに非公開グループが欠落しています。 | メンバーシップをご確認ください。ピッカーは最初の1,000件のダイアログを検査します。制限数は「**パラメータ**」で変更できます。 |
| プロキシ接続に失敗しました | ルートとIPモードを確認してください。自動MTProxyは、動作する別のエントリを試行します。「アドレスを非表示」は待機状態となり、「Direct」は最後の手段として、設定された遅延時間の後に直接接続を試みます。[ルーティングモード](https://phishdestroy.github.io/TgWitness/ja/docs/reference/connection/#ip-modes)を参照してください。 |

関連項目：プロキシおよび暗号化に関する[接続とセキュリティ](https://phishdestroy.github.io/TgWitness/ja/docs/reference/connection/)、 およびログイン後に収集されるデータの[収集方法について](https://phishdestroy.github.io/TgWitness/ja/docs/reference/collection/)。
