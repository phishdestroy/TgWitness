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

Telegram APIアプリケーションを作成しなくてもログインできます。ペアが入力されていない場合、 インポートされていない場合、またはワークスペースにすでに保存されていない場合、TgWitnessは組み込みの 50組の公開APIペア（`tgwitness/api_pool.py`）のプールからランダムな順序でペアを選択します。 Telegramがペアを拒否した場合 （`API_ID_INVALID`、`API_ID_PUBLISHED_FLOOD`、`UPDATE_APP_TO_LOGIN`）、次のペアが試され、 1回のサインインにつき最大8つまで試行されます。拒否されたペアは、再起動されるまでスキップされます。サインインに使用されたペアは アカウントとともに保存され、そのアカウントで再利用されます。**API** IDと**APIハッシュ**は、Telegramに対してアプリケーションを識別するものであり、 それ自体ではアカウントの認証を行いません。

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

- ファイルは、TgWitnessサーバー上の**メモリ内で**変換されます。アップロードされたデータは保存されず、 ZIPファイルはディスクに解凍されず、外部サービスへの接続も行われません。
- 生成されたセッションは、その後Telegramで照合されます。ファイルにユーザーIDが記載されている場合、 そのIDはTelegramが報告するアカウントと一致している必要があります。
- 異なるアカウントや異なるAPI認証情報を記述したファイルは、 いずれか1つを選択する代わりに、拒否されます。
- **「パスコード」または「セッションテキスト」**には、TDataのローカルパスコードフィールドがあり、ここに StringSessionを貼り付けたり、**ログインせずにファイルを読み**込んだりすることができます（Telegramに 接続することなくフォームに入力できます）。

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
- `phone`、`device`、`sdk`、`app_version`、`lang_pack`、または保存済みの `twoFA`パスワードなどの他のフィールドは**無視**されます。アカウントに2FAが設定されている場合、TgWitnessは2FAの入力を求めます。
- JSONファイル単体では、単なるメタデータに過ぎません。セッションファイルがない場合は、携帯電話 またはQRコードによるログインを続行してください。

### Telegram Desktop (TData)

TDataとは、Telegram Desktopアプリケーション（desktop.telegram.orgから入手できるクロスプラットフォーム アプリ）の`tdata`フォルダのことです。

| システム | デフォルトの`tdata`の場所 |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata`（ポータブル版Telegram：`Telegram.exe`の隣） |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

インポートするには：

> **並行セッションに関する警告です。**TDataをインポートすると、Telegram Desktopの認証 キーが再利用されます。独立したログインが作成されるわけではありません。そのキーをDesktopと TgWitnessで同時に使用しないでください。Telegramは`AUTH_KEY_DUPLICATED`を使用して認証を無効化することがあり、 その場合、新しいログインを行うまで両方のコピーが使用できなくなります。
>
>
>
> デスクトップ版を、トレイプロセスを含めて完全に終了し、 TgWitnessがインポートされたセッションを使用している間は、そのインスタンスを閉じたままにしておいてください。 **終了してください。ログアウトしたり、セッションを取り消したりしないでください。** セッションの取り消しは、インポートされたコピーも無効にしてしまいます。両方のクライアントを実行する必要がある場合は、 携帯電話またはQRコードでTgWitnessにサインインし、独自の認証を作成してください。専用の アカウントの使用をお勧めしますが、クローンされたキーを並行して使用しても安全であるとは限りません。
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
| `string_session` (`session_string`, `session`) | Telethon StringSessionのテキストであり、ファイル名ではありません。 |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512文字の認証キー（Auth Key）およびDC 1～5をすべてご入力ください |
| `user_id` (`id`) | オプション：認証情報が保存される前に、Telegramとの照合が行われます |

別名と本名の両方が記載されている場合は、それらが一致している必要があります。例：

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
| 多数のアカウントのCSV/JSONリスト | アカウントごとに1つのワークスペースを追加してください |
| Test-DC またはボットセッション | 本番環境のユーザーアカウントを使用してください |

## 複数のアカウント

アカウント選択ボタンの横にある「**+**」を押すか、 「**アカウント」→「設定」→「接続設定」→「ワークスペース」**を開き、ラベルを入力して サインインしてください。

- メインワークスペースを含め、ワークスペースの数に制限はありません。各ワークスペースには、独自のセッション、プロキシ ルート、情報源、キャプチャポリシー、ジャーナル、署名鍵、チェックポイント、およびエクスポート設定があります。
- 表示されているワークスペースを切り替えても、他のワークスペースは一時停止されません。
- ジャーナルは、それを作成したアカウントに紐付けられたままとなります。別の アカウントでログインするには別のワークスペースが必要となり、1つのアカウントを2つの ワークスペースに割り当てることはできません。
- メインパネルのトークンにより、すべてのワークスペースを管理します。[付与されたアクセス権限](https://phishdestroy.github.io/TgWitness/ja/docs/reference/access/)により、他のユーザーを特定のアカウントやチャットに限定し、個別の権限やセッション制限を設定することができます。
- **アカウントは**ワークスペースの名前を変更したり、追加されたワークスペースを、そのセッション、ジャーナル、 ソース、および署名鍵とともに削除したりします。メインのワークスペースはパネルから削除することはできません。

## ログアウト

「アカウント」→「Telegramからログアウト（監視を一時停止）」を選択すると、Telegramにセッションの終了が要求されます。 これにより、アカウントの「設定」→「デバイス」からもそのセッションが消え、ワークスペースの保管庫からも セッションが削除されます。ジャーナル、ソース、設定、および署名鍵は残され、 ジャーナルにはログアウトの記録が残ります。 ワークスペースは引き続きそのアカウントに属しており、 そのアカウントのみが再度接続できます。Telegramから応答がない場合でも、セッションは ここから削除され、パネルにその旨が表示されます。Telegramの「設定」→「デバイス」からセッションを終了してください。

## テレソンセッションをオフラインで変換する

このパネルは、`.session`ファイルを直接インポートします。オフラインで StringSessionファイルに変換するには、プロジェクトフォルダから以下のコマンドを実行してください：

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

このコンバーターは、Telethon SQLite のみ（最大 64 MiB）を読み込み、入力データを一切変更せず、 ネットワークリクエストも行わず、既存の出力ファイルの上書きも拒否します。

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
| プロキシ接続に失敗しました | ルーティングモードとIPモードをご確認ください。自動MTProxyは、別の有効なエントリを試行します。IP非表示モードは待機し、明示的に選択されたフォールバックモードは、設定された遅延時間が経過した後、直接接続できます。[ルーティングモードについては](https://phishdestroy.github.io/TgWitness/ja/docs/reference/connection/#ip-modes)こちらをご覧ください。 |

関連項目：プロキシおよび暗号化に関する[接続とセキュリティ](https://phishdestroy.github.io/TgWitness/ja/docs/reference/connection/)、 およびログイン後に収集されるデータの[収集方法について](https://phishdestroy.github.io/TgWitness/ja/docs/reference/collection/)。
