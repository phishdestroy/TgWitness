# 메시지는 변합니다． 본 내용을 그대로 보관하세요．

Canonical page: https://phishdestroy.github.io/TgWitness/ko/

[오픈 소스 ／ v0.9.1](https://phishdestroy.github.io/TgWitness/ko/docs/reference/changelog/)

텔레그램 채팅 내용을 내보내고， 대화 내역을 보존하며， 다른 사람이 검증할 수 있는 서명된 아카이브를 공유합니다．

[데모 열기](https://phishdestroy.github.io/TgWitness/demo/?lang=ko)[설정 가이드](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko)

가짜 데이터， 텔레그램 로그인 없음．

 [계정 또는 선택한 채팅 내보내기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/account-export/) [GitHub Actions로 수집 （미리 보기）](https://phishdestroy.github.io/TgWitness/ko/docs/capture/) [S3 오프사이트 백업： 설정 및 복구](https://phishdestroy.github.io/TgWitness/ko/#s3)

시간을 초월한 메시지 ＃0042

Northstar · 연구가상의 출처 ／ 메시지 42

1. **감지된 메시지：**09：41：02

   브리핑은 14：00에서 시작됩니다．
2. **편집 내역 보존됨**09：43：18

   브리핑은 15：00에서 시작됩니다．

   이전 버전은 그대로 유지됨
3. **삭제 알림**10：06：45

   캡처된 콘텐츠는 귀하의 저널에 보관됩니다．

세 가지 관찰． 하나의 역사． 예시

메시지는 사라지지만， 캡처된 기록은 남습니다．

## 포착된 모든 변경 사항． 필요한 바로 그곳에서．

실제 화면에 지어낸 데이터를 넣었습니다．

TgWitness ／ 저장된 채팅여러분의 관찰 작업 공간

![다크 테마로 저장된 텔레그램 대화 내역으로， 수정 및 삭제된 메시지도 맥락을 유지한 채 캡처되어 보관됩니다．](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ 저장된 채팅 평범한 채팅처럼 보이며， 편집과 삭제가 메시지 바로 옆에 표시됩니다．

TgWitness ／ 저널로컬 작업 공간

![관찰된 메시지， 수정 내역， 삭제 알림 및 관련 이벤트가 포함된 기록부](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ 저널 계정이 본 모든 것을 검색할 수 있고， 공백도 기록됩니다．

TgWitness ／ 수정 내역로컬 작업 공간

![메시지의 캡처된 이전 버전과 수정된 버전을 비교하는 상세 정보 패널](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ 편집 기록 이전 버전과 새 버전을 나란히 보여 주며， 아무것도 덮어쓰지 않습니다．

TgWitness ／ 서명된 내보내기 파일로컬 작업 공간

![서명된 ZIP， JSONL， CSV 파일 및 오프라인 HTML 보고서를 제공하는 워크스페이스 내보내기 기능](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ 서명된 내보내기 저널을 서명된 상태로， 자체 검증 도구와 함께 가져갈 수 있습니다．

[케이스 보드](https://phishdestroy.github.io/TgWitness/ko/docs/case-board/)， [보고서 설계](https://phishdestroy.github.io/TgWitness/ko/docs/reports/) 및 [공유 사본](https://phishdestroy.github.io/TgWitness/ko/docs/handover/)을 통해 저장된 기록을 추적하십시오． [계정 그룹을](https://phishdestroy.github.io/TgWitness/ko/docs/groups/) 함께 [검토하십시오](https://phishdestroy.github.io/TgWitness/ko/docs/groups/)．

01 ／ 캡처

### 범위는 사용자가 직접 선택합니다．

채팅 몇 개， 폴더 하나 또는 계정 전체． 계정마다 자체 작업 공간이 있습니다．

[수집 모드 비교](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#scope)

02 ／ 보존

### 변경 사항은 이야기에 더해집니다．

버전， 삭제， 공백은 모두 저널에 남습니다．

[이벤트 매트릭스 참조](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#events)

03 ／ 인계

### 이동하는 기록．

서명된 ZIP， 파일， 오프라인 보고서． 비밀번호는 선택 사항입니다．

[내보내기 및 검증](https://phishdestroy.github.io/TgWitness/ko/docs/exports/)

## 바이트 하나만 변경해도 검증 과정에서 바로 파악할 수 있습니다．

각 이벤트는 이전 해시에 연결되며 Ed25519 서명을 포함합니다．

![캡처된 이벤트는 이전 해시 값과 연결되며， 서명이 포함되어 있고 검증 가능한 형식으로 내보내집니다．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![캡처된 기록을 변경하면 해당 기록의 해시가 변경되어， 연결된 기록의 검증 기능이 무효화됩니다．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![별도로 보관된 체크포인트를 통해 수신자는 내보낸 기록부와 이전의 관찰 내용을 비교할 수 있습니다．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

파일 해시부터 별도로 보관된 체크포인트에 이르기까지의 검증 절차를 따르십시오．

[8가지 증거 수준 살펴보기](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#levels)

## 다른 분의 검토를 기다립니다．

메시지， 파일， 오프라인 보고서를 하나의 서명된 묶음으로．

[증거 모델 읽어보기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/)

tgwitness-evidence.zip서명된 번들

- 01

  원본 관찰 내용JSONL 기록 ＋ CSV 테이블
- 02

  읽기 쉬운 문맥오프라인 HTML 보고서 ＋ 보존된 미디어
- 03

  독립적인 검증서명된 매니페스트 ＋ 독립형 검증기

받는 사람은 귀하의 키로 모든 것을 확인하고， 다른 곳에 보관한 체크포인트가 그 이후 아무것도 다시 쓰이지 않았음을 보여 줍니다． [확인 방식 보기．](https://phishdestroy.github.io/TgWitness/ko/docs/concepts/#layers)

## S3 백업． 외부 검증．

암호화된 사본을 보관하고 독립적인 검증 절차를 추가하십시오．

기본적으로 비활성화됨

### 모든 내용을 S3 호환 스토리지에 복사

저널， 파일， 체크포인트， 채팅 내보내기를 S3로 보내기 전에 암호화합니다．

**저장 설정 및 복구**

클라이언트 측 암호화

`AES-256-GCM`은 귀하의 컴퓨터에서 실행됩니다． 공급자는 암호문만 봅니다．

예약 또는 수동 복사

지금 복사하거나 1～1，440분마다 복사하며， 진행 상황은 패널에 표시됩니다．

Object Lock

보존 일수와 모드를 고르면 패널이 실제로 적용되었는지 확인합니다．

검증된 복구

키는 따로 보관하십시오． 어디서나 복원할 수 있으며， 파일은 검증을 통과한 후에만 나옵니다．

![오프사이트 복사 패널 전체： 엔드포인트， 리전， 버킷， 액세스 키， 일정， 오브젝트 잠금 및 복구 키 제어](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

고급 옵션이 포함된 전체 패널이 펼쳐진 모습입니다． 저장소 인증 정보는 표시되지 않습니다．

저널 및 미디어`AES-256-GCM`S3 호환 스토리지

[S3 구성 및 사본 복원](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3)[검증 세부 정보 읽기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#off-site-copy-and-restore-s3)

**복구 키** 따로 보관하십시오． 없으면 사본을 읽을 수 없습니다．

### 알림 · 알림

문제， 채팅 변화， 일일 요약을 메신저， 이메일 또는 자체 웹훅으로 보냅니다．

**공유할 내용 선택** 켜지 않으면 메시지 본문은 포함되지 않습니다．

 [알림 수신처 설정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/operations/#notifications)

### 외부 타임스탬프

RFC 3161 및 OpenTimestamps를 사용한 타임스탬프 체크포인트 해시．

**결과 확인** TSA 응답을 확인하거나 OpenTimestamps 영수증을 비트코인 증명으로 업그레이드합니다．

 [타임스탬프 증빙 자료 확인：](https://phishdestroy.github.io/TgWitness/ko/docs/reference/timestamp/)

### 독립적인 증인

별도의 호스트가 서명된 관측 기록을 보관하며， `TGW1` 체크포인트를 공개할 수 있습니다．

**기준 분리** 별도의 키와 저널로 다른 호스트에서 실행합니다．

 [Witness 설정하기](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)

### 복구 및 확인 가능한 누락 사항

재시작 후 이력서． 재확인 및 `coverage.json`를 통해 복구된 메시지와 누락된 부분을 확인할 수 있습니다．

**구간 검토** 복구된 메시지와 기록된 공백을 나란히 봅니다．

 [연속성 및 누락 사항 확인](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html#continuity)

## 첫 번째 작업 공간은 여기서 시작됩니다．

먼저 데모를 써 보고， 준비되면 예비 계정을 연결하십시오．
Windows， Linux， macOS 또는 Docker．

[설정 가이드 읽기](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko)

**가져온 세션 1개， 실행 중인 클라이언트 1개．**

가져온 TData나 세션을 Telegram Desktop과 TgWitness에서 동시에 실행하지 마십시오． 텔레그램이 둘 다 끊을 수 있습니다（AUTH_KEY_DUPLICATED）． 둘 다 필요하면 전화번호나 QR로 TgWitness에 따로 로그인하십시오．

[세션 가져오기 경고 읽기](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko#session-warning)

**연결하기 전에 먼저 확인해 보세요．**

텔레그램 계정 없이 가상의 작업 공간을 체험해 보세요．

[온라인 데모 열기 →](https://phishdestroy.github.io/TgWitness/demo/?lang=ko)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**로컬 설치 명령어**

1단계

### 소스 코드 받기．

[소스 ZIP 파일을 다운로드하여](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) 압축을 풀거나， 저장소를 클론하세요：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Python 3.11 이상이 필요합니다． Windows에서는 런처가 설치를 제안합니다．

[릴리스 보기](https://github.com/phishdestroy/TgWitness/releases)

2단계

### 실행 방식을 선택하세요．

`Start.cmd`를 더블 클릭하거나 PowerShell에서 다음 명령을 실행하십시오：

```
.\Start.cmd
```

그냥 둘러보고 계신가요？ `scripts\Demo.cmd`를 더블 클릭하면 독립형 데모를 체험할 수 있습니다． 텔레그램 로그인은 필요하지 않습니다．

Python 3.11 이상 및 `venv`가 지원되는 경우：

```
sh start.sh
```

가상의 저널을 열려면 `sh start.sh --demo`를 실행하십시오．

Docker가 실행 중이고 Compose 2.20 이상이 설치된 상태에서：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

두 번째 명령어는 개인 패널 토큰을 표시합니다． 이 토큰은 본인의 컴퓨터에 보관하십시오．

실행 후 [127.0.0.1:8787에서 를](http://127.0.0.1:8787) 열어주세요．

소스 설치에서는 토큰이 `data/live/panel-token.txt`에 있습니다． [my.telegram.org](https://my.telegram.org)에서 받는 자체 API 쌍은 선택 사항입니다． [전체 설정 가이드 ↗](https://phishdestroy.github.io/TgWitness/ko/docs/reference/quickstart/)

**TgWitness 0.9.1** [새로운 소식 →](https://phishdestroy.github.io/TgWitness/ko/docs/reference/changelog/) · [기능 및 알려진 제한 사항 →](https://phishdestroy.github.io/TgWitness/ko/docs/reference/features/)

## 명확한 지침． 유용한 다음 단계．

[가이드 살펴보기 ↗](https://phishdestroy.github.io/TgWitness/ko/docs/)

[### 모드， 시나리오 및 증거 등급 4가지 수집 모드． 8단계 검증 수준． 귀하의 사건에 적합한 워크플로를 찾아보세요．](https://phishdestroy.github.io/TgWitness/ko/guides/modes.html)

[01 ### 계정 연결 전화번호， QR 코드 및 지원되는 세션 가져오기 기능을 제공합니다．](https://phishdestroy.github.io/TgWitness/ko/docs/accounts/)[02 ### 프록시 선택 공개 MTProxy 목록 또는 사용자 지정 경로．](https://phishdestroy.github.io/TgWitness/ko/docs/proxies/)[03 ### Witness 봇 설정하기 텔레그램 채널 내의 서명된 체크포인트．](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)[04 ### 내보내기 및 검증 캡처된 기록을 공유하고 그 무결성을 확인하세요．](https://phishdestroy.github.io/TgWitness/ko/docs/exports/)

## 아카이브를 살펴보세요．

기록， 출처가 있는 AI， MCP， OCR， 서명된 웹훅．

[워크플로우 살펴보기](https://phishdestroy.github.io/TgWitness/ko/docs/archive/)

## 시작하기 전에．

**이 페이지는 텔레그램과 연결되어 있나요？**

아니요． 가짜 예시가 있는 정적 페이지입니다． 앱은 귀하의 컴퓨터에서 실행되며 로그인도 거기서 합니다．

**캡처되기 전에 삭제된 메시지도 복구할 수 있나요？**

아니요． 실행 중에 계정이 본 것만 보관합니다． 나중에 찍은 스냅샷으로는 놓친 편집이나 삭제된 메시지를 재구성할 수 없습니다．

**저널 전체가 암호화되어 있나요？**

세션과 키는 암호화됩니다． 메시지와 파일은 아니므로 디스크 암호화를 사용하십시오． 내보내기에는 AES－256 비밀번호를 걸 수 있습니다．

**이 사이트는 텔레그램과 제휴 관계에 있습니까？**

아니요． Telethon 기반의 MIT 라이선스 독립 프로젝트입니다． 귀하의 계정으로 로그인합니다．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## 먼저 둘러보세요． 준비가 되면 설정을 진행하세요．

[데모 열기](https://phishdestroy.github.io/TgWitness/demo/?lang=ko)[설정 가이드](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko)
