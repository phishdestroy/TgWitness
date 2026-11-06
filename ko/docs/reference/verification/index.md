# 테스트된 내용

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/

실시간 텔레그램 테스트, 자동화된 점검, 브라우저 점검 및 아직 검증되지 않은 사항.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [문서](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | 결과 | 범위 |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | 기록 | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| 확인 | 결과 | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Phala Cloud 라이브 배포 · 2026년 11월 4일

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| 설정 | Recorded value |
| --- | --- |
| 제공자 | Phala Cloud · `tdx.small` · US-WEST-1 |
| 배포 | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

처음 두 번의 배포에서 시뮬레이션된 Phala Cloud와 5가지 차이점이 발견되었습니다. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py)는 이제 각 차이점을 재현하며, 수정 사항이 없으면 실패합니다:

| Phala Cloud에서 | 수정 전 | 수정 |
| --- | --- | --- |
| `compose_file.name`가 필요합니다 | HTTP 422, 아무것도 생성되지 않음 | Docker Compose 구성에는 CVM 이름이 포함됩니다. |
| 빈 값이 지정되지 않은 경우, Phala는 측정 대상 app-compose에 자체 사전 실행 스크립트를 추가합니다(v0.0.20: Docker 로그인, `docker compose pull`, 루트 비밀번호, `user_config`의 SSH 키). | `tdx_compose` 오류: 게시된 Docker Compose 구성 외부의 코드 | app-compose가 `pre_launch_script`를 `""`로 설정하면, Phala는 이를 제외합니다 |
| `image`가 없으면 Phala는 SSH 액세스가 활성화된 개발용 빌드인 `dstack-dev-0.5.12`를 선택합니다. | `server_state`가 실패합니다. 이 이미지에서는 하드웨어 인증 기록만 통과했으며, 제공자 기록과 `tdx_os`에만 해당 내용이 표시됩니다. | 배포 시 Phala의 현재 릴리스인 `dstack-0.5.12`의 프로덕션 빌드를 요청합니다. |
| dstack 게이트웨이가 꺼져 있는 상태에서는 CVM 세부 정보에 `instance_id`가 표시되지 않습니다. | 배포가 30분 동안 대기한 후 실패합니다 | 인스턴스 ID는 CVM 상태에서 읽어옵니다. |
| 재시작, 중지 및 시작은 CVM 작업이며, 애플리케이션 수정 사항이 아닙니다. | `provider_actions`에는 재시작 내역이 표시되지 않았습니다. | 읽기 작업도 수행됩니다. |

**Deployment 3 · attestation, access checks and restart evidence**

- CVM은 SSH 액세스를 비활성화한 상태에서 `dstack-0.5.12`를 실행했습니다. 수집기는 생성 후 약 1.5분 후에 서명된 주소를 게시했습니다. 이후 배포는 `tdx_binding`, `tdx_quote`(Intel TCB UpToDate, 하드웨어 증명 기록 v4, FMSPC `20a06f000000`, 디버그 모드 아님, 마이그레이션 불가, Intel에서 가져온 암호화 검증 데이터 지원), `tdx_compose_hash`, `tdx_compose`(바이트 단위) 및 `tdx_identity`(KMS 키)를 통과했습니다.
- trycloudflare.com 주소의 패널은 토큰이 없거나 잘못된 토큰을 입력했을 때 401을 반환했고, 패널 토큰을 입력했을 때는 200을 반환했습니다.
- `verify`에서 `--source`는 GitHub의 커밋 아카이브로 설정되었으며, 지문은 별도로 통과되었습니다: 서버, `server_state`, 방화벽(게이트웨이 없음, 공용 엔드포인트 없음), 공급자 로그, 명세서, 지문, 소스 해시, 부팅 및 5가지 `tdx_*` 검사가 통과되었습니다. Cloudflare 및 `tdx_os`는 사용할 수 없었으므로 결과는 'INCOMPLETE'로 나타났습니다.
- Phala의 API를 통해 두 번 재시작: 매번 CVM은 2분 이내에 동일한 수집기 키, 새로운 서명된 주소, 그리고 530 응답을 반환하는 기존 주소와 함께 복구되었습니다. `verify`는 새로운 부팅과 두 번의 재시작을 모두 REVIEW로 보고했습니다. `--evidence`를 통해 저널 서명과 세 번의 시작이 확인되었으며, 각 시작마다 동일한 CVM에서 생성된 고유한 Intel TDX 하드웨어 인증 기록이 있었습니다.
- `destroy`는 해당 CVM만 제거했습니다. 그 후 작업 공간은 비어 있었고, 패널 주소는 응답을 중단했습니다.
- 패널 마법사의 가격 확인 결과, `tdx.small`의 시간당 요금은 0.058달러로 표시되었습니다. 잘못된 키를 입력했을 때는 단순히 "API 키를 수락하지 않았습니다"라는 메시지가 표시되었습니다.

