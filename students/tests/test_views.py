import random
from django.test import TestCase
from django.urls import reverse

from students.models import Student


class TestViews(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_number=12345678,
            first_name="John",
            last_name="Smith",
            email_address="johnsmith@example.com",
            field_of_study="N/A",
            gpa=2.0,
        )
        self.index_url = reverse("students:index")
        self.view_student_url = reverse("students:view_student", args=[self.student.id])

    def test_index_view_GET(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/index.html")
        # Check if context contains students
        self.assertContains(response, self.student)

    def test_view_student_view_GET(self):
        response = self.client.get(self.view_student_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

    def test_add_view_GET(self):
        response = self.client.get(reverse("students:add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/add.html")
        # Check if context contains form
        self.assertTrue(response.context["form"])

    def test_add_view_POST(self):
        student_number = random.randint(10000000, 99999999)
        response = self.client.post(
            reverse("students:add"),
            {
                "student_number": student_number,
                "first_name": "John",
                "last_name": "Smith",
                "email_address": "js@example.com",
                "field_of_study": "Computer Science",
                "gpa": 3.0,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/add.html")
        # Check if context contains form
        self.assertTrue(response.context["form"])
        # Check if context contains success
        self.assertTrue(response.context["success"])
        # Check if student is created
        self.assertTrue(Student.objects.get(student_number=student_number))

    def test_add_view_POST_invalid(self):
        response = self.client.post(
            reverse("students:add"),
            {
                "student_number": "abc",
                "first_name": "John",
                "last_name": "Smith",
                "email_address": "abc",
                "field_of_study": "Computer Science",
                "gpa": "abc",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/add.html")
        # Check if context contains form
        self.assertTrue(response.context["form"])
        # Check if context contains success
        self.assertFalse(response.context.get("success", False))
        # Check if student is created
        with self.assertRaises(
            ValueError
        ):  # System will raise ValueError if student because student_number is not an integer
            Student.objects.get(student_number="abc")

    def test_edit_view_GET(self):
        response = self.client.get(reverse("students:edit", args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/edit.html")
        # Check if context contains form
        self.assertTrue(response.context["form"])
        # Check if context contains student

    def test_edit_view_POST(self):
        response = self.client.post(
            reverse("students:edit", args=[self.student.id]),
            {
                "student_number": self.student.student_number,
                "first_name": "John",
                "last_name": "Smithy",
                "email_address": "edit@example.com",
                "field_of_study": "Computer Science",
                "gpa": 3.0,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/edit.html")
        # Check if context contains form
        self.assertTrue(response.context["form"])
        # Check if success is in context
        self.assertTrue(response.context.get("success", False))
        # Check if student is updated
        student = Student.objects.get(pk=self.student.id)
        self.assertEqual(student.last_name, "Smithy")
        self.assertEqual(student.email_address, "edit@example.com")
        self.assertEqual(student.field_of_study, "Computer Science")
        self.assertEqual(student.gpa, 3.0)

    def test_edit_view_POST_invalid(self):
        response = self.client.post(
            reverse("students:edit", args=[self.student.id]),
            {
                "student_number": self.student.student_number,
                "first_name": "John",
                "last_name": "Smithy",
                "email_address": "",
                "field_of_study": "Computer Science",
                "gpa": 3.0,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/edit.html")
        # Check if context contains form
        self.assertTrue(response.context["form"])
        # Check if success is not in context
        self.assertFalse(response.context.get("success", False))
        # Check if not student is updated because email_address is empty
        student = Student.objects.get(pk=self.student.id)
        self.assertFalse(
            student.email_address == ""
        )  # False because email_address is not empty

    def test_delete_view_GET(self):
        response = self.client.get(reverse("students:delete", args=[self.student.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        # Check if student is not deleted
        self.assertTrue(Student.objects.get(pk=self.student.id))

    def test_delete_view_POST(self):
        response = self.client.post(reverse("students:delete", args=[self.student.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        # Check if student is deleted
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=self.student.id)
