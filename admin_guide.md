# 📚 SIMPLE ADMIN GUIDE - How to Add Students

## 🚀 Step 1: Access Admin Panel
1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials

## 👤 Step 2: Create a Student User Account
1. Click **"Users"** in the admin panel
2. Click **"Add User"** button (top right)
3. Fill in the form:
   - **Username**: `student1` (this is what they'll use to login)
   - **Password**: `student123` (simple password)
   - **Confirm Password**: `student123`
   - **First Name**: `John`
   - **Last Name**: `Doe`
   - **Email**: `john.doe@email.com`
   - **Role**: Select **"student"** from dropdown
4. Click **"Save"**

## 🎓 Step 3: Create Student Profile
1. Go back to admin home
2. Click **"Students"**
3. Click **"Add Student"** button
4. Fill in the form:
   - **User**: Select the user you just created (John Doe)
   - **Roll Number**: `2024001`
   - **Date of Birth**: Select a date (e.g., 2008-05-15)
   - **Student Class**: Select a class (create one first if needed)
   - **Parent Name**: `Robert Doe`
   - **Parent Phone**: `1234567890`
   - **Parent Email**: `parent@email.com`
   - **Address**: `123 Main Street`
5. Click **"Save"**

## 🏫 Step 4: Create Class (if needed)
1. Click **"Classes"**
2. Click **"Add Class"**
3. Fill in:
   - **Name**: `10`
   - **Section**: `A`
4. Click **"Save"**

## 📖 Step 5: Create Subjects (if needed)
1. Click **"Subjects"**
2. Click **"Add Subject"**
3. Fill in:
   - **Name**: `Mathematics`
   - **Code**: `MATH101`
4. Click **"Save"**

## 🔑 Step 6: Test Student Login
1. Go to: `http://127.0.0.1:8000`
2. Click **"Login as Student"**
3. Enter:
   - **Username**: `student1`
   - **Password**: `student123`
4. Click **"Login as Student"**

## ✅ Quick Summary:
1. **Create User** (username + password + role=student)
2. **Create Student Profile** (link to user + roll number + class)
3. **Test Login** on main site

## 🎯 Login Credentials Format:
- **Username**: What you set in User creation
- **Password**: What you set in User creation
- **Role**: Must be "student" for student login

That's it! The student can now login and see their dashboard.