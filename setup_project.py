#!/usr/bin/env python3
"""
Clean setup script for Student Progress Management System with AI features
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("🎓 Student Progress Management System - Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    print("📋 Setting up the AI-Enhanced Student Management System...")
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        return False
    
    # Create sample data
    if not run_command("python create_sample_data.py", "Creating sample data"):
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    
    print("\n🚀 Your AI-Enhanced Student Management System is ready!")
    print("\n📋 Features Available:")
    print("   • 🤖 AI Performance Risk Prediction")
    print("   • 📊 Automated Grade Analysis & Insights") 
    print("   • 📅 Smart Attendance Pattern Detection")
    print("   • 💡 Personalized AI Recommendations")
    print("   • 📈 Real-time Progress Monitoring")
    print("   • 🎯 Early Intervention Alerts")
    
    print("\n🔑 Login Credentials:")
    print("   • Admin:   admin / admin123")
    print("   • Teacher: teacher1 / teacher123")
    print("   • Student: student1 / student123") 
    print("   • Parent:  parent1 / parent123")
    
    print("\n🌐 Start the server:")
    print("   python manage.py runserver")
    print("   Then visit: http://127.0.0.1:8000")
    
    print("\n🎯 AI Features in Each Panel:")
    print("   • Admin: System-wide AI risk analysis and monitoring")
    print("   • Teacher: Student risk assessment and intervention alerts")
    print("   • Student: Personal AI insights and improvement recommendations")
    print("   • Parent: Children's progress monitoring with AI alerts")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)