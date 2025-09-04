from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import (
    AcademicYear, Semester, Class, Teacher, Student,
    Subject, Grade, Absence
)
from .forms import (
    AcademicYearForm, SemesterForm, ClassForm, TeacherForm, StudentForm,
    SubjectForm, GradeForm, AbsenceForm
)

login_required_decorator = method_decorator(login_required, name='dispatch')


@login_required_decorator
class AcademicYearListView(ListView):
    model = AcademicYear
    template_name = 'school/academic_year_list.html'
    context_object_name = 'academic_years'


@login_required_decorator
class AcademicYearCreateView(CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('academic_year_list')


@login_required_decorator
class AcademicYearUpdateView(UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('academic_year_list')


@login_required_decorator
class SemesterCreateView(CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('academic_year_list')


@login_required_decorator
class ClassListView(ListView):
    model = Class
    template_name = 'school/class_list.html'
    context_object_name = 'classes'


@login_required_decorator
class ClassCreateView(CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('class_list')


@login_required_decorator
class ClassUpdateView(UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('class_list')


@login_required_decorator
class TeacherListView(ListView):
    model = Teacher
    template_name = 'school/teacher_list.html'
    context_object_name = 'teachers'


@login_required_decorator
class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('teacher_list')


# === Étudiant ===
@login_required_decorator
class StudentListView(ListView):
    model = Student
    template_name = 'school/student_list.html'
    context_object_name = 'students'


@login_required_decorator
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('student_list')


@login_required_decorator
class SubjectListView(ListView):
    model = Subject
    template_name = 'school/subject_list.html'
    context_object_name = 'subjects'


@login_required_decorator
class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('subject_list')


@login_required_decorator
class GradeListView(ListView):
    model = Grade
    template_name = 'school/grade_list.html'
    context_object_name = 'grades'


@login_required_decorator
class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('grade_list')


@login_required_decorator
class AbsenceListView(ListView):
    model = Absence
    template_name = 'school/absence_list.html'
    context_object_name = 'absences'


@login_required_decorator
class AbsenceCreateView(CreateView):
    model = Absence
    form_class = AbsenceForm
    template_name = 'school/form.html'
    success_url = reverse_lazy('absence_list')

