# สิ่งที่ได้รับการทดสอบแล้ว

Canonical page: https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/

การทดสอบ Telegram แบบเรียลไทม์ การตรวจสอบอัตโนมัติ การตรวจสอบผ่านเบราว์เซอร์ และสิ่งที่ยังไม่ได้รับการยืนยัน

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [เอกสารประกอบ](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/th/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | ผลลัพธ์ | ขอบเขต |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | บันทึก | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| ตรวจสอบ | ผลลัพธ์ | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## การปรับใช้ Phala Cloud แบบสด · 4 พฤศจิกายน 2026

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| การตั้งค่า | Recorded value |
| --- | --- |
| ผู้ให้บริการ | Phala Cloud · `tdx.small` · US-WEST-1 |
| การติดตั้ง | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

การปรับใช้สองครั้งแรกพบความแตกต่างห้าจุดจาก Phala Cloud ที่จำลอง [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) ตอนนี้สามารถจำลองความแตกต่างแต่ละจุดได้ และล้มเหลวหากไม่มีการแก้ไข:

| บน Phala Cloud | ก่อนการแก้ไข | แก้ไข |
| --- | --- | --- |
| `compose_file.name` เป็นสิ่งจำเป็น | HTTP 422, ไม่มีการสร้างอะไรเลย | การกำหนดค่า Docker Compose ระบุชื่อ CVM |
| เว้นแต่จะกำหนดค่าว่าง Phala จะเพิ่มสคริปต์ก่อนการเริ่มต้นของตัวเองเข้าไปใน app-compose ที่ถูกวัด (v0.0.20: การเข้าสู่ระบบ Docker, `docker compose pull`, รหัสผ่าน root, คีย์ SSH จาก `user_config`) | `tdx_compose` ล้มเหลว: มีโค้ดอยู่นอกการกำหนดค่า Docker Compose ที่เผยแพร่ | app-compose ตั้งค่า `pre_launch_script` เป็น `""`; Phala จึงไม่รวมมันเข้าไป |
| หากไม่ใช้ `image` Phala จะเลือก `dstack-dev-0.5.12` ซึ่งเป็นเวอร์ชันพัฒนา พร้อมเปิดการเข้าถึง SSH | `server_state` ไม่ผ่าน. ในภาพนี้ มีเพียงบันทึกการรับรองฮาร์ดแวร์เท่านั้นที่ผ่าน; มีเพียงบันทึกผู้ให้บริการและ `tdx_os` ที่แสดงผลนี้ | การปรับใช้ต้องการเวอร์ชัน production build ของ Phala ในรุ่นปัจจุบัน คือ `dstack-0.5.12` |
| เมื่อปิด dstack gateway แล้ว รายละเอียด CVM จะไม่ได้รับรหัส `instance_id` | การปรับใช้รอ 30 นาทีแล้วล้มเหลว | ID ของอินสแตนซ์ถูกอ่านจากสถานะของ CVM |
| การรีสตาร์ท การหยุด และการเริ่มต้น เป็นกระบวนการของ CVM ไม่ใช่การปรับปรุงแอปพลิเคชัน | `provider_actions` ไม่ได้แสดงการรีสตาร์ท | การดำเนินการเหล่านี้ยังรวมถึงการอ่านด้วย |

**Deployment 3 · attestation, access checks and restart evidence**

- CVM ได้เรียกใช้ `dstack-0.5.12` โดยปิดการเข้าถึง SSH ผู้รวบรวมได้โพสต์ที่อยู่ที่มีลายเซ็นประมาณ 1.5 นาทีหลังจากการสร้าง จากนั้นการปรับใช้ได้ผ่าน `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, บันทึกการรับรองฮาร์ดแวร์ v4, FMSPC `20a06f000000`, ไม่อยู่ในโหมดดีบัก, ไม่สามารถย้ายได้, รองรับข้อมูลการตรวจสอบทางเข้ารหัส ที่ดึงมาจาก Intel), `tdx_compose_hash`, `tdx_compose` (ไบต์ต่อไบต์) และ `tdx_identity` (กุญแจ KMS).
- แผงควบคุมที่ที่อยู่ trycloudflare.com ตอบกลับด้วยรหัส 401 เมื่อไม่มีโทเค็นหรือใช้โทเค็นผิด, และตอบกลับด้วยรหัส 200 เมื่อใช้โทเค็นของแผงควบคุม
- `verify` โดย `--source` ถูกตั้งค่าเป็นอาร์ไคฟ์ของ GitHub สำหรับการคอมมิต และลายนิ้วมือถูกส่ง แยกกัน: เซิร์ฟเวอร์, `server_state`, ไฟร์วอลล์ (ไม่มีเกตเวย์, ไม่มีจุดสิ้นสุดสาธารณะ), บันทึกของผู้ให้บริการ, ใบแจ้งยอด, ลายนิ้วมือ, แฮชแหล่งที่มา, การบูต และการตรวจสอบ `tdx_*` ทั้งห้าผ่าน Cloudflare และ `tdx_os` ไม่สามารถใช้งานได้ ดังนั้นผลลัพธ์จึงเป็น INCOMPLETE.
- การรีสตาร์ทสองครั้งผ่าน API ของ Phala: ทุกครั้งที่ CVM กลับมาทำงานภายในเวลาไม่ถึงสองนาทีด้วย กุญแจผู้รวบรวมเดียวกัน ที่อยู่ใหม่ที่ลงนามแล้ว และที่อยู่เดิมที่ตอบกลับด้วยรหัส 530 `verify` รายงาน การบูตใหม่และทั้งสองครั้งการรีสตาร์ทเป็น REVIEW ด้วย `--evidence` ได้ยืนยันลายเซ็น ในบันทึกและสามครั้งการเริ่มต้นระบบ แต่ละครั้งมีบันทึกการรับรองฮาร์ดแวร์ Intel TDX ของตัวเองจาก CVM เดียวกัน
- `destroy` ได้ลบเฉพาะ CVM นั้นเท่านั้น พื้นที่ทำงานจึงว่างเปล่า และที่อยู่ของแผงควบคุมหยุด ตอบสนอง
- การตรวจสอบราคาของตัวช่วยสร้างในแผงควบคุมแสดง `tdx.small` ที่ $0.058 ต่อชั่วโมง หากใช้คีย์ผิด จะได้รับข้อความธรรมดา "ไม่ยอมรับคีย์ API"

**Follow-up fixes · signed address discovery and OS measurements**

- หากไม่มีกุญแจที่อยู่ `verify` จะติดตามโพสต์ที่จัดรูปแบบถูกต้องล่าสุดในหัวข้อที่อยู่ ซึ่งถูกพิมพ์ไว้ในเอกสารกำหนดค่า Docker Compose ที่เผยแพร่แล้ว โพสต์ปลอมหนึ่งรายการได้ส่งมันไปยังโฮสต์ที่ ไม่มีอยู่จริง และ `statement` ล้มเหลว: ผู้ปลอมแปลงไม่สามารถปลอมตัวเป็นผู้รวบรวมได้ แต่สามารถบล็อก การตรวจสอบจากฝ่ายที่สาม ได้นานถึง 12 ชั่วโมง ด้วยเวลาประทับที่ปลอมแปลงไว้ล่วงหน้า ผู้รวบรวมข้อมูลตอนนี้ ยังโพสต์ที่อยู่ของตนเองที่ลงนามด้วยกุญแจของตัวเองด้วย `verify` จะรับเฉพาะโพสต์ประเภทนี้เมื่อ ผู้รวบรวมข้อมูลเป็นผู้สร้างขึ้น และโพสต์จะถูกจัดเรียงตามเวลาที่ ntfy.sh รับข้อมูล [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) เล่นซ้ำโพสต์ที่ถูกปลอมแปลง CVM จะรันสิ่งนี้เฉพาะจาก commit ที่มีมันอยู่เท่านั้น ดังนั้นผู้เก็บรวบรวมในรอบนี้ยังไม่ได้ลงนามที่อยู่ของตัวเอง และ `verify` ได้แจ้งเรื่องนี้
- `tdx_os` ไม่สามารถทำงานได้โดยไม่มี `dstack-mr` ซึ่งเวอร์ชันปัจจุบันมี `measure-os` แทนที่จะเป็น `measure --json` ตามที่ระบุในเอกสารคู่มือ ผู้ตรวจสอบจะคำนวณ MRTD และ RTMR0-2 ด้วยตัวเอง จากภาพที่เผยแพร่และรูปทรงของ VM รวมถึงตาราง ACPI

**Deployment 4 · all 16 checks, report seals and restart verification**

- Deploy ได้ดาวน์โหลด `dstack-0.5.12` ที่เผยแพร่มาหนึ่งครั้ง เปรียบเทียบกับค่าแฮชของภาพระบบปฏิบัติการที่ CVM รายงาน และ `tdx_os` ผ่านการตรวจสอบ: MRTD, RTMR0, RTMR1 และ RTMR2 เท่ากับค่าที่คำนวณสำหรับ QEMU 8.2.2, 1 vCPU และ 2 GiB การคำนวณเดียวกันให้ค่า RTMR0 ที่ต่างออกไปสำหรับกรณีที่ระบุ 4 GiB, 2 vCPUs, QEMU 9.2.1 หรือการ์ดเครือข่ายใบที่สอง และล้มเหลวสำหรับเคอร์เนลที่เปลี่ยนแปลง, เฟิร์มแวร์ หรือบรรทัดคำสั่ง และสำหรับภาพระบบปฏิบัติการสำหรับการพัฒนา
- `verify` ผ่านการตรวจสอบทั้ง 16 ขั้นตอนได้ทั้งหมด รวมถึงตัวเชื่อมต่อของ quick tunnel ด้วย ดังนั้นผลลัพธ์ จึงเป็น PASS. มันได้สร้างใบรับรองในรูปแบบ HTML และ PDF ซึ่งได้รับการปิดผนึกดิจิทัลด้วยลายเซ็นและตราประทับเวลา พร้อมด้วยตราประทับเวลา eIDAS ที่ได้รับการรับรองจาก หน่วยประทับเวลา TSU 202301 ของรัฐบาลเบลเยียม (สถานะได้รับการอนุมัติในรายชื่อที่เชื่อถือได้ ของเบลเยียม), ตราประทับเวลา FreeTSA และลายเซ็นของผู้ตรวจสอบ; `check-report` ได้ยืนยันทั้งหมด รวมถึงลายเซ็นในไฟล์ PDF ด้วย
- หลังการรีสตาร์ท `verify --evidence` ยืนยันการเริ่มต้นสองครั้ง โดยแต่ละครั้งมาพร้อมกับการรับรองฮาร์ดแวร์ที่สร้างขึ้นภายใน CVM และแต่ละครั้ง ถูกบูตจาก `dstack-0.5.12` ที่เผยแพร่แล้ว; การรีสตาร์ทและการบูตใหม่ได้รับการจัดประเภทเป็น REVIEW.
- `destroy` ทำให้พื้นที่ทำงานว่างเปล่า

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- ผู้รวบรวมได้โพสต์ที่อยู่ของตนที่ลงนามด้วยกุญแจของตนเอง ติดกับโพสต์ HMAC ของผู้ดำเนินการ จากนั้นมีโพสต์ปลอมสองรายการถูกเพิ่มเข้าไปในหัวข้อ หนึ่งรายการมี HMAC เป็นศูนย์ และอีกหนึ่งรายการลงนามด้วยกุญแจ Ed25519 อื่น ทั้งสองรายการอ้างถึงเวลาในปี 2096 `verify` นำที่อยู่ซึ่งลงนามด้วย กุญแจของผู้รวบรวมข้อมูล และผ่านการตรวจสอบทั้ง 16 ขั้นตอน; ตราประทับนั้นยังคงมีตราประทับเวลาของเบลเยียมที่ได้รับการรับรอง, ตราประทับเวลาของ FreeTSA และลายเซ็นของผู้ตรวจสอบ, และ `check-report` ได้ยืนยันข้อมูลเหล่านั้น
- หลังการรีสตาร์ท คอลเลกเตอร์ได้โพสต์ที่อยู่ใหม่ที่ลงนามแล้ว: `verify` ค้นพบมันทันที ส่วน **ของผู้ดำเนินการ ค้นหาที่อยู่ปัจจุบัน** 27 วินาทีต่อมาจากการโพสต์ HMAC และทั้งสองต่างเพิกเฉย ต่อการโพสต์ที่ถูกปลอมแปลง `verify --evidence` ยืนยันการเริ่มต้นสองครั้งจาก `dstack-0.5.12`
- Deploy แสดงราคาที่ Phala คิดค่าบริการสำหรับ CVM รวมถึงค่าดิสก์: $0.06078 ต่อชั่วโมง

### Panel wizard and remaining scope

ตัวช่วยสร้างแผงควบคุมได้ทำงานกับ Phala Cloud สองครั้ง ครั้งหนึ่งผ่าน API งาน และครั้งหนึ่งผ่าน เบราว์เซอร์ด้วย Chromium จริง: การตรวจสอบราคา, การสร้างพร้อมการ commit ภายใต้ **Advanced**, การตรวจสอบการรับรองทั้งหก ผ่านทั้งหมด, รายการเซิร์ฟเวอร์แสดงราคาที่เรียกเก็บ (44.37 USD ต่อเดือน), **Find ที่อยู่ปัจจุบัน**, การดาวน์โหลดการกำหนดค่า Docker Compose ที่วัดได้ และการลบออก เบราว์เซอร์ไม่พบข้อผิดพลาดของหน้าเว็บ ทุกครั้งหลังจากนั้น พื้นที่ทำงานจะว่างเปล่า

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | นับ |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| ตรวจสอบ | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## การทดสอบ Telegram แบบสด, บัญชีทั้งหมด · 29 ตุลาคม 2026

บัญชีเดียวกันนี้ยังคงทำงานต่อไปหลังการทดสอบด้านล่างนี้ เมื่อวันที่ 29 ตุลาคม เวลา 12:10 UTC ขอบเขต ของบัญชีได้ถูกเปลี่ยนเป็นทั้งบัญชี (ช่อง, กลุ่ม, การสนทนาส่วนตัว และบอท); แผงควบคุมได้ ขอการยืนยัน และบันทึกที่มีลายเซ็นได้บันทึกการดำเนินการนี้ไว้ จนถึงเวลา 17:59 UTC บันทึกดังกล่าวมีข้อมูลดังต่อไปนี้:

| บันทึกไว้ระหว่างวันที่ 27 ตุลาคม เวลา 21:36 ถึงวันที่ 29 ตุลาคม เวลา 17:59 UTC | นับ |
| --- | --- |
| บันทึกในสมุดบันทึก | 9,968 |
| ข้อความใหม่ | 5,308 |
| ของบัญชีเหล่านั้นหลังจากเปลี่ยนไปใช้บัญชีทั้งหมด | 3,878 |
| การลบ | 784 |
| ในจำนวนนั้นถูกลบไปหลังจากที่ TgWitness ได้บันทึกข้อความไว้แล้ว | 596 |
| การแก้ไข | 41 |
| ข้อความที่เพิ่มจากการตรวจสอบซ้ำ | 2,273 |
| ข้อความที่การตรวจสอบซ้ำไม่สามารถค้นพบได้อีก | 18 |
| ข้อความที่บันทึกไว้ผ่านภาพถ่ายประวัติ | 242 |
| ไฟล์แนบที่เก็บไว้ | 247 |
| Collector เริ่มทำงาน | 19 |
| Telegram FloodWait หยุดชั่วคราว | 26 |

- เครื่องมือ **Verify** ของคณะกรรมการได้ยืนยันลายเซ็นและโซ่แฮชของบันทึกทั้ง 9,968 รายการ
- ข้อความมาจาก 2 กลุ่มหรือช่อง และ 3 การสนทนาส่วนตัวและบอต ปุ่มส่งข้อความหนึ่งถูก กดจาก**ส่วนสนทนา**; คำขอและคำตอบของ Telegram อยู่ในบันทึกหลักฐาน
- การสนทนาใหม่จะถูกเพิ่มเข้ามาเมื่อเครื่องมือเก็บข้อมูลสแกนบัญชีใหม่หลังจากรีสตาร์ท การบันทึก ข้อความเก่าของการสนทนาใหม่ถูกปิด (`history = 0`) ดังนั้นจึงไม่ถูกกล่าวถึงในส่วนนี้

ไม่รวม: ปฏิกิริยา, การเปลี่ยนแปลงสมาชิก, โปรไฟล์บุคคล, การส่งข้อความ, การเข้าร่วมผ่าน คำเชิญ, ตัวแทน (proxy), การแจ้งเตือน, บอท Witness และการจัดการหลายบัญชีพร้อมกัน ไฟล์สาธารณะ มีเพียงข้อมูลจำนวนเท่านั้น

## ไฟล์ส่งออกที่ได้รับการป้องกันด้วยรหัสผ่าน เปิดด้วย libarchive · 29 ตุลาคม 2026

ไฟล์เก็บถาวรที่สร้างขึ้นโดยรหัสการเข้ารหัสการส่งออก (WinZip AES-256, รูปแบบที่ 7-Zip และ WinRAR สามารถอ่านได้) ได้ถูกเปิดด้วย Windows `tar` (bsdtar 3.6.2, libarchive). เมื่อใช้รหัสผ่านที่ถูกต้อง ไฟล์ที่สกัดออกมาตรงกับ SHA-256 ของต้นฉบับ; หากใช้รหัสผ่านผิด ระบบจะปฏิเสธด้วยข้อความ "Incorrect passphrase". 7-Zip และ WinRAR เองไม่ได้ถูกเรียกใช้

## การทดสอบ Telegram แบบสด · 27 ถึง 29 ตุลาคม 2026

บัญชี Telegram จริงหนึ่งบัญชี ซึ่งลงชื่อเข้าใช้ผ่านกลุ่มคู่ API ที่มาพร้อมระบบ ได้บันทึก กลุ่มใหญ่หนึ่งกลุ่ม ตั้งแต่วันที่ **27 ตุลาคม เวลา 21:36 UTC จนถึงวันที่ 29 ตุลาคม เวลา 05:15 UTC** เครื่องมือเก็บข้อมูลนี้ ถูกเปิดใช้งาน 12 ครั้งในช่วงเวลาดังกล่าว

| บันทึก | นับ |
| --- | --- |
| บันทึกในสมุดบันทึก รวมถึงข้อมูลการตรวจสอบสถานะการทำงาน (heartbeats) และบันทึกการให้บริการ | 2,385 |
| ข้อความใหม่ | 1,291 |
| การลบ | 472 |
| ในจำนวนนั้นถูกลบไปหลังจากที่ TgWitness ได้บันทึกข้อความไว้แล้ว | 347 |
| การแก้ไข | 12 |
| ข้อความที่พลาดไปขณะหยุดทำงาน ถูกเพิ่มเข้ามาจากการตรวจสอบซ้ำ | 12 |
| ไฟล์แนบที่เก็บไว้ | 17 |
| ไฟล์แนบไม่ถูกดาวน์โหลด (การดาวน์โหลดถูกปิด หรือไม่มีไฟล์ที่จะดาวน์โหลด) | 14 |
| Telegram FloodWait จะหยุดชั่วคราว 3 วินาทีต่อครั้ง ระหว่างการตรวจสอบซ้ำ | 8 |

- ลายเซ็นและโซ่แฮชของบันทึกทั้งหมด 2,385 รายการสามารถตรวจสอบความถูกต้องได้กับ กุญแจสาธารณะของสมุดบันทึก
- หลังจากรีสตาร์ท ตัวเก็บข้อมูลจะดำเนินการต่อจากสถานะการอัปเดตที่บันทึกไว้ (`pts`) และ Telethon จะทำการอัปเดตให้ทัน; การตรวจสอบซ้ำจะเพิ่มข้อความที่ยังขาดอยู่
- ในทุกครั้งของ FloodWait ตัวเก็บข้อมูลจะรอตามเวลาที่ร้องขอแล้วจึงดำเนินการต่อ
- บัญชีดังกล่าวยังคงเข้าสู่ระบบอยู่ และเซสชันเดียวกันได้เชื่อมต่อใหม่เมื่อวันที่ 29 ตุลาคม

สิ่งที่ไม่รวมอยู่ในทดสอบนี้: การจัดการหลายบัญชีพร้อมกัน, บทบาทผู้ดูแลระบบ, การใช้พร็อกซี, การหยุดให้บริการ ที่นานกว่าไม่กี่ชั่วโมง และ[ขั้นตอนการรับข้อมูลแบบเรียลไทม์](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)อย่างครบถ้วน ไฟล์สาธารณะมีเพียงข้อมูลจำนวนเท่านั้น: ไม่มีตัวระบุบัญชีหรือการสนทนา, ข้อความ หรือ ข้อมูลรับรอง

## การวัดศักยภาพท้องถิ่นแบบสังเคราะห์

คำสั่ง: `python tools/check_capacity.py --events 10000 --chats 100`

| เมตริก | สังเกต |
| --- | --- |
| ข้อมูลที่ป้อน | 10,000 เหตุการณ์ข้อความสังเคราะห์จาก 100 แหล่งข้อมูลสังเคราะห์ที่เลือกมา |
| ข้อความ | 400 ตัวอักษร; ไม่รวมสื่อหรือเครือข่าย |
| การนำเข้าข้อมูล | 53.273 วินาที; 187.7 เหตุการณ์/วินาที |
| ความล่าช้าของตัวจัดการ | p50 4.162 ms; p95 7.784 ms; สูงสุด 129.118 ms |
| ส่งออกเป็น ZIP | 19.868 วินาที เมื่อเปิดใช้งาน tracemalloc |
| Peak: การติดตามการจัดสรรทรัพยากรการส่งออกของ Python | 0.51 MiB; ไม่รองรับ RSS |
| ขนาด ZIP | 4,610,962 ไบต์ |
| การตรวจสอบอย่างอิสระ | เหตุการณ์ทั้งหมด 10,000 รายการได้รับการตรวจสอบแล้ว |

การวัดนี้วัดเส้นทางบันทึก/ส่งออกแบบซีเรียลในเครื่องโฮสต์ Windows นี้เท่านั้น ไม่ วัดการส่ง MTProto บัญชีที่ใช้งานพร้อมกัน การจำกัดความเร็วของ Telegram สื่อ งานที่ทำงานต่อเนื่องเป็นเวลานาน หรือจำนวนการสนทนาจริงที่รับประกัน การวัดนี้ทำขึ้นก่อน เครื่องมือประทับเวลาออฟไลน์เวอร์ชันสุดท้าย ซึ่งไม่ส่งผลต่อเส้นทางข้อความที่วัดได้

## การค้นหาข้อความเต็มในข้อความหนึ่งล้านข้อความ · 5 พฤศจิกายน 2026

คำสั่ง: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

สมุดบันทึกที่ลงนามแบบกำหนดค่าแน่นอน (deterministic signed journal) ซึ่งประกอบด้วยข้อความสังเคราะห์ 1,000,000 ข้อความใน 200 ห้องสนทนา (รูปแบบคำภาษารัสเซีย ภาษายูเครน ภาษาอังกฤษ ภาษาจีน ภาษาญี่ปุ่น ลิงก์ และชื่อผู้ใช้) ได้รับการจัดทำดัชนีใน 71 วินาที; ดัชนีมีขนาด 58 MiB นอกเหนือจากสมุดบันทึกขนาด 1.50 GiB การค้นหา ที่ตรงกันมากที่สุดใช้เวลา 9 ถึง 190 มิลลิวินาที (ค่ามัธยฐาน) เทียบกับ 2.4 ถึง 3.2 วินาที สำหรับการค้นหา ส่วนย่อยของข้อความแบบเดิม ผลลัพธ์เต็มรูปแบบ อุปกรณ์ และข้อจำกัด: [การค้นหาข้อความเต็มรูปแบบ](https://phishdestroy.github.io/TgWitness/th/docs/reference/search/#benchmark) `tools/test_fulltext.py` ยังตรวจสอบไฟล์เก็บถาวรที่ลงนามไว้ก่อนการค้นหาข้อความเต็ม (`tools/fixtures/evidence-before-fulltext.zip`) ด้วยตัวตรวจสอบปัจจุบัน และไฟล์เก็บถาวรปัจจุบัน ด้วยตัวตรวจสอบของไฟล์เก็บถาวรนั้นเอง `verify.py`.

## คุณสมบัติเพิ่มเติม

บันทึกแบบเรียลไทม์ที่เก็บรักษาไว้จะบันทึกการเก็บรวบรวมจริง การแก้ไข การแจ้งเตือนการลบ ไฟล์แนบ การตรวจสอบซ้ำ และการจัดการข้อจำกัดอัตรา มันไม่บันทึกการส่งข้อความอย่างครบถ้วน หรือ แมทริกซ์ที่ควบคุมได้เกี่ยวกับความมองเห็นตามบทบาท ผู้ดำเนินการตอบสนอง การรอ FloodWait ที่ยืดเยื้อ การห้ามบัญชี และ การกู้คืนหลังการขัดจังหวะเครือข่าย/กระบวนการ การออกโทเคน QR ยังคงแยกต่างหากจาก การยืนยัน QR บนมือถือที่เสร็จสิ้นแล้ว

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
