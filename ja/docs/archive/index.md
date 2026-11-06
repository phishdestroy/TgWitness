# Telegram · アーカイブの操作

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/archive/

メッセージを見つけ、出典を確認し、証拠を構築する。

01**履歴を取り込む**

有効なソースの過去のメッセージをワークスペースに取り込みます。

02**情報源を参照**

検索し、各ヒットの元になった保存済みメッセージを開きます。

03**引き継ぎ内容を明確にする**

分析は 1 つのファイルに、署名付きの証拠はその隣に置きます。

記録されたデータ、認識されたテキスト、および分析者の結論は、それぞれ明確に区別されています。

## 過去のメッセージを読み込む

1. **ソース → 対象範囲のチャット**：有効なチャットを確認し、観察を開始します。
2. **全履歴を読み込む**。その時点のソース一覧がそのまま使われます。
3. **履歴の一時停止** / **履歴の再開**はいつでも可能です。再起動後は手動で再開してください。
4. ソースごとの結果とダウンロードキューを確認し、署名付きの進捗レポートをエクスポートと一緒に保管します。

これはワークスペースを埋めるためのものです。単一チャットの HTML/JSON エクスポートは別物です。[詳細](https://phishdestroy.github.io/TgWitness/ja/docs/reference/history/)。

## まずは検索し、その後AIの利用を判断する

1. **ジャーナル**はローカルで検索し、ソースと時間で絞り込めます。
2. フレーズやドメインを検索し、記録とその版を開きます。
3. AI を使う場合は、管理者が**連携機能**でプロバイダーを設定します。その後**アーカイブに問い合わせる**でチャットと期間を選び、**モデルに送信されるデータ**を見て、外に出すべきでないもののチェックを外します。
4. 引用を確認し、回答をレポートとして保存し、メモを加えます。

検索に AI は不要です。レポートは署名付きジャーナルとは別に、出典と改訂を保持します。[プロバイダーの設定](https://phishdestroy.github.io/TgWitness/ja/docs/reference/analysis/)。

## 必要な接続方法を選択してください

| タスク | 開く | セットアップ |
| --- | --- | --- |
| 選んだチャットを AI クライアントに読ませる | **連携機能 → MCP** | [MCP をインストールし、範囲限定トークンを作って接続する](https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/) |
| 保存されたメディア内のテキストを認識する | `media.saved`レコード → **添付ファイルを認識** | [ローカルの Docker ワーカーを設定する](https://phishdestroy.github.io/TgWitness/ja/docs/reference/media-analysis/) |
| イベントを n8n または SIEM に送信する | **連携機能 → 送信用ウェブフック** | [受信先を追加し、HMAC を確認し、ID の重複を除く](https://phishdestroy.github.io/TgWitness/ja/docs/reference/webhooks/) |

**どのアクセストークンをどこに設定すればよいですか？**

パネルへのアクセスは人のためのものです。MCP には専用の読み取り専用トークン、webhook には専用の HMAC シークレットがあります。どれも Telegram セッションは不要です。

[パネルのアクセス権を共有](https://phishdestroy.github.io/TgWitness/ja/docs/access/)するか、[MCPクライアントを設定してください](https://phishdestroy.github.io/TgWitness/ja/docs/reference/mcp/)。

## 情報源と結論を提示する

レポートは署名付き ZIP の隣に置いてください。レポートはあなたによるソースの読み解きで、受け取った人が検証するのは ZIP です。

[エクスポートと検証](https://phishdestroy.github.io/TgWitness/ja/docs/exports/) · [調査の全過程を網羅する](https://phishdestroy.github.io/TgWitness/ja/docs/cases/)
