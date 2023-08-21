from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4
from enum import IntEnum, Enum

class Level(IntEnum):
    L100=100
    L200=200
    L300=300
    L400=400
    L500=500
    L600=600
    L700=700


class AdmissionMode(str, Enum):
    UTME = "utme"
    DIRECT_ENTRY = "de"


class ClassSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    display_name: str
    level: Level
    faculty: str
    department: str
    governor: "StudentSchema" | None
    deputy: "StudentScheme" | None

class StudentScheme(BaseModel):
    id: Field(default_factory=uuid4)
    class_id: UUID
    first_name: str
    middle_name: str
    last_name: str
    admission_mode: AdmissionMode
    matric_no: Optional[str] # TODO: validate
    reg_no: Optional[str] # TODO: validate
    personal_email_address: EmailStr
    school_email_address: EmailStr

class PhoneNumberAvailability(str, Enum):
    CALLS = "CALLS"
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"

class PhoneNumberSchema(BaseModel):
    number: str # TODO: validate
    availability: list[PhoneNumberAvailability]
