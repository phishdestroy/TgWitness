# 소스 기록 불러오기

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/history/

활성화된 소스의 과거 메시지를 불러오고, 일시 중지 및 재시작하며, 서명된 진행 보고서를 검증할 수 있습니다.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [문서](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [컬렉션](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## 일시 중지, 재개 및 부분 결과

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- 메시지 관찰, 첨부 파일 처리 및 커서 커밋이 하나의 트랜잭션으로 수행됩니다. 실행이 재개되더라도 이미 커밋된 관찰 내용은 반복되지 않습니다. 실시간 캡처 또는 별도로 명시적으로 시작된 실행에서는 동일한 메시지를 독립적으로 관찰할 수 있습니다.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- 접근할 수 없는 소스나 수집 과정에서 비활성화된 소스는 '실패' 또는 '건너뜀'으로 표시됩니다. 다른 소스는 계속 수집되며, 전체 결과는 불완전합니다.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

이력 완료는 이력 읽기 작업에 대해서만 설명합니다. 첨부 파일은 대기 상태로 남아 있거나, 실패하거나, 구성된 정책에 따라 제외될 수 있습니다. 저널과 첨부 파일 대기열에서 미디어 수신 확인을 확인하십시오. 바이트가 보존된 완료된 수신 확인만 저장된 첨부 파일로 간주됩니다. 이력 작업은 명시적인 스냅샷 요청이며, 향후 실시간 이벤트의 범주를 선택하는 스위치와는 별개입니다.

## 전송 및 검증

**서명된 진행**보고서를 저장한 후, **‘증거 내보내기’** 기능을 사용하여 저널과 저장된 첨부 파일을 다운로드하십시오. 나중에 증거를 내보낼 경우 추가 기록이 포함될 수 있습니다. 이 보고서는 생성 시점의 저널 접두사에 카운터를 연동합니다. 이 버전의 신뢰할 수 있는 체크아웃에서 검증기를 실행하십시오:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

획득 커서는 로컬 작업 공간의 상태를 나타냅니다. 증거 ZIP 파일만 복원한다고 해서 진행 중인 획득 작업이나 텔레그램 세션이 복원되는 것은 아닙니다. 원래 작업을 계속 진행해야 하는 경우 작업 공간 백업을 보관해 두십시오.
