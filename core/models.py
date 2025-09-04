from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class AcademicYear(models.Model):
    
    start_date = models.DateField(
        verbose_name="Date de début",
        help_text="Date de début de l'année scolaire"
    )
    end_date = models.DateField(
        verbose_name="Date de fin",
        
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name="Année courante",
        help_text="Marquer comme année scolaire actuelle"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Année académique"
        verbose_name_plural = "Années académiques"
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
                raise ValidationError("La date de fin doit être après la date de début")

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Année académique {self.start_date.year}/{self.end_date.year}"


class Semester(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom du semestre")
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        verbose_name="Année académique"
    )

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        ordering = ['academic_year', 'name']

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class Class(models.Model):
    """Classe avec niveau et capacité"""
    name = models.CharField(
        max_length=100,
        verbose_name="Nom de la classe",
        unique=True
    )
    level = models.CharField(
        max_length=50,
        verbose_name="Niveau",
        
    )
    max_students = models.PositiveIntegerField(
        default=30,
        verbose_name="Nombre maximum d'étudiants"
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        verbose_name="Année académique",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Classe"
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
        return f"Classe {self.name} ({self.level}) - {self.academic_year}"


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur"
    )
    specialty = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Spécialité"
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ID employé",
        
    )
    hire_date = models.DateField(
        verbose_name="Date d'embauche",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['user__last_name', 'user__first_name']

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"Enseignant {self.full_name}"


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur"
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Numéro étudiant",
        
    )
    student_class = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Classe"
    )
    date_of_birth = models.DateField(
        verbose_name="Date de naissance",
        null=True,
        blank=True
    )
    enrollment_date = models.DateField(
        default=timezone.now,
        verbose_name="Date d'inscription"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
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
                raise ValidationError(f"La classe {self.student_class.name} est pleine")

    def __str__(self):
        return f"Étudiant {self.full_name} (ID: {self.student_id})"


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nom de la matière",
        unique=True
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Code matière",

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
        verbose_name="Enseignant principal"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Matière active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['name']

    def __str__(self):
        return f"Matière {self.name} ({self.code})"


class Grade(models.Model):
    GRADE_TYPES = [
        ('exam', 'Examen'),
        ('test', 'Contrôle'),
        ('homework', 'Devoir maison'),
        ('oral', 'Oral'),
        ('project', 'Projet'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Étudiant"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Matière"
    )
    value = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Note"
    )
    max_value = models.FloatField(
        default=20,
        validators=[MinValueValidator(1)],
        verbose_name="Note maximale"
    )
    grade_type = models.CharField(
        max_length=20,
        choices=GRADE_TYPES,
        default='test',
        verbose_name="Type d'évaluation"
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        verbose_name="Année académique"
    )
    date_graded = models.DateField(
        default=timezone.now,
        verbose_name="Date de notation"
    )
    coefficient = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(5.0)],
        verbose_name="Coefficient de la note"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Commentaire"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ['-date_graded', 'subject__name']
        indexes = [
            models.Index(fields=['student', 'academic_year']),
            models.Index(fields=['subject', 'academic_year']),
        ]

    @property
    def normalized_value(self):
        return (self.value / self.max_value) * 20

    @property
    def percentage(self):
        return (self.value / self.max_value) * 100

    def clean(self):
        if self.value > self.max_value:
            raise ValidationError("La note ne peut pas être supérieure à la note maximale")

        if self.student.student_class and self.student.student_class.academic_year != self.academic_year:
            raise ValidationError("L'année académique doit correspondre à celle de la classe de l'étudiant")

    def __str__(self):
        return f"Note de {self.student.full_name} en {self.subject.name} : {self.value}/{self.max_value}"


class Absence(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Étudiant"
    )
    date = models.DateField(
        verbose_name="Date de l'absence"
    )
    reason = models.TextField(
        blank=True,
        verbose_name="Raison"
    )
    justified = models.BooleanField(
        default=False,
        verbose_name="Justifiée"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Absence"
        verbose_name_plural = "Absences"
        ordering = ['-date']

    def __str__(self):
        return f"Absence de {self.student.full_name} le {self.date}"
