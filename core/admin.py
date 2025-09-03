
from django.contrib import admin
from .models import (
    AcademicYear,
    Semester,
    Class,
    Profile,
    Student,
    Teacher,
    Subject,
    TeachingAssignment,
    EvaluationType,
    Grade,
    Schedule,
    Absence
)

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
    ordering = ('-start_date',)

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year')
    list_filter = ('academic_year',)

class ClassAdmin(admin.ModelAdmin):
    list_display = ('level', 'name')
    search_fields = ('name', 'level')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'birth_date', 'phone', 'address')
    search_fields = ('user__first_name', 'user__last_name', 'phone')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_class', 'academic_year')
    search_fields = ('user__first_name', 'user__last_name')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    search_fields = ('user__first_name', 'user__last_name')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TeachingAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'assigned_class', 'academic_year')
    list_filter = ('academic_year', 'assigned_class')

class EvaluationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')

class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value', 'academic_year', 'semester', 'evaluation_type', 'date')
    list_filter = ('academic_year', 'semester', 'evaluation_type')
    search_fields = ('student__user__first_name', 'student__user__last_name')

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('teaching', 'weekday', 'start_time', 'end_time')
    list_filter = ('weekday',)

class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'justified')
    list_filter = ('justified',)
    search_fields = ('student__user__first_name', 'student__user__last_name')


admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(TeachingAssignment, TeachingAssignmentAdmin)
admin.site.register(EvaluationType, EvaluationTypeAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Absence, AbsenceAdmin)
