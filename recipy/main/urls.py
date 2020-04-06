from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from main.views import HomePageView, RegisterView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login', LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True),  name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
]
