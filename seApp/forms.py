from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student
from django import forms
from .models import Quiz, QuizQuestion

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Teacher

class StudentSignUpForm(UserCreationForm):
    roll_no = forms.CharField(max_length=20)
    section = forms.CharField(max_length=10)
    batch_no = forms.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]  # Required fields for signup

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "student"  # Set user type

        if commit:
            user.save()  # Save user first
            Student.objects.create(  # Create student profile
                user=user,
                roll_no=self.cleaned_data["roll_no"],
                section=self.cleaned_data["section"],
                batch_no=self.cleaned_data["batch_no"],
            )
        return user
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question', 'marks']

