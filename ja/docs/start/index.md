# 数分で始められます

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/start/

まずは、動作例をご覧ください。その後、ご自身のアカウントを連携させてください。

## アカウントなしでサイトをご覧いただけます

プロジェクトをダウンロードまたはクローンし、**Python 3.11 以降を**インストールして、デモを実行してください。ランチャーがローカル環境を作成し、指定された依存関係をインストールします。

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

ブラウザを開くと、架空のメッセージが含まれたワークスペースが表示されます。会話を開き、編集内容を比較し、エクスポートされたデータを検証してください。デモモードではTelegramには接続されません。

![TgWitnessの会話画面とメッセージ例](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

ワークスペースの例です。ご自身のジャーナルは別途開始されます。

## 独自のワークスペースを開始しましょう

デモプロセスを終了してから、通常のランチャーをご利用ください：

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

ランチャーに表示されるローカルアドレスを開いてください。求められた場合は、ターミナルに表示されたローカルファイル内の**パネルアクセストークンを入力**してください。これにより TgWitness のロックが解除されます。これは Telegram のログインとは別のものです。

## 最初のメッセージを記録しましょう

1. [専用のTelegramアカウントを連携してください。](https://phishdestroy.github.io/TgWitness/ja/docs/accounts/)
2. アカウントがアクセス可能なグループまたはチャンネルを選択し、監視を開始してください。
3. ご自身が管理するテストグループに新しいメッセージを送信し、それがジャーナルに表示されることをご確認ください。

サーバーへのインストールについては、「[Keep it running」](https://phishdestroy.github.io/TgWitness/ja/docs/server/)の手順に従ってください。
