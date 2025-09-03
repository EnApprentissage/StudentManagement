
from django.db import models
from django.contrib.auth.models import User

class AcademicYear(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date.year}/{self.end_date.year}"
    
class Semester(models.Model):
    name = models.CharField(max_length=50)  
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class Class(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.level} - {self.name}"

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class TeachingAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} - {self.subject} - {self.assigned_class} ({self.academic_year})"


class EvaluationType(models.Model):
    name = models.CharField(max_length=50)  
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.FloatField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    evaluation_type = models.ForeignKey(EvaluationType, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.value}"
    

class Schedule(models.Model):
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
    ]
    teaching = models.ForeignKey(TeachingAssignment, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    

    def __str__(self):
        return f"{self.teaching} - {self.get_weekday_display()} {self.start_time} - {self.end_time}"


class Absence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(blank=True)
    justified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} absent le {self.date}"