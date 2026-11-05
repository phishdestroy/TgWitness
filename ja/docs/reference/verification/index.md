# テスト済みの内容

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/verification/

Telegramのライブテスト、自動チェック、ブラウザチェック、および未検証のまま残っている事項について。

## Phala Cloud へのライブデプロイ · 2026年11月4日

`--provider phala --quick-tunnel`は、実際の**Phala Cloud**（`tdx.small`、リージョン US-WEST-1）に対して実行され、空のワークスペースのPhala Cloud APIキー、実際のntfy.sh、GitHub、およびIntel PCSが使用されました。 CVMにはコミット`df7d860c`（v0.8.1）がインストールされました。デプロイ、検証、および破棄は、以下の修正を加えてコマンド ラインから実行されました。7台のCVMの合計費用は約1.9米セントでした。

最初の2回のデプロイでは、シミュレートされたPhala Cloudとの間に5つの相違点が検出されました。 [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py)は現在、それぞれを再現しており、修正を施さないと失敗します：

| Phala Cloud にて | 修正前 | 修正 |
| --- | --- | --- |
| `compose_file.name` が必要です | HTTP 422、何も作成されませんでした | Docker Compose の構成には、CVM 名が含まれています |
| 空の値が指定されない限り、Phalaは測定対象のapp-composeに独自のpre-launchスクリプトを追加します（v0.0.20：Dockerログイン、`docker compose pull`、rootパスワード、`user_config`からのSSHキー） | `tdx_compose` が失敗します：公開された Docker Compose 構成の範囲外のコードが含まれています | app-compose は `pre_launch_script` を `""` に設定していますが、Phala はこの設定を省略しています |
| `image`が指定されていない場合、PhalaはSSHアクセスが有効な開発ビルドである`dstack-dev-0.5.12`を選択します | `server_state` は失敗しました。このイメージでは、ハードウェア認証レコードのみが合格しました。プロバイダーレコードと `tdx_os` のみがそれを示しています。 | デプロイでは、Phalaの現在のリリースである`dstack-0.5.12`のプロダクションビルドが求められます。 |
| dstackゲートウェイがオフの状態では、CVMの詳細に`instance_id`が表示されることはありません。 | デプロイは30分待機した後、失敗します | インスタンスIDはCVMの状態から読み取られます |
| 再起動、停止、起動はCVMの操作であり、アプリケーションの更新ではありません。 | `provider_actions`には再起動の記録はありませんでした | これらの操作には読み取り操作も含まれます |

3回目のデプロイ：

- CVMは、SSHアクセスを無効にした状態で`dstack-0.5.12`を実行しました。コレクターは、作成から約 1.5分後に署名付きアドレスを投稿しました。その後、デプロイは`tdx_binding`、`tdx_quote`（Intel TCB UpToDate、ハードウェアアテステーションレコードv4、FMSPC `20a06f000000`、デバッグモードではない、移行不可、Intelから取得した暗号検証データを サポート）、`tdx_compose_hash`、`tdx_compose`（バイト単位）、および`tdx_identity`（KMSキー）を順次通過しました。
- trycloudflare.com のアドレスにあるパネルは、トークンがない場合や誤ったトークンを指定した場合は 401 を返し、 パネル用トークンを指定した場合は 200 を返しました。
- `verify` について、`--source` は GitHub のコミットアーカイブに設定され、フィンガープリントは 個別に合格しました：サーバー、`server_state`、ファイアウォール（ゲートウェイなし、パブリックエンドポイントなし）、プロバイダーログ、 明細書、フィンガープリント、ソースハッシュ、ブート、および 5 つの `tdx_*` チェックが合格しました。 Cloudflare および `tdx_os` は利用できなかったため、結果は「INCOMPLETE」となりました。
- PhalaのAPIで二度再起動しました。毎回、CVMは二分以内に復旧し、コレクターの鍵は同じまま、新しい署名付きアドレスが発行され、以前のアドレスは530を返しました。`verify`は新たな起動と両方の再起動をREVIEWとして報告しました。`--evidence`ではジャーナルの署名と三回の起動を確認し、それぞれに同じCVM内で生成されたIntel TDXのハードウェア認証記録が付いていました。
- `destroy` コマンドは、その CVM のみを削除しました。その後、ワークスペースは空になり、パネルのアドレスは 応答しなくなりました。
- パネルのウィザードで料金を確認すると、`tdx.small`は時間あたり0.058ドルと表示されました。無効なキーを入力すると、「APIキーが受け入れられませんでした」という簡潔なメッセージが表示されました。

さらに2つの発見があり、その後修正されました：

