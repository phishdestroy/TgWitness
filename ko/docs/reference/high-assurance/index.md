# 고신뢰도 배포

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/

Hetzner 또는 Phala Cloud에 구축된 24시간 연중무휴 보안 서버, 게이트웨이 DNS, 그리고 제3자가 재현할 수 있는 검증 절차.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [문서](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [배포 및 복구](https://phishdestroy.github.io/TgWitness/ko/docs/reference/deployment/)

![배포 및 복구](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

고신뢰도 배포 방식은 아카이브 검증에 수집 환경에 대한 독립적인 검증을 추가합니다. 검토자는 클라우드 제공업체와 Cloudflare가 보유한 배포 및 액세스 기록을 조회하며, Intel TDX 배포를 통해 수집기 환경에 대한 하드웨어 인증이 추가됩니다.

일반적인 로컬 및 Docker 사용 방법은 변함이 없습니다. 다음을 사용하여 배포하지 않는 한 여기에서 실행되는 것은 없습니다 `python -m tgwitness.cloud`를 사용하여 배포하지 않는 한 여기에서 실행되는 것은 없으며, 수집기는 배포가 설정된 경우에만 호스트를 읽습니다. `TGWITNESS_ASSURANCE`.

흐름도 · 운영자 → 서버, 인바운드 규칙이 없는 방화벽 (프로바이더 API); 운영자 → 터널 및 DNS (Cloudflare API); 서버, 인바운드 규칙이 없는 방화벽 → 터널 및 DNS (발신 전용); 서버, 인바운드 규칙이 없는 방화벽 → 서버에서 생성된 서명 키; Verifier, 읽기 전용 토큰 → 프로바이더 로그 및 방화벽; Verifier, 읽기 전용 토큰 → 터널 커넥터 주소 및 인그레스; Verifier, 읽기 전용 토큰 → 서명된 /api/assurance 성명서; Verifier, 읽기 전용 토큰 → 증거 ZIP · 운영자 · Verifier, 읽기전용토큰 · 서버, 인바운드규칙이없는방화벽 · 프로바이더로그및방화벽 · 터널커넥터주소및인그레스 · 서명된 /api/assurance성명서 · 증거 ZIP · 터널및 DNS · 서버에서생성된서명키 · 프로바이더 API · Cloudflare API · 발신전용

**도표를 텍스트로 변환**

1. 운영자 → 서버, 인바운드 규칙이 없는 방화벽 (프로바이더 API)
2. 운영자 → 터널 및 DNS (Cloudflare API)
3. 서버, 인바운드 규칙이 없는 방화벽 → 터널 및 DNS (발신 전용)
4. 서버, 인바운드 규칙이 없는 방화벽 → 서버에서 생성된 서명 키
5. Verifier, 읽기 전용 토큰 → 프로바이더 로그 및 방화벽
6. Verifier, 읽기 전용 토큰 → 터널 커넥터 주소 및 인그레스
7. Verifier, 읽기 전용 토큰 → 서명된 /api/assurance 성명서
8. Verifier, 읽기 전용 토큰 → 증거 ZIP

**이 페이지에서**

- [검증자가 확인할 수 있는 사항](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#what-a-verifier-can-check)
- [제공업체](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#providers)
- [Phala Cloud의 기밀 VM (Intel TDX)](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [시작하기 전에](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#before-you-start)
- [패널에서](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#from-the-panel)
- [도메인 없이 사용하는 퀵 터널](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [배포](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#deploy)
- [디버그 배포 및 잠금](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#debug-deployment-and-lock)
- [배포 제거](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#remove-a-deployment)
- [모든 서버 (자체 인증)](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#any-server-self-attested)
- [확인](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#verify)
- [증거 인계에 관한 보고서](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#report-for-evidence-handover)
- [외부 증인으로서의 Cloudflare](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [배포 결과 확인하기](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#reading-the-deployment-result)

## 검증자가 확인할 수 있는 사항

| 주장 | 검증 방법 | 관리자: |
| --- | --- | --- |
| 이 서버는 특정 시점에 제공업체 API를 통해 생성되었습니다. | 서버 객체 및 제공자의 자체 로그에서 해당 객체의 생성 | 제공자 |
| 아무도 해당 제공자의 액세스 경로를 사용하지 않았습니다. | 콘솔 요청, 복구, 비밀번호 재설정, 재구축, ISO, 이미지, 백업에 대한 로그 | 제공자 |
| 아무것도 연결할 수 없습니다 | 프로바이더 방화벽에는 인바운드 규칙이 없으며, 첫 부팅 시부터 SSH가 숨겨집니다. | 프로바이더(방화벽), 호스트(SSH) |
| 이 패널은 터널을 통해서만 접근할 수 있습니다. | 터널 인그레스는 패널로만 트래픽을 전달하며, 커넥터는 서버 주소에서 실행됩니다. | Cloudflare |
| 이 소프트웨어는 다음과 같이 실행됩니다. | 컬렉터의 서명된 소스 트리 해시는 배포된 커밋의 체크아웃과 일치합니다. | Collector, Git과 대조 확인됨 |
| 서명 키는 해당 서버에서 생성되었습니다. | 이 키는 제공자의 서버 ID와 수신한 클라우드-이니트(cloud-init)의 해시를 명시하는 진술서에 서명합니다. | Collector, 제공업체와 대조 확인됨 |
| 이 저널은 해당 키와 서버에 속합니다. | 증거 ZIP에서 시작되는 모든 프로세스에는 해당 서버에 대한 호스트 측정값이 포함됩니다. | 증거 ZIP |

수집기는 SSH 상태, 세션, 로그인 기록 및 부팅 정보를 서명된 process-start 및 `host.state` 레코드에 기록합니다. 일반 VM에서는 이러한 기록이 로컬 인벤토리 레코드이며, 검토자는 이를 공급자의 독립적인 기록과 비교합니다. 아래의 Intel TDX 배포 환경에서는 하드웨어 기반 측정값을 추가로 검증합니다.

## 프로바이더

| `--provider` | 인증 정보 | Verifier의 읽기 전용 액세스 권한 | 검증자를 위한 제공자 로그 | 다음 용도로 보관됨 |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | 동일 프로젝트의 읽기 토큰 | 서버 및 방화벽 조치 | 리소스가 존재하는 동안 |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | 읽기 전용 개인 액세스 토큰 | 드롭렛 액션 | Droplet이 존재하는 동안 |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` 읽기 전용 범위 | 계정 이벤트, 방화벽 규칙 버전 | 90일 |
| `vultr` | `VULTR_API_KEY` | 읽기 권한과 `activity_logs` 권한 | 계정 활동 로그 (메서드, 경로, 행위자) | 30일, 감사 로그 구독 시 더 긴 기간 |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail 이벤트 기록 | 90일 |
| `phala` | `PHALA_CLOUD_API_KEY` | 동일한 워크스페이스의 API 키 | 애플리케이션 개정 및 CVM 작업: Docker Compose 구성 및 환경 변경, 재시작, OS 업그레이드 | 이 애플리케이션이 존재하는 동안 |
| `generic` | 없음 | 없음 | 없음: **자체 인증** | – |

각 케이스마다 전용 프로젝트, 팀, 계정 또는 하위 계정을 사용하십시오. 그러면 검증자의 읽기 전용 액세스 권한을 통해 해당 배포 정보만 표시됩니다. 인증 정보는 `--provider-token-file` 또는 상기 변수에서 읽으며, 명령줄에서는 절대 읽지 않습니다. AWS의 경우 파일에는 지역이 저장됩니다 `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; 리전은 `--location`.

각 제공업체의 기록에 나타나지 않는 내용은 모든 보고서에 명시되어 있습니다. 요약하자면: Hetzner는 콘솔 요청을 기록합니다. 반면 DigitalOcean의 복구 콘솔, Linode의 Lish/Glish, Vultr의 웹 콘솔은 그 자체로는 기록되지 않으므로, 첫 부팅 시 루트 계정이 잠기며 콘솔 로그인 을 하려면 비밀번호 재설정이나 부팅 방식 변경이 필요하며, 이 과정은 기록됩니다. Vultr는 인스턴스를 읽을 수 있는 모든 키에 콘솔 주소를 반환하지만, 기록이나 보고서에는 이 주소가 저장되지 않습니다.

## Phala Cloud(Intel TDX)상의 기밀 가상 머신

이 `--provider phala` 수집기(collector)는 dstack이 관리하는 [Phala](https://phala.com/)Cloud상의 인텔 TDX 기밀 가상 머신에서 실행됩니다. 호스트와 Phala 직원은 해당 메모리를 읽을 수 없으며, 프로세서는 머신이 부팅된 내용을 증명하는 인증서에 서명합니다. 검증기(verifier)는 Phala의 말만 믿지 않습니다: `tgwitness.tdx` 모든 증명서를 직접, 고정된 인텔 SGX 루트 CA 수준까지, 인텔의 해지 목록 및 인텔이 서명한 플랫폼 데이터와 대조하여 확인하며, 디버깅이나 마이그레이션이 가능한 머신은 거부합니다.

| 보고서 항목 | 이 도구가 제공하는 기능 |
| --- | --- |
| `tdx_binding` | 이 증명서에는 수집자의 서명된 진술서와 이 요청의 난수 값이 포함됩니다. |
| `tdx_quote` | 인텔은 이 인증을 보증하며, 인텔이 해당 플랫폼을 최신 상태로 평가할 때만 인증이 통과됩니다. |
| `tdx_compose_hash` | dstack 이벤트 로그에서 재현된 RTMR3는 수집기가 보고하는 앱 작성 시간을 측정합니다. |
| `tdx_compose` | 이 컴포즈는 배포된 커밋의 코드가 빌드하는 것과 바이트 단위로 완전히 일치합니다. 소스 파일은 해시로 고정되어 있고, 두 이미지는 다이제스트로 고정되어 있으며, 그 외의 코드는 없습니다. |
| `tdx_identity` | 인증 정보는 배포된 애플리케이션과 인스턴스에서 제공되며, Phala의 KMS에서 발급된 키와 암호화된 디스크를 사용합니다. |
| `tdx_os` | MRTD 및 RTMR0-2는 검증기가 Dstack-TEE가 게시한 dstack OS 이미지에서 계산한 값과, CVM이 보고한 OS 이미지 해시, 그리고 QEMU가 VM의 구성(shape)에 대해 생성한 ACPI 테이블(펌웨어, 커널, initrd, 루트 파일 시스템 해시가 포함된 명령줄, 메모리, vCPU 및 장치)을 기반으로 산출된 값과 일치합니다. 개발용 이미지는 실패합니다 |

OS 이미지(약 180MB, 이 중 21MB가 보관됨)는 [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases)에서 기록 옆의 `dstack-images`로 한 번 다운로드됩니다. `--tdx-image FOLDER`는 다른 폴더나 압축 해제된 이미지를 사용하며, `--tdx-image none`는 비교 단계를 건너뜁니다. 측정은 `dstack-mr`에 이어 Dstack-TEE/dstack의 `qemu-acpi` Rust 패키지를 따릅니다. `tools/check_dstack_image.py`는 이를 QEMU 자체의 ACPI 출력 및 실제 Phala Cloud 하드웨어 인증 레코드와 비교하며, `--live`는 공개된 이미지와도 비교합니다. `--tdx-measurements`는 여전히 JSON 형식으로 제공된 MRTD와 RTMR0-2를 비교합니다.

저널에 기록된 수집기의 모든 시작에는 이러한 인증 정보가 포함되므로, `verify --evidence`는 각 시작 시점과 부팅된 OS 이미지를 확인합니다. Phala의 애플리케이션 개정판 및 CVM의 운영 내역은 제공자 로그 역할을 합니다. 배포 후 변경된 Docker Compose 구성은 보고서 심사에서 불합격 처리되며, 재시작 내역은 검토를 위해 목록에 포함됩니다.

패널에서 [**Extras]** → [**Server 24/7]** 아래의 **[Confidential virtual machine · Phala Cloud]** 를 선택하고 Phala Cloud API 키를 붙여넣으세요. 퀵 터널은 Hetzner에서와 마찬가지로 작동합니다. 명령줄에서:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` 인텔의 인증서 및 해지 목록을 인텔에서 직접 다운로드하는 대신 파일에서 읽어옵니다. 여기에서는 게이트웨이 DNS를 사용할 수 없습니다. Phala에는 발신 트래픽을 위한 제공자 방화벽이 없기 때문입니다.

### 인증서

Phala 배포의 경우 `verify --report certificate.md`는 인증서도 기록합니다: 독립형 `certificate.html`와 A4 용지 크기의 `certificate.pdf`로, 여기에는 검증 결과, 인텔 루트에서 수집기 키까지의 신뢰 체인, 일반 서버 및 고신뢰도 서버와의 비교, 공개된 이미지에서 계산된 값과 나란히 제시된 측정 결과, 각 부분을 보증하는 주체, 인텔 인증서 체인, 모든 검사 항목, 공급자 로그, 그리고 검증 과정을 재현하는 방법이 포함됩니다. JSON 보고서가 공식 기록으로 남아 있으며, 각 페이지는 이를 시각화하여 표시합니다.

이 보고서는 서명과 타임스탬프를 통해 디지털로 봉인되었으며, `certificate.seal.json` 파일과 그 옆에 있는 `.tsq`/`.tsr` 파일에 포함되어 있습니다:

| Seal | 추가된 기능 |
| --- | --- |
| 적격 전자 타임스탬프, `http://tsa.belgium.be/connect` | 벨기에 연방 정부의 공인 신뢰 서비스 제공자(FPS Policy and Support, BOSA)에서 발급한 `certificate.json`의 정확한 바이트에 대한 RFC 3161 타임스탬프. 해당 기관은 벨기에의 EU 신뢰 목록에 ‘인증된 타임스탬프 서비스’로 등재되어 있으며, 상태는 ‘승인됨’으로 표시됩니다. 2026년 10월 20일자 목록에 따른 루트(Belgium Root CA6) 및 목록 항목들은 `tgwitness/tsa_roots.py`에 고정되어 있습니다. 규정(EU) 제910/2014호 제41조에 따라, 이러한 타임스탬프는 모든 EU 회원국에서 날짜 및 시간, 그리고 데이터의 무결성 측면에서 정확한 것으로 간주됩니다. |
| RFC 3161 타임스탬프, FreeTSA | 두 번째, 독립적인 타임스탬프 |
| 검증자 서명 | 보고서의 SHA-256 및 모든 타임스탬프를 명시한 진술문에 대해, 검증자 자신의 키(`--sign-with FOLDER`, 기본값 `~/.tgwitness/verifier`)를 사용하여 Ed25519로 서명하며, PDF 파일에는 동일한 키로 서명된 서명이 포함되어 있습니다 |

`--timestamp URL`(반복 가능)는 다른 인증 기관을 선택하고, `--timestamp none`는 아무것도 선택하지 않으며, `--sign-with
none`는 인장에 서명을 하지 않습니다. `check-report`는 보고서의 해시, 검증자 서명, 신뢰할 수 있는 루트에 대한 각 타임스탬프와 그 적격 상태, 그리고 PDF의 서명을 확인합니다. EU 외부에서 적격 타임스탬프 및 보고서 전체의 법적 효력은 이를 수령하는 법원 또는 당국에 달려 있으며, 인장은 보고서가 언제 존재했는지와 변경되지 않았음을 나타냅니다.

이 검증 결과만으로는 인텔의 TDX 모듈이나 마이크로코드의 결함, 또는 메모리 버스에 대한 물리적 접근 가능성을 배제할 수 없습니다. Phala 계정의 애플리케이션을 제어하는 사람은 누구나 다른 컴포즈를 배포할 수 있으며, 이는 새로운 컴포즈 해시를 가진 새로운 리비전으로 나타납니다. 호스트는 기기의 시간 소스와 네트워크를 제어합니다.

배포, `--evidence`를 통한 검증, 재시작, OS 이미지 비교, 서명과 타임스탬프로 디지털 봉인된 인증서 및 파기 작업이 Phala Cloud 자체에서 실행되었습니다. [(2026년 11월 4일 실행) 및](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)를 참조하십시오.

## 시작하기 전에

1. Cloudflare 존, 해당 계정 ID, 그리고 **Cloudflare Tunnel Edit**, **Zone Read** 및 **DNS Edit** 권한이 부여된 API 토큰은 `--cloudflare-token-file` 또는 `CLOUDFLARE_API_TOKEN`로 제공됩니다. 검증자의 경우: **Cloudflare 터널 읽기**, **DNS 읽기**, 그리고 감사 로그의 경우 **계정 설정 읽기 권한이** 필요합니다. 도메인이 없는 [퀵 터널](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#quick-tunnel-without-a-domain)의 경우 이러한 권한이 전혀 필요하지 않습니다.
2. 전용 프로젝트에 대한 쓰기 권한이 있는 제공자 자격 증명; `lock` 다음과 동일한 방식을 사용합니다:

   - Hetzner: 읽기 및 쓰기 권한이 있는 API 토큰;
   - DigitalOcean: 쓰기 권한이 있는 개인 액세스 토큰;
   - Linode: 개인 액세스 토큰 ( `linodes`, `firewall` 및 `events` 읽기/쓰기 권한을 가진 개인 액세스 토큰;
   - Vultr: 전용 계정 또는 하위 계정의 API 키;
   - AWS: IAM 자격 증명 허용 `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` 그리고 `ec2:RevokeSecurityGroupIngress`.
3. 실행할 커밋입니다. 릴리스 태그는 `git ls-remote`; 서버는 항상 40자 길이의 커밋만 수신합니다.

## 패널에서

사용자 컴퓨터에서 **‘Extras → Server 24/7’을** 실행하면 Hetzner용 서버를 `deploy` Hetzner용 서버를 세 단계로 실행합니다: 유럽 또는 미국을 선택하고, Hetzner 토큰(읽기 및 쓰기)을 붙여넣은 다음, 패널이 해당 토큰으로 확인한 서버 유형, 월 요금, 주소 및 버전을 검토합니다. 사용자가 확인하기 전에는 아무것도 생성되지 않습니다. 패널은 각 단계를 `deploy` 보고되는 대로 각 단계를 표시한 후, 주소, 패널 토큰 및 서명 키 지문을 보여줍니다. 도메인이 없으면 서버에 [빠른](https://phishdestroy.github.io/TgWitness/ko/docs/reference/high-assurance/#quick-tunnel-without-a-domain) 터널이 생성됩니다. **‘Your servers’ → ‘Find the current address’를** 통해 재시작 후 다시 조회할 수 있습니다. 자체 도메인 아래 고정 주소를 사용하려면 **‘Optional · your own domain** ’을 열고 Cloudflare 토큰을 추가하세요(준비된 링크를 클릭하면 Zone 읽기, DNS 편집 및 Cloudflare 터널 편집이 선택됩니다).

토큰은 브라우저 탭에서 동일한 컴퓨터의 TgWitness로 전송되는 각 요청과 함께 이동하며 어디에도 기록되지 않습니다. 배포 기록, 편집된 클라우드-이니트(cloud-init), 패널 토큰 및 빠른 터널의 경우 주소 키는 `deployments/NAME` 데이터 디렉터리 내에 보관됩니다. 패널은 직접 루프백 연결을 통해 주 관리자에게만 이 기능을 제공합니다 (`127.0.0.1`, 프록시나 터널 헤더 없음); 네트워크를 통해 접속한 패널은 대신 명령어를 표시합니다. 버전은 실행 중인 패널의 릴리스 태그를 기본값으로 하며, 이는 GitHub API를 통해 확인됩니다. 위치, 서버 유형 및 가격은 Hetzner의 API에서 가져옵니다: `cpx22` 해당 서비스가 제공되는 경우, 그렇지 않으면 최소 2GB 메모리를 갖춘 가장 저렴한 x86 유형이 사용됩니다.

## 도메인 없이 사용하는 퀵 터널

`--quick-tunnel` 다음 내용을 대체합니다 `--zone`, `--cloudflare-account` 그리고 `--panel-host`; Cloudflare 계정이나 토큰은 전혀 사용되지 않습니다:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

서버에서 cloudflared는 패널로 연결되는 [빠른 터널](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)을 열어줍니다. 이 터널의 주소는 `https://….trycloudflare.com` 주소로, cloudflared 또는 서버가 재시작될 때마다 변경됩니다. 서버의 작은 서비스가 각 주소를 무작위 ntfy.sh 토픽에 게시하며, 배포 디렉토리에만 존재하는 키로 (`address-key.txt`), 그리고 ntfy.sh가 게시물을 12시간 동안 보관하므로 3시간마다 이를 반복합니다. `deploy` 및 **현재 주소를 조회하는**기능은 서명된 게시물만 허용하므로, 위조된 게시물로 인해 사용자와 패널 토큰이 타인의 주소로 전송되는 일은 없습니다. 해당 토픽은 기록에 남아 있으며 공개된 cloud-init을 통해, 이를 보유한 사람은 누구나 현재 주소를 확인할 수 있습니다. 이 주소에서는 여전히 패널 토큰을 요청합니다. 서버는 어느 쪽으로도 인바운드 포트를 유지하지 않습니다.

검증자(verifier)는 주소 키를 가지고 있지 않으며, 토픽을 읽는 누구나 해당 토픽에 게시물을 올릴 수 있습니다. 따라서 수집기(collector)는 자신의 Ed25519 키로 서명된 주소 자체도 게시하며, `verify`는 배포 기록에서 수집기 키로 서명된 가장 최신 게시물을 가져옵니다. 게시물은 게시물이 주장하는 시간이 아니라 ntfy.sh가 수신한 시간 순으로 정렬됩니다. 이 변경 이전의 수집기는 아무것도 서명하지 않으며, `verify`는 가장 최근의 게시물을 가져와 `statement` 확인 과정에서 이를 알립니다. 위조된 게시물은 해당 확인을 실패하게 만들 뿐입니다. 주소는 여전히 수집기의 키로 응답해야 하기 때문입니다.

발생하는 문제: Cloudflare 계정에는 퀵 터널에 대한 기록이 저장되지 않으므로, `verify`는 터널, 커넥터 및 DNS 확인을 사용할 수 없는 상태로 보고하며, 결과는 기껏해야 `incomplete`(Phala Cloud에서는 검사가 통과됩니다: 커넥터가 측정된 Docker Compose 구성 내에서 실행됨); 프로바이더 기록, 방화벽, 서명된 명세서, 호스트 측정 및 설치 프로그램 비교는 평소와 같이 확인됩니다. 참조 설치 프로그램과의 바이트 비교에는 이미 `--quick-tunnel`를 인식하는 배포된 커밋이 필요합니다; 0.7.0 체크아웃은 도메인 설치 프로그램을 빌드하고 차이를 보고합니다. Cloudflare는 퀵 터널에 가동 시간 보장을 제공하지 않으며, 200개의 요청만 동시에 처리할 수 있고 Server-Sent Events를 전송하지 않으므로, 패널의 실시간 업데이트(0.7.0 이후 버전)가 퀵 터널을 통해 전달되지 않을 수 있으며 페이지를 다시 불러와야 할 수 있습니다. 이 부분은 아직 테스트되지 않았습니다. 반드시 정상적으로 작동해야 하는 경우에는 자체 도메인을 사용하십시오.

## 배포

먼저 전송될 모든 내용을 확인하세요. `plan` 프로바이더나 Cloudflare에 요청을 보내지 않습니다:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

그런 다음 동일한 옵션과 인증 정보를 사용하여 배포합니다:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

시작할 때 사용할 서버 유형: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` 그리고 `--image` 각 프로바이더의 유럽 지역 Ubuntu 24.04를 기본값으로 설정합니다.

`--repository` 다른 https Git 저장소의 커밋을 가져오며, URL에 인증 정보가 포함되지 않습니다 (기본값 `https://github.com/phishdestroy/TgWitness.git`). `deploy` 또한 `--out` 다른 배포 디렉터리를 지정할 수 있습니다(기본값 `deployments/NAME`; 이미 배포가 포함된 디렉터리는 거부됩니다) 및 `--wait`, 수집기의 서명된 진술서를 기다리는 시간(분): 1~240, 기본값 20, 또는 60 `generic`.

명령어:

1. Cloudflare 터널을 생성하여, 인그레스가 패널 호스트명을 패널로 전달하고, 지정된 경우 위트니스 호스트명을 `/api/witness/head` 그리고 `/api/assurance` 해당 호스트명으로만 전달합니다;
2. 해당 호스트 이름에 대해 프록시된 CNAME 레코드를 생성하며, 이미 존재하는 이름은 거부합니다;
3. 인바운드 규칙이 없는 프로바이더 방화벽을 생성하고, 그 뒤에 SSH 키, 백업, 콘솔 에이전트가 없으며, SSH를 숨기고 루트 권한을 잠그며, `cloudflared`, 정확히 해당 커밋을 가져와 확인한 후 TgWitness를 보안 강화된 systemd 서비스로 시작합니다;
4. 수집자가 서명한 진술서를 기다린 후, 해당 진술서에 이 서버와 이 cloud-init의 해시 값이 명시되어 있는지 확인합니다.

`deployments/case-2026-11/` 다음과 같은 내용을 포함합니다:

| 파일 | 목차 | 공유하시겠습니까? |
| --- | --- | --- |
| `deployment.json` | ID, 해시, 수행된 API 호출(메서드, 경로, 상태) 및 첫 번째 서명된 문장 | 네, 검증기를 사용하면 가능합니다. |
| `cloud-init.redacted.yaml` | 두 개의 시크릿이 다음과 같이 대체된 정확한 cloud-init은 `REDACTED` | 네 |
| `panel-token.txt` | 패널 토큰 | 아니요 |

프로바이더의 루트 비밀번호, 터널 토큰 및 패널 토큰은 절대로 `deployment.json`. 마지막에 출력된 수집기 지문을, 본인이 단독으로 관리하지 않는 채널(예: 증인 채널 또는 수신자에게 보내는 메시지)을 통해 게시하십시오.

Telegram에 로그인할 때는 `https://case.example.org` 에서 [계정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/accounts/)가이드에 설명된 대로 패널 토큰을 사용하여 텔레그램에 로그인하십시오. 패널 작업은 서명된 저널에 기록되며, 이는 SSH 세션이 아닙니다. [증인은](https://phishdestroy.github.io/TgWitness/ko/docs/reference/witness/) 폴링할 수 있습니다 `https://case-witness.example.org`.

SSH는 지원되지 않습니다. 부트스트랩에 실패하면 수집기는 응답하지 않습니다. 서버를 삭제하고 다시 배포하거나, 디버그 배포를 사용하여 원인을 파악하십시오.

### 사용자 데이터에 포함된 비밀 정보

cloud-init에는 패널 토큰과 Cloudflare 터널 토큰이라는 두 가지 비밀 정보가 포함됩니다. 서명 키는 여기에 포함되지 않으며, 서버에서 생성됩니다. Hetzner, DigitalOcean 및 Linode는 API를 통해 사용자 데이터를 반환하지 않습니다. Vultr는 인스턴스를 읽을 수 있는 모든 키에 데이터를 반환하며, EC2는 `DescribeInstanceAttribute`. AWS의 경우 검증자에게 표에 나열된 세 가지 작업만 제공하고, 절대로 `ec2:Describe*`. Vultr의 경우, 검증자의 키가 두 토큰 모두를 읽을 수 있다고 가정하십시오. 터널 토큰을 사용하면 누군가가 두 번째 커넥터를 실행할 수 있습니다: `verify` 서버에 없는 모든 커넥터를 보고하며, 각 커넥터가 새로운 챌린지에 서명하기 때문에 수집기의 진술은 그런 방식으로 위조될 수 없습니다. `--quick-tunnel` 두 번째 비밀은 주소 키입니다: 이를 읽는 사람은 패널이 수용할 허위 주소를 게시할 수 있습니다.

수집자가 발표한 공개 성명에는 서버 주소와 로그인 출처가 생략되어 있으나, 이 두 가지 정보는 모두 서명된 일지에 기록되어 있습니다.

## 디버그 배포 및 잠금

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` 단일 주소 또는 소규모 네트워크(IPv4의 경우 최대 /24, IPv6의 경우 최대 /48)에서 생성된 하나의 키에 대한 SSH를 유지합니다. 이 키는 이미 제공업체에 등록되어 있어야 합니다: Hetzner 프로젝트 내 SSH 키의 이름 또는 ID, DigitalOcean 팀 내 SSH 키의 ID 또는 지문, 프로필에 SSH 키가 추가된 Linode 사용자 이름. `KEY` 이미 다음 제공업체에 등록되어 있습니다: Hetzner 프로젝트 내 SSH 키의 이름 또는 ID, DigitalOcean 팀 내 SSH 키의 ID 또는 지문, 프로필의 SSH 키가 root에 추가된 Linode 사용자 이름, Vultr 계정 내 SSH 키의 ID, 또는 해당 리전의 EC2 키 쌍 이름. 이러한 옵션은 `generic`에는 적용되지 않습니다. 이러한 배포는 `debug` 로 기록되며, 고신뢰도로 보고되지 **않습니다**. 작업이 완료되면 `sudo tgwitness-lock` 를 마지막 SSH 세션의 마지막 명령어로 실행한 다음, 다음을 수행하십시오:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

방화벽은 모든 인바운드 규칙을 제거합니다. 그러면 보고서를 통해 SSH가 허용되었던 시점과 차단되었던 시점이 표시되며, 해당 창은 계속 표시된 상태로 유지됩니다.

## 배포 제거

`destroy` 배포 라벨을 통해 식별된 서버와 해당 방화벽을 삭제하여, 도중에 실패한 배포도 함께 제거한 다음, 해당 터널을 가리키는 DNS 레코드와 터널을 삭제합니다. 서버의 저널과 서명 키도 함께 삭제되므로, 먼저 증거를 내보내야 합니다. 기록은 삭제된 것으로 표시된 채로 남아 있으며 `removed`, 제거에 사용된 API 호출과 함께 표시됩니다.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Hetzner의 경우 API를 통한 삭제 기능이 구현되어 있습니다. 다른 제공업체의 경우 `destroy` 는 데이터를 삭제하기 전에 일시 중지되며, 제공업체 콘솔에서 삭제할 레이블 이름을 지정합니다. 수동으로 설치된 서버(`generic`)의 경우 터널 및 DNS 레코드만 삭제됩니다. 빠른 터널 배포에는 Cloudflare 토큰이 필요하지 않습니다. 이 터널은 서버에서 종료되며, 게시물은 ntfy.sh에서 12시간 이내에 만료됩니다.

## 모든 서버(자체 인증)

`--provider generic` 는 직접 구매하거나 수동으로 설치한 서버용입니다. `deploy` 터널을 생성하고 DNS를 설정하며, `install.sh` (비공개) 및 `install.redacted.sh` (게시용)을 작성한 후 대기합니다. 이 파일을 `install.sh` 방금 설치한 Ubuntu 24.04 서버에 복사한 후 그곳에서 실행하세요:

```
sudo bash install.sh
```

이 도구는 호스트의 현재 상태(로그인, 계정, `authorized_keys`, 수신 소켓, 서비스, 예약된 작업, 패키지)를 기록하고, 커밋을 설치하며, 호스트 방화벽을 활성화하고, 자신을 삭제하며, SSH를 마스킹하고 세션을 종료합니다. 이러한 서버에 대한 보고서는 기껏해야 **‘자체 인증(SELF-ATTESTED)’** 수준입니다. 즉, 설치 프로그램을 실행한 사람은 그 전에 이미 루트 권한을 가지고 있었으며, 검증자에게는 제공자 기록이 제공되지 않습니다. 하지만 이는 설명되지 않은 서버보다는 여전히 낫습니다. 인벤토리, 설치 프로그램 해시 및 이후의 모든 로그인이 서명되어 있기 때문입니다.

## 확인

검증자는 `deployment.json`, 공개된 설치 프로그램, 읽기 전용 인증 정보, 그리고 가급적이면 해당 커밋의 체크아웃 및 증거 자료 ZIP가 필요합니다:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

모든 제공업체 및 Cloudflare 값은 해당 시점에 검증자가 요청하며, 기록은 질문할 ID만 제공합니다. 종료 코드는 **PASS의** 경우 0, **FAIL의** 경우 1, **REVIEW**, **INCOMPLETE** 또는 **SELF-ATTESTED의** 경우 2입니다. `--fingerprint` 이는 독립적인 채널에서 제공되어야 하며, 그렇지 않을 경우 키는 운영자의 기록과만 비교됩니다. `python verify.py` 여전히 ‘증거([Evidence)’](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/) 섹션에서와 같이 증거 ZIP 자체를 검증합니다.

프로바이더 작업은 다음과 같이 분류됩니다: 생성 및 생성 후 30분 이내의 시작 작업은 통과; 콘솔, 복구, 비밀번호 재설정, 재구축, ISO, 이미지, 스냅샷, 백업, 시스템 관리자, EC2 인스턴스 연결 및 방화벽 개방은 실패; 전원 관련 작업 및 예상치 못한 모든 작업은 검토 대상으로 표시됩니다. 알 수 없는 작업은 절대 무사통과되지 않습니다.

## 증거 인계를 위한 보고서

`--report report.md` 마크다운 보고서를 작성하고 `report.json` 그 옆에는:

1. 결과, 수집기 키 지문, 배포, 제공자, 커밋, 서버, 방화벽, 터널;
2. 각 확인 항목과 그 상태 및 출처(프로바이더 API, Cloudflare API, 수집기 명세서, 증거 일지);
3. 각 작업에 대한 평가와, 제공자가 기록한 경우 행위자가 포함된 제공자 로그;
4. 터널의 연결, 구성 및 감사 로그를 보관하는 Cloudflare 엔드포인트;
5. 서명된 수집자 진술서;
6. 이 보고서가 입증하는 내용과 입증하지 않는 내용;
7. 이를 재현하기 위한 명령어와, 제공된 모든 파일의 SHA-256.

보고서, `report.json`, `deployment.json`, 공개된 설치 프로그램 및 증거 자료ZIP를 전달하십시오. 보고서는 조기에 작성하십시오: 서비스 제공자의 로그 기록은 제한된 기간 동안만 보관됩니다.

## 외부 증인으로서의 Cloudflare

여기에 있는 모든 기능은 선택 사항입니다. Cloudflare 계정이 없어도 서버는 정상적으로 작동하며, 현재 다음 두 가지 기능이 작동합니다:

| 무엇 | 이 도구가 제공하는 기능 | TgWitness에서 |
| --- | --- | --- |
| 퀵 터널 또는 사용자 도메인 터널 | 이 패널은 터널을 통해서만 접근할 수 있습니다. | 서버 마법사, 위 참조 |
| drand 릴레이 `drand.cloudflare.com` | drand 라운드 이후의 기록들은 이 문서보다 최신입니다. 이 일지는 진행 상황에 따라 작성되었습니다. | 증거 모드, **추가 증인**, 계정 없음 ([형식](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| 터널 상태 알림 | 터널이 중단되었을 때, 이메일 또는 Cloudflare의 웹훅을 통해 알림이 전송됩니다. | Cloudflare 대시보드에서 이를 설정하세요. |
| 게이트웨이 DNS(`--gateway-dns`, 또는 마법자 내의 **Cloudflare Gateway DNS**) | 서버가 조회한 모든 이름에 대해 Cloudflare가 TLS를 통해 응답했으며, Hetzner 방화벽은 DNS가 다른 어떤 곳에도 접근하지 못하도록 차단하고 있습니다. 게이트웨이 정책이 응답 내용을 재작성할 수 있는지 여부 | Hetzner, 무료 제로 트러스트(Zero Trust) 요금제, 도메인 없음; `verify` 방화벽, 위치, 로깅, 정책, 서버 쿼리 및 감사 로그를 확인하며, 증거 모드는 로그를 저널로 복사합니다. |
| 서버에 Cloudflare One 클라이언트가 설치된 게이트웨이로, Cloudflare로만 연결을 허용하는 아웃바운드 방화벽입니다. | DNS뿐만 아니라 서버가 수행한 모든 연결 | 아직 구현되지 않음 |
| 패널 앞쪽에서 액세스 | 패널에 누가 언제 로그인했는지 | 구현되지 않음: 자체 도메인이 필요합니다 |
| SSH 명령어 로깅 | 디버그 세션의 각 명령어 | 아직 구현되지 않음 |

Cloudflare의 자체 사본을 R2에 보관하는 Logpush는 엔터프라이즈 기능입니다. 무료 요금제의 경우 Cloudflare는 `logpush is not enabled for this account`. 게이트웨이 로그는 24 시간 동안 보관되므로, 증거 모드는 이를 서명된 저널(**Cloudflare 게이트웨이의 이 서버 DNS 쿼리 로그로**, ‘계정 분석 읽기’ 권한이 있는 읽기 전용 토큰)로 복사합니다.

제로 트러스트(Zero Trust) 계획이 없으면 계정당 하나의 DNS 위치가 할당됩니다. Cloudflare가 다른 위치를 거부할 경우, 서버는 기존 위치를 공유하며, 해당 서버의 쿼리는 주소를 통해 구분됩니다. 이 필터 역시 제로 트러스트 PII 읽기 권한이 필요하며, `destroy` 공유된 위치를 남기게 됩니다. 하나의 로그 쿼리는 최대 3시간 동안 지속되므로, 복사본을 통해 `verify` 3시간 단위로 하루를 나누어 읽어야 합니다.

Gateway DNS는 시스템 리졸버를 담당합니다. 443번 포트를 통해 다른 리졸버로 전송되는 HTTPS 기반 DNS 및 어디에서도 조회되지 않은 주소(예: 텔레그램 데이터 센터)로의 연결은 이 로그에 기록되지 않습니다.

Cloudflare는 텔레그램의 암호화 내부, 해당 텔레그램 계정에 연결된 다른 기기들 (증거 모드의 기기 목록은 텔레그램 측에서 이를 기록합니다) 또는 제공업체의 하이퍼바이저를 볼 수 없습니다.

## 배포 결과 확인하기

일반적인 VM의 경우, 제공자가 호스트 인프라를 관리하며, 로컬 인벤토리는 제공자 기록과 함께 확인됩니다. Intel TDX의 경우, 검증자는 추가로 하드웨어 견적, 수집기 바인딩, 컴포즈 및 OS 측정값을 확인합니다. 개별 결과를 확인하여 어떤 검사가 통과되었는지, 또는 사용할 수 없었는지 확인하십시오.

과거 방화벽 세부 정보는 제공업체에 따라 다르며, Linode는 규칙 버전을 보관합니다. [검증 기록](https://phishdestroy.github.io/TgWitness/ko/docs/reference/verification/)에는 테스트된 배포 환경과 남아 있는 실시간 점검 항목이 나열되어 있으며, [검증 범위는](https://phishdestroy.github.io/TgWitness/ko/docs/reference/evidence/#verification-scope) 이러한 환경 점검을 아카이브 수집 및 무결성과 연결합니다.
