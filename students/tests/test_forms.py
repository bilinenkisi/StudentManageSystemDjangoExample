from django.test import TestCase

from students.forms import StudentForm

class TestForms(TestCase):
    def test_student_form_valid_data(self):
        form = StudentForm(data={
            'student_number': 12345678,
            'first_name': 'John',
            'last_name': 'Smith',
            'email_address': 'johnsmith@example.com',
            'field_of_study': 'N/A',
            'gpa': 3.0,
        })
        self.assertTrue(form.is_valid())
    
    def test_student_form_no_data(self):
        form = StudentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)
    
    def test_student_form_invalid_data(self):
        form = StudentForm(data={
            'student_number': 'abc',
            'first_name': 'John',
            'last_name': 'Smith',
            'email_address': 'abc',
            'field_of_study': 'N/A',
            'gpa': 'abc',
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
    def test_student_form_empty_fields(self):
        form = StudentForm(data={
            'student_number': '',
            'first_name': '',
            'last_name': '',
            'email_address': '',
            'field_of_study': '',
            'gpa': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)
    
    def test_student_form_field_labels(self):
        form = StudentForm()
        self.assertTrue(form.fields['student_number'].label == 'Student Number')
        self.assertTrue(form.fields['first_name'].label == 'First Name')
        self.assertTrue(form.fields['last_name'].label == 'Last Name')
        self.assertTrue(form.fields['email_address'].label == 'Email Address')
        self.assertTrue(form.fields['field_of_study'].label == 'Field of Study')
        self.assertTrue(form.fields['gpa'].label == 'GPA')
    
    
            
        