- アドレスキーがない場合、`verify`は、アドレスに関するトピックで最も新しい、形式が正しい投稿に従いました。 この投稿は、公開されたDocker Compose構成に印刷されています。ある偽造された投稿により、存在しないホストへ送信され、 `statement`は失敗しました。偽造者はコレクターになりすますことはできませんでしたが、 第三者による検証を、偽造された将来の日時スタンプを用いて最大12時間までブロックすることができました。現在、コレクターは 自身の鍵で署名されたアドレスも投稿しており、`verify`は、 コレクターが投稿したそのような投稿のみを受け入れ、投稿はntfy.shの受信時刻順に並べ替えられます。 [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py)は、偽造された投稿を再実行します。CVMは これを、それを含むコミットからのみ実行するため、今回の実行におけるコレクターはまだ自身のアドレスに署名しておらず、 `verify`はその旨を報告しました。
- `tdx_os`は`dstack-mr`なしでは実行できませんでした。このツールの現行バージョンには、文書に記載された`measure --json`ではなく`measure-os`が含まれています。検証ツールは現在、公開されたイメージとACPIテーブルを含むVMの構成から、MRTDとRTMR0-2を直接計算します。

4回目のデプロイでは、以下の内容を含みます：

- デプロイでは、公開された `dstack-0.5.12` を一度ダウンロードし、CVM が 報告した OS イメージのハッシュと照合しました。その結果、`tdx_os` は合格しました：MRTD、RTMR0、RTMR1、および RTMR2 は、QEMU 8.2.2、1 vCPU、2 GiBの環境で計算された値と一致しました。同じ計算でも、4 GiB、2 vCPU、 QEMU 9.2.1、または2枚目のネットワークカードが指定された場合は異なるRTMR0値となり、カーネル、ファームウェア、またはコマンドラインが変更された場合や 開発用イメージでは失敗しました。
- `verify`は、クイックトンネルのコネクタを含め、16項目のチェックをすべて通過したため、結果は 「PASS」となりました。 HTMLおよびPDF形式の証明書が作成され、署名とタイムスタンプによってデジタル封印されました。タイムスタンプには、 ベルギー政府のタイムスタンプ機関TSU 202301（ベルギーの信頼リストに 登録済み）によるeIDAS認定タイムスタンプ、FreeTSAタイムスタンプ、および検証者の署名が使用されました。`check-report`はこれらすべて およびPDFの署名を確認しました。
- 再起動後、`verify --evidence` は 2 回の起動を確認しました。それぞれ、CVM 内で生成されたハードウェア認証を伴い、それぞれ 公開された `dstack-0.5.12` から起動されました。再起動と新しい起動は、いずれも REVIEW でした。
- `destroy` では、ワークスペースは空の状態になりました。

5回目のデプロイでは、コミット `53a0f7e9` からのコレクターを実行しました。これには上記のすべてが含まれています：

- コレクターは、オペレーターの HMAC 投稿の隣に、自身の鍵で署名されたアドレスを投稿しました。 その後、このトピックに 2 件の偽造投稿が追加されました。1 件は HMAC が 0 に設定されており、もう 1 件は別の Ed25519 鍵で署名されたもので、いずれも 2096 年の時刻を主張していました。 `verify`は、 コレクターの鍵で署名されたアドレスを取得し、16のチェックすべてに合格しました。このシールには、再びベルギーの認定タイムスタンプ、 FreeTSAのタイムスタンプ、および検証者の署名が記載されており、`check-report`がこれらを確認しました。
- 再起動後、コレクターは署名付きの新しいアドレスを投稿しました：`verify`は即座にそれを検出しました。 オペレーターの**は現在のアドレスを特定し、**はHMAC投稿から27秒後に検出しましたが、両者とも 偽造された投稿を無視しました。`verify --evidence`は、`dstack-0.5.12`から起動した2つのインスタンスを確認しました。
- デプロイ処理は、PhalaがCVMに請求するディスク料金込みの金額を表示しました。時間あたり0.06078ドルです。

パネルウィザードは Phala Cloud に対して 2 回実行されました。1 回はジョブ API を通じて、もう 1 回は 実際の Chromium を使用したブラウザを通じてです。価格の確認、**Advanced** でのコミットによる作成、6 つの 認証チェックすべてに合格し、サーバーリストには請求価格（月額 44.37 米ドル）が表示され、 **Find 現在のアドレス**、測定済みのDocker Compose構成のダウンロード、および削除が行われました。ブラウザではページエラーは発生しませんでした。 その後、ワークスペースは毎回空の状態になりました。

対象外：Phala上のCloudflareドメイン、CVM上のTelegramアカウント、および`dstack-0.6.1` イメージ。ウィザードでの作成前の価格はPhalaのコンピューティング料金のみとなります。これは、APIがディスク 料金を既存のCVMに対してのみ指定しているためです。サーバー一覧には、作成後の請求価格が表示されます。

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
