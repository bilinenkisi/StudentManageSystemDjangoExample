from django.shortcuts import render
from .models import Student
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import StudentForm


# Create your views here.
def index(request):
    students = Student.objects.all()

    return render(
        request,
        "students/index.html",
        {
            "students": students,
        },
    )


def view_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    return HttpResponseRedirect(reverse("students:index"))


def add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student_number = form.cleaned_data["student_number"]
            new_first_name = form.cleaned_data["first_name"]
            new_last_name = form.cleaned_data["last_name"]
            new_email_address = form.cleaned_data["email_address"]
            new_field_of_study = form.cleaned_data["field_of_study"]
            new_gpa = form.cleaned_data["gpa"]
            new_student = Student(
                student_number=new_student_number,
                first_name=new_first_name,
                last_name=new_last_name,
                email_address=new_email_address,
                field_of_study=new_field_of_study,
                gpa=new_gpa,
            )
            new_student.save()
            return render(
                request,
                "students/add.html",
                {
                    "form": form,
                    "success": True,
                },
            )

    else:
        form = StudentForm()
    return render(
        request,
        "students/add.html",
        {
            "form": form,
        },
    )
    
def edit(request, student_id):
    if request.method == "POST":
        student = Student.objects.get(pk=student_id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(
                request,
                "students/edit.html",
                {
                    "form": form,
                    "success": True,
                },
            )
    else:
        student = Student.objects.get(pk=student_id)
        form = StudentForm(instance=student)
    return render(
        request,
        "students/edit.html",
        {
            "form": form,
        },
    )
    
def delete(request, student_id):
    if request.method == "POST":
        student = Student.objects.get(pk=student_id)
        student.delete()
    return HttpResponseRedirect(reverse("students:index"))
    