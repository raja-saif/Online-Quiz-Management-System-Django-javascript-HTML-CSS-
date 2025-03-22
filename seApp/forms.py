from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student
from django import forms
from .models import Quiz, QuizQuestion

class StudentSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, label="Full Name")
    roll_no = forms.CharField(max_length=20, label="Roll Number")
    section = forms.CharField(max_length=10, label="Section")
    batch_no = forms.CharField(max_length=10, label="Batch Number")

    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'section', 'batch_no', 'password1', 'password2']



class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question', 'marks']

