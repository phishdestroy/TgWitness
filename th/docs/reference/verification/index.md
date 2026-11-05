# สิ่งที่ได้รับการทดสอบแล้ว

Canonical page: https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/

การทดสอบ Telegram แบบเรียลไทม์ การตรวจสอบอัตโนมัติ การตรวจสอบผ่านเบราว์เซอร์ และสิ่งที่ยังไม่ได้รับการยืนยัน

## การปรับใช้ Phala Cloud แบบสด · 4 พฤศจิกายน 2026

`--provider phala --quick-tunnel` ทำงานกับ **Phala Cloud** ที่จริง (`tdx.small`, region US-WEST-1) ด้วย Phala Cloud API key ของ workspace ที่ว่าง, ntfy.sh ที่จริง, GitHub และ Intel PCS. CVM ได้ติดตั้ง commit `df7d860c` (v0.8.1); กระบวนการ deploy, verify และ destroy ดำเนินการผ่านบรรทัดคำสั่ง พร้อมการแก้ไขดังต่อไปนี้ CVM 7 เครื่องมีค่าใช้จ่ายรวมประมาณ 1.9 US cents

การปรับใช้สองครั้งแรกพบความแตกต่างห้าจุดจาก Phala Cloud ที่จำลอง [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) ตอนนี้สามารถจำลองความแตกต่างแต่ละจุดได้ และล้มเหลวหากไม่มีการแก้ไข:

| บน Phala Cloud | ก่อนการแก้ไข | แก้ไข |
| --- | --- | --- |
| `compose_file.name` เป็นสิ่งจำเป็น | HTTP 422, ไม่มีการสร้างอะไรเลย | การกำหนดค่า Docker Compose ระบุชื่อ CVM |
| เว้นแต่จะกำหนดค่าว่าง Phala จะเพิ่มสคริปต์ก่อนการเริ่มต้นของตัวเองเข้าไปใน app-compose ที่ถูกวัด (v0.0.20: การเข้าสู่ระบบ Docker, `docker compose pull`, รหัสผ่าน root, คีย์ SSH จาก `user_config`) | `tdx_compose` ล้มเหลว: มีโค้ดอยู่นอกการกำหนดค่า Docker Compose ที่เผยแพร่ | app-compose ตั้งค่า `pre_launch_script` เป็น `""`; Phala จึงไม่รวมมันเข้าไป |
| หากไม่ใช้ `image` Phala จะเลือก `dstack-dev-0.5.12` ซึ่งเป็นเวอร์ชันพัฒนา พร้อมเปิดการเข้าถึง SSH | `server_state` ไม่ผ่าน. ในภาพนี้ มีเพียงบันทึกการรับรองฮาร์ดแวร์เท่านั้นที่ผ่าน; มีเพียงบันทึกผู้ให้บริการและ `tdx_os` ที่แสดงผลนี้ | การปรับใช้ต้องการเวอร์ชัน production build ของ Phala ในรุ่นปัจจุบัน คือ `dstack-0.5.12` |
| เมื่อปิด dstack gateway แล้ว รายละเอียด CVM จะไม่ได้รับรหัส `instance_id` | การปรับใช้รอ 30 นาทีแล้วล้มเหลว | ID ของอินสแตนซ์ถูกอ่านจากสถานะของ CVM |
| การรีสตาร์ท การหยุด และการเริ่มต้น เป็นกระบวนการของ CVM ไม่ใช่การปรับปรุงแอปพลิเคชัน | `provider_actions` ไม่ได้แสดงการรีสตาร์ท | การดำเนินการเหล่านี้ยังรวมถึงการอ่านด้วย |

การปรับใช้ครั้งที่สาม:

