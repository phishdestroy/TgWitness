# クイックスタート

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/quickstart/

TgWitnessのインストールおよび起動方法のすべて：Windowsパッケージ、Python、Docker、および初期チェックを含む統合デモ。

**英語** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [ウクライナ語](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [ポルトガル語（ブラジル）](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [アラビア語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [ウルドゥー語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [ヒンディー語](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [インドネシア語](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [簡体字中国語](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitnessは、ご自身のアカウントがアクセス可能なTelegramのグループやチャンネルを監視するためのスタンドアロン型アプリケーションです。 独自のデータディレクトリを使用して、ローカル上で動作します。

**初めてのご訪問ですか？**アカウントを連携する前に、[デモをご覧ください](https://phishdestroy.github.io/TgWitness/ja/docs/reference/quickstart/#explore-the-interface)。 プロキシ、ウィットネス、エクスポート、サーバー設定に関する[ガイドをお選びください](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)。

## インストールと起動

[GitHub Actions で収集（プレビュー）](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

いずれかの方法をお選びください。リリースビルドが公開されると、ポータブル版がダウンロード可能になります：

| ホスト | インストールは不要です | 出典：Python 3.11 以上 | Docker：Engine/Desktop（Compose 2.20 以降） |
| --- | --- | --- | --- |
| Windows | GitHub Releases から「`TgWitness-<version>-windows-amd64-portable.zip`」を抽出し、「`TgWitness.cmd`」をダブルクリックしてください。 | `Start.cmd` をダブルクリックしてください | `scripts\Docker.cmd` をダブルクリックしてください |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

ソースコードからの実行方法については、[現在の `main` をダウンロードして展開する](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip)か、リポジトリをクローンしてください:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

`Start.cmd` は、適切な Python が見つからない場合、現在の Windows ユーザー向けに Python 3.12 のインストール（winget、または署名済みの python.org インストーラー経由）を提案します。`start.sh` は、Python が不足している場合、お使いの Linux ディストリビューションまたは macOS 向けの正確なインストールコマンドを表示します。ソースからの初回起動時には、`.venv` が作成され、依存関係が自動的にインストールされます。

Dockerがアプリケーションをビルドし、バックグラウンドで起動します。ホスト側のPythonは 不要です。`scripts\Docker.cmd`および`scripts/docker-start.sh`は、 コンテナが正常に動作している際に、パネルアドレスとトークンを表示します。サポートされているすべてのホストにおける対応するDockerコマンドは以下の通りです：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

**http://127.0.0.1:8787** を開いてください。Docker ヘルパーまたは 2 番目の Docker コマンドによって出力されたトークンを使用するか、ポータブル版またはソースからのインストールの場合は **data/live/panel-token.txt を**参照してください。以下の 「**Telegram を接続**」に進んでください。 ネイティブインストールとDockerインストールでは、それぞれ別々のストレージを使用します。 Dockerを起動しても、既存のネイティブジャーナルはインポートされません。

サーバーの[デプロイメント](https://phishdestroy.github.io/TgWitness/ja/docs/reference/deployment/)には、HTTPSの自動設定、再起動、 公開画像、アップデート、およびバックアップが含まれます。

## インターフェースをご覧ください

1. ポータブルパッケージ内の**「TgWitness-Demo.cmd** 」、Windowsのソース フォルダ内の「**scripts\Demo.cmd** 」、またはLinux/macOS上の「`sh start.sh --demo` 」を実行してください。ソースから起動すると、まず「`.venv` 」が作成され、依存関係がインストールされます。
2. **http://127.0.0.1:8787** を開いてください。
3. ローカルデモでは、サンプルジャーナルが自動的に開かれます。ローカルから直接アクセスする場合、トークンのコピーは必要ありません。

デモ用のメッセージは架空のものです。デモモードでは、実際のTelegramアカウントに接続することはできません。

## Telegramに接続する

> [!警告] **失っても構わないもの以外は使用しないでください。** 個人用や重要なアカウントを接続すること、および大切なアカウントでAPI IDやハッシュを作成することは、強くお勧めしません。 Telegramは、使用するクライアントに関わらず、予測不能かつ多くの場合永久にアカウントを凍結することがあります。 テスト運用が円滑に行われるかどうかは、TgWitnessではなくTelegram次第であり、今後の動作については一切保証いたしません。

1. ネイティブのデモが実行中の場合は、それを停止し、**Start.cmd** または `sh start.sh` を実行してください。 そうでない場合は、上記で起動したライブインストールをそのまま実行し続けてください。
2. ご利用のインストール方法に対応したパネルトークンを使用して、パネルを開いてください。
3. プロキシが必要な場合は、「**アカウント**」**→「設定」→「接続設定」→「接続経路の変更」**から設定してください。
4. 「**アカウント**」で電話番号を入力し、**「続行」**を押すか、 **「QRコード」→「QRコードを表示」**を選択するか、ファイルを選択して**「アカウントを接続」**を押してください。 **「API ID + ハッシュ」**は任意です。ワークスペースは、保存またはインポートされたペア、 あるいは組み込みプールから取得した有効なペアを使用します。独自のアプリを使用する場合は、1組の `API ID:API Hash`ペアを「API ID」に貼り付けてください。 完全な認証キーが必要な場合は、「**認証キー」**を選択し、512文字の16進数 文字列をすべて貼り付け、提供されたDC IDを選択してください。ユーザーIDは任意ですが、入力された場合はチェックされます。
5. 選択したログイン方法（電話番号／認証コード／2FA）の手続きを完了してください。QRコードの場合は、 ログイン済みのTelegramアプリからの確認、またはサポートされている認証済みセッションのインポートが必要です。
6. 表示されているアカウントIDをご確認ください。オープン**ソース**：チャットは自動的に読み込まれます。グループを追加してください。
7. 「**保存する変更を選択**」で、イベントカテゴリまたは「 **メッセージ、編集、削除**」のプリセットを選択し、監視設定を保存してください。
8. 添付ファイルの設定を個別に選択し、「**監視開始」**を押してください。

API認証情報はアプリケーションを識別するものであり、それ自体ではアカウントへのアクセス権を付与するものではありません。 非公開グループでは公開ユーザー名は必要ありませんが、アカウントにはアクセス権が必要です。

既存のアカウントについては、[アカウントとセッション形式](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/)を参照してください。パネルは Telethon StringSession、Telethon/Pyrogram SQLite、単一アカウントの TData ZIP、およびサポートされているアカウント JSON を受け付けます。セッションとそれに付随する JSON を一緒に選択し、**アカウントを連携する**を押してください。同じオプションの API 設定を使用して QR ログインも利用できます。TDLib、ボットセッション、および CSV/JSON のアカウント一覧はサポートされていません。

複数のアカウントを扱う場合は、**アカウント → アカウントのインポート**を使用し、サポートされているセッションファイルを選択してください。付随する JSON ファイルはベース名（拡張子を除いたファイル名）でペアリングされ、インポートされた各アカウントには専用のワークスペースが割り当てられます。[一括インポートとアカウントグループ](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/#bulk-import-and-account-groups)を参照してください。

別のアカウントを追加するには、アカウント選択ボタンの横にある「**+**」を押すか、 **[アカウント] → [設定] → [接続設定] → [ワークスペース]** を開くか、**[アカウント]** を使用してください。ワークスペースごとに、 セッション、ジャーナル、鍵、ソース、キューが個別に管理されます。ビューを切り替えても、他のコレクターは実行されたままになります。 このインストール環境では、同じ Telegram アカウントを 2 つのワークスペースに割り当てることはできません。 ワークスペースの数に制限はありません。ワークスペースは1つのプロセスを共有するため、処理能力はマシンの性能に依存します。

ライブパネルトークンは、Telegramの認証情報および保存された データへのアクセスを保護するものであり、Telegram APIの認証情報とは別物です。明示的に起動され、 直接アクセスされたローカルデモのみが自動的に登録されます。リモートまたはプロキシ経由のデモでは、引き続き `data/demo/panel-token.txt`が使用されます。

## 確認とエクスポート

- **ジャーナル：**情報源やイベントの種類ごとに記録を検索・フィルタリングできます。
- イベントを選択すると、その元の記録、出典、および保存されたバージョンを確認できます。
- 編集の詳細には、変更前後の利用可能なコンテンツが表示されます。削除の詳細には、 最後にキャプチャされたコンテンツ（存在する場合）が表示されます。身元不明の行為者は、引き続き不明のままとなります。
- **エクスポート形式：**署名付きZIP、JSONL、CSV、およびオフライン用HTML。
- **チャットの完全エクスポート**（[ソース] → [チャットの完全エクスポート]）：1つのチャットの表示可能な 履歴全体を、`chat.json`（Telegram-export形式）による署名付きバンドルと、読み取り可能な `chat.html`としてダウンロードします。プライベートチャットは、そのアカウントがメンバーである場合に利用可能です。これは現在の スナップショットであり、削除されたメッセージや過去に編集されたメッセージを復元したものではありません。 `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256` を使用して コピーを検証してください。
- **チェックポイントの保存：**署名付きジャーナルの境界をコレクターの外側に保持してください。
- **署名付き実行レシートをダウンロード：**コレクターのプログラムおよびバージョンの記録を保存します。
- **タイムスタンプのリクエストの準備：**タイムスタンプ認証機関へのオフラインリクエストを準備します。 [TIMESTAMP.](https://phishdestroy.github.io/TgWitness/ja/docs/reference/timestamp/)mdの手順に従って、応答を取得し、検証してください。
- **ジャーナルの検証：**イベントの署名とチェーンリンクを確認してください。ZIP形式でのエクスポートでは、メディアファイルもチェックされます。

対応しているブラウザでは、大容量のエクスポートデータを指定したファイルに直接保存できます。その他のブラウザでは、 最大 128 MiB までバッファリングされます。サーバーが稼働している間、ストリーミング CLI を使用すれば、 レスポンス全体をバッファリングすることなく、より大容量のダウンロードが可能です：

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

別のワークスペースを追加する場合は、「**エクスポート」→「ワークスペース ID」**から `--profile ID` を追加してください。 リモートサーバーの場合は、`--url https://your-server` を追加してください。デフォルトの転送制限は 5 GiBですが、`--max-mib`を使用すると変更できます。署名付きZIPコンテンツには、デフォルトで別途4 GiBの非圧縮 検証制限があります（**Parameters**でこの制限を引き上げることができます。そのようなアーカイブの検証には `verify.py --max-gib N`を使用してください）。検証には、信頼できる検証ツールのコピーと、 独立して保管された鍵のフィンガープリント／チェックポイントを使用してください。

## インストール方法をご確認ください

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check`は、ローカルの依存関係、署名機能のサポート状況、ストレージ、鍵の設定、および リスニングアドレスを調査します。何もインストールせず、Telegramにも接続しません。ポートが 使用中の場合は、別のインスタンスが実行されている可能性があります。別の`--port`を使用するか、まずそれを停止してください。

ランチャーは`.venv`にインストールされます。補助的な`python -m tgwitness...`コマンドは、 その環境がすでに有効化されていない限り、Windowsでは`.venv\Scripts\python.exe`を、Linux/macOSでは`.venv/bin/python`を 使用する必要があります。

## セッション、保護、および運用

TelethonのSQLite形式の`.session`ファイルは、ローカルで `python -m tgwitness.sessions account.session --out account.tgwitness-session`を使用して変換し、 Accountに読み込むことができます。ファイルの直接インポートやQRコードによるログインも利用可能です。ログイン形式、SOCKS5、 HTTP CONNECT、MTProxy、および外部マスターキーについては [、CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/ja/docs/reference/connection/)をご参照ください。

**「一時停止」を選択すると、**収集が停止します。**「ロック」を選択**しても、ブラウザへのアクセスが遮断されるだけです。 タブを閉じても、収集プロセスは実行されたままになります。プロセスを停止すると収集が中断されますが、 履歴のスナップショットでは、見逃された編集や削除のすべてを復元することはできません。 イベントポリシー、添付ファイルのキュー、 アカウントの隔離、および再起動時の動作について、[収集の仕組み](https://phishdestroy.github.io/TgWitness/ja/docs/reference/collection/)をご確認ください。

セッションとシークレットは暗号化されています。メッセージの内容、メディア、およびエクスポートには、 暗号化されたディスクまたはボリュームが必要です。署名は、信頼できる鍵に対する完全性を保証するものであり、 Telegramからの送信元を証明するものではなく、また、コレクターとその鍵を管理するオペレーターによる 改ざんを防ぐものでもありません。

バックアップ／復元については [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/ja/docs/reference/operations/)、ホスティングについては [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/ja/docs/reference/deployment/)、 サービスの例については [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) をご参照ください。インストールされた パネルには、`/guide.html` にオフライン設定ガイドも含まれています。

実際の検証状況および残された課題については、 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/ja/docs/reference/verification/) および [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) に記載されています。
