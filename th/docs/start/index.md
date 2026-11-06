# เริ่มใช้งานได้ภายในไม่กี่นาที

Canonical page: https://phishdestroy.github.io/TgWitness/th/docs/start/

ลองสำรวจเดโมก่อน แล้วค่อยเชื่อมต่อบัญชีของคุณ

## ดูรอบๆ โดยไม่ต้องมีบัญชี

ดาวน์โหลดโปรเจกต์ เตรียม **Python 3.11 ขึ้นไป** แล้วรันเดโม ตัวเปิดโปรแกรมจะจัดการส่วนที่เหลือ

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

พื้นที่ทำงานที่มีข้อความแต่งขึ้นจะเปิดในเบราว์เซอร์ เปิดแชท เทียบการแก้ไข ดูการส่งออก ไม่เกี่ยวกับ Telegram

![หน้าแสดงการสนทนาของ TgWitness พร้อมตัวอย่างข้อความ](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

ตัวอย่างพื้นที่ทำงานของคุณ บันทึกของคุณจะเริ่มต้นแยกต่างหาก

## สร้างพื้นที่ทำงานของคุณเอง

ปิดเดโม แล้ว:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

เปิดที่อยู่ที่ตัวเปิดโปรแกรมแสดง แล้ววาง **โทเค็นเข้าถึงแผงควบคุม** จากไฟล์ที่ระบุ โทเค็นนี้สำหรับ TgWitness ไม่ใช่ Telegram

## บันทึกข้อความแรกของคุณ

1. [เชื่อมต่อบัญชี Telegram ที่ใช้เฉพาะสำหรับวัตถุประสงค์นี้](https://phishdestroy.github.io/TgWitness/th/docs/accounts/)
2. เลือกกลุ่มหรือช่องแล้วเริ่มการสังเกต
3. ส่งข้อความในกลุ่มทดสอบแล้วดูมันปรากฏในบันทึก

สำหรับการติดตั้งบนเซิร์ฟเวอร์ โปรดทำตามขั้นตอนในส่วน [“Keep it running](https://phishdestroy.github.io/TgWitness/th/docs/server/)”
