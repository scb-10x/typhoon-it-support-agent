"""Constants for routing decisions."""

COMPLETION_PHRASES_EN = [
    "resolved",
    "solved",
    "fixed",
    "completed",
]

COMPLETION_PHRASES_TH = [
    "แก้ไขแล้ว",
    "เรียบร้อย",
    "สำเร็จ",
    "ใช้งานได้แล้ว",
    "แก้ไข",
    "เสร็จ",
    "ใช้ได้",
]

ESCALATION_PHRASES_EN = [
    "cannot",
    "unable",
    "escalate",
    "supervisor",
]

ESCALATION_PHRASES_TH = [
    "ไม่สามารถ",
    "ต้องการความช่วยเหลือ",
    "ปัญหาซับซ้อน",
    "ติดต่อผู้เชี่ยวชาญ",
    "ส่งต่อ",
]

COMPLETION_PHRASES = COMPLETION_PHRASES_EN + COMPLETION_PHRASES_TH
ESCALATION_PHRASES = ESCALATION_PHRASES_EN + ESCALATION_PHRASES_TH



