# 계정 및 세션 형식

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/

전화번호, QR 코드 또는 인증 키로 로그인하고, Telethon, Pyrogram 또는 Telegram Desktop 세션을 가져와 여러 계정을 동시에 운영할 수 있습니다.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [문서](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [시작하기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/quickstart/)

![시작하기](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness는 Telethon을 사용하여 MTProto를 통해 텔레그램 사용자 계정(봇이 아님)으로 로그인합니다. 각 계정은 고유한 세션, 소스, 저널 및 서명 키를 가진 별도의 작업 공간(API 및 명령줄 도구에서 ‘워크스페이스’라고 함)에 존재합니다.

세션 파일, 세션 문자열 및 인증 키는 **계정 인증** 수단입니다. 이를 소지한 사람은 누구나 해당 계정으로 활동할 수 있습니다. 여기에는 메시지 내역이 포함되어 있지 않습니다.

> [!경고] **잃어도 괜찮은 것만 사용하십시오.** 개인 계정이나 그 밖의 중요한 계정을 연결하거나, 소중히 여기는 계정으로 API ID/API 해시를 생성하는 것을 강력히 권장하지 않습니다. 이는 TgWitness가 검증되지 않았기 때문이 아닙니다. 텔레그램은 클라이언트나 목적과 관계없이, 적절한 문서화 없이 요청량이 과도하다고 판단되는 경우 예측할 수 없이 계정을 제한하거나 영구적으로 차단합니다. 많은 차단 조치는 되돌릴 수 없습니다. 전용 계정을 사용하십시오. 원활한 테스트 실행은 소프트웨어가 아닌 텔레그램에 달려 있으며, 향후에 대해 어떠한 보장도 하지 않습니다.

- [한눈에 보기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#at-a-glance)
- [시작하기 전에: API ID 및 API 해시](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [전화번호](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#phone-number) · [QR 코드](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#qr-code) · [인증 키 + DC ID](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#auth-key--dc-id)
- [계정 파일](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#pyrogram-session) · [세션 + JSON 쌍](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#telethon-stringsession) · [계정 JSON](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#account-json)
- [보유 중인 자료를 파악하세요](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#identify-what-you-have) · [지원되지 않는 형식](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#unsupported-formats)
- [여러 계정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#multiple-accounts) · [계정 파일 안전하게 보관하기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#keeping-account-files-safe) · [문제 해결](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#troubleshooting)

## 한눈에 보기

| 현재 보유한 내용 | **'계정 추가**' 탭 | 또한 다음이 필요합니다. |
| --- | --- | --- |
| 전화번호 및 로그인 코드 접근 권한 | **전화** | 2단계 인증(2FA)이 활성화된 경우의 비밀번호 |
| 다른 기기에서 텔레그램이 열려 있음 | **QR 코드** | 2단계 인증(2FA)이 활성화된 경우의 비밀번호 |
| `.session` 파일(Telethon 또는 Pyrogram) | **파일** | 앱 설정을 위한 선택적 부가 JSON 파일 |
| 동일한 이름을 가진 `.session` + `.json` | **파일** (둘 다 선택) | 보통 다른 내용은 없습니다. |
| 텔레그램 데스크톱의 `tdata` 폴더 | **파일** (ZIP 파일) | 설정된 경우 데스크톱 로컬 비밀번호 |
| Telethon StringSession (텍스트, `.txt`, `.tgwitness-session`) | **파일** | 별도의 API 쌍이 필요하지 않습니다. |
| 세션 또는 인증 키(Auth Key)가 포함된 `.json` | **파일** | 별도의 API 쌍이 필요하지 않습니다. |
| 인증 키(512자 16진수) 및 해당 DC 번호 | **인증 키** | 선택 사항: 사용자 ID |

TgWitness는 파일 이름이 아닌 **내용을** 기준으로 파일을 식별합니다. 파일 이름을 변경하더라도 파일 변환은 절대 이루어지지 않습니다.

## 시작하기 전에: API ID 및 API 해시

텔레그램 API 애플리케이션을 생성하지 않고도 로그인할 수 있습니다. 쌍이 입력되지 않았거나, 가져오지 않았거나, 작업 공간에 이미 저장되어 있지 않은 경우, TgWitness는 내장된 50개의 공개 API 쌍 풀(`tgwitness/api_pool.py`)에서 쌍을 선택하며, 신규 로그인 시에는 텔레그램 데스크톱을 우선적으로 사용하고, 저장된 쌍이 있는 경우 이를 우선적으로 유지합니다. 나머지 후보들은 무작위로 섞입니다. 텔레그램이 키 쌍을 거부할 경우 (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), 다음 키 쌍이 시도되며, 로그인당 최대 8개까지 시도됩니다. 거부된 키 쌍은 재시작할 때까지 건너뜁니다. 로그인에 사용된 키 쌍은 계정과 함께 저장되어 해당 계정에 재사용됩니다. **API** ID와 **API**해시는 텔레그램에 애플리케이션을 식별하는 용도로 사용되며, 이들 자체만으로는 계정을 인증하지 않습니다.

누락된 연결 필드에는 번들된 [opentele2 2.0.0 카탈로그](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735)의 결정론적 기기/OS 쌍이 사용됩니다: 데스크톱 `2040`, 안드로이드 `6`, 안드로이드 X `21724`, iOS `10840`, macOS `2834`, 웹 `2496`. 안드로이드의 소스 빌드 ID `4`도 [텔레그램 안드로이드의 BuildVars에](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java) 명시된 대로 안드로이드 카탈로그를 사용합니다. 웹은 기본적으로 A로 설정됩니다. 가져온 `K` 앱 버전 접미사나 `macos` 언어 팩을 선택하면 K가 선택되며, 버전 `0.7.0`을 선택하면 Webogram이 선택됩니다. 알 수 없는 애플리케이션 ID는 Telethon의 호스트 기본값을 유지합니다. 가져온 필드는 항상 우선 적용되며, 여기에는 이전 앱 버전이나 빈 언어 팩도 포함됩니다. 카탈로그는 API ID/해시를 절대 변경하지 않습니다. 카탈로그의 버전 스냅샷은 로그인 중에 가져오지 않고 명시적으로 검토됩니다. 저장된 프로필은 업데이트 후에도 안정적으로 유지됩니다.

`account.getAuthorizations`는 텔레그램에 저장된 인증 메타데이터를 보고합니다. 이는 각 새로운 `initConnection` 호출을 그대로 반영한 것이 아닙니다. 실제 전송된 프로필과 비교하십시오. 기존 인증을 연결한다고 해서 해당 인증에 연결된 API 해시가 유효한 것으로 검증되는 것은 아닙니다. `initConnection`는 API ID를 전송하는 반면, 해시는 로그인 요청에 사용됩니다.

새 휴대폰 등록 또는 QR 인증 후, TgWitness는 구성 정보, 가장 가까운 데이터 센터, 온라인 상태, 언어(언어 팩이 비어 있지 않은 경우), 앱 업데이트 및 서비스 약관 업데이트를 요청하며, 요청 간 간격은 0.3~1.5초입니다. 상태 업데이트 시 계정이 잠시 온라인 상태로 표시됩니다. 이 시퀀스는 로그인 완료 시 한 번만 실행되며, 데이터 가져오기, 재연결 또는 재시작 시에는 실행되지 않습니다. 인증 정보가 먼저 저장되며, 요청이 실패하면 재시도나 로그인 정보 폐기 없이 시퀀스가 중단됩니다. 결과는 `account.initialized`로 기록되며, 응답 본문 대신 오류 이름이 사용됩니다. 이 시퀀스는 계정 제한에 대한 보장을 의미하지 않습니다.

`tdesktop` 의 경우, `tz_offset` 이 누락되면 서버의 로컬 UTC 오프셋을 사용하며, [opentele2 알고리즘](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; 라이선스: `tgwitness/client_profiles.LICENSE` )을 사용하여 900 초로 반올림됩니다. 이는 매 연결 시마다 갱신되어 일광 절약 시간제 변경 사항이 반영됩니다. 가져온 `tz_offset` 은 모든 플랫폼에서 우선 적용되며, 0을 포함하여 정확히 유지됩니다. 다른 `initConnection.params` 항목들은 그대로 유지됩니다. HTTP 로그인 양식은 파일 가져오기를 통해 반환된 숫자 형식의 시간대를 허용하며, 부울 값, 소수 값 및 지원 범위를 벗어난 오프셋은 거부됩니다.

직접, SOCKS5 및 HTTP CONNECT 경로는 Telethon의 `ConnectionTcpObfuscated` (난독화된 축약형 MTProto)를 사용합니다. HTTPS CONNECT는 프록시까지 TLS를 유지하며 터널 내부에서는 동일한 난독화된 전송 방식을 사용합니다. MTProxy는 필수적인 무작위화된 중간 전송 및 비밀 처리 방식을 유지합니다. 경로 전환 시에도 동일한 선택 사항이 적용됩니다. 난독화는 패킷 프레밍을 변경할 뿐, 텔레그램으로부터 계정 또는 해당 클라이언트의 메타데이터를 숨기거나 제한 사항에 대한 면제를 의미하지는 않습니다.

인증된 클라이언트가 연결되면, TgWitness는 구성, 가장 가까운 데이터 센터, 현재 인증 상태, 검토된 레이어 기준선, 언어, 앱 업데이트 및 서비스 약관 업데이트를 확인합니다. 이러한 진단은 클라이언트 인스턴스당 한 번, 데이터 수집 전에 실행되며, 연결 세부 정보 아래에 실행 시간과 함께 표시됩니다. `account.connection_checked`는 세션 해시, IP, 토큰 또는 API 해시 없이 결과를 기록합니다. 이 기능은 약관에 동의하거나 업데이트를 설치하지 않습니다. 요청 실패나 FloodWait 발생 시 후속 요청이 중단되며, 누락된 결과는 미확인 상태로 남습니다. 네트워크 검사가 건너뛰어지는 동안에도 로컬 검사는 결과를 보고할 수 있습니다.

FloodWait 진단 정보는 실패한 TL 메서드, 모든 Takeout/range 래퍼, 서버가 요청한 대기 시간 및 `telegram.backoff`의 유효한 마감 시간을 유지합니다. 연결 세부 정보에는 요청이 일시 중지된 동안의 메서드와 마감 시간이 표시됩니다. 이 진단 정보에는 해당 클라이언트가 생성된 이후의 메서드별 클라이언트 호출 카운터가 포함됩니다. 이 카운터는 중첩된 피어 확인을 별도로 집계하지만, 패킷이나 Telethon의 내부 재시도 횟수는 집계하지 않습니다. 현재 카운터는 상태 API의 `collector.rpc_activity`에서도 확인할 수 있습니다. 요청 인자, 사용자 이름, 액세스 해시 또는 예외 텍스트는 포함되지 않습니다. 마지막 진단 정보와 전체 마감 시간은 재시작 후에도 유지됩니다. 메서드 기록이 없는 이전 대기 기록은 소급하여 특정 메서드에 귀속시킬 수 없습니다. 소스 검토를 위한 [내보내기 제한](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) 사항과 탐색 및 기록 수집 간의 차이점을 참조하십시오.

`official_app=True` 또는 `False`는 텔레그램의 현재 인증 플래그입니다. 두 값 모두 해당 계정이 제한된 상태인지, 신뢰된 상태인지, 아니면 관찰 대상인지 여부를 나타내지 않습니다. 기존 증거 모드의 `account.devices` 스냅샷은 모든 로그인된 기기의 기록을 그대로 유지하며, 연결 진단 정보는 현재 기기의 설명만 보관합니다.

연결 전에, 자문 점검은 API 플랫폼, 언어 팩, 기기/OS 및 앱 버전 형식, 모바일 시스템 로케일, 그리고 Telethon의 실제 스키마 레이어를 검토된 카탈로그 기준선과 비교합니다. 경고는 서버 로그와 계정 상태 메타데이터에 표시되며, 이는 가져온 값을 대체하거나 스키마 레이어를 변경하지 않습니다. 별도의 계층은 호환성 검토 신호일 뿐, 계정이 손상되었거나 제한을 받는다는 증거는 아닙니다. 이러한 점검 및 `official_app`는 텔레그램이 해당 계정을 제한으로부터 안전한 것으로 간주한다는 것을 보증하지 않습니다. 연결이 끊긴 계정 상태는 별도의 기기 설명을 생성하는 대신 저장된 프로필을 사용합니다.

대신 자체 애플리케이션을 사용하려면(해당 애플리케이션을 등록한 계정이 위험에 노출됩니다. [‘내장 API 풀이 필요한 이유’](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account) 참조):

1. [my.telegram.org를](https://my.telegram.org) 열고 본인이 소유한 전화번호로 로그인하세요. 인증 코드는 SMS가 아닌 텔레그램 앱으로 전송됩니다.
2. **API 개발 도구를** 선택하세요.
3. 애플리케이션 생성: 제목 및 짧은 이름(5~32자)을 입력하고, 플랫폼은 **‘데스크톱’을 선택합니다**. URL과 설명은 비워두어도 됩니다.
4. **App api_id**(숫자)와 **App api_hash**(32자리 16진수)를 복사하십시오.

패널의 로그인 양식 아래에 있는 **‘API ID + 해시’** 입력란에, 단일 ‘`api_id:api_hash`’ 쌍을 **API**ID에 붙여넣으면 두 필드 모두 자동으로 채워집니다. 하나의 쌍으로 모든 계정에 사용할 수 있습니다. 로그인이 성공하면 해당 정보는 해당 작업 공간에만 암호화되어 저장되며, 브라우저로 다시 전송되지 않습니다.

여기에는 세 가지 다른 인증 정보가 관련되어 있습니다:

| 비밀 | 열기 | 위치 |
| --- | --- | --- |
| 패널 토큰 | TgWitness 웹 패널 | 데이터 디렉토리 내의 `panel-token.txt` 또는 `TGWITNESS_TOKEN` |
| API ID + 해시 | 단독으로는 의미가 없음; 해당 앱을 식별함 | 내장된 페어, 가져온 설정, 또는 my.telegram.org에서 직접 만든 앱을 사용할 수 있습니다. |
| 계정 인증 | 텔레그램 계정 | 전화/QR 로그인을 통해 생성되거나 세션으로 가져옴 |

텔레그램에 프록시를 통해 접속해야 하는 경우, 먼저 **‘계정’ → ‘설정’ → ‘연결 설정’ → ‘연결 경로** 변경’에서 설정을 조정하십시오.

## 전화번호

1. **계정을** 개설하고, **‘전화’** 탭으로 이동한 후 국제 번호 형식으로 번호를 입력하세요. 예: `+44 7700 900123`. 공백과 하이픈은 자동으로 제거됩니다.
2. **'계속'을** 누르세요. API ID와 해시는 비워두어도 됩니다.
3. 텔레그램에서 전송한 코드를 입력하세요(일반적으로 텔레그램 앱으로 전송되며, SMS 수신은 보장되지 않습니다).
4. 계정에 2단계 인증이 설정되어 있다면 해당 비밀번호를 입력하세요. 이는 패널 토큰도 아니고 기기 비밀번호도 아닙니다.
5. 로그인 후 표시되는 계정 ID를 확인한 다음, 소스를 선택하십시오.

로그인 코드와 2단계 인증(2FA) 비밀번호는 절대로 디스크에 기록되지 않습니다.

## QR 코드

이 기능은 계정이 이미 휴대폰이나 다른 컴퓨터에서 로그인된 상태에서 사용하십시오.

1. **QR 코드** 탭 → **QR 코드 표시**. API ID + 해시는 비워두어도 됩니다.
2. 로그인된 기기에서: **설정 → 기기 → 데스크톱 기기 연결을** 선택한 후, 코드를 스캔하고 확인합니다.
3. 텔레그램에서 요청할 경우, TgWitness에 2단계 인증(2FA) 비밀번호를 입력하십시오.

QR 이미지는 로컬에서 생성됩니다. 코드는 유효 기간이 만료되므로, **‘다른 QR 코드 생성’을** 눌러 다시 시도하십시오. 패널을 잠그거나, 작업 공간을 전환하거나, 다른 로그인을 시작하면 대기 중인 코드가 취소됩니다.

## 인증 키 + DC ID

인증 키(Auth Key)는 모든 텔레그램 세션의 기반이 되는 256바이트의 원시 인증 정보로, **512개의 16진수**문자로 표기되며, 데이터 센터 번호 **DC 1–5가** 함께 포함됩니다.

1. **'Auth 키'** 탭. 전체 키를 붙여넣으십시오. `…`가 포함된 축약된 키는 작동하지 않습니다.
2. 키와 함께 제공된 DC ID를 선택하십시오.
3. 선택적으로 **사용자 ID**를 입력할 수 있습니다. 텔레그램에서 다른 계정을 보고할 경우, TgWitness는 연결을 거부합니다.
4. Press **Connect 계정**.

인증 키(512자)는 API 해시(32자)와 다릅니다. 동일한 키는 JSON 형식으로 가져올 수도 있습니다. [계정 JSON을](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#account-json) 참조하십시오.

## 계정 파일

'계정 추가' → '파일'을 열고, 하나의 계정에 속한 파일을 최대 4개까지 선택하고, 총 용량이 8 MiB 이내가 되도록 한 다음, '계정 연결'을 누르십시오.

**'파일**', **'인증 키'** 및 '대량 가져오기' 양식에서는 연결 전에 병렬 세션 경고가 표시됩니다. 기본적으로 가져온 인증 정보는 재사용됩니다. 해당 키가 여기에서 사용 중인 동안에는 원본 클라이언트를 닫아 두십시오. **'파일'** 및 **'인증 키'** 양식에서는 아래에 설명된 **'독립적인 인증 생성'**기능도 제공합니다. 대량 가져오기는 여전히 직접 모드를 사용합니다. 휴대폰 및 대화형 QR 로그인은 별도의 인증을 생성합니다. 경고 제목은 가져오기 양식에 계속 표시되며, 파일이나 키/세션 문자열이 제공되면 전체 설명이 자동으로 열립니다. 내용을 읽은 후에는 접을 수 있으므로, 휴대폰에서도 파일 선택기 및 연결 제어 기능을 계속 사용할 수 있습니다.

- 파일은 TgWitness 서버의 **메모리 내에서** 변환됩니다. 업로드된 파일은 저장되지 않으며, ZIP 파일은 디스크에 압축 해제되지 않고, 외부 서비스와도 연결되지 않습니다.
- 생성된 세션은 이후 텔레그램을 통해 확인됩니다. 파일에 사용자 ID가 명시된 경우, 해당 ID는 텔레그램이 보고하는 계정과 일치해야 합니다.
- 서로 다른 계정이나 서로 다른 API 인증 정보를 설명하는 파일은 하나를 선택하지 않은 경우 거부됩니다.
- **‘패스코드’ 또는 ‘세션 텍스트’** 필드에는 TData의 로컬 패스코드 필드가 있으며, 이 필드에 StringSession을 붙여넣거나 **로그인 없이 Read 파일을** 불러올 수 있습니다(텔레그램에 접속하지 않고도 양식을 채울 수 있음).

### 독립적인 승인 절차 생성

‘연결 전에 **독립적인 인증 생성’** 또는 ‘인증 키’를 선택하십시오. TgWitness는 가져온 도너에 잠시 연결하여 이를 통해 새 클라이언트의 QR 로그인 토큰을 승인한 후, 승인 직후 도너와의 연결을 즉시 끊습니다. 새 클라이언트는 자체 인증 키와 별도로 선택된 데스크톱 프로필을 갖습니다. 도너가 제공한 API 자격 증명 및 기기 프로필은 도너 연결 시에만 사용됩니다. 기존 인증은 로그아웃되거나 취소되지 않습니다.

**이 단계 동안 기증자의 원래 클라이언트는 완전히 닫혀 있어야 합니다.** 초기 연결은 여전히 복사된 키를 사용하므로, 이 모드로는 초기 병행 사용 위험을 제거할 수 없습니다. 새로운 인증이 연결되면 소유자는 원래 클라이언트를 다시 열고 두 클라이언트를 독립적으로 사용할 수 있습니다. 대화형 **QR 코드** 로그인을 사용하면 원래 클라이언트가 여기서 키를 복사하거나 연결하지 않고도 로그인을 승인할 수 있습니다.

텔레그램에서 2단계 인증(2FA)을 요청하는 경우, 이 모드는 선택된 JSON에 `twoFA`가 포함되어 있으면 이를 사용하거나, 그렇지 않으면 비밀번호를 요청합니다. 가져온 비밀번호가 거부되면 비밀번호 입력 양식으로 돌아갑니다. 비밀번호는 저장되지 않습니다. 후보 키는 `independent_login.enc`에 암호화된 상태로 저장되며, 여기에는 데이터 센터 마이그레이션 중의 변경 사항도 포함됩니다. 중단 후 동일한 기증자를 선택하고 이 옵션을 선택하면 저장된 후보 키를 재개할 수 있습니다. 작업 공간은 해당 계정을 위해 계속 예약된 상태로 유지되며, 완료에 실패하더라도 새 작업 공간은 삭제되지 않습니다. 데이터 디렉터리와 볼트 키를 보관하십시오. 최종 인증 정보와 `account.authorized` 저널 기록에는 가져오기 방법, 입력 형식 및 기증자 API ID가 포함되지만, 기증자 키나 비밀번호는 포함되지 않습니다.

5년 11월 2026일, 전용 계정이 Telethon, Pyrogram 및 TData 기부자들을 대상으로 한 실시간 검증을 통과했습니다: 2단계 인증(2FA) 완료, 고유한 새 인증 키, 기부자와 새 클라이언트의 동시 접속, 공개 채널 읽기. 또한 텔레톤 사례에서는 비밀번호 입력 단계에서 중단된 후 저장된 후보를 재개했습니다. 각 새로운 인증은 로그인 후 6가지 초기화 요청을 완료했으며, 서명된 저널도 검증되었습니다. 원래 세션은 제공된 네 가지 형식 모두에서 계속 사용할 수 있었습니다.

텔레그램의 [RPC 오류 데이터베이스](https://core.telegram.org/api/errors.json)에 따르면 `FRESH_CHANGE_ADMINS_FORBIDDEN`은 관리자 변경과, `FRESH_CHANGE_PHONE_FORBIDDEN`은 전화번호 변경과, `FRESH_RESET_AUTHORISATION_FORBIDDEN`은 다른 세션의 권한 취소, 유효 기간 변경 또는 패스키 등록과 관련이 있습니다. `SESSION_TOO_FRESH_*`와 `PASSWORD_TOO_FRESH_*`는 소유권 이전 및 수익 또는 선물 인출과 관련이 있습니다. 이는 수집 작업이 아니며, 새로운 로그인이 24시간 동안의 전면적인 읽기 금지를 의미하지는 않습니다. 내보내기 기능은 별도로 `TAKEOUT_INIT_DELAY_*`를 반환할 수 있습니다. TgWitness는 서버에서 요청한 일시 중지를 유지하며, 제한을 우회하기 위해 토큰 수락을 자동으로 재시도하거나 세션을 취소하지 않습니다.

### 텔레톤 `.session`

|  |  |
| --- | --- |
| 이 도구는 무엇인가요? | Telethon 기반 도구가 생성하는 SQLite 데이터베이스(예: `my_account.session`) |
| 다음 기관에서 인정받았습니다. | 표 `sessions`(`dc_id`, `server_address`, `port`, `auth_key` 포함) 및 `version` = 7 또는 8 |
| 요구 사항 | 정확히 하나의 인증된 세션 행; 폐쇄적이고 완전한 데이터베이스 |

먼저 파일을 생성한 프로그램을 닫으십시오. 파일 옆에 `my_account.session-journal` 또는 `my_account.session-wal`가 존재한다면, 데이터베이스가 최종 확정되지 않은 상태입니다. 원본 클라이언트를 정상적으로 열었다가 닫으십시오. 이러한 사이드카 파일을 삭제하면 손상된 사본이 남을 수 있습니다.

### Pyrogram `.session`

|  |  |
| --- | --- |
| 이 도구는 무엇인가요? | Pyrogram 기반 도구가 생성하는 SQLite 데이터베이스 |
| 다음 기관에서 인정받았습니다. | `sessions` 테이블(`dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot` 포함); `version` = 2 또는 3 |
| 요구 사항 | 프로덕션 네트워크에서 승인된 **사용자** 세션 1개. 봇 및 테스트 DC 세션은 허용되지 않습니다. |

저장된 사용자 ID는 로그인 시 텔레그램과 대조하여 확인됩니다.

### 세션 + JSON 쌍

계정 정보는 종종 `447700900123.session`와 `447700900123.json`와 같이 동일한 이름을 가진 두 개의 파일로 제공됩니다. **두 파일을** 한 번에 **모두** 선택하십시오.

- JSON을 기반으로 하는 TgWitness는 `app_id`/`api_id` 및 `app_hash`/`api_hash`를 사용하므로, 일반적으로 API 인증 정보를 직접 입력할 필요가 없습니다.
- 연결 프로필은 `device_model`(별칭 `device`), `system_version` (별칭 `sdk`), `app_version`, `lang_code`, `system_lang_code`(별칭 `system_lang_pack`), `lang_pack` 및 선택 사항인 `tz_offset`(UTC 기준 초 단위, -43200 ~ 50400)을 사용합니다. 지정된 필드는 생성된 기본값 및 패널/브라우저 언어보다 우선합니다. 충돌하는 별칭은 거부됩니다. 해결된 프로필은 암호화된 작업 공간 자격 증명에 저장되며, 앱 버전을 포함하여 재시작 후 재사용됩니다.
- `phone`, 프록시 설정 및 기기 토큰은 **무시**됩니다. `twoFA`는 **'독립적인 인증 생성'이** 선택된 경우에만 읽기 전용으로 처리되며, 직접 가져오기 시에는 무시됩니다.
- 지원되는 인증 필드가 없는 JSON은 메타데이터에 불과합니다. 해당 세션 파일을 추가하거나, 휴대폰 또는 QR 로그인을 통해 계속 진행하십시오. 지원되는 세션 또는 인증 키(Auth Key)가 포함된 JSON은 단독으로 인증할 수 있습니다. [‘계정 JSON’을](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#account-json) 참조하십시오.

### 텔레그램 데스크톱 (TData)

TData는 텔레그램 데스크톱 애플리케이션(desktop.telegram.org에서 제공하는 크로스 플랫폼 앱)의 `tdata` 폴더입니다.

| 시스템 | 기본 위치: `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (휴대용 텔레그램: `Telegram.exe` 옆) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

가져오기 방법:

> **병렬 세션 경고.** TData 직접 가져오기는 텔레그램 데스크톱의 인증 키를 재사용합니다. 데스크톱과 TgWitness에서 해당 키를 동시에 사용하지 마십시오. 텔레그램은 `AUTH_KEY_DUPLICATED`를 통해 인증을 무효화할 수 있으며, 이 경우 새로 로그인할 때까지 두 인스턴스 모두 사용할 수 없게 됩니다.
>
>
>
> Desktop을 트레이 프로세스를 포함하여 완전히 종료하고, TgWitness가 가져온 세션을 사용하는 동안 해당 인스턴스를 닫은 상태로 유지하십시오. **로그아웃하거나 세션을 취소하지 말고 종료하십시오: 세션** 취소 시 가져온 인스턴스도 무효화됩니다. 두 클라이언트를 모두 실행해야 하는 경우, **'독립적인 인증 생성'을** 선택하고 새로운 로그인이 성공할 때까지 Desktop을 닫아 두거나, 휴대폰 또는 QR 코드를 통해 TgWitness에 로그인하십시오. 전용 계정을 사용하는 것이 권장되지만, 클론된 키를 병렬로 사용하는 것이 안전해지는 것은 아닙니다.
>
>
>
> 이는 가져온 `.session` 파일, StringSession 텍스트 및 Auth Key HEX에도 적용됩니다. 독립적으로 생성된 인증 정보를 보유한 다른 클라이언트는 로그인 상태를 유지할 수 있습니다. [텔레그램의 AUTH_KEY_DUPLICATED 문서를](https://core.telegram.org/api/errors#406-not-acceptable) 참조하십시오.

1. 텔레그램 데스크톱을 완전히 종료하십시오.
2. `tdata`에서 다음 두 **항목만** 포함된 ZIP 파일을 생성하십시오:

   - `key_datas`
   - 그 옆에 있는 `s`로 끝나는 16자 파일(보통 `D877F783D5D3EF8Cs`)

   미디어 캐시가 포함된 전체 폴더를 ZIP 파일로 압축하면 대개 제한을 초과하게 됩니다 (512개 항목, 압축 해제 시 32 MiB). 3. ‘파일’에서 ZIP 파일을 선택합니다. 텔레그램 데스크톱에 **로컬 비밀번호가** 설정되어 있다면, 먼저 **‘비밀번호’ 또는 ‘세션 텍스트**’ 항목에 이를 입력하십시오. 이는 2단계 인증(2FA) 비밀번호가 아닙니다.

지원 사항: 아카이브당 계정 1개, 최신 `key_datas`/`key_data0`/`key_data1` 저장소, 로컬 암호. 미지원 사항: 여러 계정이 로그인된 폴더, 구형 데스크톱 레이아웃, 암호로 보호된 ZIP 파일, 별도의 macOS 전용 앱 “Telegram for macOS”.

### Telethon StringSession

일반적으로 `1`로 시작하며 길이가 약 350자인 단일 텍스트 줄입니다. 이를 `.txt` 또는 `.tgwitness-session` 파일(최대 4 KiB)로 불러오거나, **‘Passcode’ 또는 ‘session text’** 항목 아래에 붙여넣으십시오. Telethon 문자열만 허용되며, Pyrogram 및 TDLib 문자열은 다른 형식을 사용합니다.

### 계정 JSON

**`.json`**로 끝나는 파일 내에, 최대 **64 KiB** 크기의 JSON 객체 1개.

| 필드 (별칭) | 의미 |
| --- | --- |
| `api_id` (`app_id`) | 애플리케이션 ID, 양수 |
| `api_hash` (`app_hash`) | 애플리케이션 해시, 32자리 16진수 |
| `string_session` (`session_string`, `session_str`; 구식 `session`) | Telethon StringSession 텍스트이며, 파일 이름이 아닙니다. |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512자 전체 인증 키(Auth Key) 및 DC 1–5 |
| `user_id` (`id`) | 선택 사항; 권한 부여가 저장되기 전에 텔레그램과 대조하여 확인됨 |
| `device_model` (`device`) | 연결 장치 설명 |
| `system_version` (`sdk`) | 연결 OS 버전 |
| `app_version` | 텔레그램에 전송된 애플리케이션 버전 |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | 클라이언트 언어, 시스템 언어 및 클라이언트 언어 팩; 빈 `lang_pack`도 허용됩니다. |
| `tz_offset` | `initConnection.params`에 전송되는 선택적 UTC 오프셋(초 단위); 정수 또는 소수 정수 문자열 |

별칭과 주 이름이 모두 존재하는 경우, 둘은 일치해야 합니다. 명시적인 Telethon 세션 필드는 다른 형식의 일반적인 `session` 블롭보다 우선합니다. 만약 둘 다 식별 가능한 Telethon 세션을 포함하고 있다면, 동일한 인증을 설명해야 합니다. 명시적인 필드가 없는 경우, `session`은 유효한 Telethon StringSession이어야 합니다. 예시:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

첫 번째 예시는 API 인증 정보만 입력하는 경우입니다. 전화번호나 QR 코드를 통해 로그인하거나 세션 파일을 추가하십시오. 일괄 목록(계정 목록이 담긴 JSON 배열)은 지원되지 않습니다.

## 보유 중인 자료를 파악하세요

| 보시다시피 | 이 사이트는 | 사용법 |
| --- | --- | --- |
| `*.session`; 텍스트 편집기에서 열면 맨 위에 `SQLite format 3`가 표시됩니다. | Telethon 또는 Pyrogram SQLite | **파일** (자동 감지됨) |
| `tdata` 폴더 내에 `key_datas`가 포함되어 있습니다. | 텔레그램 데스크톱 TData | 두 파일을 ZIP으로 압축한 후, **‘파일’** |
| `1`로 시작하는 한 줄의 텍스트, 약 350자 | Telethon StringSession | **파일** |
| `*.json` 및 `app_id`/`app_hash` | 관련 메타데이터 | **파일** 및 해당 세션 |
| `*.json`와 `auth_key` 또는 `string_session` | 계정 JSON | **파일** |
| 512자 `0-9a-f` | 인증 키 | **인증 키** |
| 32자 `0-9a-f` | API 해시 | **API ID + 해시** |
| TDLib 앱의 `td.binlog` 또는 `db.sqlite` | TDLib 저장소 | 지원되지 않음 |
| `123456789:AA…` | 봇 토큰 | 지원되지 않음 |

## 지원되지 않는 형식

| 서식 | 대안 |
| --- | --- |
| TDLib 저장소 (`td.binlog`) 및 TDLib 내보내기 | 전화번호 또는 QR 코드로 로그인 |
| Pyrogram 세션 **문자열** | Pyrogram `.session` 파일을 사용하거나, 휴대폰/QR 코드를 이용하십시오. |
| 여러 계정이 로그인된 상태의 TData | 텔레그램 데스크톱에서 다른 계정에서 로그아웃하거나, 각 계정의 세션 파일을 사용하십시오. |
| 봇 토큰 | 지원되지 않는 기능: TgWitness는 사용자 계정으로 활동하지 않습니다. |
| 다수의 계정을 포함한 CSV/JSON 목록 | **계정 → 계정 가져오기**를 통해 지원되는 세션 파일을 가져오거나 별도의 작업 공간에서 전화번호/QR로 로그인하세요 |
| 테스트-DC 또는 봇 세션 | 실제 운영용 사용자 계정을 사용하십시오. |

## 여러 계정

계정 선택기 옆에 있는 **+**를 누르거나, **계정 → 설정 → 연결 설정 → 작업 공간을** 열고, 레이블을 입력한 후 로그인하십시오.

- 메인 워크스페이스를 포함하여 워크스페이스 수에 제한이 없습니다. 각 워크스페이스에는 고유한 세션, 프록시 경로, 소스, 캡처 정책, 저널, 서명 키, 체크포인트 및 내보내기 설정이 있습니다.
- 표시된 작업 공간을 전환하더라도 다른 작업 공간은 일시 중지되지 않습니다.
- 저널은 이를 생성한 계정에 고정됩니다. 다른 계정으로 로그인하려면 별도의 작업 공간이 필요하며, 하나의 계정을 두 개의 작업 공간에 할당할 수는 없습니다.
- 메인 패널 토큰은 모든 작업 공간을 제어합니다. [부여된 접근 권한을](https://phishdestroy.github.io/TgWitness/ko/docs/reference/access/) 통해 다른 사용자의 접근을 선택된 계정 및 채팅으로 제한할 수 있으며, 별도의 권한 및 세션 제한을 설정할 수 있습니다.
- **계정은** 워크스페이스의 이름을 변경하거나 추가된 워크스페이스를 삭제하며, 이때 해당 세션, 저널, 출처 및 서명 키도 함께 삭제됩니다. 메인 워크스페이스는 패널에서 삭제할 수 없습니다.

### 일괄 가져오기 및 계정 그룹

**‘계정’ → ‘계정 가져오기’를** 사용하여 여러 계정을 추가하고, 파일의 기본 이름을 기준으로 파일을 매칭하며 각 로그인 결과를 확인할 수 있습니다. 각 계정에는 고유한 작업 공간이 할당됩니다.

그룹은 세션, 키 또는 증거를 병합하지 않고 관련 계정들을 한데 묶어줍니다. **‘계정’** 메뉴의 **‘그룹 열기’를** 클릭하면 해당 페이지로 이동합니다. `/groups/<id>`:

- **계정:** 각 구성원의 접속 경로, 관찰 내용 및 마지막 메시지를 표시하며, **'모두** 시작' 및 **'모두 일시 중지'** 기능이 있습니다.
- **주의 필요:** 로그아웃되었거나, 사용할 수 없거나, 연결, 입력, 소스 또는 미디어 문제가 있는 계정; 각 이름은 해당 카드로 연결됩니다.
- **여러 계정이 볼 수 있는 채팅:** 공유된 출처, 이를 관찰하는 계정 및 사용 가능한 작업 공간 관찰 기간(최대 7일) 내의 중단 사항. **N개 계정으로 내보내기 시** , 채널 또는 슈퍼그룹 내보내기 파일을 해당 계정들 간에 분할하고 하나의 아카이브에 서명합니다.
- **그룹 내보내기:** 각 계정의 서명된 내보내기 파일이 포함된 ZIP 하나씩 `accounts/` 아래에 `manifest.json` 각 계정의 SHA-256 및 키 지문 목록을 포함하며, 이는 메인 워크스페이스에서 `manifest.signature.json`. 각 계정 아카이브는 `python -m tgwitness.verify` 해당 계정의 신뢰할 수 있는 지문으로 개별적으로 검증하십시오.

멤버들은 그룹 설정을 공유하며, 각 계정은 자체 설정을 유지할 수 있습니다. [공유 설정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/settings/#account-groups), [가져오기 및 그룹 가이드](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) 그리고 [MTProxy 풀 대시보드를](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources) 참조하세요.

## 로그아웃

**계정 → 텔레그램에서 로그아웃**(관찰 일시 중지)은 텔레그램에 세션 종료를 요청하므로, 해당 세션은 계정의 **설정 →**기기에서 사라지고, 워크스페이스 볼트에서도 제거됩니다. 기록, 소스, 설정 및 서명 키는 유지되며, 기록에는 로그아웃 내역이 남습니다. 워크스페이스는 여전히 해당 계정에 속합니다: 오직 그 계정만이 다시 연결할 수 있습니다. 텔레그램이 응답하지 않더라도 세션은 여전히 여기에서 제거되며 패널에 해당 내용이 표시됩니다. 텔레그램의 **설정 →**기기에서 세션을 종료하십시오.

## 계정 파일 안전하게 보관하기

- 모든 `.session`, TData ZIP, StringSession, 인증 키 및 계정 JSON을 비밀번호처럼 취급하십시오. TgWitness는 가져온 인증 정보를 암호화된 금고에 보관하므로, 나중에 원본 파일을 삭제해도 됩니다.
- 동일한 인증 정보를 두 개의 프로그램에서 동시에 실행하지 마십시오. 텔레그램에서 인증을 취소할 수 있으며 (`AUTH_KEY_DUPLICATED`), 이 경우 두 프로그램 모두 작동이 중단됩니다.
- 만료되거나 취소된 세션은 변환을 통해 복구할 수 없습니다. 다시 로그인하십시오.

## 문제 해결

| 메시지 또는 증상 | 사용 방법 |
| --- | --- |
| *이 세션을 읽을 수 없습니다. 해당 클라이언트를 닫으십시오…* | SQLite 파일이 열려 있거나 미완성 상태입니다(`-journal`/`-wal` 사이드카). 원래 프로그램을 정상적으로 종료한 후 파일을 다시 복사하십시오. |
| *지원되는 Telethon SQLite 스키마: 7 및 8* / *Pyrogram … 2 및 3* | 이 파일은 매우 오래된 버전이나 알 수 없는 버전의 라이브러리를 사용하여 생성되었습니다. 대신 전화번호나 QR 코드를 통해 로그인하십시오. |
| *승인된 프로덕션 사용자 세션만 지원됩니다.* | 이 Pyrogram 파일은 봇이나 테스트 네트워크에 속합니다. |
| *TData 아카이브의 항목 수가 512개 또는 32 MiB를 초과함* | 전체 폴더가 아닌, ZIP 파일 중 `key_datas`와 `D877F783D5D3EF8Cs`만 포함됩니다. |
| *TData를 해독할 수 없습니다. 데스크톱 로컬 암호를 확인하십시오.* | **'패스코드' 또는 '세션 텍스트**' 항목에 텔레그램 데스크톱의 로컬 패스코드를 입력하십시오. |
| *TData 계정은 한 번에 하나씩 가져올 수 있습니다.* | 텔레그램 데스크톱에는 여러 계정이 있었습니다. [‘지원되지 않는 형식’을](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#unsupported-formats) 참조하십시오. |
| *선택된 파일들은 서로 다른 계정이나 API 인증 정보를 설명합니다.* | 단일 계정의 파일만 선택하십시오. |
| *JSON에 지원되는 API 자격 증명이나 인증 정보가 포함되어 있지 않습니다.* | [계정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/#account-json)JSON의 필드 이름을 확인하십시오. |
| *API 메타데이터만 포함* | 이 JSON 파일에는 세션 정보가 포함되어 있지 않습니다. `.session` 파일을 추가하거나 전화번호/QR 코드를 사용하십시오. |
| *인증 키(Auth Key) HEX에는 512개의 16진수 문자가 모두 포함되어야 합니다.* | 키가 잘렸거나 ‘`…`’가 포함되어 있습니다. |
| 계정 ID가 가져온 계정과 일치하지 않습니다. | 이 파일의 사용자 ID는 텔레그램이 보고한 내용과 다릅니다. 이 파일은 다른 계정의 것입니다. |
| 이 계정은 이미 다른 워크스페이스에 속해 있습니다. | 계정을 두 번 추가하는 대신 해당 작업 공간을 열어주세요. |
| 연결되어 있지만, **‘Sources**’의 채팅 목록에서 비공개 그룹이 누락되어 있습니다. | 멤버십 확인. 피커는 처음 1,000개의 대화를 검사합니다. **‘Parameters’에서** 한도를 늘리십시오. |
| 프록시 연결 실패 | 경로 및 IP 모드를 확인하세요. 자동 MTProxy은 작동하는 다른 항목을 시도합니다. ‘주소 숨기기’는 대기하며, 최후의 수단인 ‘직접 연결’은 설정된 지연 시간이 지난 후 직접 연결할 수 있습니다. [라우팅 모드를](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/#ip-modes) 참조하세요. |

참조: 프록시 및 암호화와 관련된 [연결 및 보안](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/), 그리고 로그인 후 수집되는 데이터의 [수집 방식](https://phishdestroy.github.io/TgWitness/ko/docs/reference/collection/).
