from enum import IntEnum, Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Level(IntEnum):
    L100 = 100
    L200 = 200
    L300 = 300
    L400 = 400
    L500 = 500
    L600 = 600
    L700 = 700


class AdmissionMode(str, Enum):
    UTME = "utme"
    DIRECT_ENTRY = "direct_entry"


class CreateClassSchema(BaseModel):
    display_name: str | None
    level: Level
    department_id: UUID


class UpdateClassSchema(CreateClassSchema):
    governor_id: Optional[UUID]
    deputy_id: Optional[UUID]


class CreateStudentSchema(BaseModel):
    class_id: UUID
    first_name: str
    middle_name: str
    last_name: str
    admission_mode: AdmissionMode
    matriculation_number: str | None  # TODO: validate
    jamb_registration_number: str | None  # TODO: validate
    personal_email_address: EmailStr


class StudentSchema(BaseModel):
    class_id: UUID
    first_name: str
    middle_name: str
    last_name: str
    admission_mode: AdmissionMode
    matriculation_number: str | None  # TODO: validate
    jamb_registration_number: str | None  # TODO: validate
    personal_email_address: EmailStr
    school_email_address: EmailStr | None


class PhoneNumberAvailability(str, Enum):
    CALLS = "CALLS"
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"


class PhoneNumberSchema(BaseModel):
    number: str  # TODO: validate
    availability: list[PhoneNumberAvailability]


class CreateUpdateSchoolSchema(BaseModel):
    name: str


class SchoolSchema(BaseModel):
    id: UUID
    name: str


class FacultySchema(BaseModel):
    id: UUID
    name: str
    school_id: UUID
    departments: list["DepartmentSchema"]


class CreateUpdateFacultySchema(BaseModel):
    school_id: UUID
    name: str


class DepartmentSchema(BaseModel):
    id: UUID
    name: str
    faculty_id: UUID


class CreateUpdateDepartmentSchema(BaseModel):
    faculty_id: UUID
    name: str


class ClassSchema(BaseModel):
    id: UUID
    display_name: str | None
    level: Level
    department_id: UUID
    governor_id: Optional[UUID]
    deputy_id: Optional[UUID]


class ResponseSchema(BaseModel):
    message: str | None
    data: dict | list | None
