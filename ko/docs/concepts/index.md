# 증거가 어떻게 활용되는지 확인하기

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/concepts/

메시지는 바뀝니다. 귀하가 본 것에 대한 기록은 바뀌면 안 되고, 누구나 그것을 확인할 수 있어야 합니다.

아래에 작은 실험 두 개가 있습니다. 가짜 메시지이며, 모든 것이 브라우저에서 실행되고 텔레그램으로는 아무것도 가지 않습니다.

## 채팅 내역 내보내기에서 검증 가능한 기록으로

[Telegram Desktop 내보내기](https://telegram.org/blog/export-and-more)는 지금 보이는 기록을 HTML이나 JSON으로 저장합니다. TgWitness는 여기에 계속 이어지는 변경 저널, 모든 기록의 서명, 다른 사람이 대조할 수 있는 체크포인트를 더합니다.

| 과제 | Telegram 데스크톱 내보내기 | TgWitness |
| --- | --- | --- |
| 저장된 대화 읽기 | 선택된 미디어가 포함된 HTML 또는 JSON | 저장된 채팅, 검색 가능한 일지 및 오프라인 보고서 |
| 시간에 따른 변화를 추적하십시오 | 내보낼 때 확인할 수 있는 기록 | 이전 버전, 이후 편집, 삭제를 모두 보관 |
| 인계 후 파일 확인 | 표준 HTML/JSON 내보내기 파일에는 서명이 없습니다. | 서명된 매니페스트, 서명된 기록, 봉인된 보고서를 신뢰할 수 있는 키로 확인 |
| 이전 보존 상태와 비교 | 별도의 참조 사본 또는 해시 값을 보관하십시오. | 서명된 체크포인트, 별도의 위트니스 및 선택적 외부 타임스탬프 |

이 비교는 2026년 11월 2일 기준 [Telegram Desktop 내보내기 코드](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output)를 바탕으로 합니다.

## 한 가지 메시지, 세 가지 관찰점

새 메시지, 편집, 삭제는 세 개의 별도 기록이 됩니다. 편집은 첫 기록을 덮어쓰지 않고, 삭제도 그것을 지우지 않습니다.

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

텔레그램은 누가 메시지를 삭제했는지, 정확히 언제인지 알려 주지 않습니다. TgWitness는 추측하지 않고 그 필드를 비워 둡니다.

## 기록을 변경하세요. 해시를 추적하세요.

모든 기록에는 바로 앞 기록의 해시가 들어 있습니다. 다른 곳에 보관한 체크포인트가 저널 길이와 마지막 해시를 고정합니다.

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

**C**는 아홉 개의 이벤트 필드를 UTF-8 JSON으로 만든 것입니다: 키 정렬, 불필요한 공백 없음, ASCII 이스케이프 없음, NaN/무한대 없음. `previous_hash`는 hi−1, h0은 0 64개이며, 서명은 다이제스트의 원시 32바이트를 대상으로 합니다.

필드: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. 전체 사양: [이벤트 인코딩](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#event-canonicalization).

유지된 체크포인트

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

고정된 키로 체크포인트 서명을 확인한 다음, 저널과 비교합니다. 이후의 내보내기는 더 길어도 되지만, 체크포인트 지점에서는 일치해야 합니다.

## 세 가지 질문, 세 가지 다른 확인 절차

[01 / 무결성**이 기록이 변경되었나요?** 신뢰하는 키로 해시와 서명을 확인합니다.](https://phishdestroy.github.io/TgWitness/ko/docs/exports/)[02 / 연속성**이전에 어떤 내용이 유지되었나요?** 내보내기를 증인이 보관한 체크포인트와 비교합니다.](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)[03 / 제공**이 테스트 이벤트들이 도착했나요?** 테스트 메시지를 보내고, 편집하고, 삭제한 뒤 각 계정이 무엇을 잡았는지 봅니다.](https://phishdestroy.github.io/TgWitness/ko/docs/cases/)

서명은 "바뀌었는가", 체크포인트는 "이전에 있던 것과 일치하는가", 테스트 메시지는 "모두 잡았는가"에 답합니다. [검증이 증명하는 것과 증명하지 않는 것.](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#verification-scope)

다음: 시작부터 사건 패키지까지 [계정 전체 조사](https://phishdestroy.github.io/TgWitness/ko/docs/cases/).

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
