# 証拠の仕組みをご覧ください

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/concepts/

メッセージは変わります。あなたが見たものの記録は変わるべきではなく、誰でもそれを確認できるべきです。

以下は小さな実験が 2 つです。メッセージは架空で、すべてブラウザー内で動き、Telegram には何も送られません。

## チャットのエクスポートから検証可能な記録へ

[Telegram Desktop のエクスポート](https://telegram.org/blog/export-and-more)は、今見えている履歴を HTML または JSON で保存します。TgWitness はそこに、変更を記録し続けるジャーナル、すべての記録への署名、他の人が照合できるチェックポイントを加えます。

| タスク | Telegram Desktopからのエクスポート | TgWitness |
| --- | --- | --- |
| 保存された会話を読む | HTML または JSON（選択されたメディアを含む） | 保存されたチャット、検索可能なログ、オフラインレポート |
| 経時的な変化を追跡する | エクスポート時に利用可能な履歴 | 旧版、後の編集、削除をすべて保持 |
| 引き渡し後のファイルを確認してください | 標準の HTML/JSON エクスポートファイルには署名がありません | 署名付きマニフェスト、署名付き記録、封印されたレポートを、信頼できる鍵で確認 |
| 以前の保存状態と比較する | 参照用コピーまたはハッシュ値を別途保管してください | 署名付きチェックポイント、独立したウィットネス、およびオプションの外部タイムスタンプ |

この比較は 2026 年 11 月 2 日時点の [Telegram Desktop のエクスポートコード](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output)に基づいています。

## 1つのメッセージ、3つの観察点

新しいメッセージ、編集、削除は 3 つの別々の記録になります。編集は最初の記録を上書きせず、削除も消しません。

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

Telegram は、誰がいつメッセージを削除したかを正確には伝えません。TgWitness は推測せず、その欄を空のままにします。

## 記録を変更する。ハッシュを追跡する。

どの記録にも直前の記録のハッシュが入っています。別の場所に保管したチェックポイントが、ジャーナルの長さと最後のハッシュを固定します。

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

**C** は 9 つのイベント項目を UTF-8 JSON にしたものです：キーはソート済み、余分な空白なし、ASCII エスケープなし、NaN/無限大なし。`previous_hash` は hi−1、h0 は 64 個のゼロで、署名はダイジェストの生の 32 バイトを対象とします。

項目：`seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、`payload`、`previous_hash`。完全な仕様：[イベントのエンコード](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#event-canonicalization)。

保持されたチェックポイント

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

固定した鍵でチェックポイントの署名を確認し、それからジャーナルと比べます。後のエクスポートは長くなってもかまいませんが、チェックポイントの位置で一致していなければなりません。

## 3つの質問、3つの異なる確認手順

[01 / 完全性**この記録は変更されましたか？** 信頼できる鍵でハッシュと署名を確認します。](https://phishdestroy.github.io/TgWitness/ja/docs/exports/)[02 / 継続性**以前にはどのような内容が記載されていましたか？** エクスポートを、証人が保管したチェックポイントと比べます。](https://phishdestroy.github.io/TgWitness/ja/docs/witness/)[03 / 提供**これらのテストイベントは届きましたか？** テストメッセージを送信・編集・削除し、各アカウントが何を記録したかを見ます。](https://phishdestroy.github.io/TgWitness/ja/docs/cases/)

署名は「変更されたか」、チェックポイントは「以前のものと一致するか」、テストメッセージは「すべて記録できたか」に答えます。[検証で証明できること、できないこと。](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#verification-scope)

次は：開始からケースパッケージまでの[アカウント全体の調査](https://phishdestroy.github.io/TgWitness/ja/docs/cases/)。

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
