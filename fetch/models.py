import json
from dataclasses import dataclass, field

@dataclass
class Course:
    '''Class for representing a course taken by a student in a particular semester'''
    name: str
    code: str
    course_credits: int
    grade: str


@dataclass
class Semester:
    '''Class for representing a particular semester for any student'''
    number: int
    courses: list[Course] = field(default_factory=list)
    earned_credit: int
    sgpa: float
    cgpa: float


@dataclass
class Student():
    '''Class for representing a Student'''
    name: str
    roll_no: str
    program: str 
    branch: str
    cgpa: float
    semesters: list[Semester] = field(default_factory=list)
    
    def to_json(self):
        return json.jumps(self.__dict__, default=lambda x: x.__dict__, indent=4)