#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms.settings')
django.setup()

from core.models import *
from core.ml_utils import *

def test_ai_analysis():
    print("=== Testing AI Analysis ===")
    
    # Test student data
    student = Student.objects.first()
    if student:
        print(f"Student: {student.user.get_full_name()}")
        print(f"Grades: {Grade.objects.filter(student=student).count()}")
        print(f"Attendance: {Attendance.objects.filter(student=student).count()}")
        
        # Test AI analysis
        try:
            analysis = PerformanceInsights.get_comprehensive_analysis(student)
            print(f"Risk Score: {analysis['risk_score']}")
            print(f"Status: {analysis['overall_status']['status']}")
            print(f"Grade Average: {analysis['grade_analysis']['average']}")
            print(f"Attendance Rate: {analysis['attendance_analysis']['attendance_rate']}")
            print("[SUCCESS] AI Analysis working!")
        except Exception as e:
            print(f"[ERROR] AI Analysis error: {e}")
    
    # Test parent data
    parent = Parent.objects.first()
    if parent:
        print(f"\nParent: {parent.user.username}")
        children = parent.children.all()
        print(f"Children count: {children.count()}")
        
        for child in children:
            try:
                analysis = PerformanceInsights.get_comprehensive_analysis(child)
                print(f"Child: {child.user.get_full_name()}")
                print(f"  Risk: {analysis['risk_score']}")
                print(f"  Status: {analysis['overall_status']['status']}")
            except Exception as e:
                print(f"  Error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_ai_analysis()