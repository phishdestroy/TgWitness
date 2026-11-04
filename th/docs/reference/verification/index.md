# สิ่งที่ได้รับการทดสอบแล้ว

Canonical page: https://phishdestroy.github.io/TgWitness/th/docs/reference/verification/

การทดสอบ Telegram แบบเรียลไทม์ การตรวจสอบอัตโนมัติ การตรวจสอบผ่านเบราว์เซอร์ และสิ่งที่ยังไม่ได้รับการยืนยัน

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
