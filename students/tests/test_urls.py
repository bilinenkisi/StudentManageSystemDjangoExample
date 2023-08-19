from django.urls import reverse
from django.test import SimpleTestCase
from django.urls import resolve
from students.views import delete, edit, index, view_student, add


class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse("students:index")
        self.assertEquals(resolve(url).func, index)

    def test_view_student_url_resolves(self):
        url = reverse("students:view_student", args=[1])
        self.assertEquals(resolve(url).func, view_student)

    def test_add_url_resolves(self):
        url = reverse("students:add")
        self.assertEquals(resolve(url).func, add)
    def test_edit_url_resolves(self):
        url = reverse("students:edit", args=[1])
        self.assertEquals(resolve(url).func, edit)
    def test_delete_url_resolves(self):
        url = reverse("students:delete", args=[1])
        self.assertEquals(resolve(url).func, delete)
    