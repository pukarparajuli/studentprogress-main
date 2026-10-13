#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms.settings')
django.setup()

from django.test import Client
from core.models import User

def test_student_ai_analysis():
    print("Testing student AI analysis fix...")
    
    client = Client()
    
    # Login as teacher
    teacher_user = User.objects.filter(role='teacher').first()
    if teacher_user:
        client.force_login(teacher_user)
        
        # Test the problematic URL
        response = client.get('/student-ai-analysis/1/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Student AI analysis page loads without errors!")
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            
    else:
        print("❌ No teacher user found")

if __name__ == "__main__":
    test_student_ai_analysis()