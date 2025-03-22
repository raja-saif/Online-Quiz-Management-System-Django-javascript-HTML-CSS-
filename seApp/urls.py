from django.urls import path
from seApp import views
app_name = "seApp" 

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("", views.student_signup, name="signup"),
    path("create-quiz/", views.create_quiz, name="create_quiz"),
    path('get-questions/', views.get_questions, name='get_questions'),
    path('test-api/', views.test_questions_api, name='test_api'),
    path('view_quiz/<int:quiz_id>/', views.quiz_detail, name='view_quiz'),
]