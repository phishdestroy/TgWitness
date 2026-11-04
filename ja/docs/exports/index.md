# エクスポートと検証

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/exports/

相手が自分であなたのワークスペースと照合できるファイルを渡します。

参照情報を保持する署名付きZIPファイルをエクスポート受信者が検証します

署名やチェックポイントは初めてですか？[サンプルの記録を変更して](https://phishdestroy.github.io/TgWitness/ja/docs/concepts/#chain)、どの確認が検出するかを見てください。

収集者とは別の場所にコピーを保管したいですか？ [S3の設定](https://phishdestroy.github.io/TgWitness/ja/docs/exports/#s3)、[オブジェクトロック](https://phishdestroy.github.io/TgWitness/ja/docs/exports/#s3-retention)、または[検証済み復元](https://phishdestroy.github.io/TgWitness/ja/docs/exports/#s3-restore)をご覧ください。

## 信頼できる参考資料としてご利用ください

ワークスペースの鍵のフィンガープリントは、コレクター以外の場所に書き留めてください。収集中は署名付きチェックポイントも別の場所に保管するか、[独立した証人](https://phishdestroy.github.io/TgWitness/ja/docs/witness/)を動かしてください。受け取った人は、それを使って鍵とジャーナルの以前の状態を確認します。

## 署名付きZIPファイルをダウンロードする

**エクスポート** → 署名付き証拠 ZIP。ジャーナル全体と署名付きのファイルマニフェストが含まれます。読みやすいレポートは [Report studio](https://phishdestroy.github.io/TgWitness/ja/docs/reports/) で整えるか、選んだデータだけを[引き渡し用抽出](https://phishdestroy.github.io/TgWitness/ja/docs/handover/)として送ります。

HTML、PDF、JSON のレポートにはそれぞれ封印があります。CSV は作業用のコピーにすぎません。完全性が必要なら、検証済み ZIP 内の CSV を使ってください。

## 信頼できるTgWitnessのコピーで検証してください

プロジェクトの環境で、自分のフィンガープリントとパスを使って：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

合格すると `key_pinned: true` と `checkpoint_checked: true` が表示されます。その出力はアーカイブの隣に保管してください。チェックポイントはエクスポートの末尾またはそれより前でなければなりません。

## 検証結果を使用する

- **ファイル：**マニフェストがハッシュを、署名がジャーナルを結び付けます。どんな変更も表に出ます。
- **同一性：**保管しておいたフィンガープリントが、想定どおりの鍵であることを証明します。
- **以前の状態：**チェックポイントが、引き渡し前に保存したジャーナルの先頭部分とエクスポートを比べます。
- **カバレッジ：**欠落、取得結果、送信 → 編集 → 削除のテストが、この構成で実際に記録できたものを示します。

詳細：[検証で証明できること、できないこと](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#verification-scope)。

## S3 オフサイトコピーの設定

ワークスペースの**エクスポート → オフサイトコピー**。AWS S3 と S3 互換ストレージで使えます。ジャーナルのセグメント、保存したファイル、タイムスタンプ付きのチェックポイント、完了したチャットエクスポートをコピーし、それぞれコレクターを出る前に `AES-256-GCM` で暗号化します。

オンラインデモではこれらの操作が表示されますが、アップロードは無効です。本物の認証情報は自分のインストールでだけ入力してください。

[![オフサイトコピーに関する完全な説明パネル：エンドポイント、リージョン、バケット、アクセスキー、スケジュール、オブジェクトロック、および復旧キーの設定](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

高度なオプションを展開した完全なパネルです。ストレージの認証情報は表示されていません。

| 分野 | 入力内容 |
| --- | --- |
| エンドポイント | ストレージの URL。バケットのパスや認証情報は含めません。例：`https://s3.example.invalid`。 |
| 地域 | プロバイダーの要件に合わせます。既定は `us-east-1`。 |
| バケット | 書き込める既存のバケット。例：`example-case-backup`。 |
| バケット内のフォルダ | プレフィックス。既定は `tgwitness`。その上にワークスペースごとのプレフィックスが付きます。 |
| アクセスキーID / シークレットアクセスキー | 両方そろえて入力し、Vault に保存されます。後で両方を空欄にすれば、そのまま維持されます。 |
| パス形式のアドレス | オン：`endpoint/bucket`。オフ：`bucket.endpoint`。プロバイダーによります。 |
| コピー間隔 | 1〜1,440 分、既定は 5。アプリが動いている間だけです。 |
| オブジェクトロックの保持期間 | バケットが Object Lock に対応していれば、日数とモード。0 はバケットの既定値を維持します。 |

1. バケットを作成し、**オフサイトコピーを保持する**のチェックを外したまま保存先と認証情報を入力して、**オフサイトコピーを保存**を押します。
2. **接続テスト**は暗号化したテストオブジェクトをアップロードします。
3. **暗号化キーのダウンロード**を行い、コレクターから離れた場所に保管します。鍵がなければ復元できません。
4. **オフサイトコピーを保持する**にチェックを入れて保存し、**今すぐコピー**するか、スケジュールに任せます。

## 保存状況とコピー進捗の確認

**詳細オプション**で保持日数と `GOVERNANCE` または `COMPLIANCE` を選びます。TgWitness はアップロードしたオブジェクトから保持設定を読み戻し、確認済み、未設定、確認失敗のいずれかを知らせます。

パネルには前回の実行、オブジェクト数、バイト数、コピー済みのジャーナルの境界、エラーが表示されます。ローカルファイルがない場合は報告され、次回再試行されます。残りはコピーを続けます。

アップロードは直接接続、SOCKS5、HTTP のいずれかを通ります。MTProxy のみのルートでは、コピーはエラーのまま待機します。

## 復元キーは別の場所に保管してください

鍵の JSON には、復号キー、保存先、プレフィックス、鍵のフィンガープリントが入っています。復元にはこれと、読み取り権限のあるストレージの認証情報が必要です。

エンドポイント、バケット、プレフィックスを変えた場合は、鍵をもう一度ダウンロードしてください。新しい保存先で新たなコピーが始まり、古いチャットエクスポートは元の場所に残ります。

## 別のマシンでの復元と検証

信頼できる TgWitness のインストール、鍵の JSON、読み取り専用のストレージ認証情報、空のフォルダーが必要です：

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

まず非公開の一時フォルダーですべてを確認します：ジャーナル全体、チェックポイント、ファイルのハッシュとサイズ。危険なパス、矛盾するセグメント、チェックポイントより短いジャーナルは失敗となり、その場合は何も書き出されません。

成功すると `events.jsonl`、`media/`、`checkpoints/`、`exports/` が得られます。コマンドの JSON 出力も一緒に保管し、自分で保管したチェックポイントや証人の記録と比べてください。
