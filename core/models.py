from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class AcademicYear(models.Model):
    start_date = models.DateField(
        verbose_name="Start Date",
        help_text="Start date of the academic year"
    )
    end_date = models.DateField(
        verbose_name="End Date",
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name="Current Year",
        help_text="Mark as the current academic year"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"
        ordering = ['-start_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='end_date_after_start_date'
            )
        ]

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError("The end date must be after the start date.")

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Academic Year {self.start_date.year}/{self.end_date.year}"



class Period(models.Model):
    name = models.CharField(max_length=50, verbose_name="Period Name")
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        verbose_name="Academic Year",
        related_name="periods"
    )
    start_date = models.DateField(verbose_name="Start of Period")
    end_date = models.DateField(verbose_name="End of Period")
    is_current = models.BooleanField(default=False, verbose_name="Current Period")

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        ordering = ['academic_year', 'start_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='period_end_after_start'
            )
        ]
        unique_together = [['name', 'academic_year']]

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("The end of the period must be after the start.")

    def save(self, *args, **kwargs):
        if self.is_current:
            Period.objects.filter(
                academic_year=self.academic_year,
                is_current=True
            ).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class Class(models.Model):
    name = models.CharField(
        max_length=100,)
    academic_year = models.ForeignKey(
        'AcademicYear',
        on_delete=models.CASCADE,
        related_name='classes',
        verbose_name="Class Name",
        
    )
    level = models.CharField(
        max_length=50,
        verbose_name="Level",
    )
    max_students = models.PositiveIntegerField(
        default=30,
        verbose_name="Maximum Number of Students"
    )

    
    subjects = models.ManyToManyField(
        'Subject',
        through='ClassSubject',
        related_name='classes',
        verbose_name="Subjects"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['level', 'name']
        unique_together = [['name', 'academic_year']]

    @property
    def current_students_count(self):
        return self.student_set.count()

    @property
    def is_full(self):
        return self.current_students_count >= self.max_students

    def __str__(self):
        return f"Class {self.name} ({self.level}) - {self.academic_year}"


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    specialty = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Specialty"
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Employee ID",
    )
    hire_date = models.DateField(
        verbose_name="Hire Date",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['user__last_name', 'user__first_name']

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"Teacher {self.full_name}"


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Student ID",
    )
    student_class = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Class (legacy)"
    )
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        null=True,
        blank=True
    )
    enrollment_date = models.DateField(
        default=timezone.now,
        verbose_name="Enrollment Date"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['user__last_name', 'user__first_name']

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def clean(self):
        if self.student_class and self.student_class.is_full:
            if not self.pk or self.student_class != Student.objects.get(pk=self.pk).student_class:
                raise ValidationError(f"The class {self.student_class.name} is full.")

    def __str__(self):
        return f"Student {self.full_name} (ID: {self.student_id})"


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Subject Name",
        unique=True
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Subject Code",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    coefficient = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
        verbose_name="Coefficient"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Main Teacher"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Subject"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name']

    def __str__(self):
        return f"Subject {self.name} ({self.code})"


class ClassSubject(models.Model):
    student_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='class_subjects',
        verbose_name="Class"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_subjects',
        verbose_name="Subject"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Assigned Teacher"
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Period"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Class Subject"
        verbose_name_plural = "Class Subjects"
        unique_together = [['student_class', 'subject', 'period']]

    def __str__(self):
        return f"{self.student_class} - {self.subject} ({self.period or 'all periods'})"


class Enrollment(models.Model):
    STATUS = [
        ('active', 'Active'),
        ('transferred', 'Transferred'),
        ('graduated', 'Graduated'),
        ('withdrawn', 'Withdrawn'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student")
    student_class = models.ForeignKey(Class, on_delete=models.PROTECT, verbose_name="Class")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, verbose_name="Academic Year")
    date_enrolled = models.DateField(default=timezone.now, verbose_name="Enrollment Date")
    status = models.CharField(max_length=20, choices=STATUS, default='active', verbose_name="Status")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        ordering = ['-date_enrolled']
        unique_together = [['student', 'academic_year']]

    def clean(self):
        if self.student_class.academic_year and self.student_class.academic_year != self.academic_year:
            raise ValidationError("The enrollment year must match the class's academic year.")

    def __str__(self):
        return f"Enrollment {self.student.full_name} → {self.student_class} ({self.academic_year})"



class Grade(models.Model):
    GRADE_TYPES = [
        ('exam', 'Exam'),
        ('test', 'Test'),
        ('homework', 'Homework'),
        ('oral', 'Oral'),
        ('project', 'Project'),
    ]

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        verbose_name="Enrollment",
        related_name='grades',
        null=True,
        blank=True
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name="Subject"
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        verbose_name="Period",
        null=True,
        blank=True
    )
    value = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Grade"
    )
    max_value = models.FloatField(
        default=20,
        validators=[MinValueValidator(1)],
        verbose_name="Maximum Grade"
    )
    grade_type = models.CharField(
        max_length=20,
        choices=GRADE_TYPES,
        default='test',
        verbose_name="Assessment Type"
    )
    date_graded = models.DateField(
        default=timezone.now,
        verbose_name="Grading Date"
    )
    coefficient = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(5.0)],
        verbose_name="Grade Coefficient"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Comment"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ['-date_graded', 'subject__name']
        indexes = [
            models.Index(fields=['enrollment', 'period']),
            models.Index(fields=['subject', 'period']),
        ]
        unique_together = [['enrollment', 'subject', 'period', 'date_graded', 'grade_type']]

    @property
    def normalized_value(self):
        return (self.value / self.max_value) * 20

    @property
    def percentage(self):
        return (self.value / self.max_value) * 100

    def clean(self):
        if self.value > self.max_value:
            raise ValidationError("The grade cannot exceed the maximum grade.")
        if self.period.academic_year_id != self.enrollment.academic_year_id:
            raise ValidationError("The period must belong to the same academic year as the enrollment.")
        if not ClassSubject.objects.filter(
            student_class=self.enrollment.student_class,
            subject=self.subject
        ).filter(models.Q(period__isnull=True) | models.Q(period=self.period)).exists():
            raise ValidationError("This subject is not assigned to the class for this period.")

    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.subject.name}: {self.value}/{self.max_value}"



class Attendance(models.Model):
    STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, verbose_name="Enrollment")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="Teacher")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name="Subject")
    date = models.DateField(verbose_name="Date")
    status = models.CharField(max_length=10, choices=STATUS, default='present', verbose_name="Status")
    reason = models.TextField(blank=True, verbose_name="Observation / Reason")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        ordering = ['-date']
        unique_together = [['enrollment', 'subject', 'date']]

    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.subject} - {self.date} ({self.status})"



class Profile(models.Model):
    ROLES = [
        ('adminsystem', 'System Administrator'),
        ('director', 'Director'),
        ('secretary', 'Secretary'),
        ('student_president', 'Student President'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="User")
    role = models.CharField(max_length=32, choices=ROLES, verbose_name="Role")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Phone")
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"Profile {self.user.username} - {self.get_role_display()}"
