from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher, Parent, Class, Subject, Grade, Attendance, Behavior, Comment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'first_name', 'last_name']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'role'),
        }),
    )

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_student_count']
    search_fields = ['name', 'section']
    
    def get_student_count(self, obj):
        return obj.student_set.count()
    get_student_count.short_description = 'Students'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'get_teacher_count']
    search_fields = ['name', 'code']
    
    def get_teacher_count(self, obj):
        return obj.teacher_set.count()
    get_teacher_count.short_description = 'Teachers'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'roll_number', 'student_class', 'parent_name']
    list_filter = ['student_class']
    search_fields = ['user__first_name', 'user__last_name', 'roll_number']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Student Name'
    
    fieldsets = (
        ('Student Info', {
            'fields': ('user', 'roll_number', 'date_of_birth', 'student_class')
        }),
        ('Parent Info', {
            'fields': ('parent_name', 'parent_phone', 'parent_email', 'address')
        }),
    )

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'employee_id', 'get_subjects', 'get_classes']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']
    filter_horizontal = ['subjects', 'classes']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Teacher Name'
    
    def get_subjects(self, obj):
        return ', '.join([s.name for s in obj.subjects.all()[:3]])
    get_subjects.short_description = 'Subjects'
    
    def get_classes(self, obj):
        return ', '.join([str(c) for c in obj.classes.all()[:3]])
    get_classes.short_description = 'Classes'

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_children']
    search_fields = ['user__first_name', 'user__last_name']
    filter_horizontal = ['children']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Parent Name'
    
    def get_children(self, obj):
        return ', '.join([c.user.get_full_name() for c in obj.children.all()[:3]])
    get_children.short_description = 'Children'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'subject', 'marks', 'max_marks', 'get_percentage', 'exam_type', 'date']
    list_filter = ['subject', 'exam_type', 'date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student'
    
    def get_percentage(self, obj):
        return f'{(obj.marks/obj.max_marks)*100:.1f}%'
    get_percentage.short_description = 'Percentage'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'date', 'get_status']
    list_filter = ['is_present', 'date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student'
    
    def get_status(self, obj):
        return '✅ Present' if obj.is_present else '❌ Absent'
    get_status.short_description = 'Status'

@admin.register(Behavior)
class BehaviorAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'behavior_type', 'get_short_notes', 'date']
    list_filter = ['behavior_type', 'date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student'
    
    def get_short_notes(self, obj):
        return obj.notes[:50] + '...' if len(obj.notes) > 50 else obj.notes
    get_short_notes.short_description = 'Notes'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'get_short_comment', 'get_type', 'is_acknowledged', 'date']
    list_filter = ['is_goal', 'is_acknowledged', 'date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student'
    
    def get_short_comment(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    get_short_comment.short_description = 'Comment'
    
    def get_type(self, obj):
        return '🎯 Goal' if obj.is_goal else '💬 Comment'
    get_type.short_description = 'Type'