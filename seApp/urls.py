from django.urls import path
from seApp import views
app_name = "seApp" 

urlpatterns = [
    path('', views.student_signup, name='signup'),
    path('login/', views.loginPage, name='login'),
    path("create-quiz/", views.create_quiz, name="create_quiz"),
    path('get-questions/', views.get_questions, name='get_questions'),
    path('test-api/', views.test_questions_api, name='test_api'),
    path('view-quiz/<str:quiz_title>/', views.quiz_detail, name='view_quiz'),  # ✅ NEW

]