**Follow-up fixes · signed address discovery and OS measurements**

- 주소 키가 없으면, `verify`는 주소 주제에 대한 가장 최근의 올바른 형식의 게시물을 따랐는데, 이는 게시된 Docker Compose 구성에 인쇄되어 있습니다. 한 건의 위조된 게시물이 이를 존재하지 않는 호스트로 보냈고, `statement`는 실패했습니다: 위조자는 수집자로 위장할 수는 없었지만, 제3자 검증을 최대 12시간 동안 위조된 미래 타임스탬프를 사용하여 차단할 수 있었습니다. 이제 수집기는 자신의 키로 서명된 주소 게시물도 올리며, `verify`는 수집기가 직접 작성한 게시물만 수용하며, 게시물은 ntfy.sh의 수신 시간 순으로 정렬됩니다. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py)는 위조된 게시물을 재실행합니다. CVM은 이를 포함하는 커밋에서만 이 코드를 실행하므로, 이번 실행의 수집기는 아직 자신의 주소에 서명하지 않았고 `verify`가 이를 알렸습니다.
- `tdx_os`는 `dstack-mr` 없이는 실행할 수 없었습니다. 해당 도구의 현재 버전에는 문서에 나온 `measure --json` 대신 `measure-os`가 있습니다. 검증기는 이제 공개된 이미지와 ACPI 테이블을 포함한 VM 구성으로부터 MRTD 및 RTMR0-2를 직접 계산합니다.

**Deployment 4 · all 16 checks, report seals and restart verification**

- Deploy는 게시된 `dstack-0.5.12`를 한 번 다운로드하여 CVM이 보고한 OS 이미지 해시와 대조한 결과, `tdx_os`가 통과되었습니다: MRTD, RTMR0, RTMR1 및 RTMR2 값이 QEMU 8.2.2, 1 vCPU 및 2 GiB 조건에서 계산된 값과 일치했습니다. 동일한 계산에서 4 GiB, 2 vCPU, QEMU 9.2.1 또는 두 번째 네트워크 카드를 지정했을 때는 다른 RTMR0 값이 산출되었으며, 커널, 펌웨어 또는 명령줄이 변경된 경우 및 개발용 이미지의 경우에는 테스트에 실패했습니다.
- `verify`는 퀵 터널의 커넥터를 포함하여 16가지 검사 항목을 모두 통과했으므로, 결과는 PASS였습니다. 이 시스템은 HTML 및 PDF 인증서를 생성했으며, 벨기에 정부의 타임스탬프 기관인 TSU 202301(벨기에 신뢰 목록에 등재된 상태)에서 발급한 적격 eIDAS 타임스탬프, FreeTSA 타임스탬프 및 검증자의 서명으로 디지털 봉인했습니다. `check-report`는 이 모든 항목과 PDF의 서명을 확인했습니다.
- 재시작 후, `verify --evidence`는 두 번의 시작을 확인했으며, 각 시작 시 CVM 내에서 생성된 하드웨어 인증이 동반되었고, 각각 게시된 `dstack-0.5.12`에서 부팅되었습니다. 재시작과 새로운 부팅 모두 REVIEW 상태였습니다.
- `destroy`는 작업 공간을 비워 두었습니다.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- 수집기는 운영자의 HMAC 게시물 바로 옆에 자체 키로 서명된 주소를 게시했습니다. 그 후 해당 토픽에 두 개의 위조된 게시물이 추가되었는데, 하나는 HMAC 값이 0으로 설정된 것이고 다른 하나는 다른 Ed25519 키로 서명된 것이었으며, 둘 다 2096년의 시간을 주장하고 있었습니다. `verify`는 수집자 키로 서명된 주소를 가져와 16가지 검사 항목을 모두 통과했습니다. 이 인장에는 다시 한 번 벨기에의 공인 타임스탬프, FreeTSA의 타임스탬프 및 검증자의 서명이 포함되어 있었으며, `check-report`가 이를 확인했습니다.
- 재시작 후, 수집기가 서명된 새 주소를 게시했습니다: `verify`가 이를 즉시 발견했고, 운영자의 **는 현재 주소를 찾았으며,**는 HMAC 게시물로부터 27초 후에 이를 확인했고, 둘 다 위조된 게시물을 무시했습니다. `verify --evidence`는 `dstack-0.5.12`에서 부팅된 두 대의 기기를 확인했습니다.
- 배포 결과에는 Phala가 CVM에 청구하는 금액(디스크 포함)이 표시되었습니다: 시간당 $0.06078.

