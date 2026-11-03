# 証拠の仕組みをご覧ください

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/concepts/

メッセージは変更される可能性があります。しかし、あなたが確認した内容の記録は、いつでも検証可能な状態で残しておく必要があります。

以下の2つの小規模な実験をご覧ください。これらは架空のメッセージを使用しており、ブラウザ上で動作し、Telegramには一切接続しません。

## チャットのエクスポートから検証可能な記録へ

[Telegram Desktopのエクスポート機能は、](https://telegram.org/blog/export-and-more)利用可能なチャット履歴やメディアをHTMLまたはJSON形式で保存し、オフラインでの利用を可能にします。TgWitnessは、受信した変更の継続的な記録、観察結果やエクスポートに対する署名、および受信者が独自に照合できるチェックポイントを追加します。

| タスク | Telegram Desktopからのエクスポート | TgWitness |
| --- | --- | --- |
| 保存された会話を読む | HTML または JSON（選択されたメディアを含む） | 保存されたチャット、検索可能なログ、オフラインレポート |
| 経時的な変化を追跡する | エクスポート時に利用可能な履歴 | 以前にキャプチャされたバージョン、その後の編集内容、および削除の記録がまとめて保持されます |
| 引き渡し後のファイルを確認してください | 標準の HTML/JSON エクスポートファイルには署名がありません | 署名付きマニフェスト、レコードごとの署名、および信頼できるコレクターキーと照合された封印済みのHTML/PDF/JSONレポート |
| 以前の保存状態と比較する | 参照用コピーまたはハッシュ値を別途保管してください | 署名付きチェックポイント、独立したウィットネス、およびオプションの外部タイムスタンプ |

ファイル署名の比較は、2026年11月2日に確認された[Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output)の[エクスポート](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output)ライターに基づいています。TgWitnessはコレクターの鍵を使用して署名を行います。以下のチェックでは、受信者がそれをどのように使用するかを示しています。

## 1つのメッセージ、3つの観察点

Telegramから新しいメッセージ、編集通知、削除通知が届くと、コレクターはこれら3つの観測結果を個別に追加します。編集が行われても、最初の記録は上書きされません。削除通知があっても、その記録は消去されません。

01 / メッセージの経路説明用のシーケンス

Telegram delivers an update to the collector, which appends a journal record. · Telegram · コレクター · ジャーナル · 更新 → · 追加 →

現在のチャット画面 メッセージ #42

メッセージが削除されました

そのメッセージはチャット画面から消えました。

観察記録 3件の記録

1. 01

   `message.new`

   10:00に集合してください。

   ✓
2. 02

   `message.edited`

   11:00にお会いしましょう

   ✓
3. 03

   `message.deleted`

   #42 に関する削除通知

   ✓

記録された3つの観察事項はすべて、ジャーナルに残ります。

すでに選択済みのソースに対する簡略化された手順です。運用記録も実際のジャーナルと共有されます。記録内容は、アカウントが閲覧できる範囲およびTelegramが配信する内容によって異なります。

削除通知には、信頼できる削除時刻も、メッセージを削除した人物も記載されていません。これらの情報を不明なままにしておくことで、観察と推測との区別が保たれます。

## 記録を変更する。ハッシュを追跡する。

各レコードには、前のレコードのハッシュが含まれています。そのレコード自身のハッシュは、そのリンクを含むイベントフィールド全体をカバーしています。外部に保持されたチェックポイントは、特定のジャーナルの長さと先頭ハッシュを固定します。

02 / HASH-CHAIN SANDBOX実際の SHA-256 · 記録例

記録 01**メッセージを受信しました**`h₁ = SHA-256(e₁)`64個のゼロへのリンク

RECORD 02**11:00にお会いしましょう**`h₂ = SHA-256(e₂)`h₁を含みます

RECORD 03**削除が確認されました**`h₃ = SHA-256(e₃)`h₂を含みます

他所に保存済み**3件の記録 · ヘッダー `h₃`**この固定境界を、提供されたジャーナルと比較してください。

イベントを変更すると、そのハッシュが変更されます。チェーンを再構築すると、その先頭が変更されます。末尾を削除すると、残されたチェックポイントよりも短くなります。

**記録 2 および完全なハッシュを確認してください**

これは、この例でハッシュ化された正確な UTF-8 JSON です。値は架空のものであり、9 つのフィールドとシリアライゼーションはジャーナルのフォーマットと一致しています。

```

```

保存された記録 2 のハッシュ

``

レコード2のハッシュを再計算しました

``

このサンドボックスでは、署名ではなくハッシュを計算します。実際の検証ツールでは、各イベントの Ed25519 署名、シーケンス、およびリンクもチェックされます。ハッシュを再構築するだけでは、信頼された鍵の下で有効な署名を作成することはできません。

## 実際のルールを数行でまとめると

HASH + 署名

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C**は、9つのイベントフィールドをUTF-8形式のJSONとしてシリアライズします。キーはソート済みで、余分な空白はなく、ASCIIエスケープもNaN/無限大も含まれません。イベントの`previous_hash`はhi−1です。表示されているh0は64個のゼロ文字を意味し、署名は32バイトの生のダイジェストをカバーしています。

9つのフィールドは、`seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、`payload`、`previous_hash`です。これはTgWitnessで[規定されているJSONエンコーディング](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#event-canonicalization)です。ハッシュおよび署名自体は、ハッシュ入力フィールドではありません。

保持されたチェックポイント

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

固定されたコレクターキーの下にあるチェックポイントの署名を検証し、その境界を検証済みのジャーナルと比較してください。後のエクスポートにはより多くのレコードが含まれている可能性がありますが、それらは依然として以前のチェックポイントで一致している必要があります。

## 3つの質問、3つの異なる確認手順

[01 / 完全性**この記録は変更されましたか？** ハッシュ値と署名は、別途信頼された鍵を用いて検証してください。](https://phishdestroy.github.io/TgWitness/ja/docs/exports/)[02 / 継続性**以前にはどのような内容が記載されていましたか？** 署名付きエクスポートデータを、別の証人が保持しているチェックポイントと比較してください。](https://phishdestroy.github.io/TgWitness/ja/docs/witness/)[03 / 提供**これらのテストイベントは届きましたか？** 各アカウントのジャーナルと照合し、送信、編集、削除の操作を管理します。](https://phishdestroy.github.io/TgWitness/ja/docs/cases/)

署名を使用して保存された記録を確認し、チェックポイントを使用して以前の境界と比較し、制御された配信テストを使用して収集状況を測定してください。それぞれが特定の疑問に答えるものです。[検証範囲と信頼の前提条件をよくお読みください。](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#verification-scope)

[アカウント全体の調査](https://phishdestroy.github.io/TgWitness/ja/docs/cases/)を、取得から事件資料のまとめまで追跡します。

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
