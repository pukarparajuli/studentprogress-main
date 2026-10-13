#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms.settings')
django.setup()

from core.models import *
from core.ml_utils import *
from core.views import *

def debug_ai_panels():
    print("=== Debugging AI Analysis Panels ===\n")
    
    # Check data availability
    print("1. Data Availability Check:")
    print(f"   Users: {User.objects.count()}")
    print(f"   Students: {Student.objects.count()}")
    print(f"   Teachers: {Teacher.objects.count()}")
    print(f"   Parents: {Parent.objects.count()}")
    print(f"   Grades: {Grade.objects.count()}")
    print(f"   Attendance: {Attendance.objects.count()}")
    print(f"   Subjects: {Subject.objects.count()}")
    print(f"   Classes: {Class.objects.count()}")
    
    # Test each user role
    print("\n2. Testing AI Analysis for Each Role:")
    
    # Admin Dashboard Test
    print("\n   Admin Dashboard:")
    try:
        admin_user = User.objects.filter(role='admin').first()
        if admin_user:
            print(f"   - Admin user found: {admin_user.username}")
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
            
            print(f"   - AI Summary: {risk_summary}")
            print("   [OK] Admin AI analysis working")
        else:
            print("   [ERROR] No admin user found")
    except Exception as e:
        print(f"   [ERROR] Admin AI error: {e}")
    
    # Teacher Dashboard Test
    print("\n   Teacher Dashboard:")
    try:
        teacher_user = User.objects.filter(role='teacher').first()
        if teacher_user:
            print(f"   - Teacher user found: {teacher_user.username}")
            teacher = Teacher.objects.get(user=teacher_user)
            students = Student.objects.filter(student_class__in=teacher.classes.all())
            print(f"   - Students under teacher: {students.count()}")
            
            student_risks = []
            for student in students:
                risk_score = StudentPerformancePredictor.calculate_risk_score(student)
                risk_level, risk_class = StudentPerformancePredictor.get_risk_level(risk_score)
                recommendations = StudentPerformancePredictor.get_recommendations(student, risk_score)
                
                student_risks.append({
                    'student': student.user.get_full_name(),
                    'risk_score': risk_score,
                    'risk_level': risk_level,
                    'recommendations_count': len(recommendations)
                })
            
            print(f"   - Student risks calculated: {len(student_risks)}")
            for risk in student_risks:
                print(f"     * {risk['student']}: {risk['risk_score']}% ({risk['risk_level']})")
            print("   [OK] Teacher AI analysis working")
        else:
            print("   [ERROR] No teacher user found")
    except Exception as e:
        print(f"   [ERROR] Teacher AI error: {e}")
    
    # Student Dashboard Test
    print("\n   Student Dashboard:")
    try:
        student_user = User.objects.filter(role='student').first()
        if student_user:
            print(f"   - Student user found: {student_user.username}")
            student = Student.objects.get(user=student_user)
            
            ai_analysis = PerformanceInsights.get_comprehensive_analysis(student)
            print(f"   - Risk Score: {ai_analysis['risk_score']}")
            print(f"   - Status: {ai_analysis['overall_status']['status']}")
            print(f"   - Grade Average: {ai_analysis['grade_analysis']['average']}")
            print(f"   - Attendance Rate: {ai_analysis['attendance_analysis']['attendance_rate']}")
            print(f"   - Recommendations: {len(ai_analysis['improvement_suggestions'])}")
            print("   [OK] Student AI analysis working")
        else:
            print("   [ERROR] No student user found")
    except Exception as e:
        print(f"   [ERROR] Student AI error: {e}")
    
    # Parent Dashboard Test
    print("\n   Parent Dashboard:")
    try:
        parent_user = User.objects.filter(role='parent').first()
        if parent_user:
            print(f"   - Parent user found: {parent_user.username}")
            parent = Parent.objects.get(user=parent_user)
            children = parent.children.all()
            print(f"   - Children count: {children.count()}")
            
            for child in children:
                ai_analysis = PerformanceInsights.get_comprehensive_analysis(child)
                print(f"   - Child: {child.user.get_full_name()}")
                print(f"     * Risk Score: {ai_analysis['risk_score']}")
                print(f"     * Status: {ai_analysis['overall_status']['status']}")
                print(f"     * Grade Average: {ai_analysis['grade_analysis']['average']}")
                print(f"     * Attendance Rate: {ai_analysis['attendance_analysis']['attendance_rate']}")
            print("   [OK] Parent AI analysis working")
        else:
            print("   [ERROR] No parent user found")
    except Exception as e:
        print(f"   [ERROR] Parent AI error: {e}")
    
    # Test ML Utils directly
    print("\n3. Testing ML Utils Components:")
    
    student = Student.objects.first()
    if student:
        print(f"\n   Testing with student: {student.user.get_full_name()}")
        
        # Test StudentPerformancePredictor
        try:
            risk_score = StudentPerformancePredictor.calculate_risk_score(student)
            risk_level, risk_class = StudentPerformancePredictor.get_risk_level(risk_score)
            recommendations = StudentPerformancePredictor.get_recommendations(student, risk_score)
            print(f"   [OK] StudentPerformancePredictor: {risk_score}% ({risk_level})")
        except Exception as e:
            print(f"   [ERROR] StudentPerformancePredictor error: {e}")
        
        # Test GradeAnalyzer
        try:
            grade_analysis = GradeAnalyzer.analyze_subject_performance(student)
            print(f"   [OK] GradeAnalyzer: {grade_analysis['average']}% average")
        except Exception as e:
            print(f"   [ERROR] GradeAnalyzer error: {e}")
        
        # Test AttendancePatternAnalyzer
        try:
            attendance_analysis = AttendancePatternAnalyzer.analyze_attendance_patterns(student)
            print(f"   [OK] AttendancePatternAnalyzer: {attendance_analysis['attendance_rate']}% rate")
        except Exception as e:
            print(f"   [ERROR] AttendancePatternAnalyzer error: {e}")
        
        # Test PerformanceInsights
        try:
            comprehensive_analysis = PerformanceInsights.get_comprehensive_analysis(student)
            print(f"   [OK] PerformanceInsights: Complete analysis generated")
        except Exception as e:
            print(f"   [ERROR] PerformanceInsights error: {e}")
    
    print("\n=== Debug Complete ===")

if __name__ == "__main__":
    debug_ai_panels()