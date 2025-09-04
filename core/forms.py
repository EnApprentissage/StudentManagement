from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

from .models import (
    AcademicYear, Semester, Class, Teacher, Student,
    Subject, Grade, Absence
)


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'academic_year']


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'level', 'max_students', 'academic_year']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'specialty', 'employee_id', 'hire_date', 'is_active']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'user', 'student_id', 'student_class',
            'date_of_birth', 'enrollment_date', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        student_class = cleaned_data.get('student_class')

        if student_class and student_class.is_full:
            raise ValidationError(f"La classe {student_class.name} est pleine.")
        return cleaned_data


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description', 'coefficient', 'teacher', 'is_active']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = [
            'student', 'subject', 'value', 'max_value', 'grade_type',
            'academic_year', 'date_graded', 'coefficient', 'comment'
        ]
        widgets = {
            'date_graded': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get('value')
        max_value = cleaned_data.get('max_value')
        student = cleaned_data.get('student')
        academic_year = cleaned_data.get('academic_year')

        if value and max_value and value > max_value:
            raise ValidationError("La note ne peut pas être supérieure à la note maximale.")

        if student and student.student_class and student.student_class.academic_year != academic_year:
            raise ValidationError("L'année académique doit correspondre à celle de la classe de l'étudiant.")

        return cleaned_data


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['student', 'date', 'reason', 'justified']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
