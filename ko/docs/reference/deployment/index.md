# 배포

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/deployment/

TgWitness를 Windows, Linux, macOS 또는 Docker 환경에서 HTTPS를 통해 서비스 형태로 실행할 수 있으며, 백업 및 업데이트 기능이 제공됩니다.

**영어** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [우크라이나어](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [포르투갈어 (브라질)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [우르두어](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [인도네시아어](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [베트남어](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [간체 중국어](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## 설치 방법 선택

이동식 패키지의 경우, GitHub Releases에서 `TgWitness-<version>-windows-amd64-portable.zip`를 추출하십시오. 다른 방법을 사용하려면 소스 ZIP 파일을 다운로드하여 압축을 풀거나 저장소를 복제한 후, 프로젝트 디렉터리에서 다음 명령을 실행하십시오:

| 설치 | 시작 | 백그라운드에서 실행되나요? |
| --- | --- | --- |
| Windows용 휴대용 패키지 | `TgWitness.cmd` | 아니요; 창을 열어 두세요. |
| Windows 전용 | `Start.cmd` | 아니요. 백그라운드에서 사용하려면 선택적 로그온 작업을 사용하십시오. |
| Linux/macOS 네이티브 지원 | `sh start.sh` | 아니요. 백그라운드 실행에는 systemd/launchd를 사용하십시오. |
| 지원되는 모든 호스트에서 Docker 사용 | `docker compose up -d --build --wait` | 네, Docker 데몬이 실행 중일 때입니다. |
| Windows용 Docker 보조 도구 | `scripts\Docker.cmd` | 네, 헬퍼는 웹 서버의 정상 작동 상태를 확인합니다. |
| Linux/macOS용 Docker 보조 도구 | `sh scripts/docker-start.sh` | 네, 헬퍼는 웹 서버의 정상 작동 상태를 확인합니다. |

제3자가 확인할 수 있어야 하는 클라우드 서버( SSH 없이 제공업체의 API를 통해 생성되며, Cloudflare Tunnel을 통해서만 접속 가능)에 대해서는 [‘고신뢰도 배포’를](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md) 참조하십시오.

네이티브 시작 시 비공개 `.venv`를 생성하고 고정된 종속성을 설치합니다. Docker는 호스트 Python 없이 이미지 내에서 이를 빌드합니다. 최초 설정 시 인터넷 접속이 필요합니다. Python 3.11 이상이 발견되지 않으면, `Start.cmd`는 현재 Windows 사용자를 위해 Python 3.12를 설치하기 전에 확인을 요청합니다(winget을 사용하거나, 그렇지 않은 경우 Python Software Foundation의 서명을 확인한 후 python.org 설치 프로그램을 사용함). 이 과정에서 관리자 권한을 요청하지 않습니다. Docker 및 OS 서비스는 여전히 필수 전제 조건으로 유지됩니다.

네이티브 및 포터블 설치 환경에서는 해당 폴더 내의 ``data/live``를 사용합니다. Docker는 ``tgwitness-data``라는 이름의 볼륨을 ``/data``에 사용합니다. 전체 데이터 디렉터리를 의도적으로 마이그레이션하기 전까지는 이 두 환경은 별개의 설치 환경으로 간주됩니다. 새로운 Docker 컨테이너가 네이티브 계정을 자동으로 감지할 것이라고 기대하지 마십시오.

## 설치 요구 사항

네이티브 설치에는 Python 3.11 이상과 `venv` 및 `ensurepip`가 필요하며, 첫 번째 종속성 설치를 위해 인터넷 접속이 가능해야 하고, `.venv`를 위한 쓰기 가능한 프로젝트 디렉터리가 필요합니다. 번들된 패널은 Node.js나 프론트엔드 빌드가 필요하지 않습니다. 일반 OS 계정에서 런처를 실행하십시오. TgWitness는 관리자/루트 권한을 요구하지 않습니다.

- **Windows:** `Start.cmd`는 `py -3`를 확인한 다음, `python`를 확인하고, 그 다음 사용자별 기본 설치 폴더와 Program Files 설치 폴더를 확인하며, 버전 3.11 이상이 필요합니다. 어느 것도 작동하지 않으면, 위에서 설명한 사용자별 자동 설치 옵션을 제공합니다. `py -3 start.py`도 작동합니다. 휴대용 패키지는 파이썬이 전혀 필요하지 않습니다.
- **Linux:** `start.sh`는 `python3.13`, `python3.12`, `python3.11`, `python3` 및 `python`를 시도하며, 적합한 것이 없을 경우 apt, dnf, pacman, zypper, apk 또는 Homebrew용 설치 명령어를 출력합니다. Debian/Ubuntu 설치의 경우, 선택한 인터프리터와 일치하는 `python3-venv` 패키지가 필요할 수 있습니다. 배포판의 구형 기본 Python은 Python 3.11 이상으로 교체하거나 보완해야 합니다.
- **macOS:** 최신 Python 3.11 이상 배포판을 설치하십시오. OS에서 제공하는 인터프리터가 요구 사항을 충족한다고 가정하지 마십시오. 프로젝트 디렉토리에 있는 `python3 start.py`를 사용하십시오.
- **Docker:** Compose v2.20 이상과 함께 Docker Engine/Desktop을 사용하십시오. Windows에서 Docker Desktop을 사용할 경우 Linux 컨테이너를 사용해야 합니다. 컨테이너는 자체 Python 종속성을 설치하므로, 호스트에 별도로 Python을 설치할 필요가 없습니다.

데이터 디렉토리에는 영구 로컬 스토리지를 사용하십시오. 메시지, 미디어, WAL 증가량, 내보내기 및 백업을 고려하여 용량을 계획하십시오. 모든 워크로드에 적용되는 증거 기반의 보편적인 최소 디스크/RAM 사양은 존재하지 않습니다. 호환되는 의존성 휠이 없는 CPU 아키텍처 및 Python 버전의 경우 추가 빌드 도구와 별도의 검증이 필요할 수 있습니다. "이식성"은 모든 OS 또는 하드웨어를 지원한다는 주장이 아닙니다.

Windows 11/Python 3.12 환경은 로컬에서 검증되었습니다. Linux/macOS/컨테이너 정의 및 CI 설정이 제공되지만, 이 개발 호스트에서는 실행되지 않았습니다. 정확한 범위는 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/)를 참조하십시오.

## 로컬 컴퓨터

Windows에서는 `Start.cmd`를, Linux/macOS에서는 `sh start.sh`를 사용하십시오. `scripts\Setup.cmd` 또는 `sh start.sh --setup-only`를 실행하면 환경이 준비됩니다. 런처는 첫 사용 시 필수 구성 요소를 설치하며, 이후 실행 시에는 기존 환경을 재사용합니다. 설정 및 텔레그램 데이터 수집에는 인터넷 연결이 필요하지만, 기존 기록 열람 및 내보내기 기능은 오프라인에서도 작동합니다.

설치 후 `python start.py --check`를 실행하여 수집기를 시작하지 않은 상태에서 로컬 종속성, Ed25519, 저장소, 키 구성 및 수신 주소를 확인하십시오. 구조화된 출력을 보려면 `--json`를 사용하십시오. 의도된 `--data-dir`, `--host` 및 `--port`를 전달하십시오. 이 검사는 패키지를 설치하거나, 저널을 생성하거나, 텔레그램에 연결하지 않으며, 무결성 또는 커버리지 검증도 아닙니다. 시작 시 기존 저널을 별도로 검증합니다. `python start.py --help` 역시 설치를 수행하지 않습니다.

옵션:

start.py를 실행한 후, Windows에서는 `.venv\Scripts\python.exe`, Linux/macOS에서는 `.venv/bin/python`를 사용하여 보조 명령을 실행하거나, 먼저 해당 환경을 활성화하십시오. 아래의 `python -m ...` 예제는 환경이 활성화된 상태를 전제로 합니다.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

환경 변수: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE은 새 설치 시 외부 키 모드를 선택합니다. 아래를 참조하십시오. TGWITNESS_TOKEN은 지정될 경우 최소 24자 이상이어야 하며, 암호학적으로 무작위 생성된 값을 사용해야 합니다. 이 값이 없으면 앱이 panel-token.txt 파일에 256비트 무작위 토큰을 생성합니다. 환경 변수 재정의는 해당 파일을 덮어쓰지 않습니다. 자격 증명을 갱신하려면 앱을 재시작하십시오.

데이터 디렉터리를 소유할 수 있는 프로세스는 정확히 하나뿐입니다. 크로스 플랫폼 OS 파일 잠금 기능을 통해 의도치 않은 동시 쓰기 작업을 방지합니다. Uvicorn 워커를 하나 사용하십시오. 패널을 통해 프로필(profiles)/<id>/ 아래에 추가 워크스페이스 디렉터리를 생성하여 무제한의 워크스페이스를 관리할 수 있습니다. 별도의 서비스 인스턴스의 경우, 별도의 디렉터리와 포트를 사용하십시오. SQLite WAL 파일은 네트워크 파일 시스템이 아닌 로컬 영구 저장소에 위치해야 합니다. 복제본 간에 하나의 볼륨을 공유하지 마십시오.

## Windows용 휴대용 패키지

각 GitHub 릴리스에는 `TgWitness-<version>-windows-amd64-portable.zip`와 그에 수반되는 `.sha256`가 포함되어 있습니다. 여기에는 python.org에서 제공하는 공식 임베드 가능한 Python 3.12 런타임 (`tools/build_portable.py`에 체크섬이 고정됨), TgWitness 및 고정된 종속성, 그리고 다음 세 가지 런처가 포함되어 있습니다:

| 파일 | 목적 |
| --- | --- |
| `TgWitness.cmd` | 패널을 시작합니다. 추가 옵션은 그대로 전달됩니다(예: `TgWitness.cmd --port 8790`). |
| `TgWitness-Demo.cmd` | `data\demo`에서 시뮬레이션 데모를 시작하세요. |
| `TgWitness-Check.cmd` | 시작하지 않고 준비 상태 확인 실행 |

전체 아카이브를 `Documents\TgWitness`와 같은 쓰기 가능한 폴더에 압축을 풀어 주십시오. ZIP 파일 내부나 Program Files 폴더에서 실행하지 마십시오. 런타임은 격리된 모듈 경로를 사용하므로, 다른 Python 설치본이나 `PYTHONPATH`는 이에 영향을 미치지 않습니다. 데이터는 패키지의 `data` 폴더에 저장됩니다. 업데이트하려면 TgWitness를 중지하고, 새 버전을 새로운 폴더에 압축을 풀고 `data` 폴더를 해당 위치로 복사하십시오.

Python 3.12를 사용하여 64비트 Windows 환경에서 직접 빌드하는 방법:

```
python tools/build_portable.py
```

빌더는 런타임 체크섬을 검증하고, 제한된 종속성을 패키지에 설치하며, 내장된 인터프리터를 사용하여 준비 상태 검사를 실행한 후 ZIP 파일과 체크섬을 `dist/`에 기록합니다.

## 컨테이너

```
docker compose up -d --build --wait
```

이 명령은 /data에 대한 명명된 영구 볼륨을 생성합니다. 웹 포트는 127.0.0.1:8787로 매핑됩니다. 이 프로세스는 UID 10001로 실행되며, 권한이 제거된 상태이고, 루트 파일 시스템은 읽기 전용이며, /data 및 /tmp는 쓰기 가능합니다. `--wait`는 반환하기 전에 웹 서버의 상태를 확인하며, 텔레그램 인증이나 전송을 수행하지 않습니다. 제공된 헬퍼는 빌드 후 180초의 준비 시간 제한을 사용합니다. 초기 종속성 다운로드에는 이보다 더 오랜 시간이 소요될 수 있습니다.

두 기본 Compose 파일 모두 프로젝트 이름 `tgwitness`를 사용하므로, 새 릴리스를 다른 디렉터리에 추출하더라도 새로운 데이터 볼륨이 자동으로 선택되지 않습니다. 해당 프로젝트에 대해서는 하나의 배포만 활성화된 상태로 유지하십시오. 독립적인 설치의 경우, 고유한 `docker compose -p NAME ...`와 다른 호스트 포트를 사용하고, 업데이트 시 두 가지를 모두 유지하십시오. 다른 프로젝트 이름을 사용하는 기존 배포 환경의 경우, 기존 이름에 `-p`를 추가하여 계속 사용하십시오. `docker compose ls`는 기존 프로젝트를 나열합니다.

`deploy/env.example`를 `.env`로 복사하고, `TGWITNESS_PORT`를 변경하여 다른 루프백 포트를 사용하십시오. 예를 들어, `TGWITNESS_PORT=8788`는 `http://127.0.0.1:8788`에서 패널을 노출하며, 컨테이너는 여전히 8787 포트를 수신 대기합니다. `.env`는 Git에서 제외됩니다.

초기 토큰 가져오기:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

유용한 명령어:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped`는 충돌이나 Docker 데몬 재시작 후 수집기를 다시 시작합니다. 리눅스 서버에서는 배포판의 서비스 관리자(일반적으로 `sudo systemctl enable --now docker`)를 사용하여 부팅 시 Docker를 활성화하십시오. Windows/macOS에서는 Docker Desktop의 ‘로그인 시 시작’ 설정을 활성화하십시오. 데스크톱에서 로그아웃하거나 절전 모드로 전환하거나, 중지된 Docker 데몬은 수집을 중단시킬 수 있습니다. 명시적으로 중지된 컨테이너는 다시 시작할 때까지 중지된 상태로 유지됩니다.

예시 구성에서 /tmp 볼륨의 상한은 512 MiB로 설정되어 있습니다. 내보내기 구조는 대신 각 작업 공간의 `temporary-exports/`를 영구 저장소인 /data에 사용합니다. 해당 위치에 동시 내보내기, 저널/WAL 증가, 미디어 및 백업을 위한 공간을 확보하십시오. 런처는 deploy/constraints.txt를 사용하여 적격한 런타임 종속성 버전을 고정합니다. Docker 및 고신뢰도 서버는 deploy/requirements.lock 및 deploy/build.lock을 기반으로 pip --require-hashes를 사용하여 설치됩니다. 모든 패키지 파일은 커밋에 기록된 SHA-256 해시와 일치해야 하므로, PyPI 또는 미러에서 파일이 교체된 경우 설치가 거부됩니다. Python 기본 이미지와 운영 체제 패키지는 여전히 별도의 릴리스 검증을 거쳐야 합니다.

저널과 키를 삭제할 의도가 아닌 이상, `docker compose down -v` 명령어를 사용하지 마십시오. 컨테이너 상태 보고서는 웹 서버의 가용성을 나타낼 뿐, 텔레그램 캡처 성공 여부를 나타내는 것이 아닙니다. 패널의 수집기 상태, 하트비트, 오류 및 커버리지 이벤트를 확인하십시오.

### 독립적인 증인 프로필

선택 사항인 `witness` 서비스는 자체 컨테이너 내에서 [독립적인 위트니스를](https://phishdestroy.github.io/TgWitness/ko/docs/reference/witness/) 실행하며, `witness-data` 볼륨에 자체 키와 저널을 보유하고, 수집기용으로는 읽기 전용 위트니스 토큰만 제공합니다. 패널의 ‘위트니스(Witness)’ 페이지에서 토큰을 생성하고, 봇 토큰 및 채널과 함께 `.env`에 추가한 다음, 프로필을 시작하십시오:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

이 서비스는 Compose 네트워크 내의 수집기(`http://tgwitness:8787` )에 연결됩니다(`TGWITNESS_WITNESS_COLLECTOR` 가 이를 재정의하며, 예를 들어 `/profiles/<workspace ID>` 는 다른 작업 공간을 나타냅니다). 다른 사람이 운영하는 별도 서버의 위트니스(witness)를 사용하려면, 해당 서버에서 `deploy/compose/compose.witness.yaml` 를 사용하고 `TGWITNESS_WITNESS_COLLECTOR` 를 수집기의 HTTPS 주소로 설정하십시오. 해당 파일에는 위트니스만 포함되어 있습니다.

## 공개된 이미지를 설치하세요

이 내용은 [릴리스 워크플로우가](https://phishdestroy.github.io/TgWitness/ko/docs/reference/deployment/#automated-github-releases) 성공적으로 완료되고 GHCR 패키지가 공개적으로 구성된 후에 이용 가능해집니다. 리포지토리의 소유자/이름은 이 소스 트리에 하드코딩되어 있지 않습니다. 해당 릴리스의 워크플로우 요약에 표시된 이미지를 사용하십시오.

`deploy/env.example`를 `.env`로 복사하십시오. `TGWITNESS_IMAGE`를 공개된 버전으로 설정할 때는 **소문자** 리포지토리 경로를 사용하십시오. 예:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.1
TGWITNESS_PORT=8787
```

`compose.yaml` 대신 이 파일을 단독으로 실행하십시오:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

호스트 측에서 소스 빌드, 파이썬 또는 컴파일러가 필요하지 않습니다. 릴리스 워크플로는 Docker Desktop의 Linux VM을 포함하여 Linux AMD64 및 ARM64 컨테이너를 대상으로 합니다. 워크플로 요약에서 버전 태그 또는 `ghcr.io/owner/repository@sha256:...`를 사용하십시오. `latest` 태그 이동이나 무인 애플리케이션 업그레이드는 구성되어 있지 않습니다. 프로젝트 이름이 일치할 경우, 이미지 및 소스 변형은 동일한 데이터 볼륨을 사용합니다.

## 서버에서 HTTPS 자동 적용

Docker가 설치된 서버, 사용자가 직접 관리하는 도메인, 그리고 영구적인 로컬 저장소를 사용하십시오. 도메인의 A/AAAA 레코드를 서버로 지정하고, IPv6가 서버에 도달하는 경우에만 AAAA 레코드를 공개하십시오. 인증서 발급을 위해 인바운드 TCP 80 및 443 포트와 아웃바운드 DNS/HTTPS를 허용하십시오. 다른 서비스가 이미 이 포트들을 사용하고 있어서는 안 됩니다.

`deploy/env.example`를 `.env`로 복사하고, 스키마나 경로 없이 호스트명을 설정하십시오:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

HTTPS 오버레이를 사용하여 소스 빌드를 시작합니다:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

게시된 이미지의 경우, 첫 번째 파일로 `deploy/compose/compose.image.yaml`를 대신 사용하십시오. 나중에 상태, 로그, 업데이트 및 중지 명령을 실행할 수 있도록 `-f` 인수는 모두 유지하십시오.

Caddy는 인증서를 취득 및 갱신하고, HTTP를 HTTPS로 리디렉션하며, 요청을 사설 Compose 네트워크상의 수집기로 전달합니다. 인증서 상태는 별도의 영구 볼륨에 저장됩니다. 수집기의 직접 호스트 포트는 루프백 전용으로 유지됩니다. 제공된 Caddy 구성에서는 액세스 로깅이 활성화되어 있지 않습니다.

`https://watch.your-domain.org`를 열고 패널 토큰을 입력하세요. 준비 상태 확인은 인증서 발급이나 외부 접근 가능성을 보장하지 않습니다. HTTPS가 준비되지 않은 경우, DNS, 방화벽 규칙을 확인하고 다음을 수행하세요:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

제공된 Caddy 이미지는 ‘`2-alpine`’ 태그를 따릅니다. 풀링하면 해당 이미지가 새로 고쳐집니다. 고정된 인프라 버전이 필요한 경우, 테스트를 거친 다이제스트를 배포 환경에 고정해 두십시오.

## 업데이트 및 백업

업데이트 시에도 Compose 프로젝트 이름과 데이터 볼륨을 유지합니다. 먼저 수집기를 중지하고 전체 백업을 수행하십시오. 기본 소스 기반 배포의 경우:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

매번 저장소 외부의 새로운 백업 대상을 사용하고, 이를 계정 접근 자료로 보호하십시오. 예시 경로는 참고용일 뿐이며, 본인의 개인 백업 위치를 사용하십시오. 숨겨진 파일, 모든 작업 공간, 키, 저널 및 미디어를 포함하여 디렉터리 전체를 복사하십시오. 구성된 경우 외부 볼트 마스터 키를 별도로 백업하십시오. 증거용 ZIP 파일은 복원 가능한 애플리케이션 백업이 아닙니다. HTTPS의 경우, 인증서/계정 상태를 유지해야 한다면 Caddy 볼륨도 함께 보존하십시오.

소스 배포를 위해서는 최신 릴리스 파일을 다운로드한 후 다음 명령을 실행하십시오:

```
docker compose up -d --build --wait
```

이미지를 배포하려면 `TGWITNESS_IMAGE`를 원하는 버전으로 변경한 후 다음 명령을 실행하십시오:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

앞서 언급된 중지/복사 명령어에도 설치본의 Compose 파일을 사용하십시오. `.env`, 사용자 지정 구성 및 동일한 프로젝트 이름을 유지하십시오. `down`는 이름이 지정된 볼륨을 유지하며, **`down -v`**는 **이를 삭제합니다**. `.venv`는 운영 체제 또는 Python 버전 간에 복사하지 마십시오. 네이티브 업데이트를 수행하려면 TgWitness를 중지하고, 전체 데이터 디렉터리를 백업한 후, 소스 파일을 교체하고, 실행 전에 `python start.py --setup-only`를 실행하십시오.

업데이트 후 패널 접근 권한, 계정 신원, 관찰 상태 및 적용 범위를 확인하십시오. 재시작해도 놓친 텔레그램 업데이트는 복원되지 않습니다. 향후 버전에서 저장 형식이 변경될 경우, 롤백을 수행하려면 업데이트 전 백업이 필요할 수 있습니다.

## GitHub 자동 릴리스

이 프로젝트가 Actions가 활성화된 GitHub 저장소에 푸시되면 [릴리스](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml)워크플로가 바로 사용 가능해집니다. 이 워크플로는 프리릴리스를 포함하여 GitHub 릴리스가 **게시될** 때 실행됩니다. 초안이나 태그 푸시만으로는 패키지가 게시되지 않습니다.

1. 패키지 버전과 변경 내역을 설정한 후, `v` 태그와 `pyproject.toml`의 정확한 버전(예: `v0.7.1`)을 함께 지정하여 릴리스를 게시하십시오.
2. 이 워크플로는 태그를 검증하고, Windows/Linux/macOS에서 공통으로 사용되는 Python, general/account-import/QR 브라우저, 소스 패키지 및 Docker 검사를 실행합니다. 또한 Python 3.12를 사용하여 세 가지 운영 체제 모두에서 새로운 네이티브 설치도 수행됩니다.
3. 이러한 검사가 통과되면, QEMU 환경에서 ARM64 이미지를 스모크 테스트하고, AMD64/ARM64 이미지를 `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>` 에 게시하며, 소스 ZIP 파일과 Python 휠 파일, 그리고 해당 SHA-256 사이드카 파일을 첨부합니다. Windows용 포터블 ZIP 파일은 검사 워크플로우에서 테스트된 것과 정확히 동일한 아티팩트이며, 릴리스 워크플로우는 해당 아티팩트와 그 체크섬을 다운로드하여 게시합니다.
4. 마지막 작업에서는 게시된 세 가지 패키지를 모두 다시 다운로드하여 체크섬을 확인합니다. 그런 다음 `SHA256SUMS.txt` 및 `RELEASE-MANIFEST.json` 을 게시하며, 버전, 소스 리비전 및 자산 크기를 기록합니다. 업로드 시 기존 릴리스 자산을 덮어쓰지 않습니다.
5. 첫 게시 후, GHCR 패키지 설정을 열고 익명 이미지 가져오기를 원하는 경우 가시성을 **‘공개**(**Public)**’로 설정하십시오. 공개 소스 저장소만으로는 공개 컨테이너 패키지가 보장되지 않습니다. 조직 정책에서 패키지 게시가 허용되어야 합니다. 이 워크플로는 `GITHUB_TOKEN`를 사용하며, 레지스트리 비밀번호나 VPS 인증 정보는 저장소에 포함되어서는 안 됩니다.

이 로컬 준비 과정만으로는 원격 워크플로우의 성공 여부가 확인되지 않았습니다. ARM64 에뮬레이션은 예비 테스트일 뿐, 네이티브 하드웨어나 실제 텔레그램 환경에서의 검증은 아닙니다. 이는 릴리스 패키징을 자동화하지만, 서버를 시작하려면 여전히 Compose 명령과 해당 도메인/호스트 전제 조건이 필요합니다. 릴리스가 공개될 때 기존 서버는 자동으로 업그레이드되거나 재시작되지 않습니다.

## 원격 서버

서비스를 루프백에 제한하고 SSH 터널을 사용하거나, 리버스 프록시에서 HTTPS 연결을 종료하십시오. 기본 Compose 파일은 로컬 전용이며, 선택 사항인 `deploy/compose/compose.https.yaml` 오버레이는 구성된 도메인에 대해 Caddy를 제공합니다. 베어러 토큰이 URL이나 프록시 로그에 노출되지 않도록 하십시오. 리버스 프록시는 요청 크기와 연결 빈도를 제한해야 합니다. 일반 HTTP를 인터넷에 노출하지 마십시오.

[deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 디렉토리에는 systemd, Windows 로그온 작업, macOS 사용자 에이전트 및 Caddy에 대한 예제가 제공됩니다. 설치 전에 해당 경로를 검토하고 조정하십시오. 이들은 템플릿으로 제공되는 것이며, 로컬에서 실행되는 플랫폼별 설정은 아닙니다. 일반 런처로는 백그라운드 서비스나 작업이 등록되지 않습니다.

Windows에서 창이 표시되지 않는 `pythonw.exe` 방식으로 실행하면 시작/서버 진단 정보가 데이터 디렉터리 내의 `logs/server.log`에 저장됩니다(파일당 5 MiB, 순환 백업 2개). 콘솔 방식으로 실행할 경우 콘솔 로그가 유지됩니다. 두 모드 모두에서 HTTP 액세스 로깅은 비활성화되어 있습니다. 데이터 디렉터리를 통해 로그를 보호하고, 공유하기 전에 내용을 검토하십시오.

## 재시작 및 누락된 내용

마지막으로 요청된 모니터링 상태가 유지됩니다. 모니터링이 활성화된 상태였다면, 시작 시 선택한 소스에 다시 연결하여 모니터링을 재개하려고 시도합니다. 수동 일시 중지를 하면 해당 시도가 취소됩니다. 재시작에 실패한 경우 기록되어 패널에 표시됩니다.

StringSession은 인증 정보를 유지하지만, Telethon의 영구적인 업데이트/엔티티 상태는 유지하지 않습니다. 시작 시 대화 내용이 다시 로드됩니다. Telegram/Telethon은 실행 중 일부 전송 중단을 복구할 수 있지만, TgWitness는 프로세스 재시작 시 영구적인 재생을 보장하지 않습니다. 매번 시작 시 이전 저널 헤더와 오프라인 경계를 기록합니다. 모니터는 10초마다 연결 상태를 확인하고 1분마다 하트비트를 추가합니다 (**매개변수 → 활성 기록 간격**). 짧은 중단은 감지되지 않을 수 있으며, 연결된 전송 경로라고 해서 업데이트가 완전히 전달된다는 보장은 없습니다. 스냅샷은 명시적인 현재 기록 관측값이며, 결손 부분을 보충하지 않습니다.

미디어 큐는 각 워크스페이스의 SQLite 데이터베이스에 저장됩니다. 메시지와 해당 작업은 원자적으로 커밋됩니다. 실행 중 중단된 작업은 시작 시 재시도를 위해 복구됩니다. 각 다운로드에는 120초의 기본 타임아웃에 파일 크기에 따른 256 KiB/s 속도가 적용되며, 첨부 파일 유형당 1~2,000 MiB의 제한이 있습니다. 타임아웃, 속도 및 재시도 횟수는 **‘매개변수’에서 설정할 수 있습니다**. 수집기는 크기가 알려지지 않은 파일은 건너뜁니다. 일시 중지 시 대기열에 있는 작업은 유지됩니다. 재시도는 원래 관측된 파일 디스크립터를 사용하며, 이후에 수정된 메시지의 최신 버전은 절대 사용하지 않습니다. 일시적인 오류에 대해서는 재시도 횟수에 제한이 있으며, 미디어 FloodWait 일시 중지는 재시작 후에도 유지됩니다. 미디어 복구는 텔레그램 업데이트 복구와 별개이며, 사라진 파일을 복원할 수는 없습니다.

## 백업, 복원 및 용량

vault.key, signing.enc, credentials.enc, SQLite 데이터베이스/WAL 파일, 미디어, 토큰, 체크포인트, 및 모든 프로필/하위 디렉터리를 포함한 **전체 데이터 디렉터**리를 복사하기 전에 프로세스를 중지하십시오. 대상 서비스가 중지된 상태에서 복사본 전체를 복원하십시오. 볼트 키가 누락되거나 서명 키가 일치하지 않으면 시작에 실패합니다. 강제 접근을 위해 키를 재생성하지 마십시오.

비밀 백업 파일은 암호화하고 접근 권한을 엄격히 통제하십시오. 증거 ZIP 파일은 휴대성이 뛰어나며, 애플리케이션 백업이나 텔레그램 세션 백업이 아닌 증거 자료를 검토하는 데 사용됩니다. 자동 보존 및 삭제 기능은 없습니다. 모든 메시지, 원시 메타데이터, 미디어, 임시 내보내기 파일 및 백업 파일을 저장할 디스크 공간을 미리 확보하십시오.

전체 저널을 불러오는 대신, 시작 시 검증 및 스트림 기록 내보내기를 수행합니다. 내보내기를 시작하면 읽기 스냅샷이 고정되지만 새로운 WAL 쓰기는 계속될 수 있습니다. 장시간 진행되는 내보내기의 경우 WAL 페이지가 유지될 수 있으므로 디스크 용량은 여전히 중요합니다. ZIP 파일은 독립 검증자의 기본값에 맞춰 압축 해제 시 4 GiB로 제한되며; **매개변수 → 최대 서명된 ZIP** 을 통해 상한을 높일 수 있으며, 이러한 아카이브는 `verify.py --max-gib N`로 검증됩니다. 다른 형식의 경우 이벤트 수 제한이 없습니다. 지원되는 브라우저는 응답 청크를 사용자가 선택한 파일로 스트리밍합니다. 그 외의 브라우저는 최대 128 MiB까지 버퍼링하며, 그 이상의 전송은 인증된 CLI로 전달합니다:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

다른 워크스페이스의 경우 **[Exports] → [Workspace ID]**에서 `--profile ID`를, 원격 서버의 경우 `--format zip|jsonl|csv|html`, `--url https://your-server`를, 5 GiB 전송 제한을 변경하려면 `--max-mib`를 사용하십시오. 일반 HTTP는 루프백에서만 허용됩니다. 토큰은 헤더를 통해 전송되며, 리디렉션은 거부되고, 기존 파일은 덮어쓰지 않으며, 다운로드가 완료되지 않은 파일은 완료된 파일로 게시되지 않습니다. TGWITNESS_TOKEN이 생성된 토큰을 재정의하는 경우, 해당 활성 값이 포함된 별도로 보호된 파일을 사용하십시오. panel-token.txt는 재정의에 의해 재작성되지 않습니다. 명령어의 SHA-256은 전송 체크섬일 뿐입니다. 서명된 ZIP 파일은 별도로 검증하십시오.

서버 내보내기 파일은 각 작업 공간의 비공개 `temporary-exports/` 내에 보관됩니다. 수출이 성공적으로 완료되면 해당 파일은 정리됩니다. 중단된 수출 파일은 다음 워크스페이스 시작 시, 해당 워크스페이스의 전용 인스턴스 잠금이 유지된 상태에서 제거됩니다. 이 디렉터리는 저장소 위협/용량 모델의 일부이므로, 암호화된 데이터 볼륨을 사용하십시오. 실제 운영 환경 규모의 수 기가바이트급 전송의 경우, 대상 시스템에서 여전히 적합성 검증이 필요합니다.

이 패널에는 대기 중이거나 실패한 미디어, 가장 오래된 보류 중인 미디어, 사용 가능한 디스크 공간, 텔레그램 요청 일시 중지 상태, 그리고 액세스가 확인되지 않은 소스가 표시됩니다. 이러한 진단 정보는 완전한 종단 간 전송 모니터링 기능은 아닙니다. 워크스페이스는 하나의 프로세스를 공유하므로, 문제가 있는 계정이 다른 계정에 영향을 미칠 수 있습니다. 별도의 작업자 프로세스, 보존/교체, 내구성 있는 업데이트 복구 및 전체 배포 검증은 여전히 유지됩니다. 패널 접근 범위 제한은 [‘접근 및 권한’](https://phishdestroy.github.io/TgWitness/ko/docs/reference/access/) 문서에 명시되어 있으며, 독립적인 체크포인트에 대해서는 [증인](https://phishdestroy.github.io/TgWitness/ko/docs/reference/witness/)가이드에서 다룹니다.

## 연결 및 보안 옵션

연결 경로는 워크스페이스별로 다르며, 인증 전에 구성해야 합니다. SOCKS5/HTTP CONNECT는 고정된 python-socks 종속성을 사용합니다. MTProxy는 Telethon의 실험적인 무작위 중간 전송 방식을 사용하며, 가짜 TLS ee 비밀키는 지원되지 않습니다. 직접 폴백은 선택한 [IP 모드에](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/#ip-modes) 따라 달라집니다. 'IP 숨기기' 모드는 이를 허용하지 않으며, '명시적 폴백' 모드는 지연 시간 후 이를 허용합니다. '터널/VPN' 모드는 직접 경로를 허용하지만 VPN을 생성하지는 않습니다. 이는 시스템 전체에 적용되는 네트워크 정책이 아닙니다.

새로 설치할 경우, TGWITNESS_VAULT_KEY_FILE은 별도로 보호된 무작위 마스터 키 파일을 가리키도록 설정합니다. 컨테이너 내 /data 외부에 읽기 전용으로 마운트하십시오. 각 작업 공간과 마스터 키에 대한 vault.external.json 솔트 메타데이터를 별도로 보관하십시오. 기존의 로컬 볼트는 계획적인 마이그레이션이 필요하며, 이 변수를 설정한다고 해서 자동으로 변환되지는 않습니다. 메시지/미디어 저장 및 내보내기 기능은 애플리케이션 수준에서 암호화되지 않습니다. 필요한 경우 암호화된 볼륨과 충분한 용량의 비공개 임시 저장 공간을 사용하십시오.

상세한 절차: [연결/보안](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/) 및 [운영 모드](https://phishdestroy.github.io/TgWitness/ko/docs/reference/operations/).
