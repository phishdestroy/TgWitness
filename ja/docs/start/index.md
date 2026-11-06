# Telegram · 数分で始められます

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/start/

まずデモを触ってみて、それから自分のアカウントを接続してください。

## アカウントなしでサイトをご覧いただけます

プロジェクトを入手し、**Python 3.11 以降**を用意して、デモを起動します。残りはランチャーが準備します。

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

架空のメッセージが入ったワークスペースがブラウザーで開きます。チャットを開き、編集を比べ、エクスポートを見てください。Telegram は関係しません。

![TgWitnessの会話画面とメッセージ例](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

ワークスペースの例です。ご自身のジャーナルは別途開始されます。

## 独自のワークスペースを開始しましょう

デモを閉じてから：

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

ランチャーが表示するアドレスを開き、示されたファイルにある**パネルアクセストークン**を貼り付けます。これは TgWitness 用で、Telegram 用ではありません。

## 最初のメッセージを記録しましょう

1. [専用のTelegramアカウントを連携してください。](https://phishdestroy.github.io/TgWitness/ja/docs/accounts/)
2. グループかチャンネルを選び、観察を開始します。
3. テストグループでメッセージを送り、ジャーナルに表示されるのを確認します。

サーバーへのインストールについては、「[Keep it running」](https://phishdestroy.github.io/TgWitness/ja/docs/server/)の手順に従ってください。