### Panel wizard and remaining scope

패널 마법사는 Phala Cloud에서 두 번 실행되었습니다. 한 번은 작업 API를 통해, 다른 한 번은 실제 Chromium을 사용하는 브라우저를 통해 실행되었습니다: 가격 확인, **Advanced** 아래의 커밋을 통한 생성, 6가지 인증 검사 모두 통과, 청구 가격(월 44.37 USD)이 표시된 서버 목록, **Find 현재 주소**, 측정된 Docker Compose 구성 다운로드 및 삭제. 브라우저에서는 페이지 오류가 발생하지 않았습니다. 매번 작업 공간은 그 후 비어 있었습니다.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | 개수 |
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

| 확인 | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## 실시간 텔레그램 테스트, 전체 계정 · 2026년 10월 29일

아래 테스트 이후에도 해당 계정은 계속 운영되었습니다. 10월 29일 12:10 UTC에 기록 범위가 계정 전체(채널, 그룹, 비공개 채팅 및 봇)로 전환되었으며, 패널에서 확인을 요청하자 서명된 기록부에 해당 내용이 기록되었습니다. 17:59 UTC 기준 기록부에는 다음과 같은 내용이 포함되어 있었습니다:

| 기록 기간: 10월 27일 21:36 ~ 10월 29일 17:59 (UTC) | 개수 |
| --- | --- |
| 저널 기록 | 9,968 |
| 새 메시지 | 5,308 |
| 전체 계정으로 전환한 후의 내용 | 3,878 |
| 삭제 내역 | 784 |
| TgWitness가 메시지를 저장한 후 삭제된 메시지들 | 596 |
| 수정 사항 | 41 |
| 재검토를 통해 추가된 메시지 | 2,273 |
| 재확인 과정에서 더 이상 찾을 수 없었던 메시지 | 18 |
| 기록 스냅샷을 통해 저장된 메시지 | 242 |
| 저장된 첨부 파일 | 247 |
| 수집기 시작 | 19 |
| Telegram FloodWait 일시 중지 | 26 |

- 패널의 **‘Verify’** 검사를 통해 총 9,968건의 기록에 대한 서명과 해시 체인이 모두 확인되었습니다.
- 메시지는 2개의 그룹 또는 채널과 3개의 비공개 채팅 및 봇에서 전송되었습니다. **채팅에서** 메시지 버튼이 한 번 눌렸으며, 해당 요청과 텔레그램의 응답이 저널에 기록되어 있습니다.
- 컬렉터가 재시작 시 계정을 다시 스캔하면서 새로운 채팅이 추가되었습니다. 새로운 채팅의 이전 메시지 저장은 비활성화되어 있었으므로(`history = 0`), 여기서는 다루지 않습니다.

다루지 않는 내용: 반응, 회원 변경, 인물 프로필, 메시지 전송, 초대 를 통한 가입, 프록시, 알림, 위트니스 봇 및 여러 계정의 동시 사용. 공개 파일에는 단순한 집계 수치만 포함됩니다.

## libarchive로 열 수 있는 비밀번호로 보호된 내보내기 파일 · 2026년 10월 29일

내보내기 암호화 코드(WinZip AES-256, 7-Zip 및 WinRAR이 읽을 수 있는 형식)로 생성된 아카이브를 Windows `tar`(bsdtar 3.6.2, libarchive)로 열었습니다. 올바른 암호를 입력했을 때 추출된 파일의 SHA-256 해시값은 원본과 일치했으며, 잘못된 암호를 입력했을 때는 "Incorrect passphrase"라는 오류 메시지가 표시되었습니다. 7-Zip과 WinRAR 자체는 실행되지 않았습니다.

## 텔레그램 실시간 테스트 · 2026년 10월 27일~29일

내장된 API 쌍 풀을 통해 로그인된 하나의 실제 텔레그램 계정이 **10월 27일 21:36 UTC부터 10월 29일 05:15 UTC까지** 하나의 슈퍼그룹을 기록했습니다. 이 기간 동안 수집기는 12회 실행되었습니다.

