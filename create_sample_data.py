import os
import django
from datetime import date, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms.settings')
django.setup()

from core.models import User, Class, Subject, Student, Teacher, Parent, Grade, Attendance, Behavior

# Create superuser
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@school.com',
        'role': 'admin',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_superuser': True,
        'is_staff': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()

# Create classes
class_10a = Class.objects.create(name='10', section='A')
class_9b = Class.objects.create(name='9', section='B')

# Create subjects
math = Subject.objects.create(name='Mathematics', code='MATH101')
english = Subject.objects.create(name='English', code='ENG101')
science = Subject.objects.create(name='Science', code='SCI101')

# Create teacher
teacher_user, created = User.objects.get_or_create(
    username='teacher1',
    defaults={
        'email': 'teacher@school.com',
        'role': 'teacher',
        'first_name': 'John',
        'last_name': 'Smith'
    }
)
if created:
    teacher_user.set_password('teacher123')
    teacher_user.save()

teacher, _ = Teacher.objects.get_or_create(
    user=teacher_user,
    defaults={'employee_id': 'T001'}
)
teacher.subjects.add(math, english)
teacher.classes.add(class_10a)

# Create student
student_user, created = User.objects.get_or_create(
    username='student1',
    defaults={
        'email': 'student@school.com',
        'role': 'student',
        'first_name': 'Alice',
        'last_name': 'Johnson'
    }
)
if created:
    student_user.set_password('student123')
    student_user.save()

student, _ = Student.objects.get_or_create(
    user=student_user,
    defaults={
        'roll_number': '2024001',
        'date_of_birth': date(2008, 5, 15),
        'student_class': class_10a,
        'parent_name': 'Robert Johnson',
        'parent_phone': '1234567890',
        'parent_email': 'parent@email.com',
        'address': '123 Main St'
    }
)

# Create parent
parent_user, created = User.objects.get_or_create(
    username='parent1',
    defaults={
        'email': 'parent@school.com',
        'role': 'parent',
        'first_name': 'Robert',
        'last_name': 'Johnson'
    }
)
if created:
    parent_user.set_password('parent123')
    parent_user.save()

parent, _ = Parent.objects.get_or_create(user=parent_user)
parent.children.add(student)

# Create sample grades
Grade.objects.create(
    student=student,
    subject=math,
    marks=85,
    max_marks=100,
    exam_type='Test',
    teacher=teacher
)
Grade.objects.create(
    student=student,
    subject=english,
    marks=92,
    max_marks=100,
    exam_type='Quiz',
    teacher=teacher
)

# Create sample attendance
Attendance.objects.create(
    student=student,
    date=date.today(),
    is_present=True,
    teacher=teacher
)

# Create sample behavior
Behavior.objects.create(
    student=student,
    teacher=teacher,
    behavior_type='excellent',
    notes='Great participation in class discussions'
)

print("Sample data created successfully!")
print("Login credentials:")
print("Admin: admin / admin123")
print("Teacher: teacher1 / teacher123")
print("Student: student1 / student123")
print("Parent: parent1 / parent123")