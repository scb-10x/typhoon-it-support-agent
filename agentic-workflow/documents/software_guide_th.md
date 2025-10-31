# คู่มือการใช้งานโปรแกรมทั่วไป

## ภาพรวม

เอกสารนี้รวบรวมคู่มือการใช้งานโปรแกรมที่ใช้ในบริษัท พร้อมเคล็ดลับและการแก้ปัญหาเบื้องต้น

---

## 1. Microsoft Outlook

### การตั้งค่าเริ่มต้น

**การเปิดใช้งาน Outlook ครั้งแรก:**

1. เปิด Microsoft Outlook
2. ใส่ Email: yourname@company.com
3. ใส่รหัสผ่านบริษัท
4. รอระบบ Configure อัตโนมัติ
5. ถ้าถามหา Mail Server: mail.company.com
6. เสร็จแล้วจะเห็นอีเมลในกล่องจดหมาย

### ฟีเจอร์สำคัญ

#### 1. การจัดการอีเมล

**กฎสำหรับจัดอีเมลอัตโนมัติ (Rules):**

1. คลิกขวาที่อีเมล > Rules > Create Rule
2. ตั้งเงื่อนไข:
   - จาก (From): จากผู้ส่งที่ระบุ
   - หัวเรื่อง (Subject): มีคำที่ระบุ
   - ส่งถึง (To): ส่งถึงคุณหรือ Group
3. เลือกการทำงาน:
   - ย้ายไปโฟลเดอร์
   - ลบ
   - ทำเครื่องหมายว่าอ่านแล้ว
   - เล่นเสียงแจ้งเตือน
4. บันทึก

**Quick Steps:**
- สร้างชุดคำสั่งทำอีเมลหลายอย่างพร้อมกัน
- ตัวอย่าง: "ย้ายไป Archive + ทำเครื่องหมายอ่านแล้ว"
- ตั้งค่าที่: Home > Quick Steps

**การค้นหาอีเมล:**
- ใช้ช่องค้นหาด้านบน
- Search ขั้นสูง: Ctrl + E
- ค้นหาจาก: from:john@company.com
- ค้นหามีไฟล์แนบ: hasattachments:yes
- ค้นหาช่วงเวลา: received:yesterday

#### 2. ปฏิทิน (Calendar)

**การสร้างนัดหมาย:**
1. ไปที่ Calendar (Ctrl + 2)
2. คลิก New Appointment หรือดับเบิลคลิกในปฏิทิน
3. กรอกข้อมูล:
   - Subject: หัวเรื่อง
   - Location: สถานที่/ห้องประชุม
   - Start/End: เวลาเริ่ม-จบ
4. เลือก Show As: Busy, Free, Tentative
5. ตั้ง Reminder (แจ้งเตือน)
6. Save & Close

**การสร้างการประชุม:**
1. New Meeting (หรือ Ctrl + Shift + Q)
2. เพิ่มผู้เข้าร่วมในช่อง To
3. เลือกเวลา
4. คลิก Scheduling Assistant เพื่อหาเวลาที่ทุกคนว่าง
5. เพิ่ม Teams Meeting (ถ้าต้องการ)
6. Send

**การแชร์ปฏิทิน:**
1. คลิกขวาที่ Calendar ของคุณ
2. เลือก Share > Share Calendar
3. เลือกคนที่จะแชร์ให้
4. เลือกระดับการเข้าถึง:
   - Can view when I'm busy
   - Can view titles and locations
   - Can view all details
5. Send

#### 3. Focused Inbox

**Focused Inbox คืออะไร:**
- Outlook แยกอีเมลออกเป็น 2 แท็บ:
  - **Focused**: อีเมลสำคัญ
  - **Other**: อีเมลทั่วไป

**การใช้งาน:**
- ถ้าอีเมลอยู่ผิดแท็บ คลิกขวา > Move to Focused/Other
- Outlook จะเรียนรู้และปรับปรุง
- เปิด/ปิดได้ที่ View > Show Focused Inbox

### เคล็ดลับ Outlook

**Keyboard Shortcuts:**
- Ctrl + 1: ไปที่ Mail
- Ctrl + 2: ไปที่ Calendar
- Ctrl + 3: ไปที่ Contacts
- Ctrl + N: อีเมลใหม่
- Ctrl + R: Reply
- Ctrl + Shift + R: Reply All
- Ctrl + F: Forward
- Ctrl + E: Search
- Ctrl + Q: Mark as Read
- Delete: ลบอีเมล
- F9: Send/Receive

