# 보안 및 데이터 처리

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/security/

위협 모델, 접근 모델, 저장된 기밀 정보, 네트워크 노출, 세션 가져오기 및 취약점 보고 방법.

This page describes access，storage and network protection in a local or server workspace． For collection on a GitHub runner or in an Intel TDX confidential VM，see the [verification modes](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#verification-scope)，which add checks of the collection environment． Account connections，notifications，timestamps，off-site copies and witnesses have their own routing settings．

| 분야 | 요약하자면 |
| --- | --- |
| 접근 | 관리자 키와 계정/채팅에 대한 범위 지정 액세스, 7가지 권한 및 취소 가능한 세션; 기본적으로 localhost 사용 |
| 저장된 비밀 | 세션, API 쌍, 서명 키 및 프록시 설정은 Fernet 알고리즘으로 암호화됩니다. |
| 메시지 및 미디어 | 암호화되지 않은 상태로 저장됨: 디스크 암호화 및 엄격한 권한 설정을 사용하십시오. |
| 무결성 | 모든 기록에 SHA-256 해시 체인과 Ed25519 서명이 적용됩니다. |
| Local trust boundary | The host administrator controls the workspace and its signing key；independent checkpoints retain an earlier journal boundary |

취약점 보고와 관련하여서는 [보안](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)정책을 참조하십시오.

## 접근 모델

메인 패널 토큰을 통해 모든 권한을 제어할 수 있습니다. 다른 사용자에게는 선택된 워크스페이스 및 채팅, 권한, 유효 기간, IP 제한, 로그인 횟수 제한, 취소 가능한 세션 등 [범위 지정된 액세스](https://phishdestroy.github.io/TgWitness/ko/docs/reference/access/) 권한을 부여할 수 있습니다. 채팅으로 제한된 액세스 권한을 가진 사용자는 권한 항목이 선택되어 있더라도 전체 워크스페이스 작업은 수행할 수 없습니다. 워크스페이스는 동일한 프로세스를 공유하며, 호스트 관리자로부터 데이터를 분리하지 않습니다.

패널은 기본적으로 localhost에서 수신 대기합니다. 브라우저 로그인 시 액세스 토큰이 세션 자격 증명으로 교환되며, 브라우저는 이를 베어러 토큰으로 전송합니다. 이 토큰은 인증 쿠키가 아닌 sessionStorage에 저장됩니다. 잠금/로그아웃 시 브라우저 세션이 지워집니다. 브라우저를 닫거나 세션을 종료하더라도 데이터 수집은 중단되지 않습니다.

발행된 토큰과 세션 인증 정보는 암호화된 볼트에 해시 형태로 보관됩니다. 취소 시 관련 세션이 종료되며, 권한 변경 사항은 이후의 요청에 적용됩니다. 다운로드된 파일은 회수할 수 없습니다. 관리자는 자신의 브라우저 세션도 제한할 수 있지만, 메인 패널 토큰을 직접 사용하는 스크립트는 전체 액세스 권한을 유지하며 해당 브라우저 세션 제한을 우회합니다.

인증 실패 시 클라이언트 주소를 기준으로 속도 제한이 적용됩니다. IP 제한은 애플리케이션에서 인식하는 주소를 기준으로 하므로, 이를 신뢰하기 전에 리버스 프록시 동작을 확인하십시오. Witness 자격 증명은 별도의 읽기 전용 체크포인트/상태 확인 자격 증명으로 유지됩니다.

### 데모 이용

`/api/demo-access`는 명시적으로 시작된, 격리된 합성 데모를 위한 의도적으로 인증되지 않은 부트스트랩입니다. 이는 별도의 프로세스 수명 주기 내 기능을 발급하며, 절대 실제 패널 토큰이나 TGWITNESS_TOKEN 오버라이드를 발급하지 않습니다. 이 기능을 발급하고 사용하려면 루프백 피어와 호스트가 필요하며, 헤더 전달이나 크로스 오리진 요청은 허용되지 않습니다. 추가 워크스페이스나 인증된 세션이 있는 경우 이 경로는 비활성화됩니다. 활성 워크스페이스는 이 기능을 절대 발급하지 않습니다. 이 데모는 계정을 연결하거나 수집 설정을 변경할 수 없습니다.

## 패널 콘텐츠 및 내보내기

이 패널은 외부 폰트, 분석 도구, CDN 리소스 또는 임베드된 원격 미디어를 사용하지 않습니다. 텔레그램에서 가져온 텍스트는 HTML이 아닌 일반 텍스트로 삽입됩니다. 다운로드된 첨부 파일은 바이너리 첨부 파일로 제공됩니다. JSONL 내보내기에서는 원본 문자열이 그대로 유지되며, HTML 내보내기에서는 문자열이 이스케이프 처리되고, 수식이 될 수 있는 CSV 셀 앞에는 아포스트로피가 붙습니다.

내보낸 데이터에는 인증 및 서명 비밀 정보는 제외되지만, 수집된 원본 메타데이터, 식별자, 그리고 개인 정보나 민감한 내용이 의도적으로 포함됩니다. 원본 메타데이터에는 텔레그램 액세스 해시 및 파일 참조 정보가 포함될 수 있습니다.

## 저장된 비밀

Telegram API credentials，the session and signing key are encrypted with Fernet． For local messages and media，encryption is provided by the host's disk or volume； the workspace stores ordinary files．Exports can use a password-protected AES-256 ZIP， and off-site copies use AES-256-GCM．

The vault key defaults to the protected data directory．Use an external master-key file below to store it separately．On Unix，new private-key files use mode 0600 and new data directories use 0700；on Windows，set the directory ACL for the service account and authorized administrators．Existing directory permissions are retained．

### 외부 마스터 키

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode．Disk encryption protects the local message and media files in either mode；see [connection and data protection](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/) for setup details．

## 프록시 및 네트워크 경로

프록시 구성 정보는 볼트에 암호화되어 저장됩니다. 비밀번호와 MTProxy 시크릿은 API를 통해 반환되거나 증거 기록에 기록되지 않습니다. 각 워크스페이스는 자신만의 텔레그램 경로와 [IP 모드를](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/#ip-modes) 선택합니다.

**'주소 숨기기' 모드는** 텔레그램의 직접 폴백을 차단하며, 외부 HTTP 요청을 위해 프록시를 필요로 합니다. 명시적으로 선택한 폴백 모드는 지연 시간 후 텔레그램에 직접 접속할 수 있게 하며, 터널/VPN 모드는 직접 경로를 허용합니다. 터널 모드를 선택한다고 해서 VPN이 설치되거나 검증되는 것은 아닙니다. 이러한 설정은 모든 기기 트래픽, 브라우저, 패키지 관리자 또는 로컬 프록시 호스트의 DNS 확인을 제어하지 않습니다.

MTProxy는 텔레그램 트래픽만 처리합니다. 외부 요청은 별도의 SOCKS5/HTTP 프록시, 워크스페이스의 SOCKS5/HTTP 경로 또는 허용된 직접 경로를 사용할 수 있으며, 비활성화할 수도 있습니다. 독립적인 위트니스는 자체 전송 설정을 갖습니다. 일반적인 SOCKS5/HTTP CONNECT 인증은 해당 프록시 프로토콜 자체에 의해 암호화되지 않습니다. 가짜 TLS MTProxy 비밀 정보는 여전히 지원되지 않습니다.

## 로그인 및 세션 가져오기

변환된 .tgwitness-session 파일에는 볼트에 로드 및 저장될 때까지 평문 형태의 인증 비밀번호가 포함되어 있습니다. 오프라인 CLI는 검토를 거친 Telethon 스키마를 지원합니다. 패널 가져오기 기능은 Pyrogram SQLite, 최신 단일 계정 TData ZIP, 그리고 문서화된 JSON 입력도 추가로 지원합니다. 인증이 필요하며, 4개 파일 / 8 MiB로 제한되며, 아카이브 압축 해제나 원본 파일 저장 없이 메모리 내에서 업로드를 처리합니다. 정규화된 인증 정보는 요청한 인증된 브라우저에만 반환되며, 텔레그램 인증이 성공적으로 완료된 후 암호화된 볼트에 저장됩니다. 원본 파일과 변환된 파일을 보호하고, 여러 클라이언트가 동시에 인증 정보를 복제하는 것을 방지하십시오.

데이터 처리 과정에서는 컨테이너 체크섬, 로컬 복호화 해시 및 구조 길이를 검증합니다. 제공된 데스크톱 로컬 암호는 일시적으로만 사용되며 저장되지 않습니다. 이 제한된 파서는 모든 데스크톱 버전이 호환된다는 것을 보장하지 않습니다. QR 이미지는 로컬에서 생성되며, 유효 기간이 짧은 텔레그램 로그인 토큰을 포함하고, 외부 렌더링 서비스로 전송되지 않습니다. 화면 잠금, 작업 공간 전환, 새 로그인, 경로 변경 시 보류 중인 QR 시도가 취소됩니다. 탭을 새로 고치거나 닫을 경우, 만료될 때까지 시도가 보류될 수 있습니다. QR 로그인이 성공하더라도 계정 바인딩은 여전히 적용됩니다. 일반 API 본문은 여전히 16 KiB로 제한되지만, 인증된 가져오기 경로는 최대 12 MiB의 인코딩된 JSON을 허용하며, 더 작은 디코딩된 파일 크기 제한은 별도로 적용됩니다.

로그인 코드 및 텔레그램 2단계 인증 비밀번호는 저장되지 않습니다. 전화번호/코드 해시 상태는 인증 과정에서 메모리에만 보관됩니다. 텔레그램 세션을 통해 계정 접근 권한이 부여되며, 데이터 디렉터리, 세션, 토큰, 볼트 키 또는 개인 서명 키를 GitHub에 절대 업로드하지 마십시오.

## 로그 및 전송

기본 API 유효성 검사 응답이 변경되어 자격 증명 값이 노출되지 않습니다. 애플리케이션 액세스 로깅은 비활성화되어 있습니다. 리버스 프록시를 구성할 때 Authorization 헤더나 요청 본문을 기록하도록 설정하지 마십시오. HTTP는 토큰과 로그인 비밀 정보를 평문으로 전송하므로, localhost를 벗어날 때는 항상 HTTPS 또는 SSH 터널을 사용하십시오.

## 무결성 제한 사항

Local verification checks record signatures，the hash chain，attachments and the export manifest． The administrator holds the local signing key and can create another signed journal； an independently retained checkpoint detects replacement of the prefix it covers． Keep the key fingerprint and checkpoints with the recipient or an independent witness．

For independently checked collection，choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)． Their verifiers check workflow provenance or hardware measurements in addition to archive integrity． Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies； the [evidence format](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#verification-scope) describes the checks for each mode．

## 문제가 의심될 경우

Preserve the original data directory and use a separate copy for analysis． Report the affected version，operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)，keeping account data and credentials private．
