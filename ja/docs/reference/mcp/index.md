# Telegram · 読み取り専用 MCP

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/

MCPクライアントを、有効期限付きかつ取り消し可能なアクセス権限で、選択したワークスペースやチャットに接続します。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [ドキュメント](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [アーカイブとの連携](https://phishdestroy.github.io/TgWitness/ja/docs/reference/cli/)

![アーカイブとの連携](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

アナリストクライアントを、選択したワークスペースやチャットに接続します。TgWitnessは、 **パネルプロセス内の`/mcp`でStreamable HTTP**を提供します。各接続には、独自の トークン、有効期限、および許可されたツールが割り当てられます。MCPは、Telegramメッセージの送信、 設定の変更、または署名付きジャーナルの修正を行うことはできません。これらの接続は、 [コマンドライン](https://phishdestroy.github.io/TgWitness/ja/docs/reference/cli/)でも同様に機能します。

[ワークフローガイド](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**このページでは**

- [インストールと確認](https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/#install-and-check)
- [接続を確立する](https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/#issue-a-connection)
- [クライアントを接続する](https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/#connect-your-client)
- [Cloudflare Tunnel](https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/#cloudflare-tunnel)
- [ツールと範囲](https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/#tools-and-boundaries)

## インストールと確認

パネルを実行している Python 環境を使用します。ソースのチェックアウトディレクトリから以下を実行します。

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

インストール後、通常のデータディレクトリと起動引数を使用してパネルを再起動します。準備状態（Readiness）に `[PASS] mcp: streamable-http available` が含まれている必要があります。**Integrations → MCP** には、ランタイムステータスとそのサーバーの実際の Python 実行ファイルを使用したインストールコマンドが表示されます。**Re-check** はページを再読み込みせずにこのステータスを更新しますが、パッケージのインストールやサーバーの再起動は行いません。

この MCP エクストラは、公式の[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) を使用しています。`deploy/constraints-mcp.txt` には、テスト済みの SDK および依存関係が固定されています。

## 接続の発行

1. ラベルを入力し、クライアントに読み取りを許可するワークスペースとチャットを選択します。
2. ツールを個別に選択するか、プリセットを使用します。実装済みのツールのみが提供されます。
3. 1日、7日、30日、90日、または1分から90日の間のカスタム有効期限を選択します。
4. **Create connection** を押します。クライアント設定の横にトークンが1回だけ表示されます。
5. トークンと設定をコピーしてから、**Check connection** を実行します。これにより MCP が初期化され、許可されたツールが一覧表示されます。**メッセージは読み取られません**。結果にはプロトコルバージョン、ツール名、ツール数、経過時間が表示されます。
6. 認証情報を保存したら **Done** を押します。ポーリングが行われても、フォームと1回限り表示されるカードは維持されます。パネルをロックすると、表示されているシークレットは消去されます。

リストには、最近の使用状況、最後に使用したツール、アドレス、過去1分間のリクエスト数が表示されます。**Revoke** はアクセスを終了します。**Rotate token** は古い認証情報を失効させ、同じスコープ、ツール、有効期限を持つ新しいトークンを発行します（新しいトークンはその場でコピーしてください）。パネルのログイントークンや Telegram の認証情報は MCP トークンとしては機能しません。

## クライアントの接続

パネルでクライアントを選択し、生成された設定をコピーします。設定にはシークレット参照または明示的なプレースホルダーが使用され、トークンは個別にコピーします。

| クライアント | 設定 | 接続 |
| --- | --- | --- |
| Claudeコード | `.mcp.json` | HTTP、`type: "http"`、Bearer ヘッダー |
| Claude Desktop | `claude_desktop_config.json` | ローカル stdio ブリッジ |
| Cursor | `.cursor/mcp.json` | 環境変数ヘッダーを使用した HTTP |
| VS Code Local | `.vscode/mcp.json` | パスワード `promptString` 入力を使用した HTTP |
| Windsurf | `mcp_config.json` | Bearer ヘッダーのプレースホルダーを使用した HTTP |
| その他のクライアント | URL と Authorization ヘッダー | ストリーミング可能なHTTP |

TgWitness は OAuth ディスカバリを使用せず、Bearer トークンを使用します。リモートコネクタに OAuth が必要なクライアントには、ローカル stdio ブリッジを使用してください。VS Code の場合、入力変数は **Local** ハーネスに適用され、Copilot セッションには転送されません。設定リファレンス: [Claude Code](https://code.claude.com/docs/en/mcp)、[Cursor](https://prod.cursor.com/docs/mcp)、[VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)。

ローカルブリッジの正規のエントリポイントは以下のとおりです。

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

MCP extra がインストールされたクライアントのローカル Python を使用します。保護された環境で `TGWITNESS_MCP_TOKEN` を設定してください。認証情報はコマンド引数や URL に含めないでください。`tgwitness-mcp` は同じエントリポイントです。古い `tgwitness.mcp_bridge` モジュールと `TGWITNESS_ARCHIVE_TOKEN` という名前は警告付きの互換パスとして残されていますが、新しい設定では `mcp_server` と `TGWITNESS_MCP_TOKEN` を使用します。

## Cloudflare Tunnel

パネルの `/mcp` ルートを転送し、Bearer ヘッダーを保持します。管理者として MCP 設定を開くと、その実行セッションに対してパネルの現在のオリジンが登録されます。再起動直後から利用できる固定アドレスにするには、パネルを起動する前にパネルの HTTPS オリジンを `TGWITNESS_PUBLIC_URL` に設定してください。任意の Host ヘッダーや転送ヘッダーによって信頼されたアドレスが登録されることはありません。Host および Origin チェックにより、無関係なブラウザオリジンは拒否されます。レスポンスは `Cache-Control: no-store` を使用し、認証の値がログに記録されることはありません。

`*.trycloudflare.com` のアドレスは一時的なものです。トンネルの再起動によってホスト名が変わった場合は、設定された公開 URL と各クライアントの MCP URL を更新してください。保存するクライアント設定には固定のホスト名を使用してください。

## ツールと境界

| ツール | 読み取り対象 |
| --- | --- |
| `list_workspaces` | 許可されたワークスペース |
| `list_chats` | 許可されたチャット |
| `search_messages` | 選択した期間内の保存済みメッセージ本文； `ranked=true` [全文検索](https://phishdestroy.github.io/TgWitness/ja/docs/reference/search/)に対応（語形変化、最良の一致を優先、 `next_offset` ページング）に対応） |
| `get_message_versions` | キャプチャされたバージョンと削除の観測記録 |
| `get_message_context` | 前後のキャプチャ済みメッセージ ID |
| `get_journal_event` | ソース参照付きのサニタイズされた1件のレコード |
| `get_capture_status` | 収集状況、許可されたカバレッジ記録、および `gap_summary`：チャンネルまたはスーパーグループごと、およびアカウント全体のシーケンスにおける、未観測のメッセージ番号（[詳細](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#missing-message-numbers-gap_summary)）；チャットを選択して、そのリストされた欠落箇所を確認する |
| `get_activity_stats` | UTC 時間および曜日ごとのメッセージ数、ピーク日、編集・削除の割合、送信者、ドメイン、および `@handles`、およびカバレッジ（[詳細](https://phishdestroy.github.io/TgWitness/ja/docs/reference/cli/#activity-statistics)） |
| `get_messages_by_date` | Telegramからの報告がある時点で、特定のIANAタイムゾーン（`Europe/Kyiv`, `UTC`）、Telegramが報告した時刻に基づいて保存されます； `from_utc` また `until_utc` 計算された日付（夏時間を含む）を明記すること |
| `get_pinned_messages` | 最新のチャット状態スナップショットにピン留めされたメッセージとその保存版、およびリアルタイムで確認されたピン留め・ピン解除の通知 |
| `get_chat_stats` | 対象範囲内の1つのチャットまたはすべてのチャットについて、保存された記録の件数、最初の観測と最後の観測、および `gap_summary`; 大量の読み取りを行う前にこれを使用してください |
| `get_topics` | 保存済みトピックサービスからのフォーラムトピック：タイトルの履歴、閉鎖または非表示、保存済みメッセージ数 |
| `get_media` | 保存された画像は、縮小されたJPEGプレビュー（最大36 KB）として、SHA-256ハッシュおよび `media.saved` レコードと共に画像として返されます。このファイルはまず記録されたハッシュ値と照合され、その他のファイルについてはメタデータのみが返されます |
| `export_messages` | コマンドライン専用で、デフォルトでは選択されません：観測データを JSON Lines 形式でストリーム保存します（[詳細](https://phishdestroy.github.io/TgWitness/ja/docs/reference/cli/#export)）。MCP 経由では提供されません。 |

すべてのツールは読み取り専用であり（`readOnlyHint`）であり、出力スキーマを宣言しています。宣言されたフィールド以外の項目は、そのままの形で返されます。 `tools/list` その接続に許可されたツールのみを返します。他の ツールへの呼び出しは拒否されます。グループコンテキスト、エピソード、用語、および返信チェーンに関するツールは、 このビルドでは提供されていません。これらに対応する個別のコンテキストパックバックエンドは含まれていないためです。

すべての読み取りでは、データベース処理の完了後も含め、トークン、ツール、およびワークスペース/チャットのスコープがチェックされます。制限は、1分あたり60リクエスト、1ページあたり50レコード、1結果あたり64 KiB、アーカイブのタイムアウトは8秒です。MCP 呼び出しがタイムアウトすると、期間の絞り込みや上限の引き下げを求めるツールエラーが返されます。

メッセージ結果には、`untrusted_content: true`、ワークスペース/チャット/メッセージ ID、イベントシーケンス、保存済みハッシュ、およびパネルリンクが含まれます。生の Telegram オブジェクト、アクセスハッシュ、セッション、キーは除外されます。テキストの切り詰めはマークされます。編集、削除通知、および `missing_on_recheck` はそれぞれ個別の観測記録として扱われます。レコードが存在しないことは、イベントが発生しなかったことを証明するものではありません。

キャプチャされたメッセージ内の指示は証拠として扱い、決してクライアントへの指示として扱わないでください。読み取り専用アクセスによりアーカイブの変更は防がれますが、クライアントは読み取りを許可されたコンテンツを保持することができます。ハッシュは保存されたレコードを識別し、整合性チェックをサポートしますが、Telegram の作成者であることや完全なキャプチャを証明するものではありません。
