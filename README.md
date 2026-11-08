# OQ-EMS: Online Quiz & Exam Management System

OQ-EMS is a Django web app for building quizzes from a subject-wise question bank. Instructors choose questions by subject and give each one marks, and students sign up, log in and browse the quizzes that are available.

## ✨ Features

### 👩‍🎓 Students
- Sign up with a username, password, roll number, section and batch (`StudentSignUpForm`). The account is created as a `student` user with a linked `Student` profile.
- Log in with Django's built-in `AuthenticationForm`.
- A **student dashboard** lists every available quiz with its subject and instructor, and links to each quiz.
- The **quiz view** shows the quiz title, instructor, subject, total marks, creation date and each question with its marks and type. Short-answer questions get an answer box.

### 👨‍🏫 Instructors
- A **quiz creation page** with fields for the title and subject, a list of questions loaded for the chosen subject, a list of the selected questions and a running total of marks.
- When a quiz is saved, each selected question is stored as a `QuizQuestion` with its own marks, and the quiz's `total_marks` is calculated automatically.

### 🛠️ Admin (Django admin)
- Manage quizzes, with their questions shown inline, plus the question bank, the answer bank and students.
- Filter quizzes by instructor and creation date. Filter questions by subject and type. Search by quiz title, question text or answer.

### 🔌 JSON endpoint
- `GET /get-questions/?subject=<subject>` returns the questions for that subject (`id`, `text`, `question_type`). Without a `subject` parameter, it returns the list of subjects.
- `POST /get-questions/` accepts the JSON body `{"subject": "..."}`.
- `/test-api/` is a small HTML page that calls this endpoint with `fetch`.

## 🗂️ Data model
| Model | Purpose |
|---|---|
| `CustomUser` | Extends `AbstractUser` with a `user_type` of `student` or `teacher` |
| `Student` / `Teacher` | Profiles linked one-to-one to a user (roll no, section, batch / department) |
| `Question` | Question bank entry: text, subject (Mathematics, Science, History) and type (MCQ or Short Answer) |
| `Answer` | The correct answer for a question |
| `Quiz` | Title, instructor, subject, description, total marks and creation time |
| `QuizQuestion` | Links a question to a quiz with its marks |

## 🧰 Tech stack
- **Backend:** Python, Django, `django-browser-reload`
- **Database:** SQLite
- **Frontend:** Django templates, HTML, CSS and JavaScript (`fetch` calls to the JSON endpoint)

## 📁 Project structure
```
.
├── manage.py
├── se/                  # Django project (settings, urls, wsgi/asgi)
├── seApp/               # Main app: models, views, forms, urls, admin
├── templates/           # login, signup, student_dashboard, quizCreate, quizView, test_api
├── SRS.docx             # Software Requirements Specification
├── Product Backlog.docx
└── Sprint Backlog.docx
```

## 🚀 Setup & run
```bash
git clone https://github.com/raja-saif/Online-Quiz-Management-System-Django-javascript-HTML-CSS-.git
cd Online-Quiz-Management-System-Django-javascript-HTML-CSS-

python -m venv venv
# Windows: venv\Scripts\activate    macOS/Linux: source venv/bin/activate
pip install django django-browser-reload

python manage.py makemigrations seApp   # migration files are not committed
python manage.py migrate
python manage.py createsuperuser        # to manage the question bank in /admin
python manage.py runserver
```
Then open:
- `http://127.0.0.1:8000/` to sign up
- `/login/` to log in
- `/student_dashboard/` for the student dashboard
- `/create-quiz/` to create a quiz
- `/admin/` for the Django admin

## 📌 Status
The question bank, quiz creation and viewing quizzes all work. Students cannot submit answers yet, and there is no automatic grading.

## 👤 Author
Raja Saif Ali — [GitHub](https://github.com/raja-saif) · [LinkedIn](https://www.linkedin.com/in/raja-saif-01702329a/)
