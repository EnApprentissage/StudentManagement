from django.contrib import admin
from .models import (
    AcademicYear,
    Semester,
    Class,
    Teacher,
    Student,
    Subject,
    Grade,
    Absence
)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    ordering = ('-start_date',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year')
    list_filter = ('academic_year',)
    search_fields = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'academic_year', 'max_students')
    list_filter = ('academic_year', 'level')
    search_fields = ('name', 'level')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'employee_id', 'hire_date', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id')
    list_filter = ('is_active',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'student_class', 'academic_year', 'is_active')
    list_filter = ('student_class', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'student_id')

    def academic_year(self, obj):
        return obj.student_class.academic_year if obj.student_class else None
    academic_year.short_description = 'Année académique'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'coefficient', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value', 'max_value', 'grade_type', 'academic_year', 'date_graded')
    list_filter = ('grade_type', 'academic_year', 'subject')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'subject__name')

@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'justified')
    list_filter = ('justified', 'date')
    search_fields = ('student__user__first_name', 'student__user__last_name')
