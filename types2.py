from dataclasses import dataclass
from typing import Optional

@dataclass
class Course:
    code: str
    title: str

@dataclass
class Course1:
    code: str
    title: str
    studiepoeng: float
    semester: str
    semester_count: int
    language: str

    exam_type: Optional[str]
    exam_date: Optional[str]
    trekkfrist: Optional[str]
    exam_duration: Optional[int]

    required: str
    recommended: str

    department: str

    fulltime: bool

    mål: str
