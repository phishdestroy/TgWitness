# インストール、検証、および更新

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/

1つのコマンドでインストール、署名とハッシュの確認、更新、およびアンインストールが可能です。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [ドキュメント](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/ja/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[プロジェクト](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [クイックスタート](https://phishdestroy.github.io/TgWitness/ja/docs/reference/quickstart/) · [デプロイ](https://phishdestroy.github.io/TgWitness/ja/docs/reference/deployment/)

**On this page**

- [Install with one command](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#install-with-one-command)
- [Where everything runs](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#where-everything-runs)
- [Full-text search settings](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#full-text-search-settings)
- [Command-line access](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#command-line-access)
- [Verify before running](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#verify-before-running)
- [Update an existing installation](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#update-an-existing-installation)
- [Everyday commands on Ubuntu](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#everyday-commands-on-ubuntu)
- [Remove TgWitness](https://phishdestroy.github.io/TgWitness/ja/docs/reference/installation/#remove-tgwitness)

## 1つのコマンドでインストール

ガイド付きインストーラーには、専用の Python ランタイムが含まれています。今後のインストールでも同じアドレスを使用してください。 公開されるたびに、インストーラー、ハッシュ、署名、 およびビルド情報がまとめて更新されます。

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Ubuntu サーバーでは、root 権限で実行してバックグラウンドサービスをインストールしてください。デスクトップ環境では、 通常のユーザーとして実行してください。

**Windows（PowerShell または コマンドプロンプト）：**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Windows では管理者権限は必要ありません。PowerShell の子プロセスは、 ターミナルを結果が表示されたまま開いた状態に保ちます。Python および依存関係はインストール先に残ります。

Ubuntu では、**「このコンピュータ**」、「**一時的な HTTPS リンク**」、または「**独自のドメイン**」を選択してください。 インストーラーがパネルのアドレスとアクセスキーを表示します。一時的なリンクを使用する場合は、 その HTTPS アドレスをブラウザで開き、キーを入力してください。リモート サーバーへのローカルアクセスを行う場合は、お使いのコンピュータから SSH フォワードを使用してください（`ssh -L 8787:127.0.0.1:8787 user@server`） を使用して `http://127.0.0.1:8787`。macOSおよびWindowsでは、ローカルパネルが ブラウザで開きます。ターミナルは実行したままにしておいてください。

パネルで Telegram にログインし、収集対象を選択してください。インストールしただけでは Telegram の収集は開始されません。

## すべてが動作する場所

`get.destroy.tools` は、**静的ファイルのダウンロードを提供する Cloudflare Worker** です。 TgWitnessパネル、Telegram セッション、ユーザー証拠データベースは一切含まれていません。また、 プロジェクト用 VPS にはルーティングされません。アプリケーションは、コマンドを実行したマシン上で動作します。

| インストール | プログラム | データ |
| --- | --- | --- |
| Ubuntu（root権限） | `/opt/tgwitness` | システムサービス： `/var/lib/tgwitness-<installation ID>`; 正確なパスについては `tgwitness paths` を指定して正確なパスを指定してください。 |
| Linux / macOS ユーザー | `~/.local/share/tgwitness` | `data/live` そのインストール環境下で。 |
| Windowsユーザー | `%LOCALAPPDATA%\TgWitness` | `data\live` そのインストール環境下で。 |

設定 `TGWITNESS_INSTALL_DIR` を選択して別のフォルダを指定します。インストールされたバージョンとデータは 別々に管理されます。インストーラーは、アカウント、メッセージ、鍵を ダウンロードサイトにアップロードすることはありません。Cloudflareトンネルを選択すると、パネルのトラフィックは Cloudflareを経由して送信されます。独自のドメインを使用する場合は、自身のサーバーを指すように設定します。

すべてのインストールには、ローカルの パス、コマンド、リポジトリへのリンクが記載された **START-HERE.html** および **START-HERE.txt** が含まれています。 `tgwitness guide` を実行してガイドを開きます。 Windowsでは、 `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` を使用してください。

## 全文検索の設定

[全文検索](https://phishdestroy.github.io/TgWitness/ja/docs/reference/search/)（プレビュー版）は設定が不要です。インデックスは更新後に バックグラウンドで構築されます。

| 変数またはコマンド | 効果 |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | デフォルト：インデックスは各ワークスペースの `search/fulltext.sqlite3` 各ワークスペースの |
| `TGWITNESS_FULLTEXT=memory` | インデックスファイルは存在せず、起動のたびにインデックスが再構築されます。 |
| `TGWITNESS_FULLTEXT=off` | 索引は作成せず、完全一致検索のみとする |
| `tgwitness index status` | すべてのワークスペースの状態をインデックス化 |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | 署名付きジャーナルからすべてのインデックスを再構築する |

「**ジャーナル**」**→「フィルター」→**「**検索インデックス**」で管理者が選択した設定は、 そのワークスペースの変数を上書きします。コマンドは、それを実行しているインストール環境の データディレクトリを検索します。それ以外の場所では、 `--data-dir` からパスを追加してください `tgwitness paths`. 完全なウクライナ語辞書（GPL-3.0データ）を使用するには、 `pymorphy3-dicts-uk` を インストール先の Python 環境にインストールしてください。

## コマンドラインからのアクセス

[コマンドライン](https://phishdestroy.github.io/TgWitness/ja/docs/reference/cli/)（プレビュー版）は、スクリプトやエージェントをアーカイブから読み込みます。

| 変数 | 効果 |
| --- | --- |
| `TGWITNESS_URL` | パネル発表の `tgwitness search`, `context`, `messages`, `stats` および `export`; デフォルト `http://127.0.0.1:8787` が設定されている場合 |
| `TGWITNESS_MCP_TOKEN` | **「統合」→「MCP」**から取得した接続トークンをアーカイブし、MCPクライアントと共有する。 `--token-file` 代わりにファイルから読み込む |
| `TGWITNESS_DATA` | URLやトークンが指定されていない場合は、データディレクトリから直接読み込む `--data-dir`、URL、またはトークンが指定されていない場合、データディレクトリから直接読み込みます |

## 実行前に確認してください

1行のコマンドは、初期スクリプトに対してHTTPSを信頼します。そのスクリプトは、インストール前に SHA-256およびアプリケーションと制約条件に対するプロジェクトのRSA署名を検証します。 また、最初に初期スクリプトをダウンロードして検証することも可能です。

公開リリースキーは [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub) です。 その SHA-256 は以下の通りです：

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

信頼できるリポジトリのリビジョンからこのフィンガープリントを保持してください。 同じダウンロードサーバーからのチェックサムにより不一致が検出されます。独立して信頼されている公開鍵が、 リリースの署名を認証するものです。

以下の検証用ダウンロードには、新しい空のディレクトリを使用してください。

**Linux / macOS — 新しい空のダウンロードディレクトリで実行してください**（curl および OpenSSL が必要です）：

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

`&&` ダウンロード、鍵のフィンガープリント、または署名の 検証に失敗した場合、チェーンは実行前に停止します。スクリプトのダウンロードと 署名の検証の間に公開が行われた場合は、両方を再度ダウンロードしてください。古いインストーラーは、不変のパッケージURLを維持します。

**Windows — 実行する前に、SHA-256を確認してください：**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

ハッシュ値を `install.ps1` 行と照合してください。独立した署名検証を行うには、 OpenSSL（例：Git Bashから）と、上記の同じ公開鍵フィンガープリントを使用してください：

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows へのインストール時、.NET によってパッケージの署名が検証されるため、 OpenSSL は必要ありません。これらは Authenticode ではなく、分離型 RSA-3072 / SHA-256 署名です。 [マニフェスト](https://get.destroy.tools/manifest.json)には、ソフトウェアのバージョン、 正確な Git コミット、不変のリリース ID、および各アーティファクトの SHA-256 が記録されています。このページには、 対応するソースへのリンクが掲載されています。マニフェストとチェックサム一覧にも、分離型 署名が付いています（`manifest.json.sig` および `SHA256SUMS.txt.sig`).

## 既存のインストールを更新する

**新しい公開版がダウンロードサイトを更新します。インストール済みのプログラムは、 インストーラーを再度実行すると更新されます。**無人更新機能や、 実行中のコレクションの自動再起動機能はありません。現在のインストーラーチャネルは**プレビュー版**であり、 公開済みで検証済みのビルドに基づいています。 `main`公開・検証済みのビルドに準拠しており、そのコミットは、直近の 番号付きGitHubリリースよりも新しい場合があります。ページのバージョンは `pyproject.toml`から取得されます。そのコミット およびビルドIDにより、同じプレビューバージョン内での更新が区別されます。

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

以前と同じインストールフォルダとOSユーザーを使用してください。コレクションを停止した状態で、データ ディレクトリ全体をバックアップしてください。 `tgwitness paths` これを識別します。署名付きエクスポート は、完全なインストールバックアップではありません。

**Ubuntuへのルートインストールは `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

インストールが正常に完了したら：

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Linux/macOSユーザーによるインストールでは、元の `TGWITNESS_INSTALL_DIR` 、または デフォルト設定を使用し、最初のインストールコマンドを再度実行してください。更新を行う前にフォアグラウンドの パネルを閉じ、更新後に再度起動してください。設定済みのLinuxユーザー サービスについては、その `tgwitness restart` コマンドを実行してください。

**Windows：**実行中のパネルを閉じ、Windows インストールコマンドを再度実行し、 その後、 `bin\tgwitness.cmd` 同じインストール環境で起動してください。インストーラーはデータ、 セッション、アクセス設定、署名鍵を保持します。新しい環境がチェックに合格した後にのみ ランチャーが切り替わります。インストールに失敗した場合は、以前の ランチャーがそのまま残ります。ストレージ形式の変更に備えて、アップグレード前のバックアップを保管しておいてください。

## Ubuntuでの日常的なコマンド

| コマンド | 結果 |
| --- | --- |
| `tgwitness open` | 現在のパネルURLとアクセスキー。 |
| `tgwitness paths` | プログラム、データ、およびガイドの正確なパス。 |
| `tgwitness guide --print` | オフラインでの操作手順。 |
| `tgwitness status` / `tgwitness logs` | 可用性／サービスログ。 |
| `tgwitness stop` / `tgwitness start` | サービスの停止／再開；データを保持します。 |
| `tgwitness token rotate` | 管理者キーを更新し、ブラウザのセッションを終了してください。 |
| `tgwitness tunnel off` | パブリック・クイックトンネルを無効にし、ローカルパネルは維持します。 |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | クイックトンネルリンクを作成する／そのアドレスを変更する。 |

同僚用トークン、セッション、IP制限については[「アクセス」](https://phishdestroy.github.io/TgWitness/ja/docs/reference/access/) を、 GitHubからCloudflareへのリリースワークフローについては「[インストーラーの公開](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) 」を参照してください。

## TgWitness を削除

アンインストーラーはありません。パネルを停止し、そのフォルダを削除してください。data フォルダを削除すると、ジャーナル、署名鍵、Telegramのセッション、および保存されたファイルが完全に消去されます。 その前に：

1. 必要なデータをエクスポートし（**[エクスポート] → [署名済みZIPをダウンロード]**）、署名鍵の フィンガープリントとチェックポイントは、このマシン以外の場所に保管してください。ワークスペース自体を保持するには、 データの収集を停止した状態で、データフォルダ全体をコピーしてください。
2. 「**Extras」→「Server 24/7」**で作成されたサーバーは、「**Your servers」**から削除するか、 `python -m tgwitness.cloud destroy`で作成されたサーバーは、「Your servers」から削除してください。削除されるまで、プロバイダーから課金されます。
3. Telegramの**「設定」→「デバイス」**から、各アカウントのセッションを終了してください。ファイルを削除しても、 Telegram側でのセッションはログアウトされません。

**Ubuntuへのルートインストール。**データフォルダに注意し、サービスを停止してから、 サービス、フォルダ、およびショートカットを削除してください：

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux または macOS ユーザー向けのインストール手順。**パネルを閉じます。設定済みの Linux ユーザーサービスは 次のコマンドで停止します `systemctl --user disable --now tgwitness-<ID>`で停止されます。その単位は `~/.config/systemd/user/`です。その後、 `~/.local/share/tgwitness` （またはご使用の `TGWITNESS_INSTALL_DIR`）と `~/.local/bin/tgwitness` ショートカットを削除してください。

**Windows。**パネルを閉じ、 `%LOCALAPPDATA%\TgWitness` （または `TGWITNESS_INSTALL_DIR`）を削除してください。インストーラーは、サービス、スケジュールされたタスク、ショートカットを追加しません。
