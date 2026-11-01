# 導入

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/deployment/

TgWitnessは、Windows、Linux、macOS、またはDocker上で、HTTPS経由でサービスとして実行でき、バックアップや更新機能も備えています。

**英語** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [ウクライナ語](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [ポルトガル語（ブラジル）](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [アラビア語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [ウルドゥー語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [ヒンディー語](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [インドネシア語](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [簡体字中国語](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## インストール方法を選択してください

ポータブルパッケージをご利用の場合は、GitHub Releasesから`TgWitness-<version>-windows-amd64-portable.zip`を解凍してください。 その他の方法をご利用の場合は、ソースのZIPファイルをダウンロードして解凍するか、リポジトリをクローンし、 プロジェクトディレクトリから以下のコマンドを実行してください：

| インストール | はじめに | バックグラウンドで動作しますか？ |
| --- | --- | --- |
| Windows用ポータブルパッケージ | `TgWitness.cmd` | いいえ、ウィンドウは開いたままにしておいてください。 |
| Windowsネイティブ版 | `Start.cmd` | いいえ。バックグラウンドでの使用には、オプションのログオンタスクをご利用ください。 |
| Linux/macOSネイティブ | `sh start.sh` | いいえ。バックグラウンドでの実行には、systemd または launchd を使用してください。 |
| サポートされているあらゆるホストでのDocker | `docker compose up -d --build --wait` | はい、Dockerデーモンが実行されている間は可能です。 |
| Windows 版 Docker ヘルパー | `scripts\Docker.cmd` | はい。このヘルパーは、Webサーバーの稼働状態を確認します。 |
| Linux/macOS 用の Docker ヘルパー | `sh scripts/docker-start.sh` | はい。このヘルパーは、Webサーバーの稼働状態を確認します。 |

第三者が確認可能なクラウドサーバーについては（ プロバイダーのAPIを通じて作成され、SSHを使用せず、Cloudflare Tunnel経由でのみアクセス可能なもの）、 [高保証デプロイメント](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md)をご覧ください。

ネイティブ起動時には、プライベートな`.venv`が生成され、ピン留めされた依存関係がインストールされます。 Dockerは、ホスト側のPythonを必要とせずに、イメージ内でこれらをビルドします。初回 セットアップにはインターネット接続が必要です。 Python 3.11 以降が見つからない場合、`Start.cmd` は、 現在の Windows ユーザー向けに Python 3.12 をインストールする前に確認を行います（winget を使用、それ以外の場合は Python Software Foundation の署名を確認した上で python.org の インストーラーを使用）。管理者権限を要求することは 一切ありません。Docker および OS サービスは引き続き前提条件となります。

ネイティブおよびポータブルインストールでは、フォルダ内の`data/live`を使用します。Dockerでは、`tgwitness-data`という名前のボリュームを `/data`で使用します。これらは、データディレクトリ全体を意図的に移行するまでは、 別々のインストールとして扱われます。新しいDockerコンテナがネイティブの アカウントを自動的に検出することは期待しないでください。

## インストール要件

ネイティブインストールには、`venv`および`ensurepip`を含むPython 3.11以降、 最初の依存関係のインストールに必要なインターネット接続、および `.venv`用の書き込み可能なプロジェクトディレクトリが必要です。同梱のパネルには、Node.jsやフロントエンドのビルドは不要です。ランチャーは 通常のOSアカウントから実行してください。TgWitnessでは管理者/root権限は必要ありません。

- **Windows：**`Start.cmd`は、まず`py -3`、次に`python`、さらにユーザーごとのデフォルトのインストールフォルダおよび 「Program Files」フォルダを順に確認し、バージョン3.11以降が必要です。いずれも見つからない場合は、 前述のユーザーごとの自動インストールが提案されます。`py -3 start.py`も動作します。 ポータブル版パッケージは、Pythonを一切必要としません。
- **Linux：**`start.sh`が`python3.13`、`python3.12`、`python3.11`、`python3`、および `python`を試行し、該当するものがない場合は、apt、dnf、pacman、zypper、apk、またはHomebrew用の インストールコマンドを表示します。Debian/Ubuntuでのインストールでは、選択したインタプリタに対応する `python3-venv`パッケージが必要になる場合があります。 ディストリビューションの古い デフォルトのPythonは、Python 3.11以降に置き換えるか、それを補完する必要があります。
- **macOS：**最新の Python 3.11 以上のディストリビューションをインストールしてください。OS に付属の インタプリタが要件を満たしているとは想定しないでください。プロジェクトディレクトリ内の `python3 start.py` を使用してください。
- **Docker：**Compose v2.20 以降を搭載した Docker Engine/Desktop をご利用ください。Windows 上で Docker Desktop を使用する場合は、Linux コンテナを使用する必要があります。コンテナは 独自の Python 依存関係をインストールするため、ホスト側で別途 Python をインストールする必要はありません。

データディレクトリには永続的なローカルストレージを使用してください。メッセージ、 メディア、WALの増加、エクスポート、バックアップを考慮して容量を計画してください。すべてのワークロードに適用できる、証拠に基づいた普遍的な ディスク／RAMの最低仕様は存在しません。互換性のある依存関係ホイールがないCPUアーキテクチャやPythonバージョンについては、 追加のビルドツールが必要となり、それらについて 個別の検証が必要となる場合があります。 「ポータブル」とは、あらゆるOSやハードウェアに対応していることを保証するものではありません。

Windows 11/Python 3.12 については、ローカル環境で検証済みです。Linux/macOS/コンテナの定義および CI は提供されていますが、この開発ホスト上では実行されていません。正確な範囲については、 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/ja/docs/reference/verification/) をご覧ください。

## ローカルコンピュータ

Windowsでは「`Start.cmd`」、Linux/macOSでは「`sh start.sh`」をご使用ください。「`scripts\Setup.cmd`」または 「`sh start.sh --setup-only`」を実行すると、 環境が準備されます。ランチャーは初回使用時に依存関係をインストールし、その後の起動時には その環境を再利用します。セットアップおよびTelegramのデータ収集にはインターネット接続が必要ですが、 既存の記録の閲覧やエクスポートの作成はオフラインでも可能です。

セットアップ後に`python start.py --check`を実行すると、コレクターを起動せずに、ローカルの依存関係、Ed25519、 ストレージ、鍵の設定、およびリスニングアドレスを確認できます。 構造化された出力を得るには、`--json` を使用してください。`--data-dir`、`--host`、および `--port` を実行してください。このチェックでは、パッケージのインストール、ジャーナルの作成、Telegram への接続は行われません。 また、完全性やカバレッジの検証を行うものでもありません。起動時には、既存のジャーナルが別途検証されます。 `python start.py --help` もインストールを回避します。

オプション：

start.py を実行した後、Windows では `.venv\Scripts\python.exe`、Linux/macOS では `.venv/bin/python` を使用して補助コマンドを実行するか、まずその環境を有効にしてください。 以下の `python -m ...` の例では、環境が有効になっていることを前提としています。

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

環境変数：TGWITNESS_DATA、TGWITNESS_HOST、TGWITNESS_PORT、TGWITNESS_TOKEN。 TGWITNESS_VAULT_KEY_FILE を指定すると、新規インストール時に外部キーモードが選択されます。詳細は以下をご覧ください。 TGWITNESS_TOKEN を指定する場合は、24 文字以上である必要があります。暗号学的に ランダムな値を使用してください。指定がない場合、アプリは panel-token.txt ファイルに 256 ビットのランダムなトークンを生成します。 環境変数による上書きを行っても、そのファイルは上書きされません。認証情報を更新するには、アプリを再起動してください。

データディレクトリを所有できるプロセスは、正確に1つだけです。クロスプラットフォームのOSファイルロックにより、 意図しない同時書き込みが防止されます。Uvicornワーカーは1つ使用してください。パネルでは、任意の数の ワークスペースを管理でき、追加のワークスペースディレクトリは profiles/<id>/ 配下に配置されます。 別々のサービスインスタンスについては、別々のディレクトリとポートを使用してください。SQLiteのWALファイルは、ネットワークファイルシステムではなく、 ローカルの永続ストレージに保存してください。レプリカ間で1つのボリュームを共有しないでください。

## Windows用ポータブルパッケージ

各GitHubリリースには、`TgWitness-<version>-windows-amd64-portable.zip`およびその `.sha256`が含まれています。これには、python.orgからの公式の埋め込み可能なPython 3.12ランタイム （`tools/build_portable.py`でチェックサムが固定されています）、TgWitnessおよびその固定された依存関係、 ならびに3つのランチャーが含まれています：

| ファイル | 目的 |
| --- | --- |
| `TgWitness.cmd` | パネルを起動します。追加のオプションはそのまま渡されます（例：`TgWitness.cmd --port 8790`）。 |
| `TgWitness-Demo.cmd` | `data\demo`で合成デモを開始してください |
| `TgWitness-Check.cmd` | 起動せずに準備状況チェックを実行してください |

アーカイブ全体を、`Documents\TgWitness` などの書き込み可能なフォルダに解凍してください。ZIP ファイル内や Program Files フォルダ内から 実行しないでください。ランタイムは隔離されたモジュールパスを使用するため、 他の Python インストールや `PYTHONPATH` が影響を与えることはありません。 データは パッケージ内の`data`フォルダに保存されます。更新するには、TgWitnessを停止し、新しいバージョンを新しい フォルダに解凍してから、`data`フォルダをコピーしてください。

Python 3.12 を使用して、64 ビット版 Windows 上でご自身でビルドするには：

```
python tools/build_portable.py
```

ビルダーは実行時のチェックサムを検証し、制約付きの依存関係を パッケージにインストールし、組み込みインタープリタを使用して準備状況チェックを実行し、ZIPファイル とチェックサムを`dist/`に書き込みます。

## コンテナ

```
docker compose up -d --build --wait
```

これにより、/data 用の名前付き永続ボリュームが作成されます。 Web ポートは 127.0.0.1:8787 にマッピングされます。 このプロセスは、UID 10001 として、 権限を制限された状態で実行され、ルートファイルシステムは読み取り専用、/data および /tmp は書き込み可能となっています。 `--wait`は、返却する前に Web サーバーの正常性を確認します。Telegram の 認証や配信は行いません。 提供されているヘルパーは、ビルド後に180秒のレディネス・タイムアウトを 設定しています。初期の依存関係のダウンロードには、それ以上の時間がかかる場合があります。

両方のベース Compose ファイルはプロジェクト名「`tgwitness`」を使用しているため、新しいリリースを 別のディレクトリに展開しても、自動的に新しいデータボリュームが選択されることはありません。そのプロジェクトについては、 1つのデプロイメントのみをアクティブにしておいてください。独立したインストールを行う場合は、一意の「 `docker compose -p NAME ...`」と異なるホストポートを使用し、更新時にも両方を維持してください。 異なるプロジェクト名を使用している古いデプロイメントについては、元の 名前を`-p`と組み合わせて引き続き使用してください。`docker compose ls`には既存のプロジェクトが一覧表示されます。

`deploy/env.example`を`.env`にコピーし、`TGWITNESS_PORT`を変更して別のループバック ポートを使用するようにしてください。例えば、`TGWITNESS_PORT=8788`ではパネルが `http://127.0.0.1:8788`で公開されますが、コンテナは引き続き8787番ポートでリスニングします。`.env`はGitで無視されています。

初期トークンを取得する：

```
docker compose exec tgwitness cat /data/panel-token.txt
```

便利なコマンド：

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped`は、クラッシュやDockerデーモンの 再起動後にコレクターを再起動します。Linuxサーバーでは、お使いのディストリビューションのサービス マネージャー（通常は`sudo systemctl enable --now docker`）を使用して、起動時にDockerを有効にしてください。Windows/macOSでは、 Docker Desktopの「サインイン時に起動」設定を有効にしてください。デスクトップのサインアウト、スリープ、または停止された Dockerデーモンの停止は、データ収集を中断させる可能性があります。明示的に停止されたコンテナは、 再度起動するまで停止したままとなります。

サンプル構成では、/tmp ボリュームの上限は 512 MiB に設定されています。エクスポート処理では、 代わりに各ワークスペースの`temporary-exports/`を永続的な /data 上に使用します。そこには、 同時エクスポート、ジャーナル／WAL の増加、メディア、およびバックアップ用にスペースを確保してください。 ランチャーは deploy/constraints.txt を使用して、適格なランタイム依存関係のバージョンを固定します。 Dockerおよび高信頼性サーバーは、deploy/requirements.lockおよび deploy/build.lockに基づき、pip --require-hashes オプションを使用してインストールされます。すべてのパッケージファイルは、コミットに記録されたSHA-256と 一致する必要があります。そのため、PyPIやミラーサイトで置き換えられたファイルは拒否されます。 Pythonベース イメージおよびオペレーティングシステムのパッケージについては、引き続き個別のリリース認定が必要です。

ジャーナルと鍵を破棄する意図がない限り、`docker compose down -v` を使用しないでください。 コンテナのヘルスレポートは、Webサーバーの稼働状況を報告するものであり、Telegramのキャプチャが成功したかどうかを示すものではありません。 パネルのコレクターの状態、ハートビート、エラー、およびカバレッジイベントを確認してください。

### 独立した証人プロフィール

オプションの`witness`サービスは、独自の コンテナ内で[独立したウィットネス](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/)を実行し、`witness-data`ボリューム内に独自の鍵とジャーナルを保持し、コレクターに対しては読み取り専用の ウィットネストークンのみを提供します。パネルの「**Witness**」ページでトークンを作成し、 ボットトークンとチャンネルと共に`.env`に追加してから、プロファイルを開始してください：

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

本サービスは、Composeネットワーク内のコレクター（`http://tgwitness:8787` ）にアクセスします（`TGWITNESS_WITNESS_COLLECTOR` で上書きされます。例えば、`/profiles/<workspace ID>` は 別のワークスペース用です）。他者が運営する別のサーバー上のウィットネスをご利用の場合は、 そこで`deploy/compose/compose.witness.yaml` を使用し、`TGWITNESS_WITNESS_COLLECTOR` をコレクターのHTTPS アドレスに設定してください。そのファイルにはウィットネスのみが含まれています。

## 公開されているイメージをインストールする

これは、[リリースワークフロー](https://phishdestroy.github.io/TgWitness/ja/docs/reference/deployment/#automated-github-releases) が正常に完了し、GHCRパッケージの設定が公開された後に利用可能になります。リポジトリの所有者名はこのソースツリーにハードコードされていません。 そのリリースのワークフロー概要に表示されている画像をご利用ください。

`deploy/env.example`を`.env`にコピーしてください。`TGWITNESS_IMAGE`には、公開版を指定してください。その際、 リポジトリパスは**小文字で**指定してください。例：

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.1
TGWITNESS_PORT=8787
```

`compose.yaml`の代わりに、このファイルを単独で実行してください：

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

ホスト側でソースからのビルド、Python、またはコンパイラは必要ありません。リリースワークフローは、 Docker DesktopのLinux VMを含む、Linux AMD64およびARM64コンテナを対象としています。 ワークフローの概要にあるバージョンタグ、または「`ghcr.io/owner/repository@sha256:...`」をご利用ください。 「`latest`」タグの移動や、無人でのアプリケーションアップグレードは設定されていません。 プロジェクト名が一致する場合、イメージとソースのバリアントは同じデータボリュームを使用します。

## サーバーでのHTTPSの自動設定

Dockerが動作するサーバー、ご自身が管理するドメイン、および永続的なローカルストレージをご用意ください。 ドメインのA/AAAAレコードをサーバーに向けるように設定してください。IPv6がサーバーに到達する場合にのみ、AAAAレコードを公開してください。 証明書の発行のために、着信TCP 80および443、ならびに発信DNS/HTTPSを許可してください。 これらのポートは、他のサービスによって既に使用されていない必要があります。

`deploy/env.example`を`.env`にコピーし、スキームやパスを含めないホスト名を設定してください：

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

HTTPSオーバーレイを使用してソースのビルドを開始します：

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

公開用画像の場合は、代わりに最初のファイルとして「`deploy/compose/compose.image.yaml`」を使用してください。 後のステータス、ログ、更新、および停止コマンド用に、「`-f`」の引数は両方とも保持しておいてください。

Caddyは証明書の取得と更新を行い、HTTPをHTTPSにリダイレクトし、 プライベートなComposeネットワーク上のコレクターへリクエストを転送します。証明書の状態は 専用の永続ボリュームに保存されます。コレクターの直接ホストポートは、ループバック専用に保たれます。 提供されているCaddyの設定では、アクセスログの記録は有効になっていません。

`https://watch.your-domain.org` を開き、パネルトークンを入力してください。「準備完了」と表示されても、 証明書の発行や外部への接続性が確認されたわけではありません。HTTPSが 利用できない場合は、DNSやファイアウォールのルールを確認し、以下の点もご確認ください：

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

提供されているCaddyイメージは、`2-alpine`タグに従っています。pullコマンドを実行すると、そのイメージが更新されます。 インフラのバージョンを固定する必要がある場合は、テスト済みのダイジェストをデプロイメントにピン留めしてください。

## 更新とバックアップ

アップデート後も「Compose」プロジェクト名とデータ量を維持します。まず、 コレクターを停止し、完全なバックアップを作成してください。デフォルトのソースベースのデプロイメントの場合：

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

リポジトリ外で、毎回新しいバックアップ先を使用し、それを アカウントへのアクセス権限が必要な資料として保護してください。例示されているパスはあくまで参考です。ご自身のプライベートなバックアップ 場所をご利用ください。隠しファイル、すべてのワークスペース、鍵、 ジャーナル、メディアを含め、ディレクトリ全体をコピーしてください。設定されている場合は、外部ボールトのマスターキーも別途バックアップしてください。 証拠用ZIPファイルは、復元可能なアプリケーションのバックアップではありません。HTTPSの場合、 証明書やアカウントの状態を保持する必要がある場合は、Caddyのボリュームも保存してください。

ソースからのデプロイを行うには、新しいリリースファイルを入手し、以下のコマンドを実行してください：

```
docker compose up -d --build --wait
```

イメージを展開する場合は、`TGWITNESS_IMAGE` を希望のバージョンに変更し、以下のコマンドを実行してください：

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

前述の停止／コピーコマンドについても、インストール先の Compose ファイルをご利用ください。 `.env`、カスタム設定、および同じプロジェクト名はそのまま維持してください。`down`は名前付き ボリュームを保持し、**`down -v`**は**それらを削除します**。`.venv`を異なるオペレーティングシステム間 またはPythonバージョン間でコピーしないでください。ネイティブアップデートを行う場合は、TgWitnessを停止し、データ ディレクトリ全体をバックアップした後、ソースファイルを置き換え、起動前に`python start.py --setup-only`を実行してください。

アップデート後は、パネルへのアクセス権、アカウントの身元、監視状態、およびカバー範囲をご確認ください。 再起動を行っても、見逃したTelegramの更新内容は復元されません。将来のバージョンで保存形式が変更された場合、ロールバックには アップデート前のバックアップが必要になる可能性があります。

## GitHub での自動リリース

このプロジェクトを、Actionsが有効化されたGitHubリポジトリにプッシュすると、 [リリースワークフロー](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml)がすぐに利用可能になります。これは、 GitHub Releaseが**公開**された際（プレリリースを含む）に実行されます。ドラフトやタグのプッシュ だけでは、パッケージは公開されません。

1. パッケージのバージョンと変更履歴を設定し、`v` に加え、`pyproject.toml`の正確なバージョン（例：`v0.7.1`）をタグとして付加したリリースを公開してください。
2. このワークフローでは、タグの検証を行い、Windows/Linux/macOSで共通して利用できるPython、 general/account-import/QRブラウザ、ソースパッケージ、およびDockerのチェックを実行します。また、Python 3.12を使用して、 これら3つのオペレーティングシステムすべてにおいて、新規のネイティブインストールも実施されます。
3. これらのチェックに合格した後、QEMU 上で ARM64 イメージのスモークテストを実行し、 AMD64/ARM64 イメージを`ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>` に公開し、 ソース ZIP ファイルと Python ホイール、およびそれらの SHA-256 サイドカーを添付します。 Windows 用のポータブル ZIP ファイルは、チェックワークフローによってテストされたものそのものです。 リリースワークフローでは、そのアーティファクトとそのチェックサムをダウンロードして公開します。
4. 最終処理では、公開済みの 3 つのパッケージをすべて再度ダウンロードし、その チェックサムを検証します。その後、`SHA256SUMS.txt` および`RELEASE-MANIFEST.json` を公開し、 バージョン、ソースのリビジョン、およびアセットのサイズを記録します。アップロード時には、 既存のリリースアセットの上書きは行われません。
5. 初回公開後、GHCRパッケージの設定を開き、匿名での画像取得を意図する場合は、可視性を 「**公開**」に設定してください。公開ソースリポジトリ があるだけでは、コンテナパッケージが公開される保証にはなりません。組織のポリシーで パッケージの公開が許可されている必要があります。このワークフローでは`GITHUB_TOKEN`を使用します。レジストリの パスワードやVPSの認証情報は、リポジトリ内に含めないでください。

このローカル環境での準備だけでは、リモートワークフローの成功は確認されていません。ARM64 エミュレーションは簡易的な動作確認であり、ネイティブハードウェアや実稼働環境におけるTelegramの動作確認ではありません。 これによりリリースのパッケージングが自動化されますが、サーバーの起動には依然として Compose コマンドおよびそのドメイン／ホストに関する前提条件が必要となります。リリースが公開されても、既存のサーバーは 自動的にアップグレードされたり再起動されたりすることはありません。

## リモートサーバー

サービスをループバックに限定し、SSHトンネルを使用するか、HTTPSを リバースプロキシで終端させてください。基本のComposeファイルはローカルのみに対応しています。オプションの `deploy/compose/compose.https.yaml`オーバーレイは、設定されたドメイン向けにCaddyを提供します。 ベアラートークンは、URLやプロキシログに含めないでください。リバースプロキシでは、 リクエストサイズと接続レートを制限する必要があります。プレーンなHTTPをインターネットに公開しないでください。

[deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) ディレクトリには、systemd、Windows ログオンタスク、macOS ユーザーエージェント、および Caddy の例が 用意されています。インストール前に、それらのパスを確認・調整してください。 これらはテンプレートであり、ローカルで実行されるプラットフォーム固有の設定ではありません。通常のランチャーでは、 バックグラウンドサービスやタスクは登録されません。

Windowsでは、ウィンドウなしの`pythonw.exe`起動時、起動時およびサーバーの診断情報は データディレクトリ内の`logs/server.log`に保存されます（1ファイルあたり5 MiB、ローテーションされたバックアップが2つ）。 コンソール起動時には、コンソールログが保持されます。どちらの モードでも、HTTPアクセスログの記録は無効になっています。ログはデータディレクトリと共に保護し、共有する前に内容を確認してください。

## 再起動とデータ欠落

最後に要求された監視状態は保持されます。監視がアクティブだった場合、 起動時に再接続を試み、選択された情報源の監視を再開します。手動で一時停止すると、 その設定は解除されます。再起動に失敗した場合は記録され、パネルに表示されます。

StringSessionは認証情報を保持しますが、Telethonの永続的な更新情報やエンティティの状態は保持しません。 ダイアログは起動時に再読み込みされます。Telegram/Telethonは実行中に発生した一部のトランスポート中断を回復できますが、 TgWitnessはプロセスの再起動を跨いだ永続的な再生を保証するものではありません。 起動のたびに、直前のジャーナルの先頭とオフライン境界が記録されます。 モニターは10秒ごとに接続状態を確認し、1分ごとにハートビートを追加します （**[Parameters] → [Liveness record every]**）。 短時間の中断は見逃される可能性があります。接続されたトランスポートであっても、更新の完全な 配信が保証されるわけではありません。スナップショットは、現在の履歴を明示的に記録したものであり、決して欠落部分の修復を行うものではありません。

メディアクイーは、各ワークスペースのSQLiteデータベースに保存されます。メッセージとそのジョブは アトミックにコミットされます。実行中に中断されたジョブは、起動時にリトライできるよう復旧されます。 各ダウンロードには、120秒の基本タイムアウトに加え、ファイルサイズに応じた256 KiB/sの転送速度が適用され、 添付ファイルの種類ごとに1～2,000 MiBの上限が設定されています。タイムアウト、速度、再試行回数は**「パラメータ」**で設定可能です。コレクターは サイズが不明なファイルをスキップします。一時停止しても、キューに登録された作業は保持されます。 再試行では、元の 観測されたファイルディスクリプタが使用され、その後編集されたメッセージの最新バージョンは決して使用されません。 一時的な障害に対する再試行回数には上限があり、メディアのFloodWait一時停止は再起動後も維持されます。 メディアの復旧はTelegramの更新復旧とは別であり、消失したファイルを復元することはできません。

## バックアップ、復元、および容量

vault.key、 signing.enc、credentials.enc、SQLite データベース／WAL ファイル、メディア、トークン、チェックポイント、 およびすべての profiles／サブディレクトリを含む**データディレクトリ全体を**コピーする前に、プロセスを停止してください。 復元 先先のサービスが停止している間に、完全なコピーを復元してください。Vaultキーの欠落や 署名キーの不一致により起動に失敗します。アクセスを強行するためにキーを再生成しないでください。

秘密のバックアップは暗号化し、アクセス制御を行ってください。証拠用ZIPファイルはポータブルであり、 アプリケーションのバックアップやTelegramセッションのバックアップではなく、証拠資料そのものを確認してください。 自動的な保存期間満了による削除機能はありません。すべてのメッセージ、生 メタデータ、メディア、一時的なエクスポートデータ、およびバックアップを保存するためのディスク容量を確保してください。

ジャーナル全体を読み込む代わりに、ストリーム記録の検証とエクスポートを開始します。 エクスポートを行うと、読み取りスナップショットが固定されますが、新しいWALへの書き込みは継続可能です。長時間続くエクスポートでは WALページが保持されるため、ディスク容量は依然として重要です。ZIPファイルは、独立した検証者のデフォルト設定に合わせて、 解凍後のサイズが4 GiBに制限されています。 **[パラメータ] → [最大署名付きZIP]** で上限を引き上げることができ、そのようなアーカイブは`verify.py --max-gib N`で検証されます。その他の形式にはイベント数の上限はありません。 対応しているブラウザは、ユーザーが選択したファイルにレスポンスのチャンクをストリーミングします。その他のブラウザは 最大128 MiBまでバッファリングし、それ以上の転送は認証済みのCLIに転送されます：

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

別のワークスペースの場合は**「Exports → Workspace ID」**から `--profile ID` を、 リモートサーバーの場合は `--format zip|jsonl|csv|html`、`--url https://your-server` を、 5 GiB の転送制限を変更する場合は `--max-mib` を使用してください。プレーン HTTP は ループバックの場合にのみ許可されます。トークンはヘッダーで送信され、リダイレクトは拒否され、既存のファイルは 上書きされず、ダウンロードが未完了のファイルは完了したファイルとして公開されません。 TGWITNESS_TOKENが生成されたトークンを上書きする場合、その有効な値を含む、別途保護されたファイルを使用してください。 panel-token.txtは、上書きによって書き換えられることはありません。 コマンドのSHA-256は転送チェックサムに過ぎません。署名付きZIPファイルについては、別途検証を行ってください。

サーバーのエクスポートファイルは、各ワークスペースのプライベート`temporary-exports/`内に保存されます。 正常に完了したエクスポートでは、ファイルが削除されます。中断されたエクスポートは、 そのワークスペースが独自のインスタンスロックを保持した状態で次に起動された際に削除されます。このディレクトリは、 ストレージの脅威／容量モデルの一部です。暗号化されたデータボリュームをご使用ください。本番環境規模の 数ギガバイトに及ぶ転送については、対象システムでの動作確認が必要です。

このパネルには、キューに入れられている／失敗したメディア、最も古い保留中のメディア、空きディスク容量、Telegram へのリクエストの一時停止、およびアクセスが未確認のソースが表示されます。これらの診断情報は、 完全なエンドツーエンドの配信モニターではありません。ワークスペースはプロセスを共有しているため、ノイズの多いアカウントが 他のワークスペースに影響を与える可能性があります。 個別のワーカープロセス、保存期間／ローテーション、耐久性のある更新 復旧、および完全な導入認定については、引き続き対応が必要です。パネルへのアクセス範囲については、 「[アクセスと権限](https://phishdestroy.github.io/TgWitness/ja/docs/reference/access/)」に文書化されています。独立したチェックポイントについては、 [ウィットネスガイド](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/)で説明されています。

## 接続および保護オプション

接続経路はワークスペースごとに設定され、認証の前に構成する必要があります。 SOCKS5/HTTP CONNECT では、固定された python-socks 依存関係を使用します。MTProxy では、Telethon の 実験的なランダム化中間トランスポートを使用します。Fake TLS ee シークレットはサポートされていません。 ダイレクト・フォールバックは、選択された[IP](https://phishdestroy.github.io/TgWitness/ja/docs/reference/connection/#ip-modes)モードによって異なります。「Hide IP」モードではこれを拒否しますが、「explicit fallback」モードでは、遅延の後で許可されます。「Tunnel/VPN」モードではダイレクト・ルートが許可されますが、VPNは構築されません。これはシステム全体のネットワークポリシーではありません。

新規インストールの場合、TGWITNESS_VAULT_KEY_FILE は、別途保護されたランダムな マスターキーファイルを指すように設定してください。コンテナ内の /data ディレクトリ外に、読み取り専用でマウントしてください。各ワークスペースの vault.external.json にある公開ソルトメタデータと、マスターキーは別々に保管してください。 既存のローカル・ヴォルトについては、計画的な移行が必要です。この変数を設定しても、 それらを自動的に変換することはありません。メッセージやメディアの保存およびエクスポートは、アプリケーション側で暗号化されていません。 必要に応じて、暗号化されたボリュームや十分な容量のプライベートな一時ストレージをご利用ください。

詳細な手順：[接続・セキュリティ](https://phishdestroy.github.io/TgWitness/ja/docs/reference/connection/)および [動作モード](https://phishdestroy.github.io/TgWitness/ja/docs/reference/operations/)。
