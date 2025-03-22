from django.urls import path
from seApp import views
app_name="seApp"

urlpatterns = [
    path("login/", views.loginPage, name="login"),
]