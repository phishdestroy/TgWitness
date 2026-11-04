# 테스트된 내용

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/

실시간 텔레그램 테스트, 자동화된 점검, 브라우저 점검 및 아직 검증되지 않은 사항.

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

## 나머지 자격 요건

보관된 실시간 저널은 실제 수집 내역, 수정 내역, 삭제 알림, 첨부 파일, 재확인 및 속도 제한 처리를 기록합니다. 단, 이 기록은 전송 내역의 완전한 추적이나 역할별 가시성, 반응 주체, 장기간의 FloodWait, 계정 차단 및 네트워크/프로세스 중단 복구와 관련된 통제된 매트릭스를 보장하지는 않습니다. QR 토큰 발급은 완료된 모바일 QR 확인과는 별개로 처리됩니다.

Docker 빌드/실행, Linux/macOS 설치, 지속적인 고부하 처리, 독립적인 보안 검토, 실질적인 독립적 TSA 대응, 인증서 취소/보관 검증 및 포렌식 인증은 기록된 인증 범위에서 제외됩니다. 저장된 MTProto 상태 및 캐치업 기능은 구현되었으나, 원자적 내구성 재재생 기능은 아직 확립되지 않았습니다. 관리자 로그 수집, 추가 리액터 목록 및 우선순위 단기 폴링은 별도의 기능으로 남아 있습니다. 제어된 자격 매트릭스에 대한 [실시간 승인](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) 내용을 참조하십시오.

세부적인 로컬 영수증 및 스크린샷은 test-results/ 디렉터리에 있습니다(Git에서 무시됨). docs/assets/에 있는 공개 스크린샷에는 가상의 데모 데이터만 포함되어 있습니다.