**Out of Office:**
1. File > Automatic Replies
2. เลือก "Send automatic replies"
3. กำหนดช่วงเวลา (Start/End time)
4. เขียนข้อความสำหรับ:
   - Inside organization: คนในบริษัท
   - Outside organization: คนนอกบริษัท
5. OK

**Signatures:**
1. File > Options > Mail > Signatures
2. New > ตั้งชื่อ Signature
3. พิมพ์ลายเซ็น (ชื่อ, ตำแหน่ง, เบอร์โทร)
4. ตั้งเป็น Default สำหรับอีเมลใหม่และ Reply
5. OK

### การแก้ปัญหา Outlook

**Outlook ช้า:**
1. ปิดและเปิดใหม่
2. Compact mailbox: File > Tools > Mailbox Cleanup
3. Archive อีเมลเก่า
4. ลบอีเมลที่ไม่ต้องการ
5. Empty Deleted Items

**ไม่สามารถส่งอีเมล:**
1. เช็คอินเทอร์เน็ต
2. เช็คขนาดไฟล์แนบ (ต้องไม่เกิน 25MB)
3. ลบอีเมลใน Outbox
4. ทดสอบส่งอีเมลใหม่
5. Restart Outlook

**ไม่ได้รับอีเมล:**
1. เช็ค Junk Email folder
2. เช็ค Rules ว่าย้ายอีเมลไปที่อื่น
3. Send/Receive: F9
4. เช็ค Mailbox quota
5. ติดต่อ IT

---

## 2. Microsoft Teams

### การเริ่มต้นใช้งาน

**Interface หลัก:**
- **Activity**: การแจ้งเตือนทั้งหมด
- **Chat**: แชทส่วนตัวหรือกลุ่ม
- **Teams**: ทีมและ Channel
- **Calendar**: ปฏิทินและการประชุม
- **Calls**: โทรศัพท์
- **Files**: ไฟล์ที่แชร์

### การใช้งาน Chat

**การเริ่มการสนทนา:**
1. คลิก Chat (ซ้ายมือ)
2. คลิก New Chat (ด้านบน)
3. พิมพ์ชื่อคนที่จะแชท
4. พิมพ์ข้อความ
5. Enter เพื่อส่ง

**Format ข้อความ:**
- **Bold**: Ctrl + B หรือ **text**
- *Italic*: Ctrl + I หรือ *text*
- ~~Strikethrough~~: ~text~
- `Code`: Shift + Enter แล้วเลือก Code snippet
- > Quote: เลือก Format > Quote

**ไฟล์และรูปภาพ:**
- คลิกปุ่ม Attach (คลิป)
- เลือกไฟล์จากคอมพิวเตอร์
- หรือ Drag & Drop ลงในช่องแชท

**Emoji และ GIF:**
- คลิกปุ่ม Emoji ใต้ช่องพิมพ์
- หรือพิมพ์ :smile: :thumbsup: :heart:
- เลือกแท็บ GIF เพื่อหา GIF

### การใช้งาน Teams และ Channels

**Teams คืออะไร:**
- กลุ่มของคนที่ทำงานด้วยกัน
- มี Channels ย่อยสำหรับหัวข้อต่างๆ
- แชร์ไฟล์และแอพได้

**Channels คืออะไร:**
- หัวข้อการสนทนาใน Team
- ตัวอย่าง: General, Projects, Marketing

**การ Post ข้อความใน Channel:**
1. เลือก Team และ Channel
2. พิมพ์ใน "Start a new conversation"
3. เขียนหัวข้อ (ถ้าต้องการ)
4. พิมพ์ข้อความ
5. คลิก Send (หรือ Ctrl + Enter)

**การ Reply:**
- คลิก Reply ใต้ข้อความ
- สร้าง Thread ทำให้การสนทนาเป็นระเบียบ

**การ Mention:**
- @ชื่อคน: แจ้งเตือนคนๆนั้น
- @team: แจ้งเตือนทุกคนใน Team (ใช้ระวัง!)
- @channel: แจ้งเตือนทุกคนใน Channel

### การประชุม

**การเข้าร่วมการประชุม:**
1. ไปที่ Calendar
2. คลิก Join ในการประชุม
3. เลือก Audio/Video settings
4. คลิก Join now

**การสร้างการประชุมด่วน:**
1. คลิก Meet now (ด้านบน)
2. พิมพ์ชื่อการประชุม
3. คลิก Join now
4. เชิญคนอื่นด้วย Add people

