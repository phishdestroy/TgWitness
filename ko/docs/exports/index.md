# 내보내기 및 검증

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/exports/

받는 사람이 귀하의 작업 공간과 직접 대조해 확인할 수 있는 파일을 건넵니다.

참조 유지서명된 ZIP 파일 내보내기수신자가 검증합니다

서명과 체크포인트가 처음이신가요? [예시 기록을 바꿔 보고](https://phishdestroy.github.io/TgWitness/ko/docs/concepts/#chain) 어떤 검사가 잡아내는지 보십시오.

수집 담당자와는 별도로 사본을 보관하고 싶으신가요? [S3 설정](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3), [오브젝트 잠금](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3-retention) 또는 [검증된 복구 기능을](https://phishdestroy.github.io/TgWitness/ko/docs/exports/#s3-restore) 확인해 보세요.

## 신뢰할 수 있는 참고 자료로 활용

작업 공간 키 지문은 수집기가 아닌 다른 곳에 적어 두십시오. 수집하는 동안 서명된 체크포인트도 다른 곳에 보관하거나 [독립 증인](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)을 실행하십시오. 받는 사람은 이것으로 키와 저널의 이전 상태를 확인합니다.

## 서명된 ZIP 파일 다운로드

**내보내기** → 서명된 증거 ZIP. 전체 저널과 서명된 파일 매니페스트가 들어 있습니다. 읽기 쉬운 보고서는 [Report studio](https://phishdestroy.github.io/TgWitness/ko/docs/reports/)에서 만들거나, 선택한 데이터만 [인계용 추출](https://phishdestroy.github.io/TgWitness/ko/docs/handover/)로 보냅니다.

HTML, PDF, JSON 보고서에는 각자의 봉인이 있습니다. CSV는 작업용 사본일 뿐이며, 무결성이 필요하면 검증된 ZIP 안의 CSV를 사용하십시오.

## 신뢰할 수 있는 TgWitness 사본을 통해 확인해 보세요.

프로젝트 환경에서, 귀하의 지문과 경로로:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

통과하면 `key_pinned: true`와 `checkpoint_checked: true`가 표시됩니다. 그 출력을 아카이브 옆에 보관하십시오. 체크포인트는 내보내기의 끝 또는 그 이전에 있어야 합니다.

## 검증 결과 사용

- **파일:** 매니페스트가 해시를, 서명이 저널을 묶습니다. 어떤 변경도 드러납니다.
- **신원:** 보관해 둔 지문이 예상한 키임을 증명합니다.
- **이전 상태:** 체크포인트가 내보내기를 인계 전에 저장한 저널 앞부분과 비교합니다.
- **범위:** 공백, 수집 결과, 보내기 → 편집 → 삭제 테스트가 이 구성이 실제로 잡아낸 것을 보여 줍니다.

자세히: [검증이 증명하는 것과 증명하지 않는 것](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#verification-scope).

## S3 오프사이트 백업 설정

작업 공간의 **내보내기 → 오프사이트 사본**. AWS S3와 S3 호환 저장소에서 작동합니다. 저널 세그먼트, 저장된 파일, 타임스탬프가 있는 체크포인트, 완료된 채팅 내보내기를 복사하며, 각각 수집기를 떠나기 전에 `AES-256-GCM`으로 암호화됩니다.

온라인 데모는 업로드가 꺼진 상태로 이 컨트롤을 보여 줍니다. 실제 자격 증명은 귀하의 설치에서만 입력하십시오.

[![오프사이트 복사 패널 전체: 엔드포인트, 리전, 버킷, 액세스 키, 일정, 오브젝트 잠금 및 복구 키 제어](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

고급 옵션이 포함된 전체 패널이 펼쳐진 모습입니다. 저장소 인증 정보는 표시되지 않습니다.

| 분야 | 입력할 내용 |
| --- | --- |
| 엔드포인트 | 저장소 URL. 버킷 경로나 자격 증명은 넣지 않습니다. 예: `https://s3.example.invalid`. |
| 지역 | 공급자가 요구하는 값. 기본값 `us-east-1`. |
| 버킷 | 쓰기 권한이 있는 기존 버킷. 예: `example-case-backup`. |
| 버킷 내 폴더 | 접두사, 기본값 `tgwitness`. 그 위에 작업 공간별 접두사가 붙습니다. |
| 액세스 키 ID / 비밀 액세스 키 | 둘을 함께 입력하며 볼트에 저장됩니다. 나중에 둘 다 비워 두면 그대로 유지됩니다. |
| 경로 형식 주소 | 켜짐: `endpoint/bucket`. 꺼짐: `bucket.endpoint`. 공급자에 따라 다릅니다. |
| 복사 간격 | 1~1,440분, 기본값 5. 앱이 실행 중일 때만. |
| Object Lock 보존 | 버킷이 Object Lock을 지원하면 일수와 모드. 0이면 버킷 기본값을 유지합니다. |

1. 버킷을 만들고, **오프사이트 사본 보관**을 체크하지 않은 채 대상과 자격 증명을 입력한 뒤 **오프사이트 사본 저장**을 누릅니다.
2. **연결 테스트**는 암호화된 테스트 객체를 업로드합니다.
3. **암호화 키 다운로드** 후 수집기와 떨어진 곳에 보관합니다. 키가 없으면 복구도 없습니다.
4. **오프사이트 사본 보관**을 체크하고 저장한 다음 **지금 복사**를 누르거나 일정에 맡깁니다.

## 보관 현황 및 복사 진행 상황 확인

**추가 옵션**에서 보존 일수와 `GOVERNANCE` 또는 `COMPLIANCE`를 고릅니다. TgWitness는 업로드된 객체에서 보존 설정을 다시 읽어 확인됨, 없음, 확인 실패 중 하나로 알려 줍니다.

패널에는 마지막 실행, 객체 수, 바이트, 복사된 저널 경계, 오류가 표시됩니다. 없는 로컬 파일은 보고되고 다음 실행 때 다시 시도되며, 나머지는 계속 복사됩니다.

업로드는 직접 연결, SOCKS5, HTTP로 나갑니다. MTProxy 전용 경로에서는 사본이 오류와 함께 대기합니다.

## 복구 키는 별도로 보관하십시오

키 JSON에는 복호화 키, 대상, 접두사, 키 지문이 들어 있습니다. 복구하려면 이것과 읽기 권한이 있는 저장소 자격 증명이 필요합니다.

엔드포인트, 버킷, 접두사를 바꿨나요? 키를 다시 다운로드하십시오. 새 사본은 새 대상에서 시작되며, 이전 채팅 내보내기는 원래 자리에 남습니다.

## 다른 컴퓨터에서 복원 및 검증하기

신뢰할 수 있는 TgWitness 설치, 키 JSON, 읽기 전용 저장소 자격 증명, 빈 폴더가 필요합니다:

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

모든 것은 먼저 비공개 임시 폴더에서 확인됩니다: 전체 저널, 체크포인트, 파일 해시와 크기. 안전하지 않은 경로, 충돌하는 세그먼트, 체크포인트보다 짧은 저널은 실패하며, 이때는 아무것도 기록되지 않습니다.

성공하면 `events.jsonl`, `media/`, `checkpoints/`, `exports/`를 얻습니다. 명령의 JSON 출력을 함께 보관하고, 직접 보관한 체크포인트나 증인 기록과 비교하십시오.
