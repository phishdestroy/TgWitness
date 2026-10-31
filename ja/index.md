# メッセージは変化します。目にしたものを残しておきましょう。

Canonical page: https://phishdestroy.github.io/TgWitness/ja/

[オープンソース / v0.7.0](https://phishdestroy.github.io/TgWitness/ja/docs/reference/changelog/)

Telegramのメッセージをキャプチャし、その変更履歴を保存して、署名付きの記録をエクスポートします。

[デモ版を開く](https://phishdestroy.github.io/TgWitness/demo/?lang=ja)[セットアップガイド](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja)

デモでは架空のデータを使用しています。Telegramへのログインは不要です。

 [GitHub Actions で収集（プレビュー）](https://phishdestroy.github.io/TgWitness/ja/docs/capture/) [S3オフサイトコピー：セットアップと復旧](https://phishdestroy.github.io/TgWitness/ja/#s3)

時を越えるメッセージ #0042

Northstar · リサーチ架空の情報源／メッセージ 42

1. **観測されたメッセージ：**09:41:02

   ブリーフィングは14:00から始まります。
2. **編集履歴を保持**09:43:18

   ブリーフィングは15:00から始まります。

   以前のバージョンはそのまま残されています
3. **削除通知**10:06:45

   キャプチャされたコンテンツは、お客様のジャーナルに保存されます。

3つの観測。1つの履歴。例

メッセージは消えても、記録された履歴は残ります。

## 記録されたすべての変更。必要な場所に、すぐに。

架空のデモデータを使用して、インターフェースをご覧ください。

TgWitness / 保存されたチャットあなたの監視作業スペース

![ダークテーマで保存されたTelegramの会話履歴。編集履歴や削除されたメッセージも、文脈を損なうことなく記録されます。](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / 保存されたチャット メッセージの横に編集履歴や削除通知が表示される、見慣れた会話画面です。

TgWitness / ジャーナルローカルワークスペース

![観測されたメッセージ、編集、削除通知、およびカバレッジイベントを記録したジャーナル](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / ジャーナル アカウントで観測された内容（中断を含む）を検索可能なタイムラインとして表示します。

TgWitness / 編集履歴ローカルワークスペース

![メッセージのキャプチャされた以前のバージョンと編集後のバージョンを比較する詳細表示パネル](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / 編集履歴 以前の記録を上書きすることなく、キャプチャされたバージョンを比較できます。

TgWitness / 署名付きエクスポートローカルワークスペース

![ワークスペースのエクスポート機能により、署名付きのZIP、JSONL、CSV、およびオフライン用HTMLレポートを提供します。](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / 署名付きエクスポート マニフェストと独立した検証機関を伴うジャーナルを、いつでも持ち運べます。

01 / キャプチャ

### 範囲はお客様ご自身でお選びいただけます。

選択したチャット、Telegramのフォルダ、またはアカウント全体を対象とします。アカウントごとに独立したワークスペースが用意されています。

[収集モードの比較](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#scope)

02 / 保存

### 変更点は記事に追加されます。

キャプチャされたバージョン、削除通知、および観測の欠落部分は、ジャーナルに残ります。

[イベントマトリックス「」をご覧ください。](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#events)

03 / 引き渡し

### 移動する記録。

署名付きZIPファイル、保存されたファイル、およびオフラインレポート。オプションでパスワード保護も可能です。

[のエクスポートと検証](https://phishdestroy.github.io/TgWitness/ja/docs/exports/)

## 1バイトでも変更すれば、ブロックチェーンがそれを教えてくれます。

各イベントは前のハッシュへのリンクを持ち、Ed25519署名が付与されています。

![記録されたイベントは以前のハッシュ値にリンクされ、署名が付与され、検証可能な形式でエクスポートされます。](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![キャプチャされた記録を変更すると、そのハッシュが変更され、リンクされた記録の検証が不可能になります。](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![別途保存されたチェックポイントにより、受信者はエクスポートされたジャーナルと以前の記録を比較することができます。](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

各検証メカニズムが何を確立し、その限界がどこにあるのかをご確認ください。

[8つの証拠レベルをご覧ください](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#levels)

## 別の目によるチェックをお待ちしております。

観察結果、ファイル、およびオフラインのHTMLレポートを、1つの署名付きバンドルとして引き渡します。

[証拠モデル「」をご覧ください。](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/)

tgwitness-evidence.zip署名付きバンドル

- 01

  当初の所見JSONL形式の記録 + CSVテーブル
- 02

  読みやすい文脈オフラインHTMLレポート＋保存されたメディア
- 03

  独立した検証署名付きマニフェスト + スタンドアロン型検証ツール

署名は、信頼できる鍵を基準として改ざんを検出します。Telegramでの送信元であることを証明したり、完全な記録を保証したりするものではありません。ジャーナルの内容およびメディアは、ユーザー自身が用意する暗号化されたストレージに保存する必要があります。

## S3へのコピー。外部による検証。

暗号化されたコピーを保管し、独立した検証手段を追加してください。

デフォルトではオフになっています

### すべてをS3互換のストレージにコピーします

ジャーナル、ファイル、タイムスタンプ付きのチェックポイント、およびチャットのエクスポートデータは、AWS S3または互換性のあるストレージにアップロードされる前に暗号化されます。

**保存設定と復元**

クライアント側暗号化

`AES-256-GCM`は、このマシン上のオブジェクトを暗号化します。プロバイダーは暗号化されたオブジェクトを受信します。

定期的または手動でのコピー

今すぐコピーするか、1分から1,440分の間隔を選択してください。パネルで進行状況をご確認ください。

Object Lock

バケットが対応している場合は、保存期間とモードを選択してください。このパネルでは、アップロードされたオブジェクトについて保存が確認されたかどうかが表示されます。

検証済みの復元

暗号化キーをダウンロードし、別の場所に保管してください。別のマシンで復元してください。ファイルは検証が完了した後にのみ公開されます。

![オフサイトコピーに関する完全な説明パネル：エンドポイント、リージョン、バケット、アクセスキー、スケジュール、オブジェクトロック、および復旧キーの設定](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

高度なオプションを展開した完全なパネルです。ストレージの認証情報は表示されていません。

ジャーナルおよびメディア`AES-256-GCM`S3互換のストレージ

[S3の設定とコピーの復元](https://phishdestroy.github.io/TgWitness/ja/docs/exports/#s3)[検証の詳細はこちらをご覧ください](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#off-site-copy-and-restore-s3)

**以下の機能はありません**：エクスポートされた復号鍵がなければ復元することはできませんし、独立した証人の代わりとなるものでもありません。

### 通知 · Apprise

Appriseを介して、問題の通知、チャットの変更、および日次サマリーを、メッセンジャー、メール、またはご自身のJSON Webhookでお受け取りいただけます。

「抜粋」機能を有効にしない限り、メッセージ本文は送信されません。

 [通知先の設定](https://phishdestroy.github.io/TgWitness/ja/docs/reference/operations/#notifications)

### 外部タイムスタンプ

RFC 3161 および OpenTimestamps に基づくタイムスタンプ・チェックポイント・ハッシュ。

**行わないこと**：保留中のカレンダー受領を、確定したビットコインのタイムスタンプとして扱いません。

 [タイムスタンプの証明を確認する](https://phishdestroy.github.io/TgWitness/ja/docs/reference/timestamp/)

### 独立した証人

別のホストが署名付きの観測データを保管し、`TGW1`チェックポイントを公開することができます。

**行わないこと**：1つのコレクターホスト上に存在する2つのワークスペースを、独立したウィットネスとして扱いません。

 [Witnessのセットアップ](https://phishdestroy.github.io/TgWitness/ja/docs/witness/)

### 復元と明らかな欠落

再起動後に再開します。再確認と`coverage.json`により、復元されたメッセージと欠落箇所が表示されます。

**できないこと**：見逃された編集や消去されたメッセージをすべて復元することはできません。

 [連続性と欠落を確認する](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#continuity)

## 最初のワークスペースはここから始まります。

まずはデモをご覧ください。準備が整いましたら、専用のアカウントを接続してください。Windows、Linux、macOS、またはDockerに対応しています。

[セットアップガイド「」をご覧ください。](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja)

**インポートされたセッションは1つ、実行中のクライアントは1つです。**

インポートした TData/セッションキーを、Telegram Desktop と TgWitness で同時に実行しないでください。Telegram によって共有認証が無効化される可能性があります（AUTH_KEY_DUPLICATED）。並行して使用する場合は、電話番号または QR コードを使用して、別の TgWitness ログインを作成してください。

[セッションのインポートに関する警告をお読みください](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja#session-warning)

**接続する前に、ぜひご一読ください。**

Telegramアカウントがなくても、架空のワークスペースをお試しいただけます。

[オンラインデモを開く →](https://phishdestroy.github.io/TgWitness/demo/?lang=ja)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**ローカルインストール用コマンド**

ステップ 01

### ソースを入手する。

[ソースのZIPファイルをダウンロードして](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip)解凍するか、リポジトリをクローンしてください：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

ソースの起動には Python 3.11 以上が必要です。Windows ランチャーでは、Python がインストールされていない場合、インストールを行うことができます。

[リリースを閲覧する](https://github.com/phishdestroy/TgWitness/releases)

WindowsにPythonがインストールされていない場合は、[ポータブルパッケージをダウンロードし](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip)、解凍して「`TgWitness.cmd`」をダブルクリックしてください。

ステップ 02

### 実行方法をお選びください。

`Start.cmd` をダブルクリックするか、PowerShell で以下を実行してください：

```
.\Start.cmd
```

まずは試してみたいですか？「`scripts\Demo.cmd`」をダブルクリックすると、独立したデモ環境をご利用いただけます。Telegramへのログインは不要です。

Python 3.11 以降および `venv` が利用可能な場合：

```
sh start.sh
```

代わりに架空のジャーナルを開くには、`sh start.sh --demo` を実行してください。

Dockerが実行されており、Compose 2.20以上がインストールされている場合：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

2番目のコマンドを実行すると、プライベートパネルトークンが表示されます。これをご自身のマシンに保管しておいてください。

起動後、[127.0.0.1:8787](http://127.0.0.1:8787) にアクセスしてください。

ソースからのインストールの場合、トークンは「`data/live/panel-token.txt`」です。Telegramでのログインには、組み込みのAPI設定、[またはmy.telegram.](https://my.telegram.org)orgから取得した独自のペアを使用できます。[完全なセットアップガイド ↗](https://phishdestroy.github.io/TgWitness/ja/docs/reference/quickstart/)

**TgWitness 0.7.0** [新着情報 →](https://phishdestroy.github.io/TgWitness/ja/docs/reference/changelog/) · [機能と既知の制限事項 →](https://phishdestroy.github.io/TgWitness/ja/docs/reference/features/)

## 分かりやすい手順。役立つ次のステップ。

[ガイドをご覧ください ↗](https://phishdestroy.github.io/TgWitness/ja/docs/)

[### モード、シナリオ、および証拠レベル 4つの収集モード。8つの検証レベル。ご担当の案件に適したワークフローをお選びください。](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html)

[01 ### アカウントを連携する 電話、QRコード、および対応しているセッションのインポート機能。](https://phishdestroy.github.io/TgWitness/ja/docs/accounts/)[02 ### プロキシを選択してください 公開されているMTProxyリスト、またはご自身のルートをご利用ください。](https://phishdestroy.github.io/TgWitness/ja/docs/proxies/)[03 ### Witnessボットの設定 Telegramチャンネル内の署名付きチェックポイント。](https://phishdestroy.github.io/TgWitness/ja/docs/witness/)[04 ### エクスポートと検証 記録された履歴を共有し、その完全性を確認してください。](https://phishdestroy.github.io/TgWitness/ja/docs/exports/)

## アーカイブを処理する。

履歴の読み込み、AIソースの確認、MCPクライアントの接続、保存されたメディアの認識、および署名付きWebhookの送信。

現在のソースから入手可能です。0.7.0 ポータブルプレビュー版は、これらのツールよりも以前のバージョンです。

[ワークフローの詳細はこちら](https://phishdestroy.github.io/TgWitness/ja/docs/archive/)

## ご利用開始の前に。

**このページはTelegramにリンクしていますか？**

いいえ。これは架空の例やスクリーンショットを含む静的なプロジェクトページです。実際のアプリケーションは、お使いのコンピュータまたはサーバー上で動作し、ログインもそこで行われます。

**キャプチャ前に削除されたメッセージは復元できますか？**

いいえ。TgWitnessは、収集が実行されていた間にアカウントで確認されたコンテンツを保持します。後の履歴スナップショットでは、見逃された編集や削除されたメッセージを復元することはできません。

**ジャーナル全体は暗号化されていますか？**

アカウントの認証情報および署名用秘密鍵は、暗号化された保管庫に保存されます。ローカルのメッセージや添付ファイルを保存するには、暗号化されたディスクまたはボリュームが必要です。エクスポート時には、オプションでパスワード保護されたAES-256 ZIP形式を使用することができます。

**これはTelegramと提携しているのでしょうか？**

いいえ。TgWitnessは、MITライセンスの下で配布されているTelethonを利用する独立したプロジェクトです。組み込みのAPI設定、またはご自身のAPIペアを使用して、ご自身のアカウントを認証していただきます。

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## まずは内容をご確認ください。準備が整いましたら、セットアップを行ってください。

[デモ版を開く](https://phishdestroy.github.io/TgWitness/demo/?lang=ja)[セットアップガイド](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja)
