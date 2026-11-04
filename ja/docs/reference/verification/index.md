# テスト済みの内容

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/verification/

Telegramのライブテスト、自動チェック、ブラウザチェック、および未検証のまま残っている事項について。

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | カウント |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| 確認 | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Telegramのライブテスト、アカウント全体 · 2026年10月29日

以下のテスト後も、同じアカウントは引き続き稼働していました。10月29日 12:10 UTC に、その対象範囲が アカウント全体（チャンネル、グループ、プライベートチャット、ボット）に切り替えられました。パネルが 確認を求めたところ、署名付きジャーナルにその記録が保存されました。17:59 UTC 時点で、ジャーナルには以下の内容が記録されていました：

| 記録期間：10月27日 21:36 ～ 10月29日 17:59（UTC） | カウント |
| --- | --- |
| ジャーナルの記録 | 9,968 |
| 新しいメッセージ | 5,308 |
| アカウント全体への切り替え後のそれらの内容 | 3,878 |
| 削除 | 784 |
| TgWitnessがメッセージを保存した後、そのうちの一部が削除されました | 596 |
| 編集 | 41 |
| 再確認により追加されたメッセージ | 2,273 |
| 再確認を行っても見つからなくなったメッセージ | 18 |
| 履歴スナップショットによって保存されたメッセージ | 242 |
| 保存された添付ファイル | 247 |
| コレクターの起動 | 19 |
| Telegram FloodWaitの一時停止 | 26 |

- 当パネルの「**Verify」**チェックにより、9,968件の記録すべてについて、署名およびハッシュチェーンが確認されました。
- メッセージは、2つのグループまたはチャンネル、および3つのプライベートチャットとボットから送信されました。「メッセージ」ボタンが **チャット**から1回押されました。そのリクエストとTelegramからの応答は、ジャーナルに記録されています。
- コレクターが再起動時にアカウントを再スキャンした際、新しいチャットが追加されました。新しいチャットの 以前のメッセージの保存はオフ（`history = 0`）になっていたため、ここでは扱いません。

対象外：反応、メンバーシップの変更、人物プロフィール、メッセージの送信、招待による参加、 プロキシ、通知、witnessボット、および複数のアカウントの同時利用。公開ファイルには 集計数のみが含まれます。

## libarchive を使用して開くパスワード保護されたエクスポートファイル · 2026年10月29日

エクスポート暗号化コードによって作成されたアーカイブ（WinZip AES-256、7-ZipおよびWinRARが 読み取れる形式）を、Windowsの`tar`（bsdtar 3.6.2、libarchive）で開きました。 正しいパスワードを入力したところ、 抽出されたファイルのSHA-256ハッシュ値は元のものと一致しました。間違ったパスワードを入力した場合は、「Incorrect passphrase」というメッセージが表示され、受け入れられませんでした。7-ZipおよびWinRAR自体は実行されませんでした。

## Telegram ライブテスト · 2026年10月27日～29日

1つの実際のTelegramアカウントが、組み込みのAPIペアプールを通じてログインし、 **10月27日21:36（UTC）から10月29日05:15（UTC）までの間**、1つのスーパーグループを記録しました。この期間中、 コレクターは12回起動されました。

| 記録済み | カウント |
| --- | --- |
| ジャーナル記録（ハートビートおよびサービス記録を含む） | 2,385 |
| 新しいメッセージ | 1,291 |
| 削除 | 472 |
| TgWitnessがテキストを保存した後、それらのうち削除されたもの | 347 |
| 編集 | 12 |
| 停止中に見逃されたメッセージは、再チェックによって追加されました | 12 |
| 保存された添付ファイル | 17 |
| 添付ファイルがダウンロードされませんでした（ダウンロードがオフになっているか、ダウンロードするファイルがありません） | 14 |
| Telegram FloodWaitは、再チェックの際にそれぞれ3秒間、一時停止します。 | 8 |

- 全2,385件のレコードの署名およびハッシュチェーンは、ジャーナルの 公開鍵に対して検証可能です。
- 再起動後、コレクターは保存された更新状態（`pts`）から処理を再開し、Telethon が遅れを取り戻します。その後、再チェックによって、まだ欠落しているメッセージが追加されます。
- 各FloodWaitにおいて、コレクターは指定された時間待機した後、処理を続行しました。
- そのアカウントはログイン状態が維持され、10月29日に同じセッションが再接続されました。

本テストの対象外：複数のアカウントの同時処理、管理者権限、プロキシ、 数時間を超えるサービス停止、および完全な[ライブ受入手順](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)。 公開ファイルには以下の情報のみが含まれます：アカウントやチャットの識別子、メッセージ、 認証情報は一切含まれません。

## 合成による現地能力測定

コマンド：`python tools/check_capacity.py --events 10000 --chats 100`

| 指標 | 観測されました |
| --- | --- |
| 入力 | 100の選定された合成情報源にわたる、10,000件の合成メッセージイベント |
| メッセージ本文 | 400文字；メディアやネットワークに関する記述は含まれません |
| データ取り込み | 53.273秒；187.7イベント/秒 |
| ハンドラの遅延 | p50 4.162 ms; p95 7.784 ms; 最大 129.118 ms |
| ZIP形式でのエクスポート | tracemalloc を有効にした場合、19.868 秒 |
| Pythonのexport割り当てのピーク値の追跡 | 0.51 MiB；RSSは処理されません |
| ZIPファイルのサイズ | 4,610,962 バイト |
| 独立した検証 | 10,000件のイベントすべてが検証済みです |

これは、このWindowsホスト上のローカルな連続記録／エクスポートパスを測定するものです。 MTProtoによる配信、同時接続アカウント数、Telegramによる通信制限、メディア、 長時間実行されるワークロード、または保証された実際のチャット数については 測定対象外です。この測定は、 測定されたメッセージパスに影響を与えない最終的なオフラインタイムスタンプツールが導入される前のものです。

## 残りの資格要件

保存されたライブジャーナルには、実際の収集状況、編集、削除通知、添付ファイル、 再確認、およびレート制限の処理が記録されます。 ただし、配信の網羅性や、 役割ごとの可視性、反応主体、長期にわたるFloodWait、アカウントの停止、および ネットワーク／プロセスの中断からの復旧に関する管理マトリックスについては、記録の対象外となります。QRトークンの発行は、完了した モバイルQR確認とは区別されます。

Dockerによるビルド／実行、Linux／macOSへのインストール、持続的な高負荷への対応、独立したセキュリティ レビュー、真に独立したTSA対応、証明書の失効／アーカイブの検証、および フォレンジック認証については、本ドキュメントに記載された認定範囲外となります。保存されたMTProtoの状態 およびキャッチアップ機能は実装されていますが、アトミックかつ耐久性のあるリプレイ機能については、まだ確立されていません。 管理ログの 収集、追加のリアクターリスト、および優先度の高いショートポーリングは、引き続き別個の機能として扱われます。 管理された認定マトリックスについては、[ライブ受入テスト](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)をご参照ください。

ローカルに保存された詳細な記録やスクリーンショットは、test-results/ ディレクトリに格納されています（Gitでは無視されています）。 docs/assets/ ディレクトリ内の公開用スクリーンショットには、架空のデモデータのみが含まれています。
