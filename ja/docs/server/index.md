# 稼働を継続してください

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/server/

コレクターを動かし続け、再起動してもデータを安全に保ちます。

## 起動方法を選択してください

ネイティブ：[ランチャー](https://phishdestroy.github.io/TgWitness/ja/docs/start/)と [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) のサービステンプレート。Docker の場合は、プロジェクトのフォルダーで：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

パネルは localhost:8787 で待ち受けます。ローカルか SSH トンネル経由で開き、2 つ目のコマンドで得たトークンを使います。

## データディレクトリ全体を保持してください

ネイティブ：`data/live`。Docker：`tgwitness-data` ボリューム。ジャーナル、セッション、鍵はひとまとまりです。署名付きエクスポートは証拠であって、バックアップではありません。

1. まず収集を停止します。
2. データディレクトリ全体を、ホスト以外の安全な場所にコピーします。
3. 信頼する前に、別のインストールで復元を試します。

## 再起動後にご確認ください

ワークスペースと鍵、接続、ソース、新しいメッセージが届いているかを確認します。TgWitness が取り戻すのは Telegram にまだ残っているものだけで、停止中に起きたすべてではありません。

コンテナーが「healthy」なのは Web サーバーが応答しているという意味です。収集が動いているかは、テストメッセージと証人でわかります。

## 意図した内容のみを公開してください

HTTPS、ボリューム、更新、復元はデプロイのリファレンスにあります。実際にテストした内容：[検証記録](https://phishdestroy.github.io/TgWitness/ja/docs/reference/verification/)。
