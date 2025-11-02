"""Initialize demo tickets for showcase."""

from datetime import datetime, timedelta

from ..config.user_context import get_current_user
from ..tools.ticket_tools import (
    AVAILABLE_AGENTS,
    _calculate_sla_targets,
    _check_sla_breach,
    _mock_tickets,
    _ticket_counter,
)


def initialize_demo_tickets():
    """Add sample tickets for demo purposes."""
    global _ticket_counter

    # Clear existing tickets
    _mock_tickets.clear()

    # Get current user for realistic demo data
    current_user = get_current_user()

    # Sample tickets with varied statuses and priorities
    sample_tickets = [
        {
            "subject": "ขอความช่วยเหลือการใช้ Canva Pro สำหรับ Campaign",
            "description": "สวัสดีครับ ผมต้องการใช้ Canva Pro เพื่อออกแบบ banner และ social media content สำหรับ campaign ใหม่ แต่ยังไม่มี account ขอความช่วยเหลือในการขอ license ด้วยครับ",
            "priority": "normal",
            "status": "pending",
            "requester_name": current_user.display_name,
            "requester_email": current_user.email,
            "created_at": (datetime.now() - timedelta(hours=3)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "สวัสดีค่ะคุณชาย ดิฉันได้ส่งคำขอจัดซื้อ license Canva Pro ไปยังฝ่ายจัดซื้อแล้วนะคะ รอประมาณ 2-3 วันทำการค่ะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(hours=2, minutes=30)
                    ).isoformat(),
                }
            ],
        },
        {
            "subject": "ไม่สามารถเข้าสู่ระบบ Email ได้",
            "description": "พยายามเข้าสู่ระบบ email หลายครั้งแล้วแต่ไม่สำเร็จ แสดงข้อความว่า 'Invalid credentials'",
            "priority": "high",
            "status": "open",
            "requester_name": "วริษา จันทร์สว่าง",
            "requester_email": "warisa.c@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "กำลังตรวจสอบบัญชี email ของคุณ กรุณารอสักครู่ค่ะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(hours=1, minutes=30)
                    ).isoformat(),
                }
            ],
        },
        {
            "subject": "Internet ช้าตอน Upload ไฟล์ขนาดใหญ่",
            "description": "เวลา upload ไฟล์วิดีโอขนาดใหญ่ขึ้น Google Drive หรือ Dropbox ช้ามาก ใช้เวลานานมาก แต่ download เร็วปกติครับ มีวิธีแก้ไขหรือไม่ครับ",
            "priority": "normal",
            "status": "solved",
            "requester_name": current_user.display_name,
            "requester_email": current_user.email,
            "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "ตรวจสอบแล้วพบว่า bandwidth upload ถูกจำกัดที่ router ค่ะ ดิฉันได้ปรับตั้งค่าให้เพิ่มขึ้นแล้ว ลองใช้งานดูนะคะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(days=1, hours=20)
                    ).isoformat(),
                },
                {
                    "author": current_user.display_name,
                    "body": "ขอบคุณครับ เร็วขึ้นมากเลยครับ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(days=1, hours=18)
                    ).isoformat(),
                },
            ],
        },
        {
            "subject": "คอมพิวเตอร์ทำงานช้ามาก",
            "description": "คอมพิวเตอร์ใช้เวลาเปิดโปรแกรมนาน และค้างบ่อย RAM ใช้ไปเกือบเต็มแม้ไม่ได้เปิดโปรแกรมมาก",
            "priority": "normal",
            "status": "pending",
            "requester_name": "อรุณี สว่างไสว",
            "requester_email": "arunee.s@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "comments": [],
        },
        {
            "subject": "ขอสิทธิ์ Admin สำหรับติดตั้ง Software",
            "description": "ต้องการติดตั้งโปรแกรม Adobe Creative Suite เพื่อใช้ในการทำงาน ต้องการสิทธิ์ Admin ชั่วคราว",
            "priority": "normal",
            "status": "new",
            "requester_name": "ธนพล ภาพดี",
            "requester_email": "thanapol.p@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "comments": [],
        },
        {
            "subject": "เครื่องพิมพ์ไม่ตอบสนอง",
            "description": "เครื่องพิมพ์ชั้น 15 ส่งงานพิมพ์ไปแล้วแต่ไม่มีการพิมพ์ออกมา ไฟสีเหลืองกระพริบอยู่",
            "priority": "urgent",
            "status": "open",
            "requester_name": "ปิยะ วงศ์สว่าง",
            "requester_email": "piya.w@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(hours=4)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "ทีมงานกำลังไปตรวจสอบที่เครื่องพิมพ์ค่ะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(hours=3, minutes=45)
                    ).isoformat(),
                },
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "พบว่ากระดาษติดในเครื่อง กำลังดำเนินการแก้ไขค่ะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(hours=3, minutes=30)
                    ).isoformat(),
                },
            ],
        },
        {
            "subject": "ขอ VPN Access สำหรับ Work from Home",
            "description": "ต้องการเข้าถึงระบบภายในบริษัทจากที่บ้าน กรุณาตั้งค่า VPN และส่ง credentials",
            "priority": "normal",
            "status": "solved",
            "requester_name": "ศิริพร ทำงานไกล",
            "requester_email": "siriporn.t@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "ได้ตั้งค่า VPN account เรียบร้อยแล้วค่ะ กรุณาตรวจสอบ email สำหรับ credentials",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(days=1, hours=20)
                    ).isoformat(),
                },
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "ปิด ticket เนื่องจากผู้ใช้ยืนยันว่าใช้งานได้แล้วค่ะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(days=1, hours=18)
                    ).isoformat(),
                },
            ],
        },
        {
            "subject": "WiFi ขาดๆ หายๆ ในห้องประชุม B",
            "description": "สัญญาณ WiFi ในห้องประชุม B ไม่เสถียร หลุดบ่อยมาก ส่งผลกระทบต่อการประชุมออนไลน์",
            "priority": "high",
            "status": "open",
            "requester_name": "ชัยวัฒน์ ประชุมสุข",
            "requester_email": "chaiwat.p@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(hours=6)).isoformat(),
            "comments": [],
        },
        {
            "subject": "Reset รหัสผ่าน Windows",
            "description": "ลืมรหัสผ่าน Windows ขอ reset รหัสผ่านใหม่ครับ",
            "priority": "high",
            "status": "solved",
            "requester_name": "มนัสนันท์ รื่นรมย์",
            "requester_email": "manassanan.r@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(hours=8)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "ได้ทำการ reset รหัสผ่านเรียบร้อยค่ะ รหัสผ่านชั่วคราวคือ: TempPass123! กรุณาเปลี่ยนรหัสผ่านหลังจาก login ครั้งแรกนะคะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(hours=7, minutes=45)
                    ).isoformat(),
                }
            ],
        },
        {
            "subject": "ขอเพิ่ม Storage Space OneDrive",
            "description": "OneDrive เต็มแล้ว ไม่สามารถ sync ไฟล์ได้ ขอเพิ่มพื้นที่ Storage",
            "priority": "normal",
            "status": "pending",
            "requester_name": "ภัทรพล จัดเก็บ",
            "requester_email": "phattharaphon.j@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(days=1, hours=12)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "ได้ส่งคำขออนุมัติเพิ่ม storage ไปยังฝ่าย IT Admin แล้วค่ะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(days=1, hours=10)
                    ).isoformat(),
                }
            ],
        },
        {
            "subject": "Microsoft Teams ไม่สามารถแชร์หน้าจอได้",
            "description": "เมื่อพยายามแชร์หน้าจอใน Teams แล้วผู้อื่นไม่เห็น แสดงหน้าจอดำ",
            "priority": "normal",
            "status": "closed",
            "requester_name": "สุดารัตน์ ชัยศรี",
            "requester_email": "sudarat.c@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
            "comments": [
                {
                    "author": "น้องเทค (IT Support)",
                    "body": "ปัญหาเกิดจาก permission ของ Windows ค่ะ ได้แก้ไขโดยอนุญาต Teams ให้ capture screen แล้วค่ะ",
                    "public": True,
                    "created_at": (
                        datetime.now() - timedelta(days=2, hours=22)
                    ).isoformat(),
                }
            ],
        },
        {
            "subject": "แป้นพิมพ์บางปุ่มใช้ไม่ได้",
            "description": "แป้นพิมพ์ปุ่ม E, R, T กดแล้วไม่ขึ้น อยากขอเปลี่ยนแป้นพิมพ์ใหม่",
            "priority": "low",
            "status": "new",
            "requester_name": "กิตติพงษ์ พิมพ์ดี",
            "requester_email": "kittipong.p@bluewave-tech.co.th",
            "created_at": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "comments": [],
        },
    ]

    # Add tickets to the system
    for idx, ticket_data in enumerate(sample_tickets):
        ticket_id = _ticket_counter["value"]
        _ticket_counter["value"] += 1

        created_at = ticket_data["created_at"]

        # Calculate SLA targets
        sla_targets = _calculate_sla_targets(ticket_data["priority"], created_at)

        # Determine first response and resolution times
        comments = ticket_data.get("comments", [])
        first_response_at = comments[0]["created_at"] if comments else None
        resolved_at = (
            created_at if ticket_data["status"] in ["solved", "closed"] else None
        )

        # Assign to agents based on category
        assignee = None
        category = "other"
        tags = []

        # Smart categorization and assignment based on subject
        subject_lower = ticket_data["subject"].lower()
        if "email" in subject_lower or "เข้าสู่ระบบ" in subject_lower:
            category = "email"
            assignee = AVAILABLE_AGENTS[0]
            tags = ["email", "login"]
        elif (
            "internet" in subject_lower
            or "wifi" in subject_lower
            or "network" in subject_lower
        ):
            category = "network"
            assignee = AVAILABLE_AGENTS[2]
            tags = ["network", "connectivity"]
        elif "printer" in subject_lower or "เครื่องพิมพ์" in subject_lower:
            category = "printer"
            assignee = AVAILABLE_AGENTS[0]
            tags = ["printer", "hardware"]
        elif "vpn" in subject_lower:
            category = "vpn"
            assignee = AVAILABLE_AGENTS[3]
            tags = ["vpn", "remote-access"]
        elif "password" in subject_lower or "รหัสผ่าน" in subject_lower:
            category = "account_access"
            assignee = AVAILABLE_AGENTS[1]
            tags = ["password", "account"]
        elif (
            "software" in subject_lower
            or "canva" in subject_lower
            or "adobe" in subject_lower
        ):
            category = "software"
            assignee = AVAILABLE_AGENTS[0]
            tags = ["software", "license"]
        elif "computer" in subject_lower or "คอมพิวเตอร์" in subject_lower:
            category = "hardware"
            assignee = AVAILABLE_AGENTS[0]
            tags = ["hardware", "performance"]
        elif "admin" in subject_lower or "สิทธิ์" in subject_lower:
            category = "account_access"
            assignee = AVAILABLE_AGENTS[1]
            tags = ["permissions", "admin"]
        elif "storage" in subject_lower or "onedrive" in subject_lower:
            category = "software"
            assignee = AVAILABLE_AGENTS[0]
            tags = ["storage", "cloud"]
        elif "teams" in subject_lower:
            category = "software"
            assignee = AVAILABLE_AGENTS[0]
            tags = ["teams", "collaboration"]

        # Add priority tag
        if ticket_data["priority"] == "urgent":
            tags.append("urgent")

        # Calculate due date based on priority and status
        due_date = None
        if ticket_data["status"] not in ["solved", "closed"]:
            if ticket_data["priority"] == "urgent":
                due_date = (
                    datetime.fromisoformat(created_at) + timedelta(hours=4)
                ).isoformat()
            elif ticket_data["priority"] == "high":
                due_date = (
                    datetime.fromisoformat(created_at) + timedelta(hours=8)
                ).isoformat()
            elif ticket_data["priority"] == "normal":
                due_date = (
                    datetime.fromisoformat(created_at) + timedelta(days=1)
                ).isoformat()
            else:
                due_date = (
                    datetime.fromisoformat(created_at) + timedelta(days=2)
                ).isoformat()

        ticket = {
            "id": ticket_id,
            "subject": ticket_data["subject"],
            "description": ticket_data["description"],
            "priority": ticket_data["priority"],
            "status": ticket_data["status"],
            "requester_name": ticket_data["requester_name"],
            "requester_email": ticket_data["requester_email"],
            "created_at": created_at,
            "updated_at": datetime.now().isoformat(),
            "comments": comments,
            "assignee_id": assignee["id"] if assignee else None,
            "assignee_name": assignee["name"] if assignee else None,
            "tags": tags,
            "category": category,
            "due_date": due_date,
            "first_response_at": first_response_at,
            "resolved_at": resolved_at,
            "sla_first_response_due": sla_targets["first_response_due"],
            "sla_resolution_due": sla_targets["resolution_due"],
            "sla_breach": _check_sla_breach(
                created_at, ticket_data["priority"], first_response_at, resolved_at
            ),
            "history": [
                {
                    "timestamp": created_at,
                    "action": "created",
                    "actor": ticket_data["requester_name"],
                    "changes": {"status": "new", "priority": ticket_data["priority"]},
                }
            ],
        }

        # Add assignment history if assigned
        if assignee:
            ticket["history"].append(
                {
                    "timestamp": created_at,
                    "action": "assigned",
                    "actor": "System",
                    "changes": {"assignee": {"old": None, "new": assignee["name"]}},
                }
            )

        _mock_tickets[ticket_id] = ticket

    return len(_mock_tickets)
