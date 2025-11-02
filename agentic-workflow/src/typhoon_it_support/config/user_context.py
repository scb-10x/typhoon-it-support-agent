"""Mock user context for hypothetical Thai employee in a logged-in state."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class UserProfile:
    """User profile information for the logged-in employee."""

    employee_id: str
    email: str
    full_name_th: str
    full_name_en: str
    nickname: str
    department: str
    position: str
    phone: str
    office_location: str
    manager: str
    joined_date: str

    def to_dict(self) -> Dict[str, str]:
        """Convert user profile to dictionary."""
        return {
            "employee_id": self.employee_id,
            "email": self.email,
            "full_name_th": self.full_name_th,
            "full_name_en": self.full_name_en,
            "nickname": self.nickname,
            "department": self.department,
            "position": self.position,
            "phone": self.phone,
            "office_location": self.office_location,
            "manager": self.manager,
            "joined_date": self.joined_date,
        }

    @property
    def display_name(self) -> str:
        """Get display name (Thai name with nickname)."""
        return f"{self.full_name_th} ({self.nickname})"

    @property
    def display_name_en(self) -> str:
        """Get display name (English name)."""
        return self.full_name_en


MOCK_USER_PROFILE = UserProfile(
    employee_id="EMP2024-0158",
    email="somchai.p@bluewave-tech.co.th",
    full_name_th="สมชาย พิมพ์สวัสดิ์",
    full_name_en="Somchai Phimsawat",
    nickname="ชาย",
    department="Marketing & Communications",
    position="Digital Marketing Specialist",
    phone="+66 82 345 6789",
    office_location="Bangkok Office, 15th Floor",
    manager="คุณนภา จันทร์เจริญ (Napa Chancharoen)",
    joined_date="2024-03-15",
)


COMPANY_INFO = {
    "name_th": "บริษัท บลูเวฟ เทคโนโลยี จำกัด",
    "name_en": "BlueWave Technology Co., Ltd.",
    "address_th": "เลขที่ 123/45 อาคารไอที ทาวเวอร์ ชั้น 15 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพมหานคร 10110",
    "address_en": "123/45 IT Tower, 15th Floor, Sukhumvit Road, Khlong Toei, Bangkok 10110",
    "phone": "+66 2 345 6789",
    "website": "https://bluewave-tech.co.th",
    "industry": "Software Development & IT Consulting",
    "size": "250-500 employees",
}


def get_current_user() -> UserProfile:
    """Get the current logged-in user profile.

    In a real application, this would retrieve the user from session/JWT token.
    For this hypothetical scenario, we return the mock user.
    """
    return MOCK_USER_PROFILE


def get_company_info() -> Dict[str, str]:
    """Get company information.

    Returns company details for the hypothetical organization.
    """
    return COMPANY_INFO
