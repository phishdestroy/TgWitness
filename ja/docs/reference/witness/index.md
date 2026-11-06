# 独立した証人

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/

独自の鍵とボットを使用してWitnessを実行し、署名済みのチェックポイントをチャンネルに公開し、エクスポートしたデータと照合してください。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [ドキュメント](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[エクスポートと検証](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/) · [高信頼性](https://phishdestroy.github.io/TgWitness/ja/docs/reference/high-assurance/) · [パネルガイド](https://phishdestroy.github.io/TgWitness/ja/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

フローチャート · コレクター → Witness (署名付きチェックポイント：記録数 + 先頭ハッシュ); Witness → Witnessジャーナル、独自の鍵; Witness → Telegramチャンネル (独自のボットを介して署名付きで投稿されました); 証拠 ZIP → verify.py; Witnessジャーナル、独自の鍵 → verify.py; Telegramチャンネル → verify.py (Telegram Desktopからのエクスポート、または「t.me/s」ページ) · コレクター · Witness · Witnessジャーナル、独自の鍵 · Telegramチャンネル · 証拠 ZIP · verify.py · 署名付きチェックポイント：記 · 録数 + 先頭ハッシュ · 独自のボットを介して署名付き · で投稿されました · Telegram · Desktopからのエクスポート、 · または「t.me/s」ページ

**図表をテキストで記述**

1. コレクター → Witness (署名付きチェックポイント：記録数 + 先頭ハッシュ)
2. Witness → Witnessジャーナル、独自の鍵
3. Witness → Telegramチャンネル (独自のボットを介して署名付きで投稿されました)
4. 証拠 ZIP → verify.py
5. Witnessジャーナル、独自の鍵 → verify.py
6. Telegramチャンネル → verify.py (Telegram Desktopからのエクスポート、または「t.me/s」ページ)

**On this page**

- [What the witness gets, and what it does not](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [What it checks and records](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/#what-it-checks-and-records)
- [Run a witness](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/#run-a-witness)
- [Public proof page for several workspaces](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Verify](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/#verify)

## TgWitnessが提供するもの、および提供しないもの

| Witnessには | このツールには決して |
| --- | --- |
| 1つのワークスペース用の読み取り専用**ウィットネストークン** | コレクターのTelegramセッションまたはAPI認証情報 |
| 独自のEd25519鍵とジャーナル | コレクターの保管庫、署名鍵、またはパネルトークン |
| 独自のTelegramボットトークン | メッセージの内容：ヘッダーには記録件数とハッシュ値が含まれます |

トークンは**追加情報 → 独立した証人**で生成され、一度だけ表示された後、 SHA-256としてのみ保存されます。これは正確に1つのエンドポイントを開き、 `GET /api/witness/head`、そこからは新たに 署名されたチェックポイントに加え、署名済みのコンテンツを含まないコレクションカウンターおよび運用状態が返されます。 このトークンではパネルを開いたり、メッセージの内容を読み取ったり、設定を変更したりすることはできず、 パネルトークンもここでは受け入れられません。トークンの無効化は同じページで行えます。コレクターは 新しいウィットネスキーがチェックを開始した時刻を記録し（`witness.seen`) を記録し、トークンごとの最後のチェックを表示します。 2.5 インターバル以内にチェックを行っていないウィットネスは、期限切れとしてマークされます。

新しいウィットネスは、 各ポーリングごとにランダムなチャレンジを送信します。キャプチャステートメントは、コレクターの署名の下でそれを反映します。カウンターは 正確なチェックポイントに紐付けられており、署名付きウィットネス投稿に含まれます。レガシーヘッドは スタンドアロンのウィットネスによって引き続き受け入れられます。ジャーナルの増分のみは、決して新しいメッセージとしてカウントされることはありません。

## チェックおよび記録の対象

一定の間隔（デフォルトでは10分ごと）ごとに、witnessは以下の処理を行います：

1. ヘッド自体を取得します（コレクターはこれをプッシュしたりスキップしたりすることはできません）；
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
3. 自身のジャーナルに署名付きレコードを追加します：`witness.anchor`（ステータス：`ok`、 `key_changed`、`rollback`（以前よりレコード数が少ない）、`fork`（長さは同じですが、 ヘッダーが異なる）、または`invalid`（検証に失敗した）、あるいは`witness.no_response`（ コレクターが応答しなかった場合））；
4. TgWitnessが 稼働中でBot APIにアクセス可能な間は、「no answer」を含め、署名付きの結果をチャンネルに投稿します。投稿ID（`witness.posted`）が記録され、 投稿に失敗した場合も同様に記録されます（`witness.post_failed`）。

投稿は次のような形式になります。最後の行には署名付きの記述が含まれています：

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## witnessを実行する

Telegramボット（@BotFatherで作成してください）、そのボットが 管理者となっているチャンネル、および証人からアクセス可能なコレクターのアドレス（プライベートネットワーク外で HTTPS経由）が必要となります（[導入手順の](https://phishdestroy.github.io/TgWitness/ja/docs/reference/deployment/)「HTTPSプロファイル」を参照してください）。

パネルで **[Extras] → [Independent witness] → [Configure]** を開きます。3つのステップで、 読み取り専用アクセス、チャンネルと間隔の設定、そしてウィットネスの起動を行います。公開 ポリシー、オプションのHTTP/SOCKS5プロキシ、およびカスタムBot APIアドレスは、[**Advanced settings**] にあります。このフォームを ダウンロードすると `witness.json` 。新しく 作成された読み取り専用トークンを「**アクセスファイルを次のように保存**」でダウンロードし `witness-token.txt`」を選択して、新しく作成された読み取り専用トークンをダウンロードし、そのJSONの横に `bot-token.txt`ウィットネスホスト上で生成されたものを、そのJSONファイルの隣に配置してください。コレクターはボットトークンを受け取ることはありません。 ダウンロードを行っても、サービスの起動やメッセージの公開は行われません。ホストされたプロジェクトのウィットネスは 暗黙的に登録されることはありません。

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

最初のコマンドは、ネットワークリクエストや鍵の 生成を行わずに、設定ファイルと秘密ファイルを確認します。JSON内のパスはそのファイルを基準とした相対パスであり、CLI/環境のパスは 作業ディレクトリを基準とした相対パスです。 ウィットネスのフィンガープリントは、ホストの外に保持してください。コレクターの 「last-poll」インジケーターはリクエストの確認のみを行います。公開については、Proof によって報告されるか、 ウィットネス・ジャーナルおよびチャンネルで確認してください。

パネルがSSHトンネルの背後に配置されている場合は、[このCaddyの例](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example)に従い、 別のHTTPSホスト名上で、スコープが限定されたwitnessエンドポイントのみを公開してください。 その場合、デフォルトのワークスペースでは`https://witness.example.org`が使用され、その他のワークスペースでは `https://witness.example.org/profiles/ID`が使用されます。トークンは引き続き必要となります。パネルおよびその その他のAPIルートは、その仮想ホストによって転送されません。

定期的にチェックポイントが公開される設定には「`all`」をお選びください。5分間隔の場合、ワークスペース1つあたり1日約288件の 投稿となります。「`changes`」および「`problems`」では、一部のチェックポイントを意図的に非公開としています。 MTProxyは、コレクター側のTelegramクライアント用です。WitnessのHTTPポーリングおよびTelegramのHTTPS Bot APIは、それぞれ独自のダイレクト/HTTP/SOCKS5ルート（[Bot API](https://core.telegram.org/bots/api)）を使用します。

**コレクターの隣に、Docker を使用して**（同じホスト上で — 独立したプロセスとキーですが、 オペレーターは同じです）：`.env` に値を入力し、プロファイルを起動してください。

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

掲載されている画像を使用する場合は、`docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d` をご使用ください。

**他者のサーバー**（真に独立した証人）**上で**：リポジトリをそこにコピーし、 `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` に上記の3つの値を `.env` に設定してから、

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

または、Docker を使用しない場合：

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Discordに公開する

ウィットネスは、Telegramの代わりにDiscordチャンネルに投稿することもできます。Discordで、 **「チャンネルの編集」→「統合」→「Webhook**」を開き、Webhookを作成してそのURLをコピーします。 パネル内のステップ2で、**「Discord Webhook・あなたのチャンネル」**を選択します。ウィットネスホスト上で、 そのURLを `discord-webhook.txt` の横に `witness.json`の横に保存してください。このURLは コレクターには決して送信されません。

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

「ウィットネス」には、TelegramチャンネルまたはDiscordウェブフックのいずれか1つを「パブリッシャー」として設定します（両方を設定することはできません）。投稿には 同じ署名付きステートメントが含まれ、誰にも「ping」を送ることはできません。Discordの 2,000文字を超える投稿は、短い一行のテキストに置き換えられ、完全なチェックが `witness-check.txt`。各投稿IDは `witness.posted`. `verify.py --channel`Telegramチャンネルのエクスポートデータのみを読み取るため、Discordの場合はウィットネス・ジャーナルを保管してください。そこには すべてのチェックが記録されています。

### オプション

| オプション | 環境 | デフォルト | 意味 |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | チェック間隔（分）：1～1440 |
| `--timeout` | `_TIMEOUT` | 30 | コレクターおよびBot APIの応答待ち時間は数秒、5～600 |
| `--post` | `_POST` | `all` | `all`：すべてのチェック；`changes`：新たな課題または問題；`problems`：問題と未回答のみ |
| `--title` | `_TITLE` | `TgWitness witness` | 各チャンネルの投稿の冒頭部分 |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | 最初の回答を鵜呑みにするのではなく、コレクターキーを固定してください |
| `--proxy` | `_PROXY` | 直接 | `socks5://host:port` または `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Bot APIのアドレス（例：ローカルのBot APIサーバー） |
| `--data-dir` | `_DATA` | `witness-data` | Witnessキーとジャーナル |
| `--config` | `_CONFIG` | – | 上記のいずれかのオプションを含むJSONファイル |

コレクターアドレス、トークン、チャンネルは以下から取得されます `--collector`, `--token` または `--token-file`, `--bot-token` または `--bot-token-file`, `--discord-webhook-file` および `--channel`、 または `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` および `_CHANNEL`、これにより、プロセス一覧から秘密情報が除外されます。

設定ファイルでは、アンダースコア付きのオプション名に加え、`texts` を使用します。これは、 チャンネルの投稿文を置き換えるものです：

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts`キー：`ok`、`key_changed`、`rollback`、`fork`、`invalid`、`no_response`、`collector`、 `records`、`head`。コマンドラインは環境変数に優先し、環境変数はファイルに優先します。 未知のオプションやテキストキーは、無視されるのではなく、メッセージを表示してwitnessを停止させます。 記述内容は検証結果に影響を与えません。verify.pyは、各投稿の最後に署名付きトークンを チェックします。 `--post changes`または`problems`では、投稿されなかったチェックも引き続き ウィットネス・ジャーナルに残っており、`verify.py`ではそれらが「未投稿」として一覧表示されます。開始レコードには ポリシー名が記載されています。すべてのチェックは依然としてジャーナルに表示されるため、投稿回数が減っても、独立した Telegramの送信回数が減るだけで、チェックの数が減るわけではありません。

チャンネルがなくても、Witnessは引き続きジャーナルを保持します。Witnessのキーフィンガープリント （`python -m tgwitness.witness fingerprint`）は別の場所に保管してください。

## 複数のワークスペースの公開証明ページ

`python -m tgwitness.proof` witnessesは一度に最大32のワークスペースを管理し、各ワークスペースの最新の署名済みチェック結果を 読み取り専用ページとして提供します。各ワークスペースには、dataフォルダ内に独自のwitnessキーと ジャーナル、および固定されたコレクターキーが割り当てられます。Telegramチャンネルへの投稿は、 ワークスペースごとに任意です。まずは [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example)から始めてください：

| 分野 | 意味 |
| --- | --- |
| `title` | ページタイトル（1～100文字） |
| `data_dir` | ファイルに関連付けられたWitnessの鍵とジャーナル。デフォルト `proof-data` |
| `interval`, `timeout` | チェック間隔（分単位：1～1440、デフォルトは5）；待機時間（秒単位：5～600、デフォルトは20） |
| `workspaces[].id`, `label` | 短い小文字のエイリアスと表示名 |
| `workspaces[].collector` | コレクターのアドレス。その他のワークスペースは「」で終わります。 `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | 必須。ワークスペースごとに異なります。 |
| `workspaces[].token_file` | そのワークスペースの読み取り専用ウィットネストークンを含むファイル |
| `workspaces[].channel`, `bot_token_file` | オプション：各チェック結果をチャンネルに投稿する |
| `workspaces[].proxy`, `bot_api` | オプションのルートおよびBot APIアドレス |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

最初のコマンドは、接続を開くことなくファイルとトークンファイルの有効性を検証します。 このページは GET および HEAD メソッドのみに応答します：

- `/` すべてのワークスペースが表示されます。2.5 インターバルの間、チェックが入っていないワークスペースは「stale（古くなった）」とマークされます。
- `/api/proof` JSONと同じ内容を返します。
- `/api/proof/<id>` 最新の署名付きステートメントをダウンロードします（`tgwitness-public-proof-v1`）： ウィットネス記録番号とハッシュ、ステータス、固定されたコレクターキー、チェックポイント、収集 カウンター、およびチャンネルへの投稿が成功したかどうか。これらは、そのワークスペースのウィットネスキーによって署名されています。
- `/healthz` ワークスペースのモニターが停止すると、503エラーが返されます。

[Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example) のように、ページに独自のホスト名を割り当ててください。検証のために、 ワークスペースのウィットネス・ジャーナルを `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` でエクスポートし、 以下に説明する通りに使用してください。

## 検証

証人側では、そのジャーナルをエクスポートします：

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

その後、どこからでも、コレクターの署名付きZIPファイルと、Telegram Desktopからエクスポートしたチャンネル（*「チャット履歴のエクスポート」* →「JSON」を選択すると`result.json` が生成されます）またはその公開`https://t.me/s/…` ページを使用して：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py`は、ウィットネス・ジャーナル（チェーンと署名）を確認した後、 **ウィットネスが検知したすべてのヘッドがエクスポートされたジャーナルに含まれているかを**検証します。つまり、そのカウントにおける記録には、 正確にそのハッシュが含まれている必要があります。一致しないヘッドがある場合、検証に失敗します。これは、 ウィットネスが検知した後、ジャーナルが変更されたことを意味します。 また、エクスポート後に確認されたヘッダー、証人が 記録した異常、検証に失敗した回答、この エクスポート内に一致するチェックポイントが存在する期間（「XからYまで証人確認済み」）、およびギャップについても報告します。それ以降のチェックポイントは、これらの期間を延長するものではありません。 結果には、最後に一致したレコード番号と、一致するチェックポイントのない 末尾のレコード数が含まれます。エクスポート自身の鍵で署名された回答のみがカウントされます。証人が 一度も確認したことのない鍵で署名されたエクスポートは「未確認」として報告され、`--fingerprint`がなければ、その 署名者は未固定のままとなります。 `--channel` では、署名されたすべての投稿が、証人ジャーナルと レコードごとに一致する必要があります。変更された投稿は検証に失敗し、欠落している投稿は一覧表示されます。提供された Telegram JSON エクスポート内の日付は、署名された証人トークンの範囲外にある編集可能なメタデータです。 トークンが一致しても公開日は認証されません。結果には、公開時刻の検証が 行われなかったことが明示的に報告されます。

### 証人付きエクスポートの境界が必要です

立会人の立会いのもとで作成された最終記録を含める必要がある引き継ぎの際は、`--require-witness`を追加してください：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

これには、独立して保持されている「ウィットネス・フィンガープリント」と、このエクスポートの 正確な末尾にある一致するチェックポイントが必要です。より前のプレフィックスのみを カバーするチェックポイントでは不十分です。収集を一時停止し、ウィットネスに最終状態を 確認させた上で、ジャーナルへのさらなる書き込みが行われる前にエクスポートを行ってください。ジャーナルが変更された場合は、別のチェックポイントを保持し、 その状態をエクスポートしてください。 後のチェックポイントだけでは、より短いエクスポートの最終ハッシュを検証することはできません。 `--channel`も指定されている場合、主張された投稿の欠落や空のマッチセットは、この 厳格なチェックに失敗します。このフラグがない場合でも、通常の整合性チェックでは、 アーカイブ自体が破損していないにもかかわらず、証人による検証が行われていない レコードが報告されます。

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
