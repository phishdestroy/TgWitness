# ติดตั้ง ตรวจสอบ และอัปเดต

Canonical page: https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/

ติดตั้งด้วยคำสั่งเดียว ตรวจสอบลายเซ็นและค่าแฮช อัปเดตและลบการติดตั้ง

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [เอกสารประกอบ](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [เริ่มต้นใช้งาน](https://phishdestroy.github.io/TgWitness/th/docs/reference/quickstart/)

![เริ่มต้นใช้งาน](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[โครงการ](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [เริ่มต้นอย่างรวดเร็ว](https://phishdestroy.github.io/TgWitness/th/docs/reference/quickstart/) · [การติดตั้ง](https://phishdestroy.github.io/TgWitness/th/docs/reference/deployment/)

**บนหน้านี้**

- [ติดตั้งด้วยคำสั่งเดียว](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#install-with-one-command)
- [ที่ทุกสิ่งทำงาน](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#where-everything-runs)
- [การตั้งค่าการค้นหาข้อความเต็ม](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#full-text-search-settings)
- [การเข้าถึงผ่านบรรทัดคำสั่ง](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#command-line-access)
- [ตรวจสอบก่อนที่จะดำเนินการ](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#verify-before-running)
- [อัปเดตการติดตั้งที่มีอยู่](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#update-an-existing-installation)
- [คำสั่งทั่วไปบน Ubuntu](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#everyday-commands-on-ubuntu)
- [ลบTgWitness](https://phishdestroy.github.io/TgWitness/th/docs/reference/installation/#remove-tgwitness)

## ติดตั้งด้วยคำสั่งเดียว

โปรแกรมติดตั้งแบบมีคู่มือมาพร้อมกับ Python runtime ส่วนตัว ใช้ที่อยู่เดียวกันสำหรับการ ติดตั้งในอนาคต: ทุกครั้งที่มีการเผยแพร่ จะอัปเดตโปรแกรมติดตั้ง, ค่าแฮช, ลายเซ็น และข้อมูลการสร้างไว้ด้วยกัน

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

บนเซิร์ฟเวอร์ Ubuntu ให้ทำงานในฐานะ root เพื่อติดตั้งบริการทำงานในพื้นหลัง ส่วนบนเดสก์ท็อป ให้ทำงานในฐานะผู้ใช้ปกติ

**Windows (PowerShell หรือ Command Prompt):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

ไม่จำเป็นต้องมีผู้ดูแลระบบบน Windows กระบวนการ PowerShell ลูกจะทิ้ง เทอร์มินัลของคุณไว้เปิดพร้อมผลลัพธ์ Python และส่วนประกอบที่จำเป็นจะยังคงอยู่ในโฟลเดอร์ติดตั้ง

บน Ubuntu ให้เลือก "**This computer**", **"Temporary HTTPS link**" หรือ "**Own domain**" โปรแกรมติดตั้งจะแสดงที่อยู่ของแผงควบคุมและกุญแจการเข้าถึง สำหรับลิงก์ชั่วคราว ให้เปิด ที่อยู่ HTTPS นั้นในเบราว์เซอร์ของคุณและป้อนกุญแจการเข้าถึง หากต้องการเข้าถึงแบบท้องถิ่นบนเซิร์ฟเวอร์ระยะไกล ให้ใช้การส่งต่อ SSH จากคอมพิวเตอร์ของคุณ (`ssh -L 8787:127.0.0.1:8787 user@server`) แล้วเปิด `http://127.0.0.1:8787`. บน macOS และ Windows แผงควบคุมท้องถิ่นจะเปิดใน เบราว์เซอร์ของคุณ; ให้เทอร์มินัลทำงานต่อไป

ลงชื่อเข้าใช้ Telegram ในแผงควบคุมและเลือกข้อมูลที่ต้องการเก็บรวบรวม การติดตั้งเพียงอย่างเดียว ยังไม่เริ่มการเก็บรวบรวมข้อมูลจาก Telegram

## ที่ทุกสิ่งทำงาน

`get.destroy.tools` เป็น **Cloudflare Worker ที่ให้บริการดาวน์โหลดไฟล์แบบคงที่** ไม่มีแผง TgWitness, เซสชัน Telegram หรือฐานข้อมูลหลักฐานผู้ใช้ และไม่ถูกส่งต่อไปยัง VPS ของโครงการ แอปพลิเคชันทำงานบนเครื่องที่คุณรันคำสั่ง

| การติดตั้ง | โปรแกรม | ข้อมูล |
| --- | --- | --- |
| Ubuntu ในฐานะ root | `/opt/tgwitness` | บริการระบบ: `/var/lib/tgwitness-<installation ID>`; ใช้ `tgwitness paths` เพื่อดูเส้นทางที่แม่นยำ |
| ผู้ใช้ Linux / macOS | `~/.local/share/tgwitness` | `data/live` ในระบบการติดตั้งนั้น |
| ผู้ใช้ Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` ในระบบการติดตั้งนั้น |

ตั้งค่า `TGWITNESS_INSTALL_DIR` เพื่อเลือกโฟลเดอร์อื่น เวอร์ชันที่ติดตั้งและข้อมูล ถูกแยกกัน โปรแกรมติดตั้งจะไม่ส่งบัญชี ข้อความ หรือกุญแจของคุณไปยัง เว็บไซต์ดาวน์โหลด การเลือกใช้ Cloudflare tunnel จะส่งการจราจรของแผงควบคุมผ่าน Cloudflare; การใช้โดเมนของคุณเองจะชี้ไปยังเซิร์ฟเวอร์ของคุณเอง

การติดตั้งทุกครั้งจะรวมถึงไฟล์ **START-HERE.html** และ **START-HERE.txt** ซึ่งระบุ เส้นทางในเครื่อง คำสั่ง และลิงก์ไปยัง repositori ให้เรียกใช้ `tgwitness guide` เพื่อเปิดคู่มือ บน Windows ให้ใช้ `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` ใน PowerShell

## การตั้งค่าการค้นหาข้อความเต็ม

[การค้นหาข้อความเต็ม](https://phishdestroy.github.io/TgWitness/th/docs/reference/search/) (เวอร์ชันทดลอง) ไม่ต้องการการตั้งค่าใดๆ ดัชนีจะถูกสร้างขึ้นใน เบื้องหลังหลังจากอัปเดต

| ตัวแปรหรือคำสั่ง | ผลลัพธ์ |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | ค่าเริ่มต้น: ดัชนีจะถูกเก็บไว้ใน `search/fulltext.sqlite3` ของแต่ละพื้นที่ทำงาน |
| `TGWITNESS_FULLTEXT=memory` | ไม่มีไฟล์ดัชนี; ดัชนีจะถูกสร้างใหม่ทุกครั้งที่เริ่มต้น |
| `TGWITNESS_FULLTEXT=off` | ไม่มีดัชนี; ค้นหาได้เฉพาะข้อความที่ตรงกันเท่านั้น |
| `tgwitness index status` | บันทึกสถานะของทุกพื้นที่ทำงาน |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | สร้างดัชนีใหม่ทั้งหมดจากบันทึกที่ลงนาม |

การเลือกของผู้ดูแลระบบใน **Journal → Filters → Search index** จะแทนที่ ตัวแปรสำหรับพื้นที่ทำงานนั้น คำสั่งจะค้นหาไดเรกทอรีข้อมูลของระบบติดตั้ง ที่รันคำสั่งนั้น; ในกรณีอื่น ๆ ให้เพิ่ม `--data-dir` ด้วยเส้นทางจาก `tgwitness paths`. เพื่อใช้พจนานุกรมภาษายูเครนแบบเต็ม (ข้อมูล GPL-3.0) ให้ติดตั้ง `pymorphy3-dicts-uk` ใน สภาพแวดล้อม Python ของการติดตั้ง

## การเข้าถึงผ่านบรรทัดคำสั่ง

[บรรทัดคำสั่ง](https://phishdestroy.github.io/TgWitness/th/docs/reference/cli/) (เวอร์ชันทดลอง) จะอ่านไฟล์เก็บถาวรเพื่อค้นหาสคริปต์และเอเจนต์

| ตัวแปร | ผลลัพธ์ |
| --- | --- |
| `TGWITNESS_URL` | ที่อยู่ของแผงสำหรับ `tgwitness search`, `context`, `messages`, `stats` และ `export`; ค่าเริ่มต้น `http://127.0.0.1:8787` เมื่อมีการกำหนดโทเคน |
| `TGWITNESS_MCP_TOKEN` | เก็บโทเค็นการเชื่อมต่อจาก **Integrations → MCP** ซึ่งถูกแชร์กับลูกค้า MCP; `--token-file` อ่านจากไฟล์แทน |
| `TGWITNESS_DATA` | อ่านไดเรกทอรีข้อมูลโดยตรงเมื่อไม่มี `--data-dir`, URL หรือ token |

## ตรวจสอบก่อนที่จะดำเนินการ

คำสั่งหนึ่งบรรทัดนี้ใช้ HTTPS เพื่อตรวจสอบความน่าเชื่อถือของสคริปต์เริ่มต้น สคริปต์ดังกล่าวจะตรวจสอบ SHA-256 และลายเซ็น RSA ของโครงการบนแอปพลิเคชันและข้อจำกัดก่อน การติดตั้ง คุณยังสามารถดาวน์โหลดและตรวจสอบสคริปต์เริ่มต้นก่อนได้

กุญแจการเผยแพร่สาธารณะคือ [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub)SHA-256 ของมันคือ:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

เก็บลายนิ้วมือนี้ไว้จากเวอร์ชันของรีโพสิตอรีที่คุณเชื่อถือได้ ค่าเช็กซัมจาก เซิร์ฟเวอร์ดาวน์โหลดเดียวกันจะตรวจพบความไม่ตรงกัน; กุญแจสาธารณะที่ได้รับการเชื่อถืออย่างอิสระ คือสิ่งที่ใช้ยืนยันความถูกต้องของลายเซ็นการปล่อยเวอร์ชัน

ใช้โฟลเดอร์ใหม่ที่ว่างเปล่าสำหรับไฟล์ดาวน์โหลดการตรวจสอบด้านล่างนี้

**Linux / macOS — ทำงานในโฟลเดอร์ดาวน์โหลดใหม่ที่ว่าง** (จำเป็นต้องมี curl และ OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

The `&&` กระบวนการจะหยุดลงก่อนการดำเนินการ หากการดาวน์โหลด ลายนิ้วมือของกุญแจ หรือการตรวจสอบลายเซ็น ล้มเหลว หากมีการเผยแพร่ระหว่างการดาวน์โหลดสคริปต์และ ลายเซ็นของมัน ให้ดาวน์โหลดทั้งสองอีกครั้ง โปรแกรมติดตั้งเวอร์ชันเก่าจะรักษา URL ของแพ็กเกจที่ไม่สามารถเปลี่ยนแปลงได้

**Windows — ตรวจสอบ SHA-256 ก่อนที่จะเรียกใช้:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

เปรียบเทียบค่าแฮชกับ `install.ps1` บรรทัดดังกล่าว เพื่อตรวจสอบลายเซ็นอย่างอิสระ ให้ใช้ OpenSSL (เช่น จาก Git Bash) และลายนิ้วมือกุญแจสาธารณะเดียวกันข้างต้น:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

การติดตั้งบน Windows จะตรวจสอบลายเซ็นแพ็กเกจด้วย .NET โดยไม่ จำเป็นต้องใช้ OpenSSL ลายเซ็นเหล่านี้เป็นลายเซ็น RSA-3072 / SHA-256 แบบแยกตัว ไม่ใช่ Authenticode [ไฟล์แมนิเฟสต์บันทึกเวอร์ชันซอฟต์แวร์](https://get.destroy.tools/manifest.json), การคอมมิต Git ที่แม่นยำ, ID การปล่อยเวอร์ชันที่ไม่สามารถเปลี่ยนแปลงได้ และ SHA-256 ของแต่ละอาร์ติแฟกต์ หน้าเว็บนี้เชื่อมโยง ไปยังแหล่งที่มาที่เกี่ยวข้อง ไฟล์แมนิเฟสต์และรายการเช็กซัมยังมีลายเซ็นแบบแยกตัว ด้วย (`manifest.json.sig` และ `SHA256SUMS.txt.sig`).

## อัปเดตการติดตั้งที่มีอยู่

**การเผยแพร่เวอร์ชันใหม่จะอัปเดตเว็บไซต์ดาวน์โหลด; โปรแกรมที่ติดตั้งแล้วจะอัปเดตเมื่อคุณ เรียกใช้ตัวติดตั้งอีกครั้ง** ไม่มีตัวอัปเดตอัตโนมัติหรือการรีสตาร์ทอัตโนมัติของ คอลเลกชันที่กำลังทำงานอยู่ ช่องตัวติดตั้งปัจจุบันเป็นเวอร์ชัน**พรีวิว**; มันติดตาม บิลด์ที่เผยแพร่และตรวจสอบแล้วจาก `main`, ซึ่งการ commit อาจใหม่กว่า การปล่อยเวอร์ชัน GitHub ที่มีการกำหนดหมายเลขล่าสุด เวอร์ชันของหน้านี้มาจาก `pyproject.toml`; commit และ build ID ของมันช่วยแยกแยะการอัปเดตภายในเวอร์ชันพรีวิวเดียวกัน

การเผยแพร่จะเกิดขึ้นโดยอัตโนมัติหลังจากที่ commit ที่ระบุนั้นผ่านการตรวจสอบแอปพลิเคชันและ ความปลอดภัย และแพ็กเกจที่ลงนามแล้วผ่านการทดสอบบริการ Ubuntu และ Windows PowerShell การติดตั้ง ในขณะที่การตรวจสอบกำลังดำเนินการอยู่ หรือหากการตรวจสอบล้มเหลว คำสั่งเดียวกันจะยังคงติดตั้งบิลด์ที่ผ่านการตรวจสอบก่อนหน้านี้ต่อไป บิลด์แมนิเฟสต์ จะแสดงว่า commit ใดที่มีอยู่ในขณะนี้; หมายเลขเวอร์ชันเพียงอย่างเดียวอาจยังคง ไม่เปลี่ยนแปลงระหว่างการอัปเดตเวอร์ชันพรีวิว

ใช้โฟลเดอร์การติดตั้งและผู้ใช้ระบบปฏิบัติการเดียวกันกับครั้งก่อน สำรองข้อมูล ในไดเรกทอรีทั้งหมดโดยปิดการเก็บข้อมูลไว้ก่อน; `tgwitness paths` เพื่อระบุมัน การส่งออกที่ลงนาม ไม่ใช่การสำรองข้อมูลการติดตั้งที่สมบูรณ์

**การติดตั้ง Ubuntu ในสิทธิ์ root ที่ `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

หลังจากติดตั้งสำเร็จ:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

สำหรับการติดตั้งบนระบบ Linux/macOS ให้ใช้ค่าเริ่มต้น `TGWITNESS_INSTALL_DIR` หรือ ค่าเริ่มต้น และรันคำสั่งติดตั้งครั้งแรกอีกครั้ง ปิด แผงที่ทำงานอยู่เบื้องหน้า ก่อนอัปเดต และเปิดมันขึ้นใหม่หลังจากนั้น สำหรับผู้ใช้ Linux ที่ได้กำหนดค่า บริการแล้ว ให้รัน `tgwitness restart` คำสั่ง

**Windows:** ปิดแผงที่กำลังทำงานอยู่, 실행 Windows ติดตั้งคำสั่งอีกครั้ง, แล้วเปิด `bin\tgwitness.cmd` ในกระบวนการติดตั้งเดียวกัน โปรแกรมติดตั้งจะเก็บรักษาข้อมูล, เซสชัน, การตั้งค่าการเข้าถึง และกุญแจการลงนาม มันจะเปลี่ยนตัวเปิดใช้งานเพียงเมื่อ สภาพแวดล้อมใหม่ผ่านการตรวจสอบแล้วเท่านั้น; หากการติดตั้งล้มเหลว ตัวเปิดใช้งานเดิม จะยังคงอยู่ต่อไป ให้เก็บสำเนาสำรองก่อนการอัปเกรดไว้เพื่อรับมือกับการเปลี่ยนแปลงรูปแบบการจัดเก็บข้อมูล

## คำสั่งที่ใช้ทุกวันบน Ubuntu

| คำสั่ง | ผลลัพธ์ |
| --- | --- |
| `tgwitness open` | URL ของแผงปัจจุบันและกุญแจการเข้าถึง |
| `tgwitness paths` | เส้นทางที่แม่นยำของโปรแกรม ข้อมูล และคู่มือ |
| `tgwitness guide --print` | คู่มือการใช้งานแบบออฟไลน์ |
| `tgwitness status` / `tgwitness logs` | ความพร้อมใช้งาน / บันทึกบริการ |
| `tgwitness stop` / `tgwitness start` | หยุด / ต่อบริการ; เก็บข้อมูลไว้ |
| `tgwitness token rotate` | เปลี่ยนกุญแจผู้ดูแลระบบและปิดเซสชันเบราว์เซอร์ |
| `tgwitness tunnel off` | ปิดใช้งาน Quick Tunnel สาธารณะ; เก็บแผงควบคุมท้องถิ่นไว้ |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | สร้างลิงก์ tunnel แบบรวดเร็ว / เปลี่ยนที่อยู่ของลิงก์นั้น |

ดูส่วน "[Access"](https://phishdestroy.github.io/TgWitness/th/docs/reference/access/) เพื่อทราบข้อมูลเกี่ยวกับโทเค็นของเพื่อนร่วมงาน เซสชัน และข้อจำกัด IP รวมถึง [การเผยแพร่ตัวติดตั้ง](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) สำหรับขั้นตอนการปล่อยเวอร์ชันจาก GitHub ไปยัง Cloudflare

## ลบTgWitness

ไม่มีโปรแกรมถอนการติดตั้ง: คุณต้องหยุดการทำงานของแผงควบคุมและลบโฟลเดอร์ที่เกี่ยวข้อง การลบโฟลเดอร์ข้อมูล จะลบสมุดบันทึก กุญแจการลงนาม เซสชัน Telegram และไฟล์ที่บันทึกไว้อย่างถาวร ก่อนที่จะทำเช่นนั้น:

1. ส่งออกข้อมูลที่จำเป็น (**Exports → Download signed ZIP**) และเก็บลายนิ้วมือของกุญแจลงนาม และจุดตรวจสอบไว้ภายนอกเครื่องนี้ เพื่อเก็บพื้นที่ทำงานไว้ ให้คัดลอก โฟลเดอร์ข้อมูลทั้งหมดหลังจากหยุดการเก็บข้อมูลแล้ว
2. ลบเซิร์ฟเวอร์ที่สร้างขึ้นภายใต้ **Extras → Server 24/7** จาก **Your servers** หรือด้วย `python -m tgwitness.cloud destroy`; ผู้ให้บริการจะเรียกเก็บค่าบริการจนกว่าบัญชีเหล่านั้นจะถูกลบ
3. ปิดเซสชันของบัญชีแต่ละบัญชีใน Telegram โดยไปที่ **การตั้งค่า → อุปกรณ์** การลบ ไฟล์จะไม่ทำให้เซสชันถูกปิดออกจากฝั่ง Telegram

**การติดตั้ง Ubuntu ในสิทธิ์ root** โปรดสังเกตโฟลเดอร์ข้อมูล หยุดบริการ แล้วลบ บริการ โฟลเดอร์ และทางลัด:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**การติดตั้งสำหรับผู้ใช้ Linux หรือ macOS** ปิดแผงควบคุม บริการผู้ใช้ Linux ที่ได้รับการกำหนดค่า ถูกหยุดด้วย `systemctl --user disable --now tgwitness-<ID>`; หน่วยวัดของมันคือ `~/.config/systemd/user/`. จากนั้นลบ `~/.local/share/tgwitness` (หรือของคุณ `TGWITNESS_INSTALL_DIR`) และ `~/.local/bin/tgwitness` ทางลัด

**Windows.** ปิดแผงและลบ `%LOCALAPPDATA%\TgWitness` (หรือ `TGWITNESS_INSTALL_DIR`). โปรแกรมติดตั้งไม่เพิ่มบริการ งานตามกำหนดเวลา หรือทางลัดใดๆ
