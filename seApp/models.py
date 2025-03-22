from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
class Student(AbstractUser):
    """ Custom Student model extending Django's User model """
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=10)
    batch_no = models.CharField(max_length=10)

    # Fix conflicts with default User model
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="student_users",  # Add unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="student_users_permissions",  # Add unique related_name
        blank=True
    )

    # Use roll_no as the username field
    username = None  
    USERNAME_FIELD = 'roll_no'
    REQUIRED_FIELDS = ['name', 'father_name', 'section', 'batch_no']
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"



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