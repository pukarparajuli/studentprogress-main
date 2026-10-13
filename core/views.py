from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Avg, Count
from datetime import datetime
from .models import User, Student, Teacher, Parent, Grade, Attendance, Behavior, Comment, Subject, Class
from .ml_utils import StudentPerformancePredictor, PerformanceInsights, GradeAnalyzer, AttendancePatternAnalyzer

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import HexColor, white, black
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

# Public Views
def home(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def features_view(request):
    return render(request, 'features.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        messages.success(request, f'Thank you {name}! Your message has been sent.')
        return redirect('contact')
    return render(request, 'contact.html')

def support_view(request):
    return render(request, 'support.html')

# Authentication Views
@csrf_exempt
def role_login(request, role):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user and user.role == role:
            login(request, user)
            return redirect('dashboard')
        elif user and user.role != role:
            messages.error(request, f'This account is not registered as {role.title()}.')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'role_login.html', {'role': role})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# Dashboard Views
@login_required
def dashboard(request):
    user = request.user
    
    if user.role == 'admin':
        return admin_dashboard(request)
    elif user.role == 'teacher':
        return teacher_dashboard(request)
    elif user.role == 'student':
        return student_dashboard(request)
    elif user.role == 'parent':
        return parent_dashboard(request)

def admin_dashboard(request):
    context = {
        'user': request.user,
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_classes': Class.objects.count(),
        'total_subjects': Subject.objects.count(),
        'avg_attendance': Attendance.objects.filter(is_present=True).count() / max(Attendance.objects.count(), 1) * 100,
        'avg_marks': Grade.objects.aggregate(avg=Avg('marks'))['avg'] or 0,
    }
    
    # AI Insights for Admin
    try:
        all_students = Student.objects.all()
        risk_summary = {'high': 0, 'medium': 0, 'low': 0, 'on_track': 0}
        
        for student in all_students:
            risk_score = StudentPerformancePredictor.calculate_risk_score(student)
            if risk_score >= 70:
                risk_summary['high'] += 1
            elif risk_score >= 40:
                risk_summary['medium'] += 1
            elif risk_score >= 20:
                risk_summary['low'] += 1
            else:
                risk_summary['on_track'] += 1
        
        context['ai_summary'] = risk_summary
        print(f"Admin AI Summary: {risk_summary}")  # Debug print
    except Exception as e:
        print(f"Admin AI Error: {e}")  # Debug print
        context['ai_summary'] = {'high': 0, 'medium': 0, 'low': 0, 'on_track': 0}
    
    return render(request, 'admin_dashboard.html', context)

def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    students = Student.objects.filter(student_class__in=teacher.classes.all())
    
    # AI Analysis for each student
    student_risks = []
    try:
        for student in students:
            risk_score = StudentPerformancePredictor.calculate_risk_score(student)
            risk_level, risk_class = StudentPerformancePredictor.get_risk_level(risk_score)
            recommendations = StudentPerformancePredictor.get_recommendations(student, risk_score)
            
            student_risks.append({
                'student': student,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_class': risk_class,
                'recommendations': recommendations[:2]
            })
    except Exception as e:
        for student in students:
            student_risks.append({
                'student': student,
                'risk_score': 50,
                'risk_level': 'Unknown',
                'risk_class': 'secondary',
                'recommendations': ['AI analysis unavailable']
            })
    
    student_risks.sort(key=lambda x: x['risk_score'], reverse=True)
    
    context = {
        'user': request.user,
        'teacher': teacher,
        'students': students,
        'subjects': teacher.subjects.all(),
        'classes': teacher.classes.all(),
        'student_risks': student_risks,
        'high_risk_students': [s for s in student_risks if s['risk_score'] >= 70],
    }
    return render(request, 'teacher_dashboard.html', context)

def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    
    # Comprehensive AI Analysis
    try:
        ai_analysis = PerformanceInsights.get_comprehensive_analysis(student)
        print(f"Student AI Analysis: Risk={ai_analysis['risk_score']}, Status={ai_analysis['overall_status']['status']}")  # Debug print
    except Exception as e:
        print(f"Student AI Error: {e}")  # Debug print
        ai_analysis = {
            'risk_score': 50,
            'risk_level': 'Unknown',
            'risk_class': 'secondary',
            'grade_analysis': {
                'average': 0,
                'trend': 'No Data',
                'insights': ['Complete more assessments for AI insights']
            },
            'attendance_analysis': {
                'attendance_rate': 0,
                'risk_level': 'Unknown',
                'insights': ['No attendance data available']
            },
            'improvement_suggestions': ['Complete more activities to unlock AI insights'],
            'overall_status': {
                'status': 'Getting Started',
                'color': 'info',
                'icon': 'fas fa-info-circle',
                'message': 'Complete more activities to unlock AI insights'
            }
        }
    
    context = {
        'user': request.user,
        'student': student,
        'grades': Grade.objects.filter(student=student).order_by('-date')[:10],
        'attendance': Attendance.objects.filter(student=student).order_by('-date')[:10],
        'behaviors': Behavior.objects.filter(student=student).order_by('-date')[:5],
        'comments': Comment.objects.filter(student=student).order_by('-date')[:5],
        'ai_analysis': ai_analysis,
    }
    return render(request, 'student_dashboard.html', context)

def parent_dashboard(request):
    parent = get_object_or_404(Parent, user=request.user)
    children = parent.children.all()
    
    # AI Analysis for each child
    children_analysis = []
    for child in children:
        try:
            ai_analysis = PerformanceInsights.get_comprehensive_analysis(child)
            print(f"AI Analysis for {child.user.get_full_name()}: {ai_analysis['risk_score']}")
            children_analysis.append({
                'child': child,
                'ai_analysis': ai_analysis
            })
        except Exception as e:
            print(f"Parent Dashboard AI Error for {child.user.get_full_name()}: {e}")
            # Provide more detailed fallback data
            children_analysis.append({
                'child': child,
                'ai_analysis': {
                    'risk_score': 50,
                    'risk_level': 'Unknown',
                    'risk_class': 'secondary',
                    'grade_analysis': {
                        'average': 0,
                        'trend': 'No Data',
                        'insights': ['Complete more assessments for insights']
                    },
                    'attendance_analysis': {
                        'attendance_rate': 0,
                        'risk_level': 'Unknown',
                        'insights': ['No attendance data available']
                    },
                    'improvement_suggestions': ['Complete more activities for insights'],
                    'overall_status': {
                        'status': 'Getting Started',
                        'color': 'info',
                        'icon': 'fas fa-info-circle',
                        'message': 'Complete more activities to unlock insights'
                    }
                }
            })
    
    context = {
        'user': request.user,
        'parent': parent,
        'children': children,
        'children_analysis': children_analysis,
    }
    return render(request, 'parent_dashboard.html', context)

# Academic Management Views
@csrf_exempt
@login_required
def add_grade(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')
    
    teacher = get_object_or_404(Teacher, user=request.user)
    
    if request.method == 'POST':
        student_id = request.POST['student']
        subject_id = request.POST['subject']
        marks = request.POST['marks']
        max_marks = request.POST['max_marks']
        exam_type = request.POST['exam_type']
        
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        Grade.objects.create(
            student=student,
            subject=subject,
            marks=float(marks),
            max_marks=float(max_marks),
            exam_type=exam_type,
            teacher=teacher
        )
        messages.success(request, 'Grade added successfully')
        return redirect('dashboard')
    
    context = {
        'students': Student.objects.filter(student_class__in=teacher.classes.all()),
        'subjects': teacher.subjects.all(),
    }
    return render(request, 'add_grade.html', context)

@csrf_exempt
@login_required
def mark_attendance(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')
    
    teacher = get_object_or_404(Teacher, user=request.user)
    
    if request.method == 'POST':
        date = request.POST['date']
        for student in Student.objects.filter(student_class__in=teacher.classes.all()):
            is_present = f'student_{student.id}' in request.POST
            Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={'is_present': is_present, 'teacher': teacher}
            )
        messages.success(request, 'Attendance marked successfully')
        return redirect('dashboard')
    
    context = {
        'students': Student.objects.filter(student_class__in=teacher.classes.all()),
        'today': datetime.now().date()
    }
    return render(request, 'mark_attendance.html', context)

# Report Views
@login_required
def student_report(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Permission check
    if request.user.role == 'student' and request.user != student.user:
        return redirect('dashboard')
    elif request.user.role == 'parent':
        parent = get_object_or_404(Parent, user=request.user)
        if student not in parent.children.all():
            return redirect('dashboard')
    
    grades = Grade.objects.filter(student=student).order_by('-date')
    attendance = Attendance.objects.filter(student=student)
    behaviors = Behavior.objects.filter(student=student).order_by('-date')
    
    # AI Analysis
    try:
        ai_analysis = PerformanceInsights.get_comprehensive_analysis(student)
    except:
        ai_analysis = None
    
    context = {
        'student': student,
        'grades': grades,
        'attendance_rate': attendance.filter(is_present=True).count() / max(attendance.count(), 1) * 100,
        'behaviors': behaviors,
        'ai_analysis': ai_analysis,
    }
    return render(request, 'student_report.html', context)

@login_required
def teacher_reports(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')
    
    teacher = get_object_or_404(Teacher, user=request.user)
    students = Student.objects.filter(student_class__in=teacher.classes.all())
    
    context = {
        'students': students,
        'teacher': teacher
    }
    return render(request, 'teacher_reports.html', context)

# AI Views
@login_required
def ai_insights(request):
    if request.user.role not in ['teacher', 'admin']:
        return redirect('dashboard')
    
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        students = Student.objects.filter(student_class__in=teacher.classes.all())
    else:
        students = Student.objects.all()
    
    # Generate AI insights
    student_analysis = []
    risk_summary = {'high': 0, 'medium': 0, 'low': 0, 'on_track': 0}
    
    for student in students:
        try:
            risk_score = StudentPerformancePredictor.calculate_risk_score(student)
            risk_level, risk_class = StudentPerformancePredictor.get_risk_level(risk_score)
            recommendations = StudentPerformancePredictor.get_recommendations(student, risk_score)
            
            student_analysis.append({
                'student': student,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_class': risk_class,
                'recommendations': recommendations
            })
            
            if risk_score >= 70:
                risk_summary['high'] += 1
            elif risk_score >= 40:
                risk_summary['medium'] += 1
            elif risk_score >= 20:
                risk_summary['low'] += 1
            else:
                risk_summary['on_track'] += 1
        except:
            continue
    
    student_analysis.sort(key=lambda x: x['risk_score'], reverse=True)
    
    context = {
        'student_analysis': student_analysis,
        'risk_summary': risk_summary,
        'total_students': len(student_analysis)
    }
    return render(request, 'ai_insights.html', context)

@login_required
def student_ai_analysis(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Permission check
    if request.user.role == 'student' and request.user != student.user:
        return redirect('dashboard')
    elif request.user.role == 'parent':
        parent = get_object_or_404(Parent, user=request.user)
        if student not in parent.children.all():
            return redirect('dashboard')
    elif request.user.role not in ['teacher', 'admin']:
        return redirect('dashboard')
    
    # Get comprehensive AI analysis
    ai_analysis = {
        'risk_score': 50,
        'risk_level': 'Unknown',
        'risk_class': 'secondary',
        'grade_analysis': {'average': 0, 'trend': 'No Data', 'insights': ['Analysis unavailable']},
        'attendance_analysis': {'attendance_rate': 0, 'insights': ['No data']},
        'improvement_suggestions': ['Complete more activities for insights'],
        'overall_status': {'status': 'Analysis Unavailable', 'color': 'secondary', 'message': 'Data insufficient'}
    }
    
    try:
        ai_analysis = PerformanceInsights.get_comprehensive_analysis(student)
        print(f"AI Analysis Success: Risk={ai_analysis['risk_score']}")
    except Exception as e:
        print(f"AI Analysis Error: {e}")
    
    # Get subject-wise performance - Simplified approach
    subjects_analysis = []
    try:
        # Get all grades for this student
        grades = Grade.objects.filter(student=student).select_related('subject')
        
        # Group by subject
        subjects_dict = {}
        for grade in grades:
            subject = grade.subject
            if subject.id not in subjects_dict:
                subjects_dict[subject.id] = {
                    'subject': subject,
                    'grades': []
                }
            subjects_dict[subject.id]['grades'].append(grade)
        
        # Analyze each subject
        for subject_data in subjects_dict.values():
            try:
                analysis = GradeAnalyzer.analyze_subject_performance(student, subject_data['subject'])
                subjects_analysis.append({
                    'subject': subject_data['subject'],
                    'analysis': analysis
                })
            except Exception as e:
                print(f"Subject analysis error for {subject_data['subject'].name}: {e}")
                continue
                
    except Exception as e:
        print(f"Overall subject analysis error: {e}")
    
    context = {
        'student': student,
        'ai_analysis': ai_analysis,
        'subjects_analysis': subjects_analysis,
    }
    return render(request, 'student_ai_analysis.html', context)

# PDF Export
@login_required
def export_report_pdf(request, student_id):
    if not HAS_REPORTLAB:
        messages.error(request, 'PDF generation requires reportlab. Run: pip install reportlab')
        return redirect('student_report', student_id=student_id)
    
    student = get_object_or_404(Student, id=student_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.user.get_full_name()}_Report.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Header
    p.setFillColor(HexColor('#667eea'))
    p.rect(0, height-100, width, 100, fill=1, stroke=0)
    
    p.setFillColor(white)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height-60, f"Student Report - {student.user.get_full_name()}")
    
    # Content
    y = height - 150
    p.setFillColor(black)
    p.setFont("Helvetica", 12)
    
    # Student Info
    p.drawString(50, y, f"Roll Number: {student.roll_number}")
    p.drawString(300, y, f"Class: {student.student_class}")
    y -= 30
    
    # Grades
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Recent Grades:")
    y -= 20
    
    p.setFont("Helvetica", 10)
    grades = Grade.objects.filter(student=student).order_by('-date')[:10]
    for grade in grades:
        p.drawString(50, y, f"{grade.subject.name}: {grade.marks}/{grade.max_marks} ({grade.percentage():.1f}%)")
        y -= 15
        if y < 100:
            break
    
    # AI Analysis
    try:
        ai_analysis = PerformanceInsights.get_comprehensive_analysis(student)
        y -= 30
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "AI Analysis:")
        y -= 20
        
        p.setFont("Helvetica", 10)
        p.drawString(50, y, f"Risk Level: {ai_analysis['risk_level']}")
        y -= 15
        p.drawString(50, y, f"Overall Status: {ai_analysis['overall_status']['status']}")
    except:
        pass
    
    p.save()
    return response