# PostgreSQL Setup Instructions

## 1. pgAdmin4 Database Creation
1. Open pgAdmin4
2. Connect to PostgreSQL server
3. Right-click "Databases" → Create → Database
4. Name: `student_system_db`
5. Click Save

## 2. Update Django Settings
Edit `sms/settings.py` and replace `'your_postgres_password'` with your actual PostgreSQL password.

## 3. Install Dependencies & Setup
```bash
pip install psycopg2-binary
python manage.py makemigrations
python manage.py migrate
python create_sample_data.py
python manage.py runserver
```

## 4. Login Credentials
- Admin: admin / admin123
- Teacher: teacher1 / teacher123
- Student: student1 / student123
- Parent: parent1 / parent123

## 5. Access Application
http://127.0.0.1:8000