**ระหว่างการประชุม:**
- **Mute/Unmute**: Ctrl + Shift + M
- **Turn off video**: Ctrl + Shift + O
- **Share screen**: คลิกปุ่ม Share
- **Turn on captions**: คลิก More > Turn on live captions
- **Record**: คลิก More > Start recording (ต้องได้รับอนุญาต)
- **Background effects**: คลิก More > Apply background effects

**การ Share Screen:**
1. คลิกปุ่ม Share (ในการประชุม)
2. เลือก:
   - Desktop: แชร์ทั้งหน้าจอ
   - Window: แชร์หน้าต่างเดียว
   - PowerPoint: แชร์ PowerPoint แบบพิเศษ
   - Whiteboard: กระดานไวท์บอร์ด
3. คลิก Share
4. Stop sharing เมื่อเสร็จ

### การใช้งาน Files

**การเข้าถึงไฟล์:**
- ไฟล์ใน Channel: ไปที่ Team > Channel > แท็บ Files
- ไฟล์ใน Chat: ไปที่ Chat > แท็บ Files ด้านบน
- ไฟล์ทั้งหมด: คลิก Files (ซ้ายมือ)

**การอัปโหลดไฟล์:**
1. ไปที่ Channel หรือ Chat
2. คลิก Files
3. คลิก Upload
4. เลือกไฟล์
5. คลิก Open

**การทำงานร่วมกัน:**
- คลิกไฟล์ใน Teams จะเปิดใน Office Online
- แก้ไขพร้อมกันได้หลายคน
- เห็นคนอื่นแก้ไข real-time
- บันทึกอัตโนมัติ

### เคล็ดลับ Teams

**Status:**
- **Available**: ว่างพร้อมทำงาน
- **Busy**: ไม่ว่าง
- **Do not disturb**: อย่ารบกวน (แจ้งเตือนเฉพาะสำคัญ)
- **Away**: ไม่อยู่
- **Appear offline**: ซ่อนตัว

**Keyboard Shortcuts:**
- Ctrl + E: Search
- Ctrl + 1: Activity
- Ctrl + 2: Chat
- Ctrl + 3: Teams
- Ctrl + 4: Calendar
- Ctrl + 5: Calls
- Ctrl + N: New Chat/Call
- Ctrl + Shift + M: Mute/Unmute (ในการประชุม)
- Ctrl + Shift + O: Video on/off (ในการประชุม)

**Notifications:**
- Settings > Notifications
- ปรับการแจ้งเตือนสำหรับแต่ละ Team/Channel
- ตั้งเวลา Quiet hours (ไม่แจ้งเตือน)

---

## 3. OneDrive for Business

### การตั้งค่าเริ่มต้น

**การติดตั้ง:**
1. ติดตั้ง OneDrive มากับ Windows 10/11
2. คลิกไอคอน Cloud ที่ Taskbar
3. Sign in ด้วย yourname@company.com
4. เลือก folder location (ค่า default: C:\Users\YourName\OneDrive - Company)
5. เลือก folders ที่จะ sync
6. Done

### การใช้งานพื้นฐาน

**การบันทึกไฟล์:**
- บันทึกไฟล์ไปที่ OneDrive - Company
- ไฟล์จะ sync ขึ้น cloud อัตโนมัติ
- เข้าถึงได้จากอุปกรณ์อื่น

**Files On-Demand:**
- ไฟล์ที่ไม่ได้ใช้จะอยู่ใน cloud อย่างเดียว (ไอคอน cloud)
- เปิดใช้งานจะดาวน์โหลดอัตโนมัติ
- ประหยัดพื้นที่ฮาร์ดดิสก์
- ตั้งค่าที่: OneDrive Settings > Settings > Files On-Demand

**การแชร์ไฟล์:**

**จาก File Explorer:**
1. คลิกขวาที่ไฟล์
2. เลือก Share
3. พิมพ์ชื่อหรืออีเมลคนที่จะแชร์
4. เลือกสิทธิ์: Can edit หรือ Can view
5. Send

**จากเว็บ:**
1. ไปที่ office.com > OneDrive
2. เลือกไฟล์
3. คลิก Share
4. Copy link หรือส่งอีเมล
5. ตั้งค่าสิทธิ์และ expiration date
6. Apply

**การทำงานร่วมกัน:**
- แก้ไขไฟล์พร้อมกันได้หลายคน
- เห็น Real-time changes
- AutoSave เปิดโดยอัตโนมัติ
- Version History: คลิกขวา > Version history

### การกู้คืนไฟล์

