🧠 Online Learning System

A role-based learning platform where students can enroll in courses, instructors can manage content, and admins can oversee the system.
Ideal for schools, academies, or training centers that want a modular, scalable platform.

✨ Features
👩‍🎓 Students

Browse courses by category

Enroll and access lessons

Submit and read course reviews

👨‍🏫 Instructors

Create and manage courses

Add and edit lessons

View enrolled students

🧑‍💼 Admin / Employee

Full platform control

Manage users, courses, and categories

Monitor statistics and reports



⚙️ Setup Guide
# 1. Clone the repository
git clone https://github.com/HoutWill/Online-Learning-System.git
cd Online-Learning-System

# 2. Create and activate virtual environment
python -m venv env
env\Scripts\activate        # Windows
source env/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver


🔗 Visit the app at: http://127.0.0.1:8000/


🔑 Sample Login Credentials
Role	Username	Password
Student 	hout	   pass123456
Instructor	teacherA	-----------
Employee	admin1	    ----------






Online-Learning-System/
├── accounts/          # User auth & roles
├── courses/            # Courses and lessons
├── enrollment/         # Enrollment logic
├── templates/           # HTML templates
├── static/               # CSS, JS, Images
├── db.sqlite3            # Default database
└── manage.py


📌 Notes

Default database is SQLite — switch to PostgreSQL or MySQL by editing settings.py.

Ensure DEBUG=True only during development.