| 기록됨 | 개수 |
| --- | --- |
| 하트비트 및 서비스 기록을 포함한 저널 기록 | 2,385 |
| 새 메시지 | 1,291 |
| 삭제 내역 | 472 |
| TgWitness가 해당 텍스트를 저장한 후 삭제된 것들 | 347 |
| 수정 사항 | 12 |
| 중지된 동안 누락된 메시지는 재검사를 통해 추가됨 | 12 |
| 저장된 첨부 파일 | 17 |
| 첨부 파일이 다운로드되지 않았습니다(다운로드 기능이 꺼져 있거나 다운로드할 파일이 없음). | 14 |
| Telegram FloodWait는 재확인 과정에서 각각 3초씩 일시 정지합니다. | 8 |

- 총 2,385건의 기록에 대한 서명과 해시 체인은 저널의 공개 키를 통해 검증됩니다.
- 재시작 후, 수집기는 저장된 업데이트 상태(`pts`)에서 작업을 재개하고 Telethon이 누락된 메시지를 보충한 뒤, 재검사를 통해 아직 누락된 메시지를 추가합니다.
- 각 FloodWait에서 수집기는 요청된 시간을 기다린 후 작업을 계속했습니다.
- 계정은 로그인 상태가 유지되었으며, 10월 29일에 동일한 세션이 다시 연결되었습니다.

이번 테스트에서 다루지 않은 사항: 여러 계정 동시 처리, 관리자 역할, 프록시, 몇 시간 이상 지속되는 서비스 중단, 그리고 전체 [실시간 승인 절차](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). 공개 파일에는 다음 항목만 포함됩니다: 계정 또는 채팅 식별자, 메시지, 인증 정보는 포함되지 않습니다.

## 합성 지역 역량 측정

명령어: `python tools/check_capacity.py --events 10000 --chats 100`

| 지표 | 관찰됨 |
| --- | --- |
| 입력 | 선별된 100개의 가상 출처에서 발생한 10,000건의 가상 메시지 이벤트 |
| 메시지 본문 | 400자; 미디어 또는 네트워크 관련 내용 없음 |
| 데이터 수집 | 53.273초; 초당 187.7건 |
| 핸들러 지연 시간 | p50 4.162 ms; p95 7.784 ms; 최대 129.118 ms |
| ZIP 파일로 내보내기 | tracemalloc 활성화 시 19.868초 소요 |
| 추적된 Python export 할당량의 최대치 | 0.51 MiB; RSS 처리 불가 |
| ZIP 파일 크기 | 4,610,962 바이트 |
| 독립적인 검증 | 총 10,000건의 이벤트가 검증되었습니다. |

이 측정값은 해당 Windows 호스트의 로컬 순차 기록/내보내기 경로를 나타냅니다. 이 측정값은 MTProto 전송, 동시 계정 수, 텔레그램 전송 제한, 미디어, 장시간 지속되는 워크로드 또는 실제 채팅 건수를 보장하지 않습니다. 이 측정값은 최종 오프라인 타임스탬프 도구가 도입되기 전의 것으로, 해당 도구는 측정된 메시지 경로를 변경하지 않습니다.

## 100만 건의 메시지에 대한 전체 텍스트 검색 · 2026년 11월 5일

명령어: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

200개의 채팅에서 생성된 1,000,000개의 합성 메시지(러시아어 어형, 우크라이나어, 영어, 중국어, 일본어, 링크 및 핸들 포함)로 구성된 결정론적 서명된 저널이 71초 만에 색인화되었으며, 1.50 GiB 크기의 저널 외에도 색인 파일로 58 MiB가 추가로 사용되었습니다. 최적 일치 검색은 9~190 ms(중앙값)가 소요되었으며, 이는 이전의 부분 문자열 검색에 소요되던 2.4~3.2초와 대비됩니다. 전체 결과, 하드웨어 및 제한 사항: [전체 텍스트 검색](https://phishdestroy.github.io/TgWitness/ko/docs/reference/search/#benchmark). `tools/test_fulltext.py` 또한 현재 검증기를 사용하여 전체 텍스트 검색 (`tools/fixtures/evidence-before-fulltext.zip`)를 현재 검증기로 검증하고, 현재 아카이브를 해당 아카이브 자체의 `verify.py`.

## 나머지 자격 요건

보관된 실시간 저널은 실제 수집 내역, 수정 내역, 삭제 알림, 첨부 파일, 재확인 및 속도 제한 처리를 기록합니다. 단, 이 기록은 전송 내역의 완전한 추적이나 역할별 가시성, 반응 주체, 장기간의 FloodWait, 계정 차단 및 네트워크/프로세스 중단 복구와 관련된 통제된 매트릭스를 보장하지는 않습니다. QR 토큰 발급은 완료된 모바일 QR 확인과는 별개로 처리됩니다.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
