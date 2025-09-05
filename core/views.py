
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import (
    AcademicYear, Period, Class, Teacher, Student, Subject,
    ClassSubject, Enrollment, Attendance, Grade, Profile
)
from .forms import (
    AcademicYearForm, PeriodForm, ClassForm, TeacherForm, StudentForm, SubjectForm,
    ClassSubjectForm, EnrollmentForm, AttendanceForm, GradeForm, ProfileForm
)

class AcademicYearListView(ListView):
    model = AcademicYear
    template_name = "academicyear/academic_year_list.html"
    context_object_name = "academic_years"


class AcademicYearDetailView(DetailView):
    model = AcademicYear
    template_name = "academicyear/academic_year_detail.html"
    context_object_name = "academic_year"


class AcademicYearCreateView(CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = "academicyear/academic_year_form.html"
    success_url = reverse_lazy("academic_year_list")


class AcademicYearUpdateView(UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = "academicyear/academic_year_form.html"
    success_url = reverse_lazy("academic_year_list")


class AcademicYearDeleteView(DeleteView):
    model = AcademicYear
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("academic_year_list")



class PeriodListView(ListView):
    model = Period
    template_name = "period/period_list.html"
    context_object_name = "periods"


class PeriodDetailView(DetailView):
    model = Period
    template_name = "period/period_detail.html"
    context_object_name = "period"


class PeriodCreateView(CreateView):
    model = Period
    form_class = PeriodForm
    template_name = "period/period_form.html"
    success_url = reverse_lazy("period_list")


class PeriodUpdateView(UpdateView):
    model = Period
    form_class = PeriodForm
    template_name = "period/period_form.html"
    success_url = reverse_lazy("period_list")


class PeriodDeleteView(DeleteView):
    model = Period
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("period_list")



class ClassListView(ListView):
    model = Class
    template_name = "class/class_list.html"
    context_object_name = "classes"


class ClassDetailView(DetailView):
    model = Class
    template_name = "class/class_detail.html"
    context_object_name = "class_obj"


class ClassCreateView(CreateView):
    model = Class
    form_class = ClassForm
    template_name = "class/class_form.html"
    success_url = reverse_lazy("class_list")


class ClassUpdateView(UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "class/class_form.html"
    success_url = reverse_lazy("class_list")


class ClassDeleteView(DeleteView):
    model = Class
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("class_list")



class TeacherListView(ListView):
    model = Teacher
    template_name = "teacher/teacher_list.html"
    context_object_name = "teachers"


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = "teacher/teacher_detail.html"
    context_object_name = "teacher"


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "teacher/teacher_form.html"
    success_url = reverse_lazy("teacher_list")


class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "teacher/teacher_form.html"
    success_url = reverse_lazy("teacher_list")


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("teacher_list")


class StudentListView(ListView):
    model = Student
    template_name = "student/student_list.html"
    context_object_name = "students"


class StudentDetailView(DetailView):
    model = Student
    template_name = "student/student_detail.html"
    context_object_name = "student"


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student/student_form.html"
    success_url = reverse_lazy("student_list")


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student/student_form.html"
    success_url = reverse_lazy("student_list")


class StudentDeleteView(DeleteView):
    model = Student
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("student_list")



class SubjectListView(ListView):
    model = Subject
    template_name = "subject/subject_list.html"
    context_object_name = "subjects"


class SubjectDetailView(DetailView):
    model = Subject
    template_name = "subject/subject_detail.html"
    context_object_name = "subject"


class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "subject/subject_form.html"
    success_url = reverse_lazy("subject_list")


class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "subject/subject_form.html"
    success_url = reverse_lazy("subject_list")


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("subject_list")
