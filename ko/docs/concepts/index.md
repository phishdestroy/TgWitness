# 증거가 어떻게 활용되는지 확인하기

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/concepts/

메시지는 변경될 수 있습니다. 여러분이 확인한 내용의 기록은 언제든지 검증 가능해야 합니다.

아래의 두 가지 간단한 실험을 살펴보세요. 이 실험들은 가상의 메시지를 사용하며, 브라우저 내에서만 실행되고 텔레그램에 연결되지 않습니다.

## 채팅 내역 내보내기에서 검증 가능한 기록으로

[Telegram Desktop의 내보내기 기능은](https://telegram.org/blog/export-and-more) 사용 가능한 채팅 기록과 미디어를 HTML 또는 JSON 형식으로 내보내 오프라인에서 사용할 수 있게 합니다. TgWitness는 수신된 변경 사항에 대한 지속적인 기록, 관찰 내용 및 내보내기 파일에 대한 서명, 수신자가 독립적으로 비교할 수 있는 체크포인트를 추가합니다.

| 과제 | Telegram 데스크톱 내보내기 | TgWitness |
| --- | --- | --- |
| 저장된 대화 읽기 | 선택된 미디어가 포함된 HTML 또는 JSON | 저장된 채팅, 검색 가능한 일지 및 오프라인 보고서 |
| 시간에 따른 변화를 추적하십시오 | 내보낼 때 확인할 수 있는 기록 | 이전에 캡처된 버전, 이후의 수정 내역 및 삭제 기록이 함께 보존됩니다. |
| 인계 후 파일 확인 | 표준 HTML/JSON 내보내기 파일에는 서명이 없습니다. | 서명된 매니페스트, 레코드별 서명 및 봉인된 HTML/PDF/JSON 보고서는 신뢰할 수 있는 수집기 키를 기준으로 검증됩니다. |
| 이전 보존 상태와 비교 | 별도의 참조 사본 또는 해시 값을 보관하십시오. | 서명된 체크포인트, 별도의 위트니스 및 선택적 외부 타임스탬프 |

파일 서명 비교는 2026년 11월 2일에 검토된 [텔레그램 데스크톱 내보내기 작성기를](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) 기준으로 합니다. TgWitness는 수집기의 키로 서명하며, 아래의 확인 사항은 수신자가 이를 어떻게 사용하는지 보여줍니다.

## 한 가지 메시지, 세 가지 관찰점

텔레그램에서 새 메시지, 수정 알림, 삭제 알림이 전송되면 수집기는 세 가지 별도의 기록을 추가합니다. 수정 알림은 첫 번째 기록을 대체하지 않습니다. 삭제 알림도 해당 기록을 지우지 않습니다.

01 / 메시지 이동 경로예시 순서

Telegram delivers an update to the collector, which appends a journal record. · 텔레그램 · 수집기 · 저널 · 업데이트 → · 추가 →

현재 채팅 보기 메시지 #42

메시지가 삭제되었습니다.

해당 메시지가 채팅 화면에서 사라졌습니다.

관찰 일지 3건의 기록

1. 01

   `message.new`

   10:00에 만나요

   ✓
2. 02

   `message.edited`

   11:00에 만나요

   ✓
3. 03

   `message.deleted`

   #42에 대한 삭제 공지

   ✓

수신된 세 가지 관찰 사항 모두는 기록부에 그대로 남아 있습니다.

이미 선택된 소스 하나에 대한 간소화된 경로. 운영 기록도 실제 저널을 공유합니다. 캡처 내용은 해당 계정이 볼 수 있는 내용과 텔레그램이 제공하는 내용에 따라 달라집니다.

삭제 알림에는 신뢰할 수 있는 삭제 시간이나 메시지를 삭제한 사람이 명시되지 않습니다. 이러한 정보를 알 수 없게 함으로써, ‘관찰’과 ‘추측’ 사이의 구분이 유지됩니다.

## 기록을 변경하세요. 해시를 추적하세요.

각 기록에는 이전 기록의 해시가 포함됩니다. 해당 기록의 해시는 해당 링크를 포함한 이벤트 필드 전체를 포괄합니다. 외부에 보관된 체크포인트는 특정 저널 길이와 시작 해시를 고정합니다.

02 / HASH-CHAIN SANDBOX실제 SHA-256 · 기록 예시

기록 01**메시지 수신됨**`h₁ = SHA-256(e₁)`64개의 0으로 구성된 링크

기록 02**11:00에 만나요**`h₂ = SHA-256(e₂)`h₁ 포함

기록 03**삭제 감지됨**`h₃ = SHA-256(e₃)`h₂ 포함

다른 곳에 보관됨**기록 3건 · 헤드 `h₃`**이 고정된 경계를 제공된 기록부와 비교해 보십시오.

이벤트를 변경하면 해시가 변경됩니다. 체인을 재구성하면 체인의 선단이 변경됩니다. 체인의 끝부분을 제거하면 체인의 길이가 보존된 체크포인트보다 짧아집니다.

**기록 2번 및 전체 해시값 확인**

이 예시에서 해시 처리된 정확한 UTF-8 JSON 데이터입니다. 값은 가상의 것이며, 9개의 필드와 직렬화 형식은 저널 형식과 일치합니다.

```

```

저장된 기록 2의 해시

``

기록 2의 해시 재계산

``

이 샌드박스는 서명이 아닌 해시를 계산합니다. 실제 검증기는 모든 이벤트의 Ed25519 서명, 시퀀스 및 링크도 함께 확인합니다. 해시만 재구성해서는 신뢰할 수 있는 키 하에서 유효한 서명을 생성할 수 없습니다.

## 실제 규칙을 몇 줄로 요약하면 다음과 같습니다.

해시 + 서명

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C**는 9개의 이벤트 필드를 UTF-8 JSON 형식으로 직렬화합니다: 정렬된 키, 여분의 공백 없음, ASCII 이스케이프 없음, NaN/무한대 없음. 이벤트의 `previous_hash`는 hi−1입니다. 표시된 h0는 64개의 0 문자를 의미하며, 서명은 32바이트의 원시 다이제스트를 포함합니다.

9개의 필드는 `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` 및 `previous_hash`입니다. 이는 TgWitness에 [문서화된 JSON 인코딩](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#event-canonicalization) 방식이며, 해시 및 서명 자체는 해시 입력 필드가 아닙니다.

유지된 체크포인트

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

고정된 수집기 키 아래에 있는 체크포인트 서명을 확인한 다음, 그 경계를 검증된 저널과 비교하십시오. 이후에 내보낸 파일에는 더 많은 기록이 포함될 수 있으나, 이전 체크포인트에서는 여전히 일치해야 합니다.

## 세 가지 질문, 세 가지 다른 확인 절차

[01 / 무결성**이 기록이 변경되었나요?** 별도로 신뢰할 수 있는 키를 사용하여 해시값과 서명을 검증합니다.](https://phishdestroy.github.io/TgWitness/ko/docs/exports/)[02 / 연속성**이전에 어떤 내용이 유지되었나요?** 서명된 내보내기 파일을 별도의 증인이 보관한 체크포인트와 비교해 보십시오.](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)[03 / 제공**이 테스트 이벤트들이 도착했나요?** 각 계정의 기록부와 전송, 수정, 삭제 작업을 대조하여 일치 여부를 확인합니다.](https://phishdestroy.github.io/TgWitness/ko/docs/cases/)

서명을 사용하여 보존된 기록을 확인하고, 체크포인트를 사용하여 이전 경계와 비교하며, 제어된 전달 테스트를 통해 수집 상태를 측정하십시오. 각각은 특정 질문에 대한 답을 제공합니다. [검증 범위와 신뢰 가정을 숙지하십시오.](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#verification-scope)

정보 수집부터 사건 자료 정리까지, [계정 전체에 대한 조사](https://phishdestroy.github.io/TgWitness/ko/docs/cases/) 과정을 따라가 보세요.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
