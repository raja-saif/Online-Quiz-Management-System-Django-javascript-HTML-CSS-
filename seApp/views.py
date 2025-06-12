from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentSignUpForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.



def student_signup(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        print("Form Valid:", form.is_valid())  # Debugging
        print("Form Errors:", form.errors)  # Print errors

        if form.is_valid():
            student = form.save()
            login(request, student)
            return redirect("seApp:student_dashboard")  # Redirect after signup
    else:
        print("GET Request: Showing Signup Form")
        form = StudentSignUpForm()

    return render(request, "signup.html", {"form": form})


def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        
        print("Form Valid:", form.is_valid())  # Debugging
        print("Form Errors:", form.errors)  # Print errors
        print("Form Data:", form.data)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("seApp:student_dashboard")  # Redirect to dashboard
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Question, Quiz, QuizQuestion
from .forms import QuizForm, QuizQuestionForm

# Quiz Creation Page
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, QuizQuestion
from .forms import QuizForm

def create_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.instructor = request.user
            quiz.subject = request.POST.get("subject")  # Save selected subject
            quiz.save()

            selected_questions = request.POST.getlist('questions[]')  # Get selected question IDs
            total_marks = 0

            for question_id in selected_questions:
                try:
                    question = Question.objects.get(id=question_id)
                    marks = int(request.POST.get(f"marks_{question_id}", 0))  # Get marks for each question
                    total_marks += marks
                    QuizQuestion.objects.create(quiz=quiz, question=question, marks=marks)  # Save question
                except Question.DoesNotExist:
                    print(f"Question with ID {question_id} not found.")

            quiz.total_marks = total_marks
            quiz.save()

            return redirect("seApp:view_quiz", quiz_title=quiz.title)  # FIX: Correct redirect

    else:
        form = QuizForm()

    subjects = Question.objects.values_list("subject", flat=True).distinct()
    return render(request, "quizCreate.html", {"form": form, "subjects": subjects})



# Fetch questions based on selected subject (AJAX Call)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Question
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


# Modified view to accept GET requests as well

@csrf_exempt  # For easier testing - remove in production
def get_questions(request):
    print(f"Request method: {request.method}")
    
    # Handle GET requests
    if request.method == "GET":
        # Get subject from query parameters
        subject = request.GET.get("subject", "").strip().lower()
        print(f"GET subject: {subject}")
        
        if not subject:
            # Return all subjects if no subject specified
            subjects = list(Question.objects.values_list("subject", flat=True).distinct())
            return JsonResponse({"subjects": subjects}, safe=False)
        
        # Return questions for the specified subject
        questions = list(Question.objects.filter(subject=subject).values("id", "text", "question_type"))
        return JsonResponse(questions, safe=False)
    
    # Handle POST requests
    elif request.method == "POST":
        try:
            # Parse JSON data from request body
            body = request.body.decode('utf-8')
            print(f"POST body: {body}")
            
            data = json.loads(body)
            subject = data.get("subject", "").strip().lower()
            print(f"POST subject: {subject}")
            
            if not subject:
                return JsonResponse({"error": "Subject not provided"}, status=400)
            
            # Return questions for the specified subject
            questions = list(Question.objects.filter(subject=subject).values("id", "text", "question_type"))
            return JsonResponse(questions, safe=False)
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return JsonResponse({"error": f"Invalid JSON: {str(e)}"}, status=400)
        except Exception as e:
            print(f"Exception: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    
    # Reject other request methods
    else:
        return JsonResponse({"error": f"Only GET and POST requests are allowed. You sent: {request.method}"}, status=405)

def test_questions_api(request):
    """A simple test page to check our API endpoint"""
    return render(request, 'test_api.html')

@login_required
def quiz_detail(request, quiz_title):
    """View for displaying a quiz's details"""
    quiz = get_object_or_404(Quiz, title=quiz_title)
    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question')
    
    return render(request, 'quizView.html', {
        'quiz': quiz,
        'quiz_questions': quiz_questions,
    })

def student_dashboard(request):
    """Dashboard view for students showing available quizzes"""
    quizzes = Quiz.objects.all()  # Show all quizzes
    return render(request, "student_dashboard.html", {"quizzes": quizzes})


'''
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('green_app:home')  # Replace with your home page or desired redirect page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('green_app:home')  # Redirect to a home page or any other page
        else:
            messages.error(request,"User Name or Password is incorrect.")    
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('green_app:home')  # Redirect to the login page or any other page

'''