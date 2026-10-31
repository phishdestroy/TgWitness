# 계속 운영해 주세요

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/server/

시스템 재시작 시에도 수집기를 계속 가동하고 데이터를 온전하게 유지합니다.

## 실행 방법 선택

로컬 설치의 경우, [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 디렉토리에 있는 [런처](https://phishdestroy.github.io/TgWitness/ko/docs/start/) 및 서비스 예제를 사용하십시오. Docker를 사용하는 경우, Docker Compose를 설치한 후 프로젝트 디렉토리에서 다음 명령을 실행하십시오:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

기본 패널은 호스트의 루프백 주소, 포트 8787에서 연결을 수신 대기합니다. 로컬에서 또는 SSH 터널을 통해 패널을 열어주세요. 두 번째 명령어에서 생성된 토큰을 사용하여 패널 잠금을 해제하세요.

## 전체 데이터 디렉터리를 유지하십시오.

네이티브 설치 환경에서는 `data/live`를 사용합니다. Docker는 영구 저장소인 `tgwitness-data` 볼륨을 사용합니다. 저널, 계정 세션, 키 및 운영 상태를 함께 보관하십시오. 서명된 내보내기 파일은 유용한 증거 자료이지만, 전체 설치 백업은 아닙니다.

1. 일관된 백업을 수행하기 전에 데이터 수집을 중지하십시오.
2. 전체 비공개 데이터 디렉터리를 호스트 외부의 보호된 저장소로 복사하십시오.
3. 백업에 의존하기 전에 격리된 설치 환경에서 복원 테스트를 수행하십시오.

## 재시작 후 확인하세요

예상 작업 공간 및 키, 텔레그램 연결, 선택된 소스, 새 메시지 캡처 설정을 확인하십시오. 저장된 MTProto 상태와 캐치업 기능을 통해 텔레그램에 여전히 남아 있는 업데이트를 복구할 수 있습니다. 그러나 만료된 모든 업데이트나 캡처 전에 삭제된 수정 내역은 복원할 수 없습니다.

컨테이너 상태란 웹 서버가 응답함을 의미합니다. 제어된 메시지와 검증 절차를 통해 데이터 수집 및 외부 공개 여부를 평가하십시오.

## 의도한 내용만 게시하십시오

배포 안내서에는 HTTPS 예시, 영구 볼륨 명령어, 업데이트 및 복원 단계가 포함되어 있습니다. 배포를 위한 Docker 명령어가 제공되며, 현재 [검증 기록](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/)에는 실제로 테스트된 환경이 명시되어 있습니다.
