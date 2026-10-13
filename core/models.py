from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    # photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Uncomment after installing Pillow

class Class(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} - {self.section}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField(blank=True)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.roll_number}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    subjects = models.ManyToManyField(Subject)
    classes = models.ManyToManyField(Class)
    
    def __str__(self):
        return self.user.get_full_name()

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField(Student, related_name='parents')
    
    def __str__(self):
        return self.user.get_full_name()

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_marks = models.FloatField(default=100)
    exam_type = models.CharField(max_length=50, default='Test')
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    def percentage(self):
        return (self.marks / self.max_marks) * 100
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['student', 'date']
    
    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.is_present else 'Absent'}"

class Behavior(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    behavior_type = models.CharField(max_length=50, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('needs_improvement', 'Needs Improvement'),
    ])
    notes = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.behavior_type}"

class Comment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    is_goal = models.BooleanField(default=False)
    is_acknowledged = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment for {self.student}"