# 계속 운영해 주세요

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/server/

수집기를 계속 실행하고, 재시작을 거쳐도 데이터를 안전하게 지킵니다.

## 실행 방법 선택

네이티브: [런처](https://phishdestroy.github.io/TgWitness/ko/docs/start/)와 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md)의 서비스 템플릿. Docker는 프로젝트 폴더에서:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

패널은 localhost:8787에서 대기합니다. 로컬이나 SSH 터널로 열고, 두 번째 명령에서 나온 토큰을 사용합니다.

## 전체 데이터 디렉터리를 유지하십시오.

네이티브: `data/live`. Docker: `tgwitness-data` 볼륨. 저널, 세션, 키는 함께 있어야 합니다. 서명된 내보내기는 증거이지 백업이 아닙니다.

1. 먼저 수집을 멈춥니다.
2. 데이터 디렉터리 전체를 호스트 밖 안전한 곳에 복사합니다.
3. 믿기 전에 별도의 설치에서 복원해 보십시오.

## 재시작 후 확인하세요

작업 공간과 키, 연결, 소스, 새 메시지가 들어오는지 확인합니다. TgWitness는 텔레그램에 아직 남아 있는 것을 따라잡을 뿐, 꺼져 있는 동안 일어난 모든 일을 따라잡지는 못합니다.

컨테이너가 "healthy"라는 것은 웹 서버가 응답한다는 뜻입니다. 수집이 작동하는지는 테스트 메시지와 증인이 알려 줍니다.

## 의도한 내용만 게시하십시오

HTTPS, 볼륨, 업데이트, 복원은 배포 참조에 있습니다. 실제로 테스트된 것: [검증 기록](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/).
