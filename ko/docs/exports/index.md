# 내보내기 및 검증

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/exports/

수신자가 수집 작업 공간 및 저장된 내역과 대조하여 확인할 수 있는 파일을 제공하십시오.

참조 유지서명된 ZIP 파일 내보내기수신자가 검증합니다

서명과 체크포인트가 처음이신가요? [샘플 기록을 변경해](https://phishdestroy.github.io/TgWitness/ko/docs/concepts/#chain) 보고 어떤 검사가 이를 감지하는지 확인해 보세요.

수집 담당자와는 별도로 사본을 보관하고 싶으신가요? [S3 설정](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3), [오브젝트 잠금](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3-retention) 또는 [검증된 복구 기능을](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3-restore) 확인해 보세요.

## 신뢰할 수 있는 참고 자료로 활용

컬렉터 외부에 워크스페이스의 공개 키 지문을 저장하십시오. 수집 중에는 서명된 체크포인트를 다른 곳에 보관하거나 [독립적인 증인을](https://phishdestroy.github.io/TgWitness/ko/docs/witness/) 활용하십시오. 이러한 참조 정보를 통해 수신자는 키와 이전 저널 경계를 확인할 수 있습니다.

## 서명된 ZIP 파일 다운로드

**‘Exports’를** 열고 서명된 증거용 ZIP 파일을 생성하십시오. 여기에는 전체 작업 공간 일지와 서명된 파일 매니페스트가 포함됩니다. [‘Report Studio’를](https://phishdestroy.github.io/TgWitness/ko/docs/reports/) 사용하여 가독성 높은 보고서를 작성하거나, [‘handover](https://phishdestroy.github.io/TgWitness/ko/docs/handover/)extract’를 통해 선별되고 최소화된 데이터만 전달할 수 있습니다.

HTML, PDF 및 JSON 보고서에는 각각 서명된 인장이 포함되어 있으며 별도로 확인할 수 있습니다. CSV는 분석에 편리한 사본입니다. 검증된 ZIP 파일 내의 정확한 CSV 파일을 사용하여 무결성을 확인하십시오. 수신자가 원본 기록 및 첨부 파일도 필요로 하는 경우, 서명된 ZIP 파일을 보관하십시오.

## 신뢰할 수 있는 TgWitness 사본을 통해 확인해 보세요.

설치된 프로젝트 환경에서 예시 지문 및 파일 경로를 다음과 같이 변경하십시오:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

두 참조 모두 검증을 통과하면 결과 보고서에 `key_pinned: true`와 `checkpoint_checked: true`가 표시됩니다. 검증 결과를 원본 아카이브와 함께 보관하십시오. 보관된 체크포인트는 내보내기 경계를 포함하거나 그 이전이어야 합니다.

## 검증 결과 사용

- **전달된 파일을 확인하십시오:** 매니페스트는 파일의 해시를 연결하고, 레코드 서명은 저장된 저널을 연결합니다. 변경된 파일이나 끊어진 레코드 체인이 감지됩니다.
- **작업 공간 신원을 확인하십시오:** 독립적으로 보관된 지문은 예상한 서명 키와 일치하는지 확인합니다.
- **이전 경계를 비교해 보십시오:** 보존된 체크포인트는 인계 전에 저장된 저널 접두사와 비교하여 내보내기 내용을 확인합니다.
- **수집 범위를 검토하십시오:** 누락된 부분, 수집 결과, 그리고 통제된 ‘보내기 → 편집 → 삭제’ 테스트를 통해 이 설정이 포착한 이벤트들을 확인할 수 있습니다.

이 결과를 수신자 사본에 함께 보관하십시오. 검사의 범위와 출처 주장 및 수집 범위에 대한 별도 평가에 대해 [검증이 무엇을 확립하는지](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#verification-scope) 확인하십시오.

## S3 오프사이트 백업 설정

실행 중인 작업 공간에서 [Exports] → [Off-site copy]를 엽니다. 이 선택적 기능은 AWS S3 및 기타 S3 호환 서비스와 연동됩니다. 이 기능은 저널 세그먼트, 보존된 사진 및 파일, 타임스탬프 응답이 포함된 체크포인트, 완료된 채팅 내보내기 파일을 복사합니다. 모든 객체는 업로드 전에 수집기에서 `AES-256-GCM`를 사용하여 암호화됩니다.

온라인 데모에서는 업로드 기능이 비활성화된 상태에서 동일한 제어 기능을 보여줍니다. 저장소 인증 정보는 본인이 직접 실행 중인 작업 공간에서만 입력하십시오.

[![오프사이트 복사 패널 전체: 엔드포인트, 리전, 버킷, 액세스 키, 일정, 오브젝트 잠금 및 복구 키 제어](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

고급 옵션이 포함된 전체 패널이 펼쳐진 모습입니다. 저장소 인증 정보는 표시되지 않습니다.

| 분야 | 입력할 내용 |
| --- | --- |
| 엔드포인트 | 버킷 경로나 인증 정보가 포함되지 않은 저장 서비스 URL. 가상의 예시: `https://s3.example.invalid`. |
| 지역 | 통신사가 요구하는 지역 코드입니다. 애플리케이션의 기본값은 `us-east-1`입니다. |
| 버킷 | 접근 가능한 기존 버킷. 가상의 예시: `example-case-backup`. |
| 버킷 내 폴더 | 객체 접두사; 기본값은 `tgwitness`입니다. 애플리케이션은 이 작업 공간의 서명 키 지문에서 파생된 접두사를 추가합니다. |
| 액세스 키 ID / 비밀 액세스 키 | 저장소 인증 정보를 모두 함께 입력하십시오. 이 정보는 워크스페이스 볼트에 저장됩니다. 저장된 인증 정보 쌍을 유지하려면 이후 저장 시 두 항목 모두 비워 두십시오. |
| 경로 형식 주소 | 서비스 제공업체에 따라, 기능이 활성화된 경우 ‘`endpoint/bucket`’를, 비활성화된 경우 ‘`bucket.endpoint`’를 사용하십시오. |
| 복사 간격 | 1분에서 1,440분까지 설정 가능하며, 기본값은 5분입니다. 예약된 백업을 수행하려면 애플리케이션이 실행 중이어야 합니다. |
| Object Lock 보존 | Object Lock을 지원하는 버킷의 보존 기간 및 모드. 보존 기간을 0일로 설정하면 버킷의 기본 보존 설정이 적용됩니다. |

1. 서비스 제공업체에서 버킷을 생성한 후, 저장 위치와 인증 정보를 입력하십시오. 준비 단계에서는 **‘오프사이트 사본 보관’ 옵션을** 선택 해제해 두었다가, 나중에 **‘오프사이트 사본 저장’을** 선택하십시오.
2. **'연결 테스트'를** 선택하세요. 그러면 암호화된 테스트 객체가 업로드되고 저장소의 응답이 확인됩니다.
3. **'암호화 키 다운로드'를** 선택하십시오. 해당 파일은 복구 시 필요하므로 수집기와는 별도로 보관하십시오.
4. **'오프사이트 사본 보관'** 확인란을 선택하고 다시 저장하십시오. 수동 처리를 원하면 **'지금 복사'를** 선택하거나, 예약된 일정을 그대로 실행하십시오.

## 보관 현황 및 복사 진행 상황 확인

'추가**옵션**(**More options**)'에서 보존 기간을 선택하고, 버킷이 Object Lock을 지원하는 경우 '`GOVERNANCE`' 또는 '`COMPLIANCE`'를 선택하십시오. TgWitness는 업로드된 객체의 보존 모드 및 기한을 다시 읽어옵니다. 별도의 보존 결과(확인됨, 보존 정보 누락 또는 확인 실패)를 검토하십시오.

패널에는 마지막 처리 결과, 객체 수, 전송된 바이트 수, 복사된 저널 경계 및 오류 사항이 표시됩니다. 누락되거나 변경된 로컬 미디어는 보고되며, 다음 처리 시 재시도됩니다. 해당 미디어 이후의 파일, 체크포인트 및 대기 중인 내보내기 작업은 여전히 복사될 수 있습니다.

업로드는 워크스페이스의 Direct, SOCKS5 또는 HTTP 경로를 사용합니다. S3 복사 시 이 경로 중 하나를 선택하십시오. MTProxy 전용 경로를 선택하면 복사 작업이 오류와 함께 보류 상태로 남게 됩니다.

## 복구 키는 별도로 보관하십시오

다운로드한 JSON 파일에는 복호화 키, 대상 설정, 작업 공간 객체 접두사 및 서명 키 지문이 포함되어 있습니다. 복구를 위해서는 이 키 파일과 버킷에 대한 읽기 권한이 있는 별도의 저장소 인증 정보가 모두 필요합니다. 이를 복구 계획에 반드시 포함시켜 두십시오.

엔드포인트, 버킷 또는 폴더 접두사를 변경하는 경우, 대상 설정이 일치하도록 키 파일을 다시 다운로드하십시오. 애플리케이션은 로컬에 보관된 저널, 파일 및 체크포인트의 새 복사본을 새로운 대상 위치에서 시작합니다. 로컬 업로드 대기열에서 이미 제거된 완료된 채팅 내보내기 파일은 이전 대상 위치에 그대로 남아 있습니다.

## 다른 컴퓨터에서 복원 및 검증하기

신뢰할 수 있는 TgWitness 설치본, 다운로드한 키 JSON 파일, 읽기 권한이 있는 저장소 인증 정보, 그리고 빈 출력 디렉터리를 사용하십시오. 아래의 가상의 인증 정보 자리 표시자를 실제 정보로 대체하십시오.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

다운로드된 파일과 복호화된 객체는 비공개 임시 저장소에 보관되며, 이 동안 전체 저널, 보존된 체크포인트, 보존된 미디어의 해시 및 크기가 검증됩니다. 안전하지 않은 경로, 충돌하는 저널 세그먼트, 체크포인트보다 짧은 저널은 거부됩니다. 검증에 실패한 경우 복원된 파일은 게시되지 않습니다.

복원이 성공하면 복사본에 포함된 자료에 대해 `events.jsonl`, `media/`, `checkpoints/` 및 `exports/`가 생성됩니다. 복원된 자료와 함께 명령어의 JSON 결과도 보관하십시오.

복구된 자료를 별도로 보관해 둔 체크포인트나 증인 기록과 비교한 후, 필요한 기간에 대한 기록된 수집 범위를 검토하십시오.