**Recycle Bin:**
1. เปิด OneDrive บนเว็บ
2. คลิก Recycle bin (ซ้ายมือ)
3. เลือกไฟล์ที่จะกู้คืน
4. คลิก Restore

**File Restore (กรณี Ransomware):**
1. OneDrive.com > Settings > Restore your OneDrive
2. เลือกวันที่ที่ต้องการย้อนกลับ
3. Restore
4. ไฟล์ทั้งหมดจะกลับไปเป็นวันนั้น

### เคล็ดลับ OneDrive

**การตรวจสอบ Sync:**
- ไอคอน OneDrive ที่ Taskbar:
  - เมฆสีขาว: Sync เสร็จแล้ว
  - เมฆสีฟ้าวนซิงค์: กำลัง sync
  - X แดง: มีปัญหา

**การแก้ปัญหา Sync:**
1. คลิก OneDrive icon
2. Settings > Pause syncing (เลือกเวลา)
3. Resume syncing
4. ถ้ายังไม่ได้ลอง Restart OneDrive
5. Settings > Quit OneDrive > เปิดใหม่

**Storage Quota:**
- เช็คได้ที่ OneDrive icon > Settings > Account
- ค่า default: 1TB
- ถ้าใกล้เต็มให้ลบไฟล์ไม่จำเป็น
- หรือย้ายไฟล์ไปที่ SharePoint

---

## 4. SharePoint

### SharePoint คืออะไร

SharePoint เป็นที่เก็บเอกสารส่วนกลางสำหรับทีม มีการจัดการเอกสารและ workflow

### การเข้าถึง SharePoint

**ผ่าน Teams:**
- ไฟล์ใน Teams Channel ทั้งหมดเก็บอยู่ใน SharePoint
- คลิก Files > Open in SharePoint

**ผ่านเว็บ:**
- ไปที่ office.com
- คลิก SharePoint (ซ้ายมือ)
- เลือก Site ที่ต้องการ

### การทำงานกับเอกสาร

**การอัปโหลด:**
1. ไปที่ Document Library
2. คลิก Upload
3. เลือก Files หรือ Folder
4. เลือกไฟล์
5. Upload

**การสร้าง folder:**
1. ไปที่ Document Library
2. คลิก New > Folder
3. พิมพ์ชื่อ folder
4. Create

**การจัดระเบียบ:**
- สร้าง folder structure ที่ชัดเจน
- ใช้ชื่อไฟล์ที่เข้าใจง่าย
- ใช้ Metadata tags
- ใช้ Version control

### Permissions

**ระดับสิทธิ์:**
- **Full Control**: ทำอะไรก็ได้
- **Edit**: แก้ไขเอกสารได้
- **Contribute**: สร้างและแก้ไขของตัวเองได้
- **Read**: อ่านอย่างเดียว

**การแชร์ folder:**
1. เลือก folder
2. คลิก Share
3. พิมพ์ชื่อคนที่จะแชร์
4. เลือกสิทธิ์
5. Send

### Version History

**การดู Version:**
1. คลิกขวาที่ไฟล์
2. เลือก Version history
3. เห็นรายการทุก version
4. คลิกวันที่เพื่อดู/เปิดไฟล์

**การกู้คืน Version:**
1. Version history
2. คลิกลูกศรข้าง version ที่ต้องการ
3. Restore

---

## 5. Microsoft Office Suite

### Word

**การทำงานร่วมกัน:**
- บันทึกไฟล์ใน OneDrive/SharePoint
- Share ไฟล์ให้คนอื่น
- คนอื่นเห็นคุณแก้ไข real-time
- แต่ละคนมีสี cursor แตกต่างกัน
- Comments: Review > New Comment

**Keyboard Shortcuts:**
- Ctrl + B: Bold
- Ctrl + I: Italic
- Ctrl + U: Underline
- Ctrl + E: Center align
- Ctrl + L: Left align
- Ctrl + R: Right align
- Ctrl + K: Insert hyperlink
- Ctrl + F: Find
- Ctrl + H: Replace
- Ctrl + Z: Undo
- Ctrl + Y: Redo

**Styles:**
- Home > Styles
- ใช้ Heading 1, 2, 3 สำหรับหัวข้อ
- สร้าง Table of Contents อัตโนมัติได้

### Excel

**พื้นฐาน:**
- **Formula เริ่มด้วย =**: =A1+B1
- **Functions**: =SUM(A1:A10)
- **AutoFill**: ลากมุมขวาล่างของ cell
- **Format as Table**: Home > Format as Table

