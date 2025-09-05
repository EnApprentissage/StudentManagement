from django import forms
from .models import (
    AcademicYear, Period, Class, Teacher, Student, Subject,
    ClassSubject, Enrollment, Attendance, Grade, Profile
)


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['start_date', 'end_date', 'is_current']
        labels = {
            'start_date': "Start Date",
            'end_date': "End Date",
            'is_current': "Current Year"
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['name', 'academic_year', 'start_date', 'end_date', 'is_current']
        labels = {
            'name': "Period Name",
            'academic_year': "Academic Year",
            'start_date': "Start Date",
            'end_date': "End Date",
            'is_current': "Current Period"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'level', 'max_students', 'academic_year', 'subjects']
        labels = {
            'name': "Class Name",
            'level': "Level",
            'max_students': "Max Students",
            'academic_year': "Academic Year",
            'subjects': "Subjects"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'specialty', 'employee_id', 'hire_date', 'is_active']
        labels = {
            'user': "User",
            'specialty': "Specialty",
            'employee_id': "Employee ID",
            'hire_date': "Hire Date",
            'is_active': "Active"
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'student_id', 'student_class', 'date_of_birth', 'enrollment_date', 'is_active']
        labels = {
            'user': "User",
            'student_id': "Student ID",
            'student_class': "Class",
            'date_of_birth': "Date of Birth",
            'enrollment_date': "Enrollment Date",
            'is_active': "Active"
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'student_class': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description', 'coefficient', 'teacher', 'is_active']
        labels = {
            'name': "Subject Name",
            'code': "Code",
            'description': "Description",
            'coefficient': "Coefficient",
            'teacher': "Teacher",
            'is_active': "Active"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = ['student_class', 'subject', 'teacher', 'period', 'is_active']
        labels = {
            'student_class': "Class",
            'subject': "Subject",
            'teacher': "Teacher",
            'period': "Period",
            'is_active': "Active"
        }
        widgets = {
            'student_class': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'student_class', 'academic_year', 'date_enrolled', 'status']
        labels = {
            'student': "Student",
            'student_class': "Class",
            'academic_year': "Academic Year",
            'date_enrolled': "Enrollment Date",
            'status': "Status"
        }
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'student_class': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'date_enrolled': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['inscription', 'teacher', 'subject', 'date', 'status', 'reason']
        labels = {
            'inscription': "Enrollment",
            'teacher': "Teacher",
            'subject': "Subject",
            'date': "Date",
            'status': "Status",
            'reason': "Reason"
        }
        widgets = {
            'inscription': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['inscription', 'subject', 'period', 'value', 'max_value', 'grade_type', 'date_graded', 'coefficient', 'comment']
        labels = {
            'inscription': "Enrollment",
            'subject': "Subject",
            'period': "Period",
            'value': "Grade",
            'max_value': "Max Grade",
            'grade_type': "Assessment Type",
            'date_graded': "Grading Date",
            'coefficient': "Coefficient",
            'comment': "Comment"
        }
        widgets = {
            'inscription': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1}),
            'max_value': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1}),
            'grade_type': forms.Select(attrs={'class': 'form-select'}),
            'date_graded': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'role', 'phone']
        labels = {
            'user': "User",
            'role': "Role",
            'phone': "Phone Number"
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
