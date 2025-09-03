from django.contrib import admin

from django.contrib import admin
from .models import Student, Teacher, Subject, Grade, Class, AcademicYear

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Class)
admin.site.register(AcademicYear)