**Functions ที่ใช้บ่อย:**
- `=SUM(range)`: รวม
- `=AVERAGE(range)`: หาค่าเฉลี่ย
- `=COUNT(range)`: นับตัวเลข
- `=IF(condition, true, false)`: เงื่อนไข
- `=VLOOKUP(value, table, col, FALSE)`: ค้นหา
- `=CONCATENATE(text1, text2)`: รวมข้อความ

**Pivot Tables:**
1. เลือกข้อมูล
2. Insert > PivotTable
3. เลือก location
4. ลาก fields ไปที่ Rows, Columns, Values
5. วิเคราะห์ข้อมูล

**Keyboard Shortcuts:**
- Ctrl + Arrow: ข้ามไปสุดข้อมูล
- Ctrl + Shift + Arrow: เลือกทั้ง range
- Ctrl + ;: ใส่วันที่วันนี้
- Ctrl + : ใส่เวลาตอนนี้
- F2: Edit cell

### PowerPoint

**การออกแบบ:**
- Design > Themes: เลือกธีม
- Design > Slide Size: เลือกขนาด (16:9 แนะนำ)
- Layout: Home > Layout

**การใส่เนื้อหา:**
- **Text**: คลิก Text Box
- **Picture**: Insert > Pictures
- **Chart**: Insert > Chart
- **Table**: Insert > Table
- **Video**: Insert > Video

**การนำเสนอ:**
- F5: เริ่มจากต้น
- Shift + F5: เริ่มจาก slide ปัจจุบัน
- Esc: ออกจากโหมดนำเสนอ
- B: หน้าจอดำ
- W: หน้าจอขาว
- Ctrl + P: ใช้ Pen
- Ctrl + A: ใช้ Arrow

**Presenter View:**
- Alt + F5: เปิด Presenter View
- เห็น notes, slide ถัดไป, timer
- คนดูเห็นแค่ slide

---

## 6. การแก้ปัญหาทั่วไป

### AutoSave ไม่ทำงาน

**สาเหตุ:**
- ไฟล์อยู่ local ไม่ได้อยู่ใน OneDrive/SharePoint
- ไฟล์เป็น Compatibility Mode (.xls, .doc เก่า)
- ไม่ได้ Sign in Office

**วิธีแก้:**
1. บันทึกไฟล์ไปที่ OneDrive
2. Save as แบบใหม่ (.xlsx, .docx)
3. Sign in: File > Account > Sign in

### ไฟล์เปิดเป็น Read-Only

**สาเหตุ:**
- ไม่มีสิทธิ์แก้ไข
- คนอื่นเปิดอยู่แล้ว (ไฟล์ local)
- ไฟล์ถูก Lock

**วิธีแก้:**
1. ขอสิทธิ์จากเจ้าของไฟล์
2. Save as เป็นชื่อใหม่
3. รอคนอื่นปิดไฟล์
4. ใช้ OneDrive จะแก้ไขพร้อมกันได้

### ไม่เห็น Teams/Channels

**วิธีแก้:**
1. เช็คว่าถูกเพิ่มเข้า Team แล้ว
2. Teams > Show hidden teams
3. Refresh: Ctrl + R
4. Sign out and sign in again
5. ติดต่อเจ้าของ Team เพื่อเพิ่มคุณ

---

## 7. ติดต่อขอความช่วยเหลือ

### IT Helpdesk
- **โทรศัพท์**: ext. 1234 หรือ +66-2-XXX-XXXX
- **อีเมล**: helpdesk@company.com
- **เวลาทำการ**: จันทร์-ศุกร์ 8:00-18:00

### IT Portal
- **URL**: https://itportal.company.com
- **สำหรับ**: คู่มือ, FAQ, Software requests

### Microsoft Support
- **ใน Office apps**: Help > Contact Support
- **Online**: support.microsoft.com

---

## 8. Resources เพิ่มเติม

### Video Tutorials
- Microsoft 365 Training: support.microsoft.com/training
- LinkedIn Learning: บริษัทมี subscription

### Quick Reference Guides
- ดาวน์โหลดได้จาก IT Portal > Resources
- PDF คู่มือย่อสำหรับ Office apps

### Practice Files
- ไฟล์ตัวอย่างสำหรับฝึกซ้อมใน SharePoint > Training Materials

---

*เอกสารนี้อัพเดทเป็นประจำ | ปรับปรุงล่าสุด: ตุลาคม 2568*
*เวอร์ชั่น: 1.0*

