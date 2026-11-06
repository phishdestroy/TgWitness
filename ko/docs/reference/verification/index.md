# 테스트된 내용

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/

실시간 텔레그램 테스트, 자동화된 점검, 브라우저 점검 및 아직 검증되지 않은 사항.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [문서](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [증거 및 검증](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/)

![증거 및 검증](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**2026년 11월 6일 업데이트.** 결과는 각 실행에 대해 기록된 개정판, 환경 및 워크로드와 연동됩니다. [현재 기능](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) 섹션에서는 사용 가능한 워크플로를 설명하며, 이 페이지에는 실제로 확인된 내용이 기록됩니다.

[성능 그래프](https://phishdestroy.github.io/TgWitness/docs/validation/) · [영문 감사 보고서](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [다운로드 가능한 측정 결과](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| 최신 증거 | 결과 | 범위 |
| --- | --- | --- |
| 릴리스 감사 · 11월 6일 | 1,461개의 핵심 테스트 통과; 37개의 플랫폼 테스트 건너뛰기 | 소스 `92e539af40d8`; 공개된 조사 결과 유지 |
| 최신 내보내기 · 11월 6일 | 127.713 및 141.781 레코드/초, 전체 사이클 | 서버당 계정 2개; WARP를 통한 텍스트 및 메타데이터 전송 |
| 보관된 아카이브 · 11월 6일 | 48개의 아카이브; 3,598,381개의 레코드 검증 완료 | 고정된 작업 공간 키를 기준으로 기존 아카이브를 확인함 |
| Trusted Live · 11월5일 | 보호된 CPU 기록 및 WARP 검사 | 공식 데스크톱 로그인 및 네이티브 내보내기 기능은 여전히 제한 없이 사용 가능합니다. |
| Phala / Intel TDX · 11월 4일 | 후속 실행에서16개의 검증자 점검 항목을 모두 통과했습니다. | 과거 배포 내역; CVM에는 텔레그램 계정이 없음 |

**이 페이지에서**

- [릴리스 감사 및 최신 내보내기 · 6년 11월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu 및 WARP · 5년 11월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Phala Cloud 실시간 배포 · 4년 11월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [실시간 서버 일지 목록 · 1년 11월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [최근 오프라인 및 오류 주입 검사 · 1년 11월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [실시간 텔레그램 테스트, 전체 계정 · 29년 10월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [libarchive를 사용하여 암호로 보호된 내보내기 파일 열기 · 29년 10월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [실시간 텔레그램 테스트 · 27년 10월 29일 ~ 2026일29](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [합성 로컬 용량 측정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#synthetic-local-capacity-measurement)
- [100만 건의 메시지에 대한 전체 텍스트 검색 · 5년 11월 2026일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [남은 자격 요건](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#remaining-qualification)

## 릴리스 감사 및 최신 내보내기 · 6년 11월 2026일

감사에는 소스 코드 v0.9.1( `92e539af40d8368d198ff5e040f1d876f2c1310e`)이 사용되었으며, 릴리스 버전은 `92e539af40d8-83e41104669e`입니다. 설치된 패키지에 대한 스모크 테스트는 세 대의 서버에서 통과되었습니다. 서명된 보고서는 당시 관찰된 상태를 그대로 반영합니다.

[![두 가지 새로운 워크로드에 대한 수집 및 전체 내보내기 비율](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| 작업량 | 기록 | 획득 | 전체 주기 | 전체 주기 비율 |
| --- | --- | --- | --- | --- |
| 서버 A · 계정 2개 | 27,030 | 189.043초 | 211.647초 | 127.713 레코드/초 |
| 서버 B · 계정 2개 | 29,299 | 182.513초 | 206.650초 | 141.781 레코드/초 |

두 내보내기 작업 모두 재개 기능 없이 시작되었으며, 첨부 파일과 아바타는 제외되었고, 중복되거나 재사용된 레코드 없이 완료되었습니다. 전체 주기에는 준비, 수집, 선별, 패키징 및 아카이브 검증 단계가 포함됩니다. 서버 A에서는 보호된 채팅 읽기 검사도 실행되었습니다. 서버 A에서 4건, 서버 B에서 3건의 FloodWait 이벤트가 적절히 처리되었습니다. 이러한 관찰 결과만으로는 일반적인 처리량 보장을 입증할 수 없습니다.

| 확인 | 결과 | 자격 요건 |
| --- | --- | --- |
| 핵심 pytest | 1,461개 통과 | 37개 플랫폼 생략 |
| 브라우저 / 브라우저 사용자 경험 / 증거 / 사이트 | 102 / 66 / 15 / 9 통과 | 이 프로그램들은 다른 테스트와 중복되며, 카운트 값은 합산되지 않습니다. |
| 캡처 애드온 | 124개 통과 | 필수 Chromium 샌드박스로 인해 차단된 세 가지 공식 웹 검사 |
| API 인증 | 269개 경로; 538건의 요청 통과 | 누락된 인증 정보 및 접근 권한 취소 |
| 보존된 아카이브 | 48개 중 48개 검증 완료 | 3,598,381개 레코드; 고정된 작업 공간 키 |
| 실시간 플릿 읽기 확인 | 40개 프로필 중 24개가 통과되었습니다 | 16개의 WARP 경로가 자격 요건을 충족하지 못했으며, 해당 프로필은 연결되지 않았습니다. |

[서명된](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md)보고서는 모든 공개된 조사 결과를 기록하며, 여기에는 감사 대상인 메인 빌드에는 포함되지 않은 미공개 비밀 채팅 스냅샷의 결함 3건이 포함됩니다. 이전의 [공개 기록 평가에서는](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) 다른 리비전과 워크로드를 사용했으므로, 해당 비율을 이번 비교 결과와 합산해서는 안 됩니다.

[고정된 키와 검증기를](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files) 사용하여 원본 보고서를 검증하십시오. 이 서명은 운영자의 보고서가 변조되는 것을 방지합니다. 이는 독립적인 인증, 텔레그램 작성자 증명 또는 GDPR 인증이 아닙니다.

## Trusted Live CPU Ubuntu 및 WARP · 5년 11월 2026일

유지된 통합 실행은 RunPod CPU 호스트 내부의 QEMU에서 CPU 전용 Ubuntu 24.04.5 게스트(4 vCPU, 8 GiB)를 사용했습니다. 수집기에는 `14e642a5`가, 검증에는 `02072461`가 사용되었습니다. 최종 수정 사항은 [PR #114](https://github.com/phishdestroy/TgWitness/pull/114)에 `755f78f6`로 병합되었으며, 해당 트리는 테스트된 PR 헤드와 일치했습니다. 이는 TEE가 아니었습니다.

- 실제 WARP 커넥터는 정상으로 보고되었으며, 프록시된 HTTPS에서는 WARP 및 게이트웨이가 활성화된 것으로 보고되었습니다. 세 개의 프로브가 동일한 출구 주소를 감지했으나, 이는 고정 IP를 보장하는 것은 아닙니다.
- WARP 연결을 끊자 프록시를 거친 요청이 실패했습니다. 게이트웨이 서비스에 대한 직접 HTTPS 접속은 거부되었습니다. 레코더 네임스페이스에서는 직접 IPv4/IPv6, 외부 DNS 및 Docker의 내장 UDP 리졸버가 차단되었습니다.
- 범위가 지정된 읽기 전용 제공자 토큰은 health/connections를 읽을 수 있었으나 커넥터 등록 토큰은 읽을 수 없었습니다. 서명된 제공자 관측 결과에는 명시적으로 사용할 수 없는 샘플이 포함되어 있었습니다. 위트니스는 운영자의 호스트에서 실행되었으므로, 이는 독립적인 제3자 보관 방식이 아닌 기록 및 보존 방식을 보여줍니다.
- 공식 데스크톱 버전이 인증되지 않은 환영 화면에 도달했습니다. 캡처 과정에서 보안이 적용된 키보드 입력이 거부되었습니다. 세 개의 H.264 디스플레이 세그먼트가 디코딩되었으며 해당 시계 오버레이가 검사되었습니다. 18개 이벤트로 구성된 프리플라이트 아카이브는 고정된 레코더 키 및 보존된 체크포인트와 대조하여 검증되었습니다.
- 최종 캡처 테스트는 Windows 및 Linux CI 환경에서 실제 Chromium/FFmpeg을 사용하여 114개 사례를 통과했습니다. 5개의 앵커 테스트와 종속성 권고 사항 점검도 모두 통과했습니다.

초기 2 vCPU/4 GiB 구성이 동시 이미지 빌드 부하로 인해 타임아웃이 발생하여 가드 기능을 통해 중단되었으며, 이는 성공으로 간주되지 않습니다. 수동 테스트 계정 로그인, 네이티브 채팅 내보내기, 실제 하이브리드 비교 및 텔레그램 측 로그아웃은 여전히 진행 중입니다. 제공된 텔레톤 세션은 가져오지 않았습니다. 첨부 파일, 자동 OCR, 로컬 drand BLS 검증 및 Trusted Live TDX 인증은 검증 기준을 충족하지 못했습니다.

## Phala Cloud 라이브 배포 · 2026년 11월 4일

**과거 결과:** 이후 배포 버전들은 인텔 TDX 및 퀵 터널을 포함한 16가지 검증자 점검을 모두 통과했습니다. 증거 재시작, 서명된 주소 탐지 및 보고서 타임스탬프는 별도로 점검되었습니다. 각 테스트 CVM은 실행 후 제거되었습니다.

| 설정 | 기록된 값 |
| --- | --- |
| 제공자 | Phala Cloud · `tdx.small` · US-WEST-1 |
| 배포 | `--provider phala --quick-tunnel`; 초기에는 빈 작업 공간 |
| 초기 수집기 | `df7d860c` · v0.8.1 |
| 모든 수정 사항이 반영된 수집기 | `53a0f7e9` |
| 프로덕션 게스트 | `dstack-0.5.12`; SSH 액세스 비활성화됨 |
| 외부 서비스 | ntfy.sh, GitHub 및 Intel PCS |
| 관측된 비용 | 7개의 CVM, 총합 약 1.9미국 센트; 과거 테스트 가격 |

아래 순서에서는 초기 오류, 수정 사항 및 완료된 검사를 구분하여 나열합니다. 이 CVM들에는 텔레그램 계정이 연결되어 있지 않았습니다.

**배포 1–2 · 제공자별 차이점 및 회귀 테스트**

처음 두 번의 배포에서 시뮬레이션된 Phala Cloud와 5가지 차이점이 발견되었습니다. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py)는 이제 각 차이점을 재현하며, 수정 사항이 없으면 실패합니다:

| Phala Cloud에서 | 수정 전 | 수정 |
| --- | --- | --- |
| `compose_file.name`가 필요합니다 | HTTP 422, 아무것도 생성되지 않음 | Docker Compose 구성에는 CVM 이름이 포함됩니다. |
| 빈 값이 지정되지 않은 경우, Phala는 측정 대상 app-compose에 자체 사전 실행 스크립트를 추가합니다(v0.0.20: Docker 로그인, `docker compose pull`, 루트 비밀번호, `user_config`의 SSH 키). | `tdx_compose` 오류: 게시된 Docker Compose 구성 외부의 코드 | app-compose가 `pre_launch_script`를 `""`로 설정하면, Phala는 이를 제외합니다 |
| `image`가 없으면 Phala는 SSH 액세스가 활성화된 개발용 빌드인 `dstack-dev-0.5.12`를 선택합니다. | `server_state`가 실패합니다. 이 이미지에서는 하드웨어 인증 기록만 통과했으며, 제공자 기록과 `tdx_os`에만 해당 내용이 표시됩니다. | 배포 시 Phala의 현재 릴리스인 `dstack-0.5.12`의 프로덕션 빌드를 요청합니다. |
| dstack 게이트웨이가 꺼져 있는 상태에서는 CVM 세부 정보에 `instance_id`가 표시되지 않습니다. | 배포가 30분 동안 대기한 후 실패합니다 | 인스턴스 ID는 CVM 상태에서 읽어옵니다. |
| 재시작, 중지 및 시작은 CVM 작업이며, 애플리케이션 수정 사항이 아닙니다. | `provider_actions`에는 재시작 내역이 표시되지 않았습니다. | 읽기 작업도 수행됩니다. |

**배포3 · 인증, 접근 확인 및 재시작 증거**

- CVM은 SSH 액세스를 비활성화한 상태에서 `dstack-0.5.12`를 실행했습니다. 수집기는 생성 후 약 1.5분 후에 서명된 주소를 게시했습니다. 이후 배포는 `tdx_binding`, `tdx_quote`(Intel TCB UpToDate, 하드웨어 증명 기록 v4, FMSPC `20a06f000000`, 디버그 모드 아님, 마이그레이션 불가, Intel에서 가져온 암호화 검증 데이터 지원), `tdx_compose_hash`, `tdx_compose`(바이트 단위) 및 `tdx_identity`(KMS 키)를 통과했습니다.
- trycloudflare.com 주소의 패널은 토큰이 없거나 잘못된 토큰을 입력했을 때 401을 반환했고, 패널 토큰을 입력했을 때는 200을 반환했습니다.
- `verify`에서 `--source`는 GitHub의 커밋 아카이브로 설정되었으며, 지문은 별도로 통과되었습니다: 서버, `server_state`, 방화벽(게이트웨이 없음, 공용 엔드포인트 없음), 공급자 로그, 명세서, 지문, 소스 해시, 부팅 및 5가지 `tdx_*` 검사가 통과되었습니다. Cloudflare 및 `tdx_os`는 사용할 수 없었으므로 결과는 'INCOMPLETE'로 나타났습니다.
- Phala의 API를 통해 두 번 재시작: 매번 CVM은 2분 이내에 동일한 수집기 키, 새로운 서명된 주소, 그리고 530 응답을 반환하는 기존 주소와 함께 복구되었습니다. `verify`는 새로운 부팅과 두 번의 재시작을 모두 REVIEW로 보고했습니다. `--evidence`를 통해 저널 서명과 세 번의 시작이 확인되었으며, 각 시작마다 동일한 CVM에서 생성된 고유한 Intel TDX 하드웨어 인증 기록이 있었습니다.
- `destroy`는 해당 CVM만 제거했습니다. 그 후 작업 공간은 비어 있었고, 패널 주소는 응답을 중단했습니다.
- 패널 마법사의 가격 확인 결과, `tdx.small`의 시간당 요금은 0.058달러로 표시되었습니다. 잘못된 키를 입력했을 때는 단순히 "API 키를 수락하지 않았습니다"라는 메시지가 표시되었습니다.

**후속 수정 사항 · 서명된 주소 탐지 및 OS 측정**

- 주소 키가 없으면, `verify`는 주소 주제에 대한 가장 최근의 올바른 형식의 게시물을 따랐는데, 이는 게시된 Docker Compose 구성에 인쇄되어 있습니다. 한 건의 위조된 게시물이 이를 존재하지 않는 호스트로 보냈고, `statement`는 실패했습니다: 위조자는 수집자로 위장할 수는 없었지만, 제3자 검증을 최대 12시간 동안 위조된 미래 타임스탬프를 사용하여 차단할 수 있었습니다. 이제 수집기는 자신의 키로 서명된 주소 게시물도 올리며, `verify`는 수집기가 직접 작성한 게시물만 수용하며, 게시물은 ntfy.sh의 수신 시간 순으로 정렬됩니다. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py)는 위조된 게시물을 재실행합니다. CVM은 이를 포함하는 커밋에서만 이 코드를 실행하므로, 이번 실행의 수집기는 아직 자신의 주소에 서명하지 않았고 `verify`가 이를 알렸습니다.
- `tdx_os`는 `dstack-mr` 없이는 실행할 수 없었습니다. 해당 도구의 현재 버전에는 문서에 나온 `measure --json` 대신 `measure-os`가 있습니다. 검증기는 이제 공개된 이미지와 ACPI 테이블을 포함한 VM 구성으로부터 MRTD 및 RTMR0-2를 직접 계산합니다.

**배포 4 · 전체 16개 검사, 보고서 봉인 및 재시작 검증**

- Deploy는 게시된 `dstack-0.5.12`를 한 번 다운로드하여 CVM이 보고한 OS 이미지 해시와 대조한 결과, `tdx_os`가 통과되었습니다: MRTD, RTMR0, RTMR1 및 RTMR2 값이 QEMU 8.2.2, 1 vCPU 및 2 GiB 조건에서 계산된 값과 일치했습니다. 동일한 계산에서 4 GiB, 2 vCPU, QEMU 9.2.1 또는 두 번째 네트워크 카드를 지정했을 때는 다른 RTMR0 값이 산출되었으며, 커널, 펌웨어 또는 명령줄이 변경된 경우 및 개발용 이미지의 경우에는 테스트에 실패했습니다.
- `verify`는 퀵 터널의 커넥터를 포함하여 16가지 검사 항목을 모두 통과했으므로, 결과는 PASS였습니다. 이 시스템은 HTML 및 PDF 인증서를 생성했으며, 벨기에 정부의 타임스탬프 기관인 TSU 202301(벨기에 신뢰 목록에 등재된 상태)에서 발급한 적격 eIDAS 타임스탬프, FreeTSA 타임스탬프 및 검증자의 서명으로 디지털 봉인했습니다. `check-report`는 이 모든 항목과 PDF의 서명을 확인했습니다.
- 재시작 후, `verify --evidence`는 두 번의 시작을 확인했으며, 각 시작 시 CVM 내에서 생성된 하드웨어 인증이 동반되었고, 각각 게시된 `dstack-0.5.12`에서 부팅되었습니다. 재시작과 새로운 부팅 모두 REVIEW 상태였습니다.
- `destroy`는 작업 공간을 비워 두었습니다.

**배포5 · 수집자가 서명한 디스커버리 및 위조 게시물 거부**

수집기는 위의 수정 사항이 포함된 `53a0f7e9` 커밋부터 실행되었습니다.

- 수집기는 운영자의 HMAC 게시물 바로 옆에 자체 키로 서명된 주소를 게시했습니다. 그 후 해당 토픽에 두 개의 위조된 게시물이 추가되었는데, 하나는 HMAC 값이 0으로 설정된 것이고 다른 하나는 다른 Ed25519 키로 서명된 것이었으며, 둘 다 2096년의 시간을 주장하고 있었습니다. `verify`는 수집자 키로 서명된 주소를 가져와 16가지 검사 항목을 모두 통과했습니다. 이 인장에는 다시 한 번 벨기에의 공인 타임스탬프, FreeTSA의 타임스탬프 및 검증자의 서명이 포함되어 있었으며, `check-report`가 이를 확인했습니다.
- 재시작 후, 수집기가 서명된 새 주소를 게시했습니다: `verify`가 이를 즉시 발견했고, 운영자의 **는 현재 주소를 찾았으며,**는 HMAC 게시물로부터 27초 후에 이를 확인했고, 둘 다 위조된 게시물을 무시했습니다. `verify --evidence`는 `dstack-0.5.12`에서 부팅된 두 대의 기기를 확인했습니다.
- 배포 결과에는 Phala가 CVM에 청구하는 금액(디스크 포함)이 표시되었습니다: 시간당 $0.06078.

### 패널 마법사 및 나머지 범위

패널 마법사는 Phala Cloud에서 두 번 실행되었습니다. 한 번은 작업 API를 통해, 다른 한 번은 실제 Chromium을 사용하는 브라우저를 통해 실행되었습니다: 가격 확인, **Advanced** 아래의 커밋을 통한 생성, 6가지 인증 검사 모두 통과, 청구 가격(월 44.37 USD)이 표시된 서버 목록, **Find 현재 주소**, 측정된 Docker Compose 구성 다운로드 및 삭제. 브라우저에서는 페이지 오류가 발생하지 않았습니다. 매번 작업 공간은 그 후 비어 있었습니다.

다음 항목은 포함되지 않습니다: Phala상의 Cloudflare 도메인, CVM상의 텔레그램 계정, 그리고 `dstack-0.6.1` 이미지. 생성 전 마법사의 가격은 Phala의 컴퓨팅 가격뿐입니다. 이는 해당 API가 기존 CVM에 대해서만 디스크 가격을 명시하기 때문이며, 서버 목록에는 생성 후 청구된 가격이 표시됩니다. 이 섹션의 모든 가격은 4년 2026월 4일에 관측된 것입니다.

## 실시간 서버 일지 목록 · 1년 11월 2026일

UTC 기준 약 19:15에, 실행 중인 서버의 10개 워크스페이스 데이터베이스에서 순차적인 읽기 전용 SQLite `query_only` 쿼리를 통해 이벤트 수를 집계했습니다. 쿼리 실행 중에도 데이터 수집이 계속되었으므로, 이는 워크스페이스 전반에 걸친 원자적인 스냅샷이 아닙니다.

| 10개의 워크스페이스 데이터베이스 전반에 걸쳐 관찰됨 | 개수 |
| --- | --- |
| `message.new` 이벤트가 하나 이상 포함된 워크스페이스 | 8 |
| 운영 이벤트를 포함한 일지 기록 | 1,610,818 |
| `message.new` 이벤트 | 900,232 |
| `message.edited` 이벤트 | 80,683 |
| `message.deleted` 이벤트 | 400,536 |
| `message.recovered` 이벤트 | 53,403 |
| `message.snapshot` 이벤트 | 2,183 |
| `media.saved` 이벤트 | 50,418 |
| `media.failed` 이벤트 | 5,575 |
| `coverage.gap` 이벤트 | 11 |
| WAL 파일 및 미디어를 제외한 데이터베이스 바이트 | 7,909,003,264 |

다음은 **이벤트 수**, 고유한 메시지, 사람 또는 미디어 파일이 아닙니다. 동일한 메시지가 여러 워크스페이스에 나타날 수 있으며, 수정이나 삭제를 통해 또 다른 저널 이벤트가 생성될 수 있습니다. `media.failed` 은 현재 미디어 대기열이 아닌 과거의 오류 이벤트를 집계합니다. 쿼리들은 **아님** 서명과 전체 해시 체인을 새로 검증하지 않았으며, 1,610,818 레코드를 확인하거나, 전달률이나 처리량을 측정하거나, 모든 텔레그램 이벤트가 캡처되었음을 입증하지 않았습니다. 메시지 내용, 계정 또는 채팅 ID, 워크스페이스 레이블, 인증 정보 또는 비공개 파일은 여기에 게시되지 않습니다.

이번 검토 시점에, 별도로 구성된 공개 모니터는 세 가지 소스를 다루었습니다: 캡처 응답 중 하나는 ‘OK’였으며, 두 개는 `no_response`를 보고했습니다. 해당 모니터는 10개 워크스페이스의 상태 요약이 아닙니다. `no_response`는 관찰자가 해당 점검 시점에 응답을 얻지 못했음을 의미하며, 메시지 손실을 입증하는 것은 아닙니다. 아래에 있는 10월 29일의 소규모 테스트는 별도의 명시적 서명 및 해시 체인 검증을 거쳤습니다.

## 최근 오프라인 및 오류 주입 검사 · 1년 11월 2026일

이 검증 과정에서는 가상의 데이터와 로컬 파일을 사용하며, 이는 다른 실제 텔레그램 전송 측정 결과가 아닌 현재 소스에 대한 회귀 증거를 추가합니다:

| 확인 | 테스트 대상 |
| --- | --- |
| [소스 아카이브](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | 소스 바이트는 동일하지만 파일 수정 시간이 변경된 두 개의 빌드에서 동일한 ZIP 파일과 체크섬이 생성되었습니다. 압축된 바이트와 파일 해시는 정확히 일치했으며, 비공개 테스트 파일은 제외되었습니다. 쓰기 오류를 시뮬레이션했을 때 이전 압축 파일과 체크섬은 그대로 유지되었습니다. |
| [계정 내보내기 복구](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | 두 번째 ZIP 구성 요소에서 시뮬레이션된 디스크 오류로 인해 공개된 ZIP 파일이나 부분 ZIP 파일이 생성되지 않았습니다. 재개 기능은 모든 서명된 수령증을 바이트 단위로 동일하게 유지했으며, 예상된 서명 지문을 사용하여 독립적으로 검증 가능한 아카이브를 생성했고, 부분 결과로서 합성된 커버리지 공백을 보존했습니다. 스케일 어설션은 기록이 증가함에 따라 작업 및 수령증 스캔이 반복되는 것을 방지합니다. |
| [개인정보 노출 최소화](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | 세 가지 신원 확인 모드 모두와 텍스트 생략 상황에서 합성 유니코드 이름 및 별칭, 중첩된 메타데이터, 알 수 없는 발신자 및 미디어 필드를 확인했습니다. 마스킹 제한 오류가 발생하더라도 편집 기능이 무음으로 약화되지는 않았으며, 원래 서명된 계정 내보내기 파일은 변경되지 않은 상태로 유지되었습니다. |
| [리눅스 미디어 디코더 및 OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | `5a9e0814` 커밋 시점에 수행된 [리눅스 도커 CI 검사는](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) 생성된 Ogg/Opus, MP3, M4A, 동영상이 포함된 MP4, WAV 및 FLAC 입력 파일; 위조된 재생 시간 및 보조 파일 참조 제어; 그리고 48개의 변형된 파서 피처(34개 거부, 14개 범위 내에서 디코딩됨)를 통과했습니다. 실제 Tesseract OCR은 원본 바이트를 변경하지 않은 상태로 실행되었습니다. 디코더와 OCR은 Whisper 모델 없이 네트워크가 격리된 컨테이너에서 실행되었습니다. |

이 검사는 [풀 리퀘스트](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) 및 [전체 검사](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) 워크플로우에서 실행됩니다. 이 검사는 가능한 모든 저장소 오류나 공개된 내용이 자동으로 게시해도 안전한지 여부를 테스트하는 것이 아니라, 이러한 오류 경계만을 테스트합니다. 미디어 검사는 음성 인식 정확도나 텔레그램 전송 상태를 측정하지 않습니다. 공유하기 전에 각 파생물을 검토하십시오.

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

Docker/Compose 및 설치 검사는 CI에 기록되며, 실제 Phala 배포 및 외부 타임스탬프 검증은 위에서 설명되어 있습니다. 이는 지속적인 고부하, 완전한 라이브 플랫폼/역할 매트릭스, 독립적인 보안 검토, 장기 보관 검증 또는 포렌식 인증을 보장하지는 않습니다. 저장된 MTProto 상태 및 캐치업 기능이 구현되었으나, 원자적 무손실 라이브 리플레이는 아직 구현되지 않았습니다. 최신 백필(backfill) 기능은 메시지와 커서를 원자적으로 커밋하고 사용 가능한 최근 작업(Recent Actions)을 보존하지만, 그 합성 커버리지는 라이브 검증과는 별개입니다. 제어된 검증 매트릭스에 대해서는 [라이브 승인(live acceptance)](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)을 참조하십시오.

[공개 감사 디렉토리](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md)에는 서명된 보고서와 집계된 측정값만 포함되어 있습니다. 상세한 운영 기록, 원본 캡처 자료 및 계정 자료는 비공개로 유지됩니다. `docs/assets/`에 있는 애플리케이션 스크린샷은 가상의 데모 데이터를 사용합니다.
