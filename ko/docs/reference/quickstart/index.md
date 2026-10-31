# 빠른 시작

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/quickstart/

TgWitness를 설치하고 실행하는 모든 방법: Windows 패키지, Python, Docker 및 종합 데모와 초기 점검 절차.

**영어** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [우크라이나어](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [포르투갈어 (브라질)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [우르두어](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [인도네시아어](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [베트남어](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [간체 중국어](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness는 사용자의 계정이 접근할 수 있는 텔레그램 그룹 및 채널을 모니터링하기 위한 독립형 애플리케이션입니다. 이 애플리케이션은 자체 데이터 디렉터리를 사용하여 로컬에서 실행됩니다.

**처음 방문하셨나요?** 계정을 연결하기 전에 [데모를 살펴보세요](https://phishdestroy.github.io/TgWitness/ko/docs/reference/quickstart/#explore-the-interface). 프록시, 위트니스, 데이터 내보내기 또는 서버 설정에 대한 [가이드를 선택하세요](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md).

## 설치 및 시작

[GitHub Actions로 수집 (미리 보기)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

다음 방법 중 하나를 선택하십시오. 릴리스 빌드가 공개된 후 휴대용 다운로드 파일을 이용할 수 있습니다:

| 호스트 | 설치된 항목 없음 | 출처: Python 3.11 이상 | Docker: Engine/Desktop (Compose 2.20 이상) |
| --- | --- | --- | --- |
| Windows | GitHub 릴리스에서 `TgWitness-<version>-windows-amd64-portable.zip`를 추출한 후, `TgWitness.cmd`를 더블 클릭하세요. | `Start.cmd`를 더블 클릭하세요 | `scripts\Docker.cmd`를 더블 클릭하세요 |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

소스 코드를 확인하려면 GitHub 릴리스에서 소스 ZIP 파일을 다운로드하여 압축을 풀거나 저장소를 클론하십시오. `Start.cmd`는 적합한 Python이 발견되지 않을 경우 (winget 또는 python.org의 서명된 설치 프로그램) Windows 사용자를 위해 Python 3.12를 설치해 줍니다. `start.sh`는 Python이 없는 경우 사용자의 Linux 배포판이나 macOS에 맞는 정확한 설치 명령어를 출력합니다. 소스 코드를 처음 실행하면 `.venv`가 생성되고 종속성이 자동으로 설치됩니다.

Docker가 애플리케이션을 빌드하고 백그라운드에서 실행하므로, 호스트 측에서 Python을 설치할 필요가 없습니다. 컨테이너 상태가 정상일 때 `scripts\Docker.cmd`와 `scripts/docker-start.sh`가 패널 주소와 토큰을 출력합니다. 지원되는 모든 호스트에서 사용할 수 있는 해당 Docker 명령어는 다음과 같습니다:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

**http://127.0.0.1:8787**을 엽니다. Docker 헬퍼나 두 번째 Docker 명령어로 출력된 토큰을 사용하거나, 포터블 또는 소스 설치의 경우 **data/live/panel-token.txt 파일을** 참조하십시오. 아래의 **'텔레그램 연결'** 단계로 진행하십시오. 네이티브 설치와 Docker 설치는 별도의 저장소를 사용하며, Docker를 시작한다고 해서 기존 네이티브 저널이 가져오지 않습니다.

서버의 경우, [배포 과정에는](https://phishdestroy.github.io/TgWitness/ko/docs/reference/deployment/) 자동 HTTPS 설정, 재시작, 공개된 이미지, 업데이트 및 백업이 포함됩니다.

## 인터페이스 살펴보기

1. 휴대용 패키지에서 **TgWitness-Demo.cmd를** , Windows 소스 폴더에서 **scripts\Demo.cmd를** , 또는 Linux/macOS에서 `sh start.sh --demo` 를 실행하십시오. 소스에서 처음 실행하면 `.venv` 가 생성되고 종속성이 설치됩니다.
2. **http://127.0.0.1:8787을** 열어보세요.
3. 로컬 데모를 실행하면 샘플 저널이 자동으로 열립니다. 직접 로컬에 액세스하기 위해 토큰을 복사할 필요가 없습니다.

데모 메시지는 가상의 내용입니다. 데모 모드에서는 실제 텔레그램 계정에 연결할 수 없습니다.

## 텔레그램 연결

> [!경고] **잃어도 괜찮은 것만 사용하십시오.** 개인 계정이나 중요한 계정을 연결하거나, 소중한 계정으로 API ID/해시를 생성하는 것을 강력히 권장하지 않습니다. 텔레그램은 클라이언트와 관계없이 예측할 수 없이, 종종 영구적으로 계정을 차단합니다. 원활한 테스트 실행은 TgWitness가 아닌 텔레그램에 달려 있으며, 향후에 대해 어떠한 보장도 하지 않습니다.

1. 기본 데모가 실행 중이라면 중지하고 **Start.cmd** 또는 `sh start.sh`를 실행하십시오. 그렇지 않은 경우, 위에서 시작한 라이브 설치 환경을 계속 실행하십시오.
2. 설치 방법에 해당하는 패널 토큰을 사용하여 패널을 열어주세요.
3. 프록시가 필요한 경우, **‘계정 → 설정 → 연결 설정 → 연결 경로** 변경’에서 설정하십시오.
4. '계정'에서 전화번호를 입력하고 **'계속'을** 누르거나, **'QR 코드' → 'QR 코드 표시'를** 선택하거나, 파일을 선택하고 **'계정 연결'을** 누르십시오. **API ID + 해시는** 선택 사항입니다. 워크스페이스는 저장되거나 가져온 쌍, 또는 내장 풀에서 작동하는 쌍을 사용합니다. 자체 앱을 사용하려면 API ID에 `API ID:API Hash` 쌍 하나를 붙여넣으십시오. 전체 인증 키를 사용하려면 **‘인증 키’를** 선택하고 512자 전체의 16진수 문자를 붙여넣은 다음, 제공된 DC ID를 선택하십시오. 사용자 ID는 선택 사항이며, 입력 시 자동으로 선택됩니다.
5. 선택한 로그인 방법(전화번호/인증 코드/2단계 인증)을 완료하거나, QR 코드의 경우 로그인된 텔레그램 앱에서 확인을 거치거나, 지원되는 인증된 세션을 가져오십시오.
6. 표시된 계정 ID를 확인하세요. 오픈 **소스**: 채팅 내역은 자동으로 불러오며, 그룹은 직접 추가해야 합니다.
7. **'보존할 변경 사항** 선택'에서 이벤트 범주를 선택하거나 **'메시지, 수정 및 삭제'** 사전 설정을 선택한 다음, 모니터링 설정을 저장하십시오.
8. 첨부 파일 설정을 각각 선택한 후, **‘관찰 시작’을** 누르십시오.

API 자격 증명은 귀하의 애플리케이션을 식별하는 용도로 사용되며, 그 자체만으로는 계정에 대한 접근 권한을 부여하지 않습니다. 비공개 그룹의 경우 공개 사용자 이름이 필요하지 않지만, 귀하의 계정이 해당 그룹에 대한 접근 권한을 가지고 있어야 합니다.

기존 계정의 경우 [계정 및 세션 형식을](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/) 참조하십시오. 이 패널은 Telethon StringSession, Telethon/Pyrogram SQLite, 단일 계정 TData ZIP 및 지원되는 계정 JSON을 지원합니다. 세션과 해당 JSON 파일을 함께 선택한 후, **'계정 연결'을** 누르십시오. QR 로그인도 동일한 선택적 API 설정으로 사용할 수 있습니다. TDLib, 봇 및 대량 계정 목록은 지원되지 않습니다.

다른 계정을 추가하려면 계정 선택기 옆의 **+**를 누르거나 **계정 → 설정 → 연결 설정 → 작업 공간을** 열거나, **‘계정’을** 사용하십시오. 작업 공간은 각각 별도의 세션, 저널, 키, 소스 및 큐를 가지고 있습니다. 보기를 전환해도 다른 수집기는 계속 실행됩니다. 이 설치 환경에서는 동일한 텔레그램 계정을 두 개의 작업 공간에 할당할 수 없습니다. 워크스페이스의 수는 정해져 있지 않으며, 하나의 프로세스를 공유하므로 용량은 시스템 사양에 따라 달라집니다.

라이브 패널 토큰은 텔레그램 인증 정보 및 저장된 자료에 대한 접근을 보호하며, 텔레그램 API 자격 증명과는 별개입니다. 명시적으로 시작되고 직접 액세스된 로컬 데모에만 자동으로 등록됩니다. 원격/프록시 데모의 경우 여전히 `data/demo/panel-token.txt`를 사용합니다.

## 검토 및 내보내기

- **저널:** 출처 및 이벤트 유형별로 관측 내역을 검색하고 필터링할 수 있습니다.
- 이벤트를 선택하여 원본 기록, 출처 및 저장된 버전을 확인하세요.
- 편집 내역에는 변경 전후의 내용이 표시됩니다. 삭제 내역에는 마지막으로 캡처된 내용이 있는 경우 해당 내용이 표시되며, 신원이 확인되지 않은 행위자는 여전히 미확인 상태로 남습니다.
- **내보내기 형식:** 서명된 ZIP, JSONL, CSV 및 오프라인용 HTML.
- **전체 채팅 내보내기** (소스 → 전체 채팅 내보내기): 하나의 채팅에서 표시되는 전체 내역을 `chat.json`(Telegram-export 형식)로 서명된 번들 및 가독 가능한 `chat.html` 파일로 다운로드합니다. 비공개 채팅은 해당 계정이 멤버일 때 작동합니다. 이는 현재 시점의 스냅샷이며, 삭제되거나 이전에 편집된 메시지를 재구성한 것이 아닙니다. `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`를 사용하여 사본을 검증하십시오.
- **체크포인트 저장:** 서명된 기록부의 경계를 수집기 외부로 유지하십시오.
- **서명된 실행 영수증 다운로드:** 수집기의 프로그램/버전 기록을 보존합니다.
- **타임스탬프 요청 준비:** 타임스탬프 인증 기관에 대한 오프라인 요청을 준비합니다. [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/ko/docs/reference/timestamp/) 문서를 따라 응답을 수신하고 검증합니다.
- **저널 검증:** 이벤트 서명 및 체인 링크를 확인합니다. ZIP 파일로 내보낼 경우 미디어 파일도 함께 검증됩니다.

지원되는 브라우저에서는 대용량 내보내기 파일을 선택한 위치에 직접 저장할 수 있습니다. 그 외 브라우저의 경우 최대 128 MiB까지 버퍼링됩니다. 서버가 실행 중일 때, 스트리밍 CLI는 전체 응답을 버퍼링하지 않고도 더 큰 용량의 파일을 다운로드할 수 있도록 지원합니다:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

다른 작업 공간을 추가하려면 [**내보내기] → [작업 공간 ID**]를 사용하여 `--profile ID`를 추가하십시오. 원격 서버의 경우 `--url https://your-server`를 추가하십시오. 기본 전송 한도는 5 GiB이며, `--max-mib`를 사용하면 이를 변경할 수 있습니다. 서명된 ZIP 콘텐츠는 기본적으로 별도의 4 GiB 압축 해제 검증 한도가 적용됩니다(**Parameters를** 사용하면 이 한도를 높일 수 있으며, 해당 아카이브는 `verify.py --max-gib N`로 검증하십시오). 검증기의 신뢰할 수 있는 사본과 독립적으로 보관된 키 지문/체크포인트를 사용하여 아카이브를 검증하십시오.

## 설치 방법 확인하기

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check`는 로컬 종속성, 서명 지원, 저장소, 키 구성 및 수신 주소를 확인합니다. 이 도구는 아무것도 설치하지 않으며 텔레그램에 연결하지도 않습니다. 포트가 사용 중이라면 다른 인스턴스가 실행 중일 수 있습니다. 다른 `--port`를 사용하거나 먼저 해당 인스턴스를 중지하십시오.

런처는 `.venv`에 설치됩니다. 보조 `python -m tgwitness...` 명령어는 해당 환경이 이미 활성화된 경우가 아니라면, Windows에서는 `.venv\Scripts\python.exe`를, Linux/macOS에서는 `.venv/bin/python`를 사용해야 합니다.

## 세션, 보안 및 운영

폐쇄적이고 일관된 Telethon SQLite `.session` 파일은 로컬에서 `python -m tgwitness.sessions account.session --out account.tgwitness-session`를 사용하여 변환한 후 Account에 불러올 수 있습니다. 직접 파일 가져오기 및 QR 로그인도 가능합니다. 로그인 형식, SOCKS5, HTTP CONNECT, MTProxy 및 외부 마스터 키에 대해서는 [CONNECTION-SECURITY.md를](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/) 참조하십시오.

**관찰을 일시 중지하면** 수집이 중단됩니다. **잠금** 기능은 브라우저 액세스만 차단합니다. 탭을 닫아도 수집 프로세스는 계속 실행됩니다. 프로세스를 중지해야만 수집이 중단되며, 기록 스냅샷만으로는 누락된 모든 수정 또는 삭제 내역을 복원할 수 없습니다. 이벤트 정책, 첨부 파일 대기열, 계정 격리 및 재시작 동작에 대한 [수집 방식에 대해](https://phishdestroy.github.io/TgWitness/ko/docs/reference/collection/) 알아보세요.

세션과 비밀 정보는 암호화됩니다. 메시지 내용, 미디어 및 내보내기 파일은 암호화된 디스크나 볼륨이 필요합니다. 서명은 신뢰할 수 있는 키를 기준으로 무결성을 입증할 뿐이며, 텔레그램의 출처를 입증하거나, 수집기 및 해당 키를 제어하는 운영자가 조작하는 것을 방지하지는 않습니다.

백업/복원 방법은 [OPERATIONS.md를](https://phishdestroy.github.io/TgWitness/ko/docs/reference/operations/), 호스팅 방법은 [DEPLOYMENT.md를](https://phishdestroy.github.io/TgWitness/ko/docs/reference/deployment/), 서비스 예시는 [deploy/를](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 참조하십시오. 설치된 패널에는 `/guide.html`에 오프라인 설정 가이드도 포함되어 있습니다.

실제 검증 결과 및 남아 있는 한계 사항은 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/) 및 [READINESS.](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md)md에 기록되어 있습니다.
