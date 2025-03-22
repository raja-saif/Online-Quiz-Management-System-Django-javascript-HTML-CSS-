from django.shortcuts import render

# Create your views here.



def loginPage(request):
    return render(request, 'login.html') 
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