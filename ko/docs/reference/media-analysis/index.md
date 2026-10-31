# 로컬 OCR 및 텍스트 변환

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/media-analysis/

로컬 워커를 통해 캡처된 이미지와 오디오를 인식하고, 추출된 텍스트를 원본 파일과 연결된 상태로 유지합니다.

**현재 메인 버전:** 소스 체크아웃을 사용하십시오. 0.7.0 휴대용 미리보기 버전은 이 기능이 구현되기 전의 버전입니다.

[워크플로우 가이드](https://phishdestroy.github.io/TgWitness/docs/archive/) · [위키](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

`media.saved` 저널 기록을 열고, **‘첨부 파일 인식’을** 선택한 다음, **‘아카이브에 문의’** 아래에서 OCR 또는 전사 기능을 선택하십시오. 처리는 수동으로 로컬에서 이루어집니다. 클라우드 미디어 모드나 자동 업로드 기능은 없습니다. 원본 첨부 파일의 바이트 데이터와 `media_sha256`는 변경되지 않으며, 인식된 텍스트는 명시적으로 ‘기계 인식’으로 표시되고 원본 해시, 엔진/모델 버전, 언어, 매개변수 및 완료 시간과 함께 별도로 저장됩니다. 전사본에는 반환된 타임스탬프가 유지됩니다.

**'인식된 텍스트 검색'** 및 OCR/전사본 필터를 사용하여 이 결과들을 검색하십시오. 이는 별도의 파생 데이터 검색 기능으로, 기계 인식 결과를 원본 텔레그램 텍스트로 자동 변환하거나 서명된 이벤트에 추가하지 않습니다.

## 선택적 워커 설정

버전 1은 로컬 Docker 데몬이 설치된 Linux 호스트가 필요합니다. Windows 환경에서는 자체 로컬 데몬을 갖춘 Linux VM/WSL 환경 내에서 TgWitness를 실행할 수 있습니다. 이 패널은 신뢰할 수 없는 첨부 파일을 직접 디코딩하지 않습니다.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

TgWitness 서비스 환경에서 다음 변수들을 설정하고 서비스를 재시작하십시오. 데몬 소켓은 기본적으로 `/var/run/docker.sock`로 설정되어 있으며, 루트 권한이 없는 환경에서는 `TGWITNESS_DOCKER_SOCKET`로 설정할 수 있습니다. 워커는 원격 Docker 컨텍스트 대신 해당 Unix 소켓을 명시적으로 사용합니다. 패널 사용자에게 Docker API를 노출하거나 인식 컨테이너 내에 해당 소켓을 마운트하지 마십시오.

텍스트 변환을 위해서는 CTranslate2와 호환되는 Whisper 모델을 별도로 설치한 후, `TGWITNESS_WHISPER_MODEL_DIR`를 해당 모델의 디렉터리로 설정하십시오. 워커는 `local_files_only=True`를 사용하여 모델을 불러오며, 선택된 모델과 입력 데이터는 읽기 전용으로 마운트됩니다. 엔진의 [모델 로딩 문서를](https://github.com/SYSTRAN/faster-whisper) 참조하십시오. 제공된 OCR 이미지에는 영어 및 러시아어 훈련 데이터가 포함되어 있습니다. 필요 시 이미지에 다른 언어를 추가할 수 있으며, 언어 코드는 [Tesseract의 CLI 규격을](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html) 따릅니다.

처리 과정에서 모델이 불러오지 않습니다. 빌드/설치 파일 다운로드 시 네트워크를 사용할 수 있으며, 각 실제 인식 컨테이너에서는 네트워크 기능이 비활성화되어 있습니다. 네트워크를 활성화하기 전에 이미지를 설치하십시오. 런타임에는 `--pull=never`가 사용됩니다.

## 한계 및 복구

이 컨테이너는 읽기 전용 루트 권한, 기능 제한(dropped capabilities), `no-new-privileges` , CPU 1개, 2 GiB 메모리, PID 제한 및 제한된 임시 파일 시스템을 갖춘 비특권 사용자로 실행됩니다. 선택한 파일의 검증된 사본과 선택 사항인 모델 디렉터리만 마운트됩니다. 수집기의 데이터베이스, 볼트 및 세션은 마운트되지 않습니다. [Docker 런타임 플래그가](https://docs.docker.com/reference/cli/docker/container/run/) 이러한 제한을 강제 적용하며, 이는 하드웨어 엔클레이브가 아닌 컨테이너 경계로 유지됩니다.

파일 크기는 50 MiB, 이미지는 2,000만 픽셀, 오디오는 재생 시간이 알려진 경우 30분으로 제한되며, 처리 시간은 5분으로 제한됩니다. 한 번에 하나의 워커만 실행되며, 워크스페이스당 대기 중이거나 실행 중인 작업은 최대 20개, 보존된 작업은 100개까지 허용됩니다. '취소'는 컨테이너를 중지시키고, '재시도'는 이전 시도에 연결된 새로운 작업을 생성합니다. 중단된 작업은 재시작 후 표시됩니다. 모델이 설정된 제한을 충족하지 못할 경우 처리가 실패할 수 있으며, 격리 조치 없이 무음으로 실행되지 않습니다.
