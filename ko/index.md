# 메시지는 변합니다. 본 내용을 그대로 보관하세요.

Canonical page: https://phishdestroy.github.io/TgWitness/ko/

[오픈 소스 / v0.7.1](https://phishdestroy.github.io/TgWitness/ko/docs/reference/changelog/)

텔레그램 메시지를 캡처하고, 변경 내역을 보존하며, 서명된 기록을 내보냅니다.

[데모 열기](https://phishdestroy.github.io/TgWitness/demo/?lang=ko)[설정 가이드](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko)

데모에는 가상의 데이터가 사용됩니다. 텔레그램 로그인은 필요하지 않습니다.

 [GitHub Actions로 수집 (미리 보기)](https://phishdestroy.github.io/TgWitness/ko/docs/capture/) [S3 오프사이트 백업: 설정 및 복구](https://phishdestroy.github.io/TgWitness/ko/#s3)

시간을 초월한 메시지 #0042

Northstar · 연구가상의 출처 / 메시지 42

1. **감지된 메시지:**09:41:02

   브리핑은 14:00에서 시작됩니다.
2. **편집 내역 보존됨**09:43:18

   브리핑은 15:00에서 시작됩니다.

   이전 버전은 그대로 유지됨
3. **삭제 알림**10:06:45

   캡처된 콘텐츠는 귀하의 저널에 보관됩니다.

세 가지 관찰. 하나의 역사. 예시

메시지는 사라지지만, 캡처된 기록은 남습니다.

## 포착된 모든 변경 사항. 필요한 바로 그곳에서.

가상의 데모 데이터를 통해 인터페이스를 둘러보세요.

TgWitness / 저장된 채팅여러분의 관찰 작업 공간

![다크 테마로 저장된 텔레그램 대화 내역으로, 수정 및 삭제된 메시지도 맥락을 유지한 채 캡처되어 보관됩니다.](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / 저장된 채팅 메시지: 메시지 옆에 편집 내역 및 삭제 알림이 함께 표시되는, 익숙한 대화 보기 화면입니다.

TgWitness / 저널로컬 작업 공간

![관찰된 메시지, 수정 내역, 삭제 알림 및 관련 이벤트가 포함된 기록부](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / 저널: 중단 사항을 포함하여 귀하의 계정이 감지한 내용을 검색 가능한 타임라인 형태로 제공합니다.

TgWitness / 수정 내역로컬 작업 공간

![메시지의 캡처된 이전 버전과 수정된 버전을 비교하는 상세 정보 패널](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / 편집 내역: 이전 기록을 덮어쓰지 않고 캡처된 버전을 비교할 수 있습니다.

TgWitness / 서명된 내보내기 파일로컬 작업 공간

![서명된 ZIP, JSONL, CSV 파일 및 오프라인 HTML 보고서를 제공하는 워크스페이스 내보내기 기능](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / 서명된 내보내기: 매니페스트와 독립적인 검증 기관을 통해 증거 일지를 어디서나 활용할 수 있습니다.

01 / 캡처

### 범위는 사용자가 직접 선택합니다.

선택한 채팅, 텔레그램 폴더 또는 전체 계정을 기록할 수 있습니다. 계정마다 별도의 작업 공간이 제공됩니다.

[수집 모드 비교](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#scope)

02 / 보존

### 변경 사항은 이야기에 더해집니다.

캡처된 버전, 삭제 알림 및 관찰 누락 내역은 기록부에 그대로 유지됩니다.

[이벤트 매트릭스 참조](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#events)

03 / 인계

### 이동하는 기록.

서명된 ZIP 파일, 원본 파일 보존 및 오프라인 보고서 제공. 선택적 암호 보호 기능.

[내보내기 및 검증](https://phishdestroy.github.io/TgWitness/ko/docs/exports/)

## 바이트 하나만 변경해도 체인이 알려줍니다.

각 이벤트는 이전 해시에 연결되며 Ed25519 서명을 포함합니다.

![캡처된 이벤트는 이전 해시 값과 연결되며, 서명이 포함되어 있고 검증 가능한 형식으로 내보내집니다.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![캡처된 기록을 변경하면 해당 기록의 해시가 변경되어, 연결된 기록의 검증 기능이 무효화됩니다.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![별도로 보관된 체크포인트를 통해 수신자는 내보낸 기록부와 이전의 관찰 내용을 비교할 수 있습니다.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

각 검증 메커니즘이 무엇을 입증하는지, 그리고 그 한계가 어디에 있는지 확인해 보십시오.

[8가지 증거 수준 살펴보기](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#levels)

## 다른 분의 검토를 기다립니다.

관찰 결과, 파일 및 오프라인 HTML 보고서를 하나의 서명된 번들로 전달합니다.

[증거 모델 읽어보기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/)

tgwitness-evidence.zip서명된 번들

- 01

  원본 관찰 내용JSONL 기록 + CSV 테이블
- 02

  읽기 쉬운 문맥오프라인 HTML 보고서 + 보존된 미디어
- 03

  독립적인 검증서명된 매니페스트 + 독립형 검증기

서명은 신뢰할 수 있는 키를 기준으로 변조를 감지합니다. 이는 텔레그램 발신 출처를 증명하거나 완전한 캡처를 보장하지는 않습니다. 저널 콘텐츠와 미디어는 사용자가 직접 제공하는 암호화된 저장 공간에 보관해야 합니다.

## S3 백업. 외부 검증.

암호화된 사본을 보관하고 독립적인 검증 절차를 추가하십시오.

기본적으로 비활성화됨

### 모든 내용을 S3 호환 스토리지에 복사

저널, 파일, 타임스탬프가 포함된 체크포인트 및 채팅 내역 내보내기 — AWS S3 또는 호환 가능한 저장소로 업로드되기 전에 암호화됩니다.

**저장 설정 및 복구**

클라이언트 측 암호화

`AES-256-GCM`는 이 시스템에 있는 객체를 암호화합니다. 제공자는 암호화된 객체를 수신합니다.

예약 또는 수동 복사

지금 복사하거나 1분에서 1,440분 사이의 간격을 선택하세요. 패널에서 진행 상황을 확인하세요.

Object Lock

버킷이 지원하는 경우 보존 기간과 모드를 선택하십시오. 이 패널은 업로드된 객체에 대해 보존이 확인되었는지 여부를 표시합니다.

검증된 복구

암호화 키를 다운로드하여 별도로 보관하십시오. 다른 컴퓨터에서 복원하십시오. 파일은 검증 완료 후에만 공개됩니다.

![오프사이트 복사 패널 전체: 엔드포인트, 리전, 버킷, 액세스 키, 일정, 오브젝트 잠금 및 복구 키 제어](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

고급 옵션이 포함된 전체 패널이 펼쳐진 모습입니다. 저장소 인증 정보는 표시되지 않습니다.

저널 및 미디어`AES-256-GCM`S3 호환 스토리지

[S3 구성 및 사본 복원](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3)[검증 세부 정보 읽기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#off-site-copy-and-restore-s3)

**기능**: 내보낸 복호화 키가 없으면 메시지를 복원하지 않으며, 독립적인 증인을 대체하지도 **않습니다**.

### 알림 · 알림

Apprise를 통해 문제 알림, 채팅 변경 사항 및 일일 요약 정보를 메신저, 이메일 또는 사용자 지정 JSON 웹훅으로 받아볼 수 있습니다.

'발췌문' 기능을 활성화하지 않는 한 메시지 본문을 전송하지 **않습니다**.

 [알림 수신처 설정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/operations/#notifications)

### 외부 타임스탬프

RFC 3161 및 OpenTimestamps를 사용한 타임스탬프 체크포인트 해시.

**하지 않는 사항**: 처리 중인 캘린더 수신 내역을 확인된 비트코인 타임스탬프로 간주하지 않습니다.

 [타임스탬프 증빙 자료 확인:](https://phishdestroy.github.io/TgWitness/ko/docs/reference/timestamp/)

### 독립적인 증인

별도의 호스트가 서명된 관측 기록을 보관하며, `TGW1` 체크포인트를 공개할 수 있습니다.

**하지 않는** 사항: 하나의 수집기 호스트에 있는 두 개의 작업 공간을 독립적인 위트니스로 만들지 않습니다.

 [Witness 설정하기](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)

### 복구 및 확인 가능한 누락 사항

재시작 후 이력서. 재확인 및 `coverage.json`를 통해 복구된 메시지와 누락된 부분을 확인할 수 있습니다.

**하지 않는** 기능: 누락된 편집 내역이나 사라진 메시지를 모두 복원하지는 않습니다.

 [연속성 및 누락 사항 확인](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#continuity)

## 첫 번째 작업 공간은 여기서 시작됩니다.

먼저 데모를 살펴보세요. 준비가 되면 전용 계정을 연결하세요. Windows, Linux, macOS 또는 Docker에서 사용 가능합니다.

[설정 가이드 읽기](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko)

**가져온 세션 1개, 실행 중인 클라이언트 1개.**

텔레그램 데스크톱과 TgWitness에서 가져온 TData/세션 키를 동시에 실행하지 마십시오. 텔레그램에서 공유된 인증 정보가 무효화될 수 있습니다(AUTH_KEY_DUPLICATED). 병행하여 사용하려면 전화번호나 QR 코드를 통해 별도의 TgWitness 계정을 생성하십시오.

[세션 가져오기 경고 읽기](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko#session-warning)

**연결하기 전에 먼저 확인해 보세요.**

텔레그램 계정 없이 가상의 작업 공간을 체험해 보세요.

[온라인 데모 열기 →](https://phishdestroy.github.io/TgWitness/demo/?lang=ko)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**로컬 설치 명령어**

1단계

### 소스 코드 받기.

[소스 ZIP 파일을 다운로드하여](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) 압축을 풀거나, 저장소를 클론하세요:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

소스 런처를 실행하려면 Python 3.11 이상이 필요합니다. Windows 런처는 Python이 설치되어 있지 않은 경우 자동으로 설치해 줍니다.

[릴리스 보기](https://github.com/phishdestroy/TgWitness/releases)

Windows에 Python이 설치되어 있지 않으신가요? [휴대용 패키지를 다운로드하여](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.1/TgWitness-0.7.1-windows-amd64-portable.zip) 압축을 풀고, ‘`TgWitness.cmd`’ 파일을 더블클릭하세요.

2단계

### 실행 방식을 선택하세요.

`Start.cmd`를 더블 클릭하거나 PowerShell에서 다음 명령을 실행하십시오:

```
.\Start.cmd
```

그냥 둘러보고 계신가요? `scripts\Demo.cmd`를 더블 클릭하면 독립형 데모를 체험할 수 있습니다. 텔레그램 로그인은 필요하지 않습니다.

Python 3.11 이상 및 `venv`가 지원되는 경우:

```
sh start.sh
```

가상의 저널을 열려면 `sh start.sh --demo`를 실행하십시오.

Docker가 실행 중이고 Compose 2.20 이상이 설치된 상태에서:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

두 번째 명령어는 개인 패널 토큰을 표시합니다. 이 토큰은 본인의 컴퓨터에 보관하십시오.

실행 후 [127.0.0.1:8787에서 를](http://127.0.0.1:8787) 열어주세요.

소스 코드 설치 시 토큰은 `data/live/panel-token.txt`입니다. 텔레그램 로그인은 내장된 API 설정을 사용하거나 [my.telegram.](https://my.telegram.org)org에서 생성한 본인만의 키 쌍을 사용할 수 있습니다. [전체 설정 가이드 ↗](https://phishdestroy.github.io/TgWitness/ko/docs/reference/quickstart/)

**TgWitness 0.7.1** [새로운 소식 →](https://phishdestroy.github.io/TgWitness/ko/docs/reference/changelog/) · [기능 및 알려진 제한 사항 →](https://phishdestroy.github.io/TgWitness/ko/docs/reference/features/)

## 명확한 지침. 유용한 다음 단계.

[가이드 살펴보기 ↗](https://phishdestroy.github.io/TgWitness/ko/docs/)

[### 모드, 시나리오 및 증거 등급 4가지 수집 모드. 8단계 검증 수준. 귀하의 사건에 적합한 워크플로를 찾아보세요.](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html)

[01 ### 계정 연결 전화번호, QR 코드 및 지원되는 세션 가져오기 기능을 제공합니다.](https://phishdestroy.github.io/TgWitness/ko/docs/accounts/)[02 ### 프록시 선택 공개 MTProxy 목록 또는 사용자 지정 경로.](https://phishdestroy.github.io/TgWitness/ko/docs/proxies/)[03 ### Witness 봇 설정하기 텔레그램 채널 내의 서명된 체크포인트.](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)[04 ### 내보내기 및 검증 캡처된 기록을 공유하고 그 무결성을 확인하세요.](https://phishdestroy.github.io/TgWitness/ko/docs/exports/)

## 아카이브를 살펴보세요.

이력을 불러오고, AI 출처를 검토하며, MCP 클라이언트를 연결하고, 저장된 미디어를 인식하며, 서명된 웹훅을 전송합니다.

[워크플로우 살펴보기](https://phishdestroy.github.io/TgWitness/ko/docs/archive/)

## 시작하기 전에.

**이 페이지는 텔레그램과 연결되어 있나요?**

아닙니다. 이 페이지는 가상의 예시와 스크린샷이 포함된 정적 프로젝트 페이지입니다. 실제 애플리케이션은 사용자의 컴퓨터나 서버에서 실행되며, 로그인 절차도 해당 환경에서 이루어집니다.

**캡처되기 전에 삭제된 메시지도 복구할 수 있나요?**

아닙니다. TgWitness는 수집이 진행되는 동안 귀하의 계정이 확인한 콘텐츠를 보관합니다. 이후의 기록 스냅샷으로는 놓친 수정 내역이나 삭제된 메시지를 복원할 수 없습니다.

**저널 전체가 암호화되어 있나요?**

계정 인증 정보와 서명 비밀키는 암호화된 볼트에 저장됩니다. 로컬 메시지와 첨부 파일은 암호화된 디스크 또는 볼륨에 저장해야 합니다. 내보내기 시에는 선택적으로 암호로 보호된 AES-256 ZIP 파일을 사용할 수 있습니다.

**이 사이트는 텔레그램과 제휴 관계에 있습니까?**

아닙니다. TgWitness는 MIT 라이선스로 배포되는 Telethon을 사용하는 독립적인 프로젝트입니다. 사용자는 내장된 API 설정이나 자체 API 키를 사용하여 자신의 계정을 직접 인증합니다.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## 먼저 둘러보세요. 준비가 되면 설정을 진행하세요.

[데모 열기](https://phishdestroy.github.io/TgWitness/demo/?lang=ko)[설정 가이드](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko)
