from django.db import IntegrityError
from django.test import TestCase

from students.models import Student


class TestModels(TestCase):
    def test_student_model(self):
        # Create a student object
        student = Student.objects.create(
            student_number=12345678,
            first_name="John",
            last_name="Smith",
            email_address="johnsmith@example.com",
            field_of_study="N/A",
            gpa=3.0,
        )

        # Check that the student object is created
        self.assertEqual(student.student_number, 12345678)
        self.assertEqual(student.first_name, "John")
        self.assertEqual(student.last_name, "Smith")
        self.assertEqual(student.email_address, "johnsmith@example.com")
        self.assertEqual(student.field_of_study, "N/A")
        self.assertEqual(student.gpa, 3.0)
        self.assertEqual(str(student), "Student: John Smith")

    def test_student_model_no_student_number(self):
        # Should raise an error if no student number is provided
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                first_name="John",
                last_name="Smith",
                email_address="johnsmith@example.com",
                field_of_study="N/A",
                gpa=3.0,
            )
