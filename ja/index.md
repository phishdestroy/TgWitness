# メッセージは変化します。目にしたものを残しておきましょう。

Canonical page: https://phishdestroy.github.io/TgWitness/ja/

[オープンソース ／ v0.9.1](https://phishdestroy.github.io/TgWitness/ja/docs/reference/changelog/)

Telegramのチャットをエクスポートし、その履歴を保持した上で、他者が検証可能な署名付きアーカイブを共有します。

[デモ版を開く](https://phishdestroy.github.io/TgWitness/demo/?lang=ja)[セットアップガイド](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja)

架空のデータで、Telegram へのログインは不要です。

 [アカウントまたは選択したチャットをエクスポートする](https://phishdestroy.github.io/TgWitness/ja/docs/reference/account-export/) [GitHub Actions で収集（プレビュー）](https://phishdestroy.github.io/TgWitness/ja/docs/capture/) [S3オフサイトコピー：セットアップと復旧](https://phishdestroy.github.io/TgWitness/ja/#s3)

時を越えるメッセージ ＃0042

Northstar · リサーチ架空の情報源／メッセージ 42

1. **観測されたメッセージ：**09：41：02

   ブリーフィングは14：00から始まります。
2. **編集履歴を保持**09：43：18

   ブリーフィングは15：00から始まります。

   以前のバージョンはそのまま残されています
3. **削除通知**10：06：45

   キャプチャされたコンテンツは、お客様のジャーナルに保存されます。

3つの観測。1つの履歴。例

メッセージは消えても、記録された履歴は残ります。

## 記録されたすべての変更。必要な場所に、すぐに。

本物の画面に、架空のデータを入れています。

TgWitness ／ 保存されたチャットあなたの監視作業スペース

![ダークテーマで保存されたTelegramの会話履歴。編集履歴や削除されたメッセージも、文脈を損なうことなく記録されます。](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ 保存したチャット 普通のチャットと同じ見た目で、編集と削除がメッセージのすぐ横に表示されます。

TgWitness ／ ジャーナルローカルワークスペース

![観測されたメッセージ、編集、削除通知、およびカバレッジイベントを記録したジャーナル](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ ジャーナル アカウントが見たものすべてを検索でき、欠落も記録されます。

TgWitness ／ 編集履歴ローカルワークスペース

![メッセージのキャプチャされた以前のバージョンと編集後のバージョンを比較する詳細表示パネル](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ 編集履歴 旧版と新版を並べて表示し、何も上書きしません。

TgWitness ／ 署名付きエクスポートローカルワークスペース

![ワークスペースのエクスポート機能により、署名付きのZIP、JSONL、CSV、およびオフライン用HTMLレポートを提供します。](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ 署名付きエクスポート ジャーナルを署名付きで持ち出せ、専用の検証ツールも付いています。

[「Case Board](https://phishdestroy.github.io/TgWitness/ja/docs/case-board/)」、[レポート作成](https://phishdestroy.github.io/TgWitness/ja/docs/reports/)、[共有用コピー](https://phishdestroy.github.io/TgWitness/ja/docs/handover/)を通じて、保存された記録を追跡してください。[アカウントグループを](https://phishdestroy.github.io/TgWitness/ja/docs/groups/)まとめて[確認してください](https://phishdestroy.github.io/TgWitness/ja/docs/groups/)。

01 ／ キャプチャ

### 範囲はお客様ご自身でお選びいただけます。

いくつかのチャット、フォルダー、またはアカウント全体。アカウントごとに専用のワークスペースがあります。

[収集モードの比較](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#scope)

02 ／ 保存

### 変更点は記事に追加されます。

版、削除、欠落はすべてジャーナルに残ります。

[イベントマトリックス「」をご覧ください。](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#events)

03 ／ 引き渡し

### 移動する記録。

署名付き ZIP、ファイル、オフラインレポート。パスワードは任意です。

[のエクスポートと検証](https://phishdestroy.github.io/TgWitness/ja/docs/exports/)

## 1バイトでも変更すれば、
検証機能によって検出されます。

各イベントは前のハッシュへのリンクを持ち、Ed25519署名が付与されています。

![記録されたイベントは以前のハッシュ値にリンクされ、署名が付与され、検証可能な形式でエクスポートされます。](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![キャプチャされた記録を変更すると、そのハッシュが変更され、リンクされた記録の検証が不可能になります。](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![別途保存されたチェックポイントにより、受信者はエクスポートされたジャーナルと以前の記録を比較することができます。](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

ファイルのハッシュ値から、別途保持されているチェックポイントに至るまでの検証手順に従ってください。

[8つの証拠レベルをご覧ください](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#levels)

## 別の目によるチェックをお待ちしております。

メッセージ、ファイル、オフラインレポートを 1 つの署名付きバンドルにまとめます。

[証拠モデル「」をご覧ください。](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/)

tgwitness-evidence.zip署名付きバンドル

- 01

  当初の所見JSONL形式の記録 ＋ CSVテーブル
- 02

  読みやすい文脈オフラインHTMLレポート＋保存されたメディア
- 03

  独立した検証署名付きマニフェスト ＋ スタンドアロン型検証ツール

受け取った人はあなたの鍵ですべてを確認でき、別の場所に保管したチェックポイントがその後の書き換えがないことを示します。[確認の仕組み。](https://phishdestroy.github.io/TgWitness/ja/docs/concepts/#layers)

## S3へのコピー。外部による検証。

暗号化されたコピーを保管し、独立した検証手段を追加してください。

デフォルトではオフになっています

### すべてをS3互換のストレージにコピーします

ジャーナル、ファイル、チェックポイント、チャットのエクスポートを、S3 へ送る前に暗号化します。

**保存設定と復元**

クライアント側暗号化

`AES-256-GCM` はあなたのマシン上で動きます。プロバイダーが見るのは暗号文だけです。

定期的または手動でのコピー

今すぐ、または 1〜1，440 分ごとにコピーし、進行状況はパネルに表示されます。

Object Lock

保持日数とモードを選ぶと、実際に適用されたかをパネルが確認します。

検証済みの復元

鍵は別に保管してください。どこでも復元でき、ファイルは検証に通ってから出力されます。

![オフサイトコピーに関する完全な説明パネル：エンドポイント、リージョン、バケット、アクセスキー、スケジュール、オブジェクトロック、および復旧キーの設定](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

高度なオプションを展開した完全なパネルです。ストレージの認証情報は表示されていません。

ジャーナルおよびメディア`AES-256-GCM`S3互換のストレージ

[S3の設定とコピーの復元](https://phishdestroy.github.io/TgWitness/ja/docs/exports/#s3)[検証の詳細はこちらをご覧ください](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#off-site-copy-and-restore-s3)

**復元キー** 別に保管してください。これがないとコピーは読めません。

### 通知 · Apprise

問題、チャットの変化、日次サマリーをメッセンジャー、メール、または独自の webhook に送ります。

**共有する内容を選ぶ** オンにしない限り、メッセージ本文は含まれません。

 [通知先の設定](https://phishdestroy.github.io/TgWitness/ja/docs/reference/operations/#notifications)

### 外部タイムスタンプ

RFC 3161 および OpenTimestamps に基づくタイムスタンプ・チェックポイント・ハッシュ。

**結果を追う** TSA の応答を確認するか、OpenTimestamps の受領証を Bitcoin の証明にアップグレードします。

 [タイムスタンプの証明を確認する](https://phishdestroy.github.io/TgWitness/ja/docs/reference/timestamp/)

### 独立した証人

別のホストが署名付きの観測データを保管し、`TGW1`チェックポイントを公開することができます。

**参照を分ける** 別のホストで、専用の鍵とジャーナルを使って実行します。

 [Witnessのセットアップ](https://phishdestroy.github.io/TgWitness/ja/docs/witness/)

### 復元と明らかな欠落

再起動後に再開します。再確認と`coverage.json`により、復元されたメッセージと欠落箇所が表示されます。

**区間を確認する** 復元したメッセージと記録された欠落を並べて表示します。

 [連続性と欠落を確認する](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html#continuity)

## 最初のワークスペースはここから始まります。

まずデモを試し、準備ができたら予備のアカウントを接続してください。
Windows、Linux、macOS、Docker に対応。

[セットアップガイド「」をご覧ください。](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja)

**インポートされたセッションは1つ、実行中のクライアントは1つです。**

インポートした TData やセッションを Telegram Desktop と TgWitness で同時に動かさないでください。Telegram が両方を無効にすることがあります（AUTH_KEY_DUPLICATED）。両方必要な場合は、電話番号か QR で TgWitness に別途ログインしてください。

[セッションのインポートに関する警告をお読みください](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja#session-warning)

**接続する前に、ぜひご一読ください。**

Telegramアカウントがなくても、架空のワークスペースをお試しいただけます。

[オンラインデモを開く →](https://phishdestroy.github.io/TgWitness/demo/?lang=ja)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**ローカルインストール用コマンド**

ステップ 01

### ソースを入手する。

[ソースのZIPファイルをダウンロードして](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip)解凍するか、リポジトリをクローンしてください：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Python 3.11 以上が必要です。Windows ではランチャーがインストールを提案します。

[リリースを閲覧する](https://github.com/phishdestroy/TgWitness/releases)

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

ソースからインストールした場合、トークンは `data/live/panel-token.txt` にあります。[my.telegram.org](https://my.telegram.org) で取得する独自の API ペアは任意です。[詳しいセットアップガイド ↗](https://phishdestroy.github.io/TgWitness/ja/docs/reference/quickstart/)

**TgWitness 0.9.1** [新着情報 →](https://phishdestroy.github.io/TgWitness/ja/docs/reference/changelog/) · [機能と既知の制限事項 →](https://phishdestroy.github.io/TgWitness/ja/docs/reference/features/)

## 分かりやすい手順。役立つ次のステップ。

[ガイドをご覧ください ↗](https://phishdestroy.github.io/TgWitness/ja/docs/)

[### モード、シナリオ、および証拠レベル 4つの収集モード。8つの検証レベル。ご担当の案件に適したワークフローをお選びください。](https://phishdestroy.github.io/TgWitness/ja/guides/modes.html)

[01 ### アカウントを連携する 電話、QRコード、および対応しているセッションのインポート機能。](https://phishdestroy.github.io/TgWitness/ja/docs/accounts/)[02 ### プロキシを選択してください 公開されているMTProxyリスト、またはご自身のルートをご利用ください。](https://phishdestroy.github.io/TgWitness/ja/docs/proxies/)[03 ### Witnessボットの設定 Telegramチャンネル内の署名付きチェックポイント。](https://phishdestroy.github.io/TgWitness/ja/docs/witness/)[04 ### エクスポートと検証 記録された履歴を共有し、その完全性を確認してください。](https://phishdestroy.github.io/TgWitness/ja/docs/exports/)

## アーカイブを処理する。

履歴、出典付き AI、MCP、OCR、署名付き webhook。

[ワークフローの詳細はこちら](https://phishdestroy.github.io/TgWitness/ja/docs/archive/)

## ご利用開始の前に。

**このページはTelegramにリンクしていますか？**

いいえ。架空の例を載せた静的ページです。アプリはあなた自身のマシンで動き、ログインもそこで行います。

**キャプチャ前に削除されたメッセージは復元できますか？**

いいえ。動作中にアカウントが見たものを保存します。後から撮ったスナップショットでは、見逃した編集や削除されたメッセージは再構成できません。

**ジャーナル全体は暗号化されていますか？**

セッションと鍵は暗号化されます。メッセージとファイルはされないので、ディスク暗号化を使ってください。エクスポートには AES－256 のパスワードを設定できます。

**これはTelegramと提携しているのでしょうか？**

いいえ。Telethon 上に作られた MIT ライセンスの独立プロジェクトです。ログインには自分のアカウントを使います。

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## まずは内容をご確認ください。準備が整いましたら、セットアップを行ってください。

[デモ版を開く](https://phishdestroy.github.io/TgWitness/demo/?lang=ja)[セットアップガイド](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja)