- CVM ได้เรียกใช้ `dstack-0.5.12` โดยปิดการเข้าถึง SSH ผู้รวบรวมได้โพสต์ที่อยู่ที่มีลายเซ็นประมาณ 1.5 นาทีหลังจากการสร้าง จากนั้นการปรับใช้ได้ผ่าน `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, บันทึกการรับรองฮาร์ดแวร์ v4, FMSPC `20a06f000000`, ไม่อยู่ในโหมดดีบัก, ไม่สามารถย้ายได้, รองรับข้อมูลการตรวจสอบทางเข้ารหัส ที่ดึงมาจาก Intel), `tdx_compose_hash`, `tdx_compose` (ไบต์ต่อไบต์) และ `tdx_identity` (กุญแจ KMS).
- แผงควบคุมที่ที่อยู่ trycloudflare.com ตอบกลับด้วยรหัส 401 เมื่อไม่มีโทเค็นหรือใช้โทเค็นผิด, และตอบกลับด้วยรหัส 200 เมื่อใช้โทเค็นของแผงควบคุม
- `verify` โดย `--source` ถูกตั้งค่าเป็นอาร์ไคฟ์ของ GitHub สำหรับการคอมมิต และลายนิ้วมือถูกส่ง แยกกัน: เซิร์ฟเวอร์, `server_state`, ไฟร์วอลล์ (ไม่มีเกตเวย์, ไม่มีจุดสิ้นสุดสาธารณะ), บันทึกของผู้ให้บริการ, ใบแจ้งยอด, ลายนิ้วมือ, แฮชแหล่งที่มา, การบูต และการตรวจสอบ `tdx_*` ทั้งห้าผ่าน Cloudflare และ `tdx_os` ไม่สามารถใช้งานได้ ดังนั้นผลลัพธ์จึงเป็น INCOMPLETE.
- การรีสตาร์ทสองครั้งผ่าน API ของ Phala: ทุกครั้งที่ CVM กลับมาทำงานภายในเวลาไม่ถึงสองนาทีด้วย กุญแจผู้รวบรวมเดียวกัน ที่อยู่ใหม่ที่ลงนามแล้ว และที่อยู่เดิมที่ตอบกลับด้วยรหัส 530 `verify` รายงาน การบูตใหม่และทั้งสองครั้งการรีสตาร์ทเป็น REVIEW ด้วย `--evidence` ได้ยืนยันลายเซ็น ในบันทึกและสามครั้งการเริ่มต้นระบบ แต่ละครั้งมีบันทึกการรับรองฮาร์ดแวร์ Intel TDX ของตัวเองจาก CVM เดียวกัน
- `destroy` ได้ลบเฉพาะ CVM นั้นเท่านั้น พื้นที่ทำงานจึงว่างเปล่า และที่อยู่ของแผงควบคุมหยุด ตอบสนอง
- การตรวจสอบราคาของตัวช่วยสร้างในแผงควบคุมแสดง `tdx.small` ที่ $0.058 ต่อชั่วโมง หากใช้คีย์ผิด จะได้รับข้อความธรรมดา "ไม่ยอมรับคีย์ API"

ผลการค้นพบเพิ่มเติมอีกสองข้อ ซึ่งได้แก้ไขแล้ว:

- หากไม่มีกุญแจที่อยู่ `verify` จะติดตามโพสต์ที่จัดรูปแบบถูกต้องล่าสุดในหัวข้อที่อยู่ ซึ่งถูกพิมพ์ไว้ในเอกสารกำหนดค่า Docker Compose ที่เผยแพร่แล้ว โพสต์ปลอมหนึ่งรายการได้ส่งมันไปยังโฮสต์ที่ ไม่มีอยู่จริง และ `statement` ล้มเหลว: ผู้ปลอมแปลงไม่สามารถปลอมตัวเป็นผู้รวบรวมได้ แต่สามารถบล็อก การตรวจสอบจากฝ่ายที่สาม ได้นานถึง 12 ชั่วโมง ด้วยเวลาประทับที่ปลอมแปลงไว้ล่วงหน้า ผู้รวบรวมข้อมูลตอนนี้ ยังโพสต์ที่อยู่ของตนเองที่ลงนามด้วยกุญแจของตัวเองด้วย `verify` จะรับเฉพาะโพสต์ประเภทนี้เมื่อ ผู้รวบรวมข้อมูลเป็นผู้สร้างขึ้น และโพสต์จะถูกจัดเรียงตามเวลาที่ ntfy.sh รับข้อมูล [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) เล่นซ้ำโพสต์ที่ถูกปลอมแปลง CVM จะรันสิ่งนี้เฉพาะจาก commit ที่มีมันอยู่เท่านั้น ดังนั้นผู้เก็บรวบรวมในรอบนี้ยังไม่ได้ลงนามที่อยู่ของตัวเอง และ `verify` ได้แจ้งเรื่องนี้
- `tdx_os` ไม่สามารถทำงานได้โดยไม่มี `dstack-mr` ซึ่งเวอร์ชันปัจจุบันมี `measure-os` แทนที่จะเป็น `measure --json` ตามที่ระบุในเอกสารคู่มือ ผู้ตรวจสอบจะคำนวณ MRTD และ RTMR0-2 ด้วยตัวเอง จากภาพที่เผยแพร่และรูปทรงของ VM รวมถึงตาราง ACPI

การปรับใช้ครั้งที่สี่ มีดังนี้:

- Deploy ได้ดาวน์โหลด `dstack-0.5.12` ที่เผยแพร่มาหนึ่งครั้ง เปรียบเทียบกับค่าแฮชของภาพระบบปฏิบัติการที่ CVM รายงาน และ `tdx_os` ผ่านการตรวจสอบ: MRTD, RTMR0, RTMR1 และ RTMR2 เท่ากับค่าที่คำนวณสำหรับ QEMU 8.2.2, 1 vCPU และ 2 GiB การคำนวณเดียวกันให้ค่า RTMR0 ที่ต่างออกไปสำหรับกรณีที่ระบุ 4 GiB, 2 vCPUs, QEMU 9.2.1 หรือการ์ดเครือข่ายใบที่สอง และล้มเหลวสำหรับเคอร์เนลที่เปลี่ยนแปลง, เฟิร์มแวร์ หรือบรรทัดคำสั่ง และสำหรับภาพระบบปฏิบัติการสำหรับการพัฒนา
- `verify` ผ่านการตรวจสอบทั้ง 16 ขั้นตอนได้ทั้งหมด รวมถึงตัวเชื่อมต่อของ quick tunnel ด้วย ดังนั้นผลลัพธ์ จึงเป็น PASS. มันได้สร้างใบรับรองในรูปแบบ HTML และ PDF ซึ่งได้รับการปิดผนึกดิจิทัลด้วยลายเซ็นและตราประทับเวลา พร้อมด้วยตราประทับเวลา eIDAS ที่ได้รับการรับรองจาก หน่วยประทับเวลา TSU 202301 ของรัฐบาลเบลเยียม (สถานะได้รับการอนุมัติในรายชื่อที่เชื่อถือได้ ของเบลเยียม), ตราประทับเวลา FreeTSA และลายเซ็นของผู้ตรวจสอบ; `check-report` ได้ยืนยันทั้งหมด รวมถึงลายเซ็นในไฟล์ PDF ด้วย
- หลังการรีสตาร์ท `verify --evidence` ยืนยันการเริ่มต้นสองครั้ง โดยแต่ละครั้งมาพร้อมกับการรับรองฮาร์ดแวร์ที่สร้างขึ้นภายใน CVM และแต่ละครั้ง ถูกบูตจาก `dstack-0.5.12` ที่เผยแพร่แล้ว; การรีสตาร์ทและการบูตใหม่ได้รับการจัดประเภทเป็น REVIEW.
- `destroy` ทำให้พื้นที่ทำงานว่างเปล่า

การปรับใช้ครั้งที่ห้าได้รันตัวเก็บข้อมูลจาก commit `53a0f7e9` ซึ่งรวมถึงทุกข้อข้างต้น:

- ผู้รวบรวมได้โพสต์ที่อยู่ของตนที่ลงนามด้วยกุญแจของตนเอง ติดกับโพสต์ HMAC ของผู้ดำเนินการ จากนั้นมีโพสต์ปลอมสองรายการถูกเพิ่มเข้าไปในหัวข้อ หนึ่งรายการมี HMAC เป็นศูนย์ และอีกหนึ่งรายการลงนามด้วยกุญแจ Ed25519 อื่น ทั้งสองรายการอ้างถึงเวลาในปี 2096 `verify` นำที่อยู่ซึ่งลงนามด้วย กุญแจของผู้รวบรวมข้อมูล และผ่านการตรวจสอบทั้ง 16 ขั้นตอน; ตราประทับนั้นยังคงมีตราประทับเวลาของเบลเยียมที่ได้รับการรับรอง, ตราประทับเวลาของ FreeTSA และลายเซ็นของผู้ตรวจสอบ, และ `check-report` ได้ยืนยันข้อมูลเหล่านั้น
- หลังการรีสตาร์ท คอลเลกเตอร์ได้โพสต์ที่อยู่ใหม่ที่ลงนามแล้ว: `verify` ค้นพบมันทันที ส่วน **ของผู้ดำเนินการ ค้นหาที่อยู่ปัจจุบัน** 27 วินาทีต่อมาจากการโพสต์ HMAC และทั้งสองต่างเพิกเฉย ต่อการโพสต์ที่ถูกปลอมแปลง `verify --evidence` ยืนยันการเริ่มต้นสองครั้งจาก `dstack-0.5.12`
- Deploy แสดงราคาที่ Phala คิดค่าบริการสำหรับ CVM รวมถึงค่าดิสก์: $0.06078 ต่อชั่วโมง

ตัวช่วยสร้างแผงควบคุมได้ทำงานกับ Phala Cloud สองครั้ง ครั้งหนึ่งผ่าน API งาน และครั้งหนึ่งผ่าน เบราว์เซอร์ด้วย Chromium จริง: การตรวจสอบราคา, การสร้างพร้อมการ commit ภายใต้ **Advanced**, การตรวจสอบการรับรองทั้งหก ผ่านทั้งหมด, รายการเซิร์ฟเวอร์แสดงราคาที่เรียกเก็บ (44.37 USD ต่อเดือน), **Find ที่อยู่ปัจจุบัน**, การดาวน์โหลดการกำหนดค่า Docker Compose ที่วัดได้ และการลบออก เบราว์เซอร์ไม่พบข้อผิดพลาดของหน้าเว็บ ทุกครั้งหลังจากนั้น พื้นที่ทำงานจะว่างเปล่า

ไม่รวม: โดเมน Cloudflare บน Phala, บัญชี Telegram บน CVM และภาพ `dstack-0.6.1` ราคาที่แสดงในตัวช่วยสร้างก่อนการสร้างเป็นราคาการประมวลผลของ Phala เท่านั้น เนื่องจาก API ของมันระบุราคาดิสก์ เฉพาะสำหรับ CVM ที่มีอยู่แล้วเท่านั้น; รายการเซิร์ฟเวอร์แสดงราคาที่เรียกเก็บเงินหลังการสร้าง

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

## คุณสมบัติเพิ่มเติม

บันทึกแบบเรียลไทม์ที่เก็บรักษาไว้จะบันทึกการเก็บรวบรวมจริง การแก้ไข การแจ้งเตือนการลบ ไฟล์แนบ การตรวจสอบซ้ำ และการจัดการข้อจำกัดอัตรา มันไม่บันทึกการส่งข้อความอย่างครบถ้วน หรือ แมทริกซ์ที่ควบคุมได้เกี่ยวกับความมองเห็นตามบทบาท ผู้ดำเนินการตอบสนอง การรอ FloodWait ที่ยืดเยื้อ การห้ามบัญชี และ การกู้คืนหลังการขัดจังหวะเครือข่าย/กระบวนการ การออกโทเคน QR ยังคงแยกต่างหากจาก การยืนยัน QR บนมือถือที่เสร็จสิ้นแล้ว

การสร้าง/การรัน Docker, การติดตั้งบน Linux/macOS, การรองรับโหลดสูงอย่างต่อเนื่อง, การตรวจสอบความปลอดภัยอย่างอิสระ การตอบสนอง TSA ที่อิสระจริง, การตรวจสอบการเพิกถอน/การเก็บรักษาใบรับรอง และการ รับรองทางนิติวิทยาศาสตร์ ยังคงอยู่นอกขอบเขตการรับรองที่บันทึกไว้ การบันทึกสถานะ MTProto และการติดตามสถานะได้ถูกนำไปใช้แล้ว; แต่การเล่นซ้ำแบบอะตอมิกและทนทานยังไม่ได้รับการยืนยัน การเก็บรวบรวม บันทึกผู้ดูแลระบบ, รายชื่อรีแอคเตอร์เพิ่มเติม และการสำรวจแบบสั้นตามลำดับความสำคัญ ยังคงเป็นคุณสมบัติที่แยกต่างหาก ดู[การยอมรับแบบสด](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)สำหรับเมทริกซ์การรับรองที่ควบคุม

ใบเสร็จรับเงินและภาพหน้าจอรายละเอียดท้องถิ่นอยู่ในโฟลเดอร์ test-results/ (ถูก Git ละเว้น) ภาพหน้าจอสาธารณะในโฟลเดอร์ docs/assets/ มีเพียงข้อมูลสาธิตที่สมมติขึ้นเท่านั้น
