# 설치, 확인 및 업데이트

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/installation/

단 한 줄의 명령어로 설치하고, 서명과 해시를 확인하며, 업데이트 및 제거할 수 있습니다.

[프로젝트](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [빠른 시작](https://phishdestroy.github.io/TgWitness/ko/docs/reference/quickstart/) · [배포](https://phishdestroy.github.io/TgWitness/ko/docs/reference/deployment/)

## 단 한 줄의 명령어로 설치하기

가이드형 설치 프로그램에는 전용 Python 런타임이 포함되어 있습니다. 향후 설치 시에도 동일한 주소를 사용하십시오. 각 릴리스마다 설치 프로그램, 해시, 서명 및 빌드 정보가 함께 업데이트됩니다.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Ubuntu 서버에서는 백그라운드 서비스를 설치하기 위해 root 권한으로 실행하십시오. 데스크톱에서는 일반 사용자 권한으로 실행하십시오.

**Windows (PowerShell 또는 명령 프롬프트):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Windows에서는 관리자 권한이 필요하지 않습니다. 자식 PowerShell 프로세스는 터미널을 열어둔 채로 결과를 표시합니다. Python 및 종속성은 설치 폴더에 남아 있습니다.

Ubuntu에서는 **‘이 컴퓨터**’, **‘임시 HTTPS 링크’** 또는 **‘자신만의 도메인’을** 선택하세요. 설치 프로그램이 패널 주소와 액세스 키를 표시합니다. 임시 링크를 사용하려면 브라우저에서 해당 HTTPS 주소를 열고 키를 입력하세요. 원격 서버에 로컬로 액세스하는 경우, 컴퓨터에서 SSH 포워딩을 사용하여 (`ssh -L 8787:127.0.0.1:8787 user@server`) 를 사용하여 `http://127.0.0.1:8787`를 엽니다. macOS 및 Windows에서는 로컬 패널이 브라우저에서 열리므로, 해당 터미널을 계속 실행해 두십시오.

패널에서 텔레그램에 로그인한 후 수집할 항목을 선택하세요. 설치만으로는 텔레그램 데이터 수집이 시작되지 않습니다.

## 모든 것이 실행되는 곳

`get.destroy.tools` 는 **정적 파일을 제공하는 Cloudflare**Worker입니다. 이 서비스에는 TgWitness 패널, 텔레그램 세션 또는 사용자 증거 데이터베이스가 없습니다. 또한 프로젝트용 VPS로 라우팅되지 않습니다. 이 애플리케이션은 명령어를 실행하는 컴퓨터에서 직접 실행됩니다.

| 설치 | 프로그램 | 데이터 |
| --- | --- | --- |
| 루트 권한으로 실행되는 우분투 | `/opt/tgwitness` | 시스템 서비스: `/var/lib/tgwitness-<installation ID>`; 정확한 경로를 확인하려면 `tgwitness paths` 정확한 경로를 확인하려면 이 명령어를 사용하십시오. |
| Linux / macOS 사용자 | `~/.local/share/tgwitness` | `data/live` 해당 설치 환경에서. |
| Windows 사용자 | `%LOCALAPPDATA%\TgWitness` | `data\live` 해당 설치 환경에서. |

설정 `TGWITNESS_INSTALL_DIR` 다른 폴더를 선택하려면 [설정]을 클릭하세요. 설치된 버전과 데이터는 별도로 관리됩니다. 설치 프로그램은 사용자의 계정, 메시지 또는 키를 다운로드 사이트로 업로드하지 않습니다. Cloudflare 터널을 선택하면 패널 트래픽이 Cloudflare를 통해 전송되며, 사용자 지정 도메인을 사용하면 사용자 자신의 서버로 연결됩니다.

모든 설치 패키지에는 로컬 경로, 명령어 및 저장소 링크가 포함된 **START-HERE.html** 및 **START-HERE.txt** 파일이 들어 있습니다. `tgwitness guide` 를 실행하여 가이드를 엽니다. Windows에서는 `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` PowerShell에서 다음 명령을 실행하세요.

## 실행 전 확인 사항

이 한 줄짜리 명령어는 초기 스크립트에 대해 HTTPS를 신뢰합니다. 해당 스크립트는 설치 전에 SHA-256와 애플리케이션 및 제약 조건에 대한 프로젝트의 RSA 서명을 확인합니다. 또한 초기 스크립트를 먼저 다운로드하여 검증할 수도 있습니다.

공개 배포 키는 [release-signing.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub)pub입니다. 해당 키의 SHA-256는 다음과 같습니다:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

신뢰할 수 있는 저장소 리비전으로부터 이 지문을 보관하십시오. 동일한 다운로드 서버의 체크섬을 통해 불일치를 감지하며, 독립적으로 신뢰받는 공개 키를 통해 릴리스 서명의 진위 여부를 인증합니다.

아래의 검증용 다운로드 파일을 저장할 새로운 빈 디렉터리를 사용하십시오.

**Linux / macOS — 새롭고 빈 다운로드 디렉터리에서 실행하십시오**(curl 및 OpenSSL 필요):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

`&&` 다운로드, 키 지문 또는 서명 검사가 실패하면 체인은 실행 전에 중단됩니다. 스크립트 다운로드와 서명 사이에 게시물이 생성된 경우, 둘 다 다시 다운로드하십시오. 기존 설치 프로그램은 변경 불가능한 패키지 URL을 유지합니다.

**Windows — 실행하기 전에 SHA-256를 확인하세요:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

해시 값을 `install.ps1` 줄을 비교하십시오. 독립적인 서명 검증을 위해서는 OpenSSL(예: Git Bash에서 실행)과 위의 동일한 공개 키 지문을 사용하십시오:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows 설치 과정 자체에서 .NET을 통해 패키지 서명을 검증하므로 OpenSSL이 필요하지 않습니다. 이는 Authenticode가 아닌 분리된 RSA-3072 / SHA-256 서명입니다. [매니페스트](https://get.destroy.tools/manifest.json)에는 소프트웨어 버전, 정확한 Git 커밋, 불변 릴리스 ID 및 각 아티팩트의 SHA-256가 기록됩니다. 이 페이지는 해당 소스 코드로 연결됩니다. 매니페스트와 체크섬 목록에도 분리된 서명이 있습니다 (`manifest.json.sig` 그리고 `SHA256SUMS.txt.sig`).

## 기존 설치 환경 업데이트

**새로운 버전이 출시되면 다운로드 사이트가 업데이트되며, 설치된 프로그램은 설치 프로그램을 다시 실행할 때 업데이트됩니다..** 실행 중인 컬렉션에 대해서는 무인 업데이트 기능이나 자동 재시작 기능이 제공되지 않습니다. 현재 설치 프로그램 채널은 **미리보기**이며, 다음에서 게시되고 검증된 빌드를 따릅니다 `main`에서 게시되고 검증된 빌드를 따르며, 해당 커밋은 마지막 번호가 매겨진 GitHub 릴리스보다 최신일 수 있습니다. 페이지의 버전은 `pyproject.toml`에서 제공되며, 해당 커밋 및 빌드 ID를 통해 동일한 프리뷰 버전 내의 업데이트를 구분할 수 있습니다.

이전과 동일한 설치 폴더와 OS 사용자를 사용하십시오. 수집을 중지한 상태에서 전체 데이터 디렉터리를 백업하십시오; `tgwitness paths` 이를 식별합니다. 서명된 내보내기 파일은 전체 설치 백업이 아닙니다.

**Ubuntu 루트 설치 경로: `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

설치가 성공적으로 완료된 후:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Linux/macOS 사용자 설치의 경우, 원래의 `TGWITNESS_INSTALL_DIR` 또는 기본 설정을 사용하고 첫 번째 설치 명령을 다시 실행하십시오. 업데이트 전에 전경 패널을 닫았다가 업데이트 후 다시 시작하십시오. 구성된 리눅스 사용자 서비스의 경우, 해당 `tgwitness restart` 명령을 실행하십시오.

**Windows:** 실행 중인 패널을 닫고, Windows 설치 명령을 다시 실행한 후, 동일한 설치 환경에서 `bin\tgwitness.cmd` 같은 설치 환경에서 실행하십시오. 설치 프로그램은 데이터, 세션, 액세스 설정 및 서명 키를 유지합니다. 새로운 환경이 검증을 통과한 후에만 런처를 전환하며, 설치에 실패하면 이전 런처가 그대로 유지됩니다. 저장소 형식 변경에 대비하여 업그레이드 전 백업을 보관하십시오.

## Ubuntu에서 자주 사용하는 명령어

| 명령어 | 결과 |
| --- | --- |
| `tgwitness open` | 현재 패널 URL 및 액세스 키. |
| `tgwitness paths` | 프로그램, 데이터 및 가이드의 정확한 경로. |
| `tgwitness guide --print` | 오프라인 사용 안내서. |
| `tgwitness status` / `tgwitness logs` | 가용성/서비스 로그. |
| `tgwitness stop` / `tgwitness start` | 서비스 중지/재개; 데이터 보존. |
| `tgwitness token rotate` | 관리자 키를 변경하고 브라우저 세션을 종료하십시오. |
| `tgwitness tunnel off` | 공개 퀵 터널을 비활성화하고, 로컬 패널은 유지합니다. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | 퀵 터널 링크 생성 / 주소 변경. |

동료 토큰, 세션 및 IP 제한에 대해서는 [‘액세스’를](https://phishdestroy.github.io/TgWitness/ko/docs/reference/access/) , GitHub에서 Cloudflare로의 릴리스 워크플로우에 대해서는 [‘설치 프로그램 게시’를](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) 참조하십시오.

## TgWitness 제거

별도의 제거 프로그램은 없습니다. 패널을 중지한 후 해당 폴더를 삭제하면 됩니다. data 폴더를 삭제하면 저널, 서명 키, 텔레그램 세션 및 저장된 파일이 영구적으로 삭제됩니다. 그 전에:

1. 필요한 내용을 내보내고(**내보내기 → 서명된 ZIP 다운로드**), 서명 키의 지문과 체크포인트는 이 컴퓨터 외부에 보관하십시오. 작업 공간 자체를 보관하려면, 데이터 수집을 중지한 상태에서 전체 데이터 폴더를 복사하십시오.
2. **'Extras → Server** 24/7'에서 생성된 서버는 **'Your**servers'에서 삭제하거나 `python -m tgwitness.cloud destroy`; 해당 서버는 삭제될 때까지 제공업체에서 요금을 청구합니다.
3. Telegram의 **‘설정’ →**‘기기’에서 각 계정의 세션을 종료하십시오. 파일을 삭제한다고 해서 Telegram 측에서 세션이 로그아웃되는 것은 아닙니다.

**Ubuntu 루트 설치.** 데이터 폴더를 확인한 후, 서비스를 중지하고, 서비스와 폴더, 바로가기를 제거하십시오:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux 또는 macOS 사용자 설치 방법.** 패널을 닫습니다. 구성된 Linux 사용자 서비스는 다음 명령어로 중지됩니다 `systemctl --user disable --now tgwitness-<ID>`; 해당 유닛은 `~/.config/systemd/user/`입니다. 그런 다음 `~/.local/share/tgwitness` (또는 사용자의 `TGWITNESS_INSTALL_DIR`)와 `~/.local/bin/tgwitness` 바로 가기를 삭제하십시오.

**Windows.** 패널을 닫고 `%LOCALAPPDATA%\TgWitness` (또는 `TGWITNESS_INSTALL_DIR`). 설치 프로그램은 서비스, 예약된 작업 또는 바로 가기를 추가하지 않습니다.
