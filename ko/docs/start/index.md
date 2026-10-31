# 몇 분 만에 시작하세요

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/start/

먼저, 실제 작동 예시를 살펴보세요. 그런 다음 본인의 계정을 연결하세요.

## 계정 없이 둘러보기

프로젝트를 다운로드하거나 클론한 후, **Python 3.11 이상을** 설치하고 데모를 실행하세요. 런처가 로컬 환경을 생성하고 지정된 종속성을 설치합니다.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

브라우저를 열면 가상의 메시지가 포함된 작업 공간이 표시됩니다. 대화를 열고, 수정 내역을 비교하며, 내보낸 파일을 확인해 보세요. 데모 모드는 텔레그램에 연결되지 않습니다.

![TgWitness 대화 화면 및 예시 메시지](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

작업 공간 예시입니다. 실제 저널은 별도로 생성됩니다.

## 나만의 작업 공간 만들기

데모 과정을 종료한 후 일반 실행 프로그램을 사용하십시오:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

런처에 표시된 로컬 주소를 엽니다. 요청이 있을 경우, 터미널에 표시된 로컬 파일의 **패널 액세스 토**큰을 입력하십시오. 이렇게 하면 TgWitness가 잠금 해제되며, 이는 텔레그램 로그인과는 별개의 절차입니다.

## 첫 번째 메시지를 캡처하세요

1. [전용 텔레그램 계정을 연결하세요.](https://phishdestroy.github.io/TgWitness/ko/docs/accounts/)
2. 계정이 접근할 수 있는 그룹이나 채널을 선택한 후, 모니터링을 시작하세요.
3. 사용자가 관리하는 테스트 그룹에 새 메시지를 보내고, 해당 메시지가 저널에 표시되는지 확인하십시오.

서버 설치를 위해서는 [‘Keep it running’을](https://phishdestroy.github.io/TgWitness/ko/docs/server/) 따르십시오.
