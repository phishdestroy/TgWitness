# 독립적인 증인

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/witness/

자체 키와 봇을 사용하여 위트니스를 실행하고, 서명된 체크포인트를 채널에 게시한 후, 내보낸 데이터를 이를 기준으로 대조하여 확인하십시오.

[내보내기 및 검증](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/) · [높은 신뢰도](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/) · [패널 가이드](https://phishdestroy.github.io/TgWitness/ko/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector．It checks the collector's signature and journal continuity，signs the result with its own key，and publishes it to a Telegram channel．Run it on a separate server with read-only access to the collector's witness endpoint．

흐름도 · 수집기 → Witness (서명된 체크포인트: 기록 수 + 헤더 해시); Witness → Witness 저널, 자체 키; Witness → 텔레그램 채널 (자체 봇을 통해 서명된 게시물); 증거 ZIP → verify.py; Witness 저널, 자체 키 → verify.py; 텔레그램 채널 → verify.py (텔레그램 데스크톱 내보내기 또는 t.me/s 페이지) · 수집기 · Witness · Witness 저널, 자체키 · 텔레그램채널 · 증거 ZIP · verify.py · 서명된체크포인트: 기록수 + · 헤더해시 · 자체봇을통해서명된게시물 · 텔레그램데스크톱내보내기또는 · t.me/s 페이지

**도표를 텍스트로 변환**

1. 수집기 → Witness (서명된 체크포인트: 기록 수 + 헤더 해시)
2. Witness → Witness 저널, 자체 키
3. Witness → 텔레그램 채널 (자체 봇을 통해 서명된 게시물)
4. 증거 ZIP → verify.py
5. Witness 저널, 자체 키 → verify.py
6. 텔레그램 채널 → verify.py (텔레그램 데스크톱 내보내기 또는 t.me/s 페이지)

## TgWitness가 제공하는 기능과 제공하지 않는 기능

| 이 도구는 | 증인은 결코 |
| --- | --- |
| 단일 워크스페이스용 읽기 전용 **위트니스 토큰** | 수집기의 텔레그램 세션 또는 API 인증 정보 |
| 자체 Ed25519 키 및 저널 | 수집기의 보관소, 서명 키 또는 패널 토큰 |
| 자체 텔레그램 봇 토큰 | 메시지 내용: 헤더에는 기록 수와 해시가 포함됩니다. |

토큰은 **[추가 기능] → [독립 위트니스**]에서 생성되며, 한 번만 표시되고 SHA-256 형태로만 저장됩니다. 이 토큰은 정확히 하나의 엔드포인트만 열며, `GET /api/witness/head`이 엔드포인트는 갓 서명된 체크포인트와 서명된 콘텐츠가 없는 컬렉션 카운터, 운영 상태 정보를 반환합니다. 이 토큰으로는 패널을 열거나, 메시지 내용을 읽거나, 설정을 변경할 수 없으며, 해당 곳에서는 패널 토큰이 허용되지 않습니다. 같은 페이지에서 토큰을 취소할 수 있습니다. 수집기는 새로운 위트니스 키가 확인을 시작할 때(`witness.seen`) 시점을 기록하고 토큰별 마지막 확인 시점을 표시하며, 2.5 간격 내에 확인하지 않은 위트니스는 기한이 지난 것으로 표시됩니다.

새로운 증인은 각 폴링마다 무작위 챌린지를 전송하며, 캡처 문장은 수집자 서명 아래에서 이를 반영합니다. 카운터는 정확한 체크포인트에 바인딩되며 서명된 증인 게시물에 포함됩니다. 기존 헤더는 독립형 증인에 의해 계속 허용됩니다. 저널의 증가량만으로는 새로운 메시지로 간주되지 않습니다.

## 확인 및 기록 대상

지정된 간격(기본값 10분)마다 TgWitness는 다음과 같은 작업을 수행합니다:

1. 헤드 자체를 가져옵니다(수집기는 이를 푸시하거나 건너뛸 수 없습니다);
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen)，a nondecreasing count and an unchanged head at an unchanged count． Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint．Once continuity proofs have been used，removing them is rejected；
3. 자체 저널에 서명된 기록을 추가합니다: `witness.anchor` (상태 `ok`, `key_changed`, `rollback`(이전보다 기록 수가 적음), `fork`(길이는 동일하지만 헤더가 다름) 또는 `invalid`(검증에 실패함), 또는 `witness.no_response`( 수집기가 응답하지 않은 경우);
4. TgWitness가 실행 중이고 봇 API에 접속할 수 있는 동안에는 “응답 없음”을 포함하여 서명된 결과를 채널에 게시합니다. 게시물 ID(`witness.posted`)가 기록되며, 게시 실패 시에도 ID(`witness.post_failed`)가 기록됩니다.

게시물은 다음과 같은 형식을 띠며, 마지막 줄에는 서명된 진술이 포함됩니다:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Witness 실행하기

텔레그램 봇(@BotFather를 통해 생성)과, 해당 봇이 관리자로 등록된 채널, 그리고 증인이 접근할 수 있는 수집기 주소가 필요합니다. 이 주소는 사설 네트워크 외부에서 HTTPS를 통해 접속 가능해야 합니다([배포](https://phishdestroy.github.io/TgWitness/ko/docs/reference/deployment/) 안내서의 HTTPS 프로필 참조).

패널에서 **[추가 기능] → [독립 위트니스] → [구성]**을 엽니다. 다음 세 단계로 읽기 전용 액세스, 채널 및 간격 설정을 마친 후 위트니스를 실행합니다. 게시 정책, 선택 사항인 HTTP/SOCKS5 프록시 및 사용자 지정 봇 API 주소는 [**고급 설정**]에서 확인할 수 있습니다. 이 양식을 다운로드하면 `witness.json` 이 작업 공간의 수집기 키가 고정된 상태로 제공됩니다. **‘액세스 파일 저장**’을 통해 새로 생성된 읽기 전용 토큰을 다운로드한 후 `witness-token.txt`를 선택하여 새로 생성된 읽기 전용 토큰을 다운로드하세요. 이 토큰과 `bot-token.txt`위트니스 호스트에서 생성된 파일을 해당 JSON 파일 옆에 배치하십시오. 수집기는 봇 토큰을 절대 수신하지 않습니다. 다운로드를 해도 서비스가 시작되거나 메시지가 게시되지 않습니다. 호스팅된 프로젝트 위트니스는 암묵적으로 등록되지 않습니다.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

첫 번째 명령어는 네트워크 요청이나 키 생성 없이 구성 파일과 비밀 파일을 확인합니다. JSON 내의 경로는 해당 파일을 기준으로 하며, CLI/환경 경로는 작업 디렉터리를 기준으로 합니다. 호스트 외부에 위트니스 지문을 보관하십시오. 수집기의 마지막 폴링(last-poll) 표시기는 요청을 확인하는 역할만 하며, 게시 여부는 Proof를 통해 보고되거나 위트니스 저널 및 채널에서 확인됩니다.

패널이 SSH 터널 뒤에 위치하는 경우, [이 Caddy 예시를](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example) 참고하여 별도의 HTTPS 호스트 이름에서 범위가 지정된 위트니스 엔드포인트만 노출하십시오. 기본 작업 공간은 `https://witness.example.org`를 사용하며, 다른 작업 공간은 `https://witness.example.org/profiles/ID`를 사용합니다. 토큰은 여전히 필요하며, 패널 및 기타 API 경로는 해당 가상 호스트를 통해 전달되지 않습니다.

정기적으로 게시되는 체크포인트를 원하시면 `all`를 선택하세요. 5분 간격으로 기록할 경우, 워크스페이스당 하루 약 288개의 게시물이 생성됩니다. `changes`/`problems`는 일부 체크포인트를 의도적으로 게시하지 않습니다. MTProxy는 수집기의 텔레그램 클라이언트용입니다. HTTP 폴링 및 텔레그램의 HTTPS 봇 API는 각각 자체적인 직접/HTTP/SOCKS5 경로([봇 API](https://core.telegram.org/bots/api))를 사용합니다.

**컬렉터 옆에서, Docker를 사용하여**(동일한 호스트 — 독립적인 프로세스 및 키, 하지만 동일한 운영자): `.env`에 값을 입력하고 프로필을 시작합니다.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

이미지를 게재할 경우 `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`를 사용하십시오.

**타인의 서버**(진정한 독립적인 증인)**에서**: 해당 리포지토리를 복사하고, `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org`와 위의 세 가지 값을 `.env`에 설정한 다음,

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

또는 Docker 없이:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Discord에 게시하기

위트니스는 텔레그램 대신 디스코드 채널에 게시할 수 있습니다. 디스코드에서 **‘채널 편집’ → ‘통합’ → ‘웹훅’을** 열고, 웹훅을 생성한 후 URL을 복사하세요. 패널에서 2단계에서 **‘디스코드 웹훅 · 귀하의 채널’을** 선택하세요. 위트니스 호스트에서 해당 URL을 `discord-webhook.txt` 옆에 `witness.json`옆에 저장하십시오; 이 URL은 수집기로 절대 전송되지 않습니다.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

위트니스는 텔레그램 채널 또는 디스코드 웹훅 중 하나의 게시자만 가질 수 있으며, 둘 다 가질 수는 없습니다. 게시물에는 동일한 서명된 진술이 포함되며, 누구에게도 알림을 보낼 수 없습니다. 디스코드의 2,000자 제한을 초과하는 게시물은 짧은 한 줄로 대체되며, 전체 체크가 `witness-check.txt`. 각 게시물 ID는 `witness.posted`. `verify.py --channel`텔레그램 채널 내보내기만 읽을 수 있으므로, 디스코드의 경우 위트니스 저널을 보관하십시오. 여기에는 모든 체크가 포함되어 있습니다.

### 옵션

| 옵션 | 환경 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | 점검 간격: 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | 컬렉터 및 봇 API 응답 대기 시간: 5–600초 |
| `--post` | `_POST` | `all` | `all`: 모든 항목 확인; `changes`: 새로운 문제 또는 오류; `problems`: 오류만 있고 답변이 누락된 경우 |
| `--title` | `_TITLE` | `TgWitness witness` | 각 채널 게시물의 첫 문장 |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | 첫 번째 답변을 신뢰하기보다는 수집기 키를 고정하세요 |
| `--proxy` | `_PROXY` | 직접 | `socks5://host:port` 또는 `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | 봇 API 주소(예: 로컬 봇 API 서버) |
| `--data-dir` | `_DATA` | `witness-data` | Witness 키 및 저널 |
| `--config` | `_CONFIG` | – | 위의 옵션 중 하나를 포함한 JSON 파일 |

수집기 주소, 토큰 및 채널은 다음에서 가져옵니다. `--collector`, `--token` 또는 `--token-file`, `--bot-token` 또는 `--bot-token-file`, `--discord-webhook-file` 그리고 `--channel`, 또는 `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` 그리고 `_CHANNEL`, 이를 통해 프로세스 목록에서 비밀 정보가 제외됩니다.

구성 파일은 밑줄(_)이 포함된 옵션 이름과, 채널 게시물의 단어를 대체하는 `texts`를 사용합니다:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` 키: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. 명령줄이 환경 변수보다 우선하며, 환경 변수가 파일보다 우선합니다. 알 수 없는 옵션이나 텍스트 키는 무시되지 않고 메시지와 함께 위트니스를 중지시킵니다. 표현 방식은 검증에 절대 영향을 미치지 않습니다: verify.py는 모든 게시물 끝에 있는 서명된 토큰을 확인합니다. `--post changes`나 `problems`의 경우, 게시되지 않은 검사는 여전히 위트니스 저널에 남아 있으며, `verify.py`는 이를 ‘게시되지 않음’으로 나열합니다. 시작 레코드에는 정책이 명시됩니다. 모든 검사는 여전히 저널에 표시되므로, 게시 횟수가 적다는 것은 독립적인 텔레그램 전송 횟수가 적다는 것을 의미할 뿐, 검사 횟수가 적다는 것을 의미하지는 않습니다.

채널이 없어도 Witness는 여전히 로그를 보관합니다. Witness 키 지문 (`python -m tgwitness.witness fingerprint`)은 다른 곳에 보관하십시오.

## 여러 워크스페이스를 위한 공개 증명 페이지

`python -m tgwitness.proof` 한 번에 최대 32개의 워크스페이스를 처리하며, 각 워크스페이스의 최신 서명된 확인 내역을 담은 읽기 전용 페이지를 제공합니다. 모든 워크스페이스는 데이터 폴더 내에 고유한 위트니스 키와 저널, 그리고 고정된 컬렉터 키를 갖습니다. 텔레그램 채널에 게시하는 기능은 워크스페이스별로 선택 사항입니다. 다음 파일을 기준으로 시작하세요: [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| 분야 | 의미 |
| --- | --- |
| `title` | 페이지 제목, 1–100자 |
| `data_dir` | 파일과 관련된 Witness 키 및 저널; 기본값 `proof-data` |
| `interval`, `timeout` | 점검 간격(분, 1–1440, 기본값 5); 대기 시간(초, 5–600, 기본값 20) |
| `workspaces[].id`, `label` | 짧은 소문자 별명과 표시되는 이름 |
| `workspaces[].collector` | 컬렉터 주소; 다른 워크스페이스는 `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | 필수 항목이며, 워크스페이스마다 다릅니다. |
| `workspaces[].token_file` | 해당 워크스페이스의 읽기 전용 위트니스 토큰이 포함된 파일 |
| `workspaces[].channel`, `bot_token_file` | 선택 사항: 각 확인 결과를 채널에 게시하기 |
| `workspaces[].proxy`, `bot_api` | 선택적 경로 및 봇 API 주소 |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

첫 번째 명령어는 연결을 열지 않고 파일과 토큰 파일을 검증합니다. 이 페이지는 GET 및 HEAD 요청에만 응답합니다:

- `/` 모든 워크스페이스를 표시하며, 2.5 간격 동안 확인 표시가 없는 워크스페이스는 ‘유효하지 않음’으로 표시됩니다.
- `/api/proof` JSON과 동일한 결과를 반환합니다.
- `/api/proof/<id>` 최신 서명된 명세서를 다운로드합니다 (`tgwitness-public-proof-v1`): 증인 기록 번호 및 해시, 상태, 고정된 수집기 키, 체크포인트, 수집 카운터 및 채널 게시 성공 여부, 해당 워크스페이스의 증인 키로 서명됨.
- `/healthz` 워크스페이스의 모니터가 중지되면 503 오류를 반환합니다.

[Caddyfile.proof.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example)example과 같이 이 페이지에 고유한 호스트 이름을 지정하십시오. 검증을 위해 아래 설명된 대로 `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` 내보낸 후 아래 설명대로 사용하십시오.

## 확인

Witness 측에서 저널을 내보내려면:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

그런 다음, 수집기가 생성한 서명된 ZIP 파일과 텔레그램 데스크톱에서 내보낸 채널 (*채팅 기록 내보내기* → JSON 선택 시 `result.json` 가 생성됨) 또는 해당 채널의 공개 `https://t.me/s/…` 페이지를 사용하여 어디서든:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py`는 위트니스 저널(체인 및 서명)을 확인한 다음, **위트니스가 확인한 모든 헤드가 내보낸 저널의 일부인지** 검사합니다. 해당 카운트에 해당하는 기록은 정확히 해당 해시를 가져야 합니다. 일치하지 않는 헤드가 있으면 검증에 실패하며, 이는 위트니스가 확인한 후 저널이 변경되었음을 의미합니다. 또한 내보내기 후 확인된 헤더, 증인이 기록한 이상 현상, 검증에 실패한 응답, 이 내보내기 파일에 일치하는 체크포인트가 존재하는 기간("X부터 Y까지 증인 확인됨") 및 누락된 부분을 보고합니다. 이후의 체크포인트는 해당 기간을 연장하지 않습니다. 결과에는 마지막으로 일치한 레코드 번호와 일치하는 체크포인트가 없는 후속 레코드 수가 포함됩니다. 수출본 자체 키로 서명된 답변만 집계됩니다: 증인이 한 번도 본 적 없는 키로 서명된 수출본은 ‘증인 확인되지 않음’으로 보고되며, `--fingerprint`가 없는 경우 서명자는 고정되지 않은 상태로 남습니다. `--channel`를 사용할 경우, 서명된 모든 게시물은 증인 저널과 레코드 단위로 일치해야 합니다. 변경된 게시물은 검증에 실패하며, 누락된 게시물은 목록에 표시됩니다. 제공된 Telegram JSON 내보내기 파일의 날짜는 서명된 증인 토큰 외부의 편집 가능한 메타데이터입니다. 토큰이 일치한다고 해서 게시 날짜가 인증되는 것은 아니며, 결과에는 게시 시간 검증이 수행되지 않았음이 명시적으로 보고됩니다.

### 증인이 확인한 내보내기 범위 필요

증인이 확인한 최종 기록을 반드시 포함해야 하는 업무 인계 시, `--require-witness`를 추가하십시오:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

이를 위해서는 독립적으로 보관된 위트니스 지문과 이 내보내기 파일의 정확한 끝 부분에 위치한 일치하는 체크포인트가 필요합니다. 이전 접두사만 포함하는 체크포인트는 불충분합니다. 수집을 일시 중지하고, 위트니스가 최종 상태를 관찰하도록 한 뒤, 저널에 추가 기록이 이루어지기 전에 내보내십시오. 저널이 변경되면 다른 체크포인트를 보관하고 해당 상태를 내보내십시오. 후속 체크포인트만으로는 더 짧은 내보내기 파일의 최종 해시를 검증할 수 없습니다. `--channel` 플래그가 함께 제공될 경우, 주장된 게시물이 누락되었거나 일치 세트가 비어 있으면 이 엄격한 검사에 실패합니다. 플래그가 없어도 일반적인 무결성 검사에서는 여전히 증인이 없는 레코드를 보고하지만, 그 외에는 손상되지 않은 아카이브를 거부하지는 않습니다.

Keep the witness journal and its pinned key separately．Online checks verify continuity between checkpoints；offline verification compares every retained checkpoint with the export．Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification．The report lists witness downtime and failed publications by interval．
