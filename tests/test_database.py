import unittest
from database.models import Course, Semester, Student


class CourseTestCase(unittest.TestCase):
    def setUp(self):
        self.course = Course(
            name = "Operating System",
            code = "123",
            course_credits = 4,
            grade = "B+"
        )

    def tearDown(self):
        self.course = None


class SemesterTestCase(unittest.TestCase):
    def setUp(self):
        self.course = Course(
            name = "Operating System",
            code = "123",
            course_credits = 4,
            grade = "B+"
        )
        self.semester = Semester(
            number = 1,
            earned_credits = 4,
            sgpa = 8,
            cgpa = 8,
            courses = [self.course]
        )
    
    def tearDown(self):
        self.course = None
        self.semester = None

    def test_semester_course(self):
        self.assertNotEqual(len(self.semester.courses), 0)
        self.assertEqual(sum([course.course_credits for course in self.semester.courses]), self.semester.earned_credits)


class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.course = Course(
            name = "Operating System",
            code = "123",
            course_credits = 4,
            grade = "B+"
        )
        self.semester = Semester(
            number = 1,
            earned_credits = 4,
            sgpa = 8,
            cgpa = 8,
            courses = [self.course]
        )
        self.student = Student(
            name = "Rahul Dev Kureel",
            roll_no = "181210039",
            program = "B.Tech.",
            branch = "CSE",
            cgpa = 8,
            semesters = [self.semester]
        )

    def tearDown(self):
        self.student = None
        self.semester = None
        self.course = None
    
    def test_student(self):
        self.assertEqual(self.student.semesters[-1].cgpa, self.student.cgpa)
        self.assertNotEqual(len(self.student.semesters), 0)


if __name__ == "__main__":
    unittest.main()