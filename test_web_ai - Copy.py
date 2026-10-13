#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from core.models import *
from core.views import *

def test_web_ai_interface():
    print("=== Testing Web AI Interface ===\n")
    
    # Create a test client
    client = Client()
    
    # Test each dashboard
    print("1. Testing Dashboard Access:")
    
    # Test Admin Dashboard
    print("\n   Admin Dashboard:")
    try:
        admin_user = User.objects.filter(role='admin').first()
        if admin_user:
            client.force_login(admin_user)
            response = client.get('/dashboard/')
            print(f"   - Status Code: {response.status_code}")
            print(f"   - Template Used: {response.templates[0].name if response.templates else 'None'}")
            
            # Check if AI data is in context
            if 'ai_summary' in response.context:
                ai_summary = response.context['ai_summary']
                print(f"   - AI Summary in context: {ai_summary}")
                print("   [OK] Admin AI data available in template")
            else:
                print("   [ERROR] AI Summary not in context")
        else:
            print("   [ERROR] No admin user found")
    except Exception as e:
        print(f"   [ERROR] Admin dashboard error: {e}")
    
    # Test Teacher Dashboard
    print("\n   Teacher Dashboard:")
    try:
        teacher_user = User.objects.filter(role='teacher').first()
        if teacher_user:
            client.force_login(teacher_user)
            response = client.get('/dashboard/')
            print(f"   - Status Code: {response.status_code}")
            print(f"   - Template Used: {response.templates[0].name if response.templates else 'None'}")
            
            # Check if AI data is in context
            if 'student_risks' in response.context:
                student_risks = response.context['student_risks']
                print(f"   - Student risks count: {len(student_risks)}")
                if student_risks:
                    print(f"   - First student risk: {student_risks[0]['risk_score']}%")
                print("   [OK] Teacher AI data available in template")
            else:
                print("   [ERROR] Student risks not in context")
        else:
            print("   [ERROR] No teacher user found")
    except Exception as e:
        print(f"   [ERROR] Teacher dashboard error: {e}")
    
    # Test Student Dashboard
    print("\n   Student Dashboard:")
    try:
        student_user = User.objects.filter(role='student').first()
        if student_user:
            client.force_login(student_user)
            response = client.get('/dashboard/')
            print(f"   - Status Code: {response.status_code}")
            print(f"   - Template Used: {response.templates[0].name if response.templates else 'None'}")
            
            # Check if AI data is in context
            if 'ai_analysis' in response.context:
                ai_analysis = response.context['ai_analysis']
                print(f"   - Risk Score: {ai_analysis['risk_score']}")
                print(f"   - Status: {ai_analysis['overall_status']['status']}")
                print("   [OK] Student AI data available in template")
            else:
                print("   [ERROR] AI analysis not in context")
        else:
            print("   [ERROR] No student user found")
    except Exception as e:
        print(f"   [ERROR] Student dashboard error: {e}")
    
    # Test Parent Dashboard
    print("\n   Parent Dashboard:")
    try:
        parent_user = User.objects.filter(role='parent').first()
        if parent_user:
            client.force_login(parent_user)
            response = client.get('/dashboard/')
            print(f"   - Status Code: {response.status_code}")
            print(f"   - Template Used: {response.templates[0].name if response.templates else 'None'}")
            
            # Check if AI data is in context
            if 'children_analysis' in response.context:
                children_analysis = response.context['children_analysis']
                print(f"   - Children analysis count: {len(children_analysis)}")
                if children_analysis:
                    child_ai = children_analysis[0]['ai_analysis']
                    print(f"   - First child risk: {child_ai['risk_score']}%")
                    print(f"   - First child status: {child_ai['overall_status']['status']}")
                print("   [OK] Parent AI data available in template")
            else:
                print("   [ERROR] Children analysis not in context")
        else:
            print("   [ERROR] No parent user found")
    except Exception as e:
        print(f"   [ERROR] Parent dashboard error: {e}")
    
    print("\n=== Web Interface Test Complete ===")

if __name__ == "__main__":
    test_web_ai_interface()