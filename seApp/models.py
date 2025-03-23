from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """ Custom user manager for handling different user roles (students & teachers). """
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    """ Custom user model for Students & Teachers """
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Fix group and permission conflicts
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Student(models.Model):
    """ Student Profile (Linked to CustomUser) """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # TEMPORARY FIX
    Sname = models.CharField(max_length=30,null=True, blank=True)#abhi k liye null set kiyua
    roll_no = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=10)
    batch_no = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username if self.user else 'No User'} - {self.roll_no}"


class Teacher(models.Model):
    """ Teacher Profile (Linked to CustomUser) """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.department}"


# Question Bank
class Question(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('history', 'History'),
    ]

    text = models.TextField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    question_type = models.CharField(max_length=50, choices=[('MCQ', 'MCQ'), ('Short Answer', 'Short Answer')])

    def __str__(self):
        return f"{self.text} ({self.get_subject_display()})"

# Answer Bank (Stores correct answers)
class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    correct_answer = models.TextField()

    def __str__(self):
        return f"Answer for: {self.question.text}"

# Quiz Model (Stores quizzes created by teachers)
# Updated Quiz Model (Removed student_name)
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)  # Optional description for admin details
    
    subject = models.CharField(max_length=20, choices=Question.SUBJECT_CHOICES, default='math')  # Add Subject Field

    def __str__(self):
        return f"Quiz: {self.title} ({self.get_subject_display()}) by {self.instructor.username}"
    
    def get_question_count(self):
        """Returns the total number of questions in this quiz"""
        return self.quiz_questions.count()
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

# Quiz Questions Model (Links selected questions with a quiz)
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.question.text} - {self.marks} Marks"