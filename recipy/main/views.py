from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView

from main.forms import RegistrationForm


class HomePageView(TemplateView):
    template_name = 'main/home.html'


class LoginView(TemplateView):
    template_name = 'main/login.html'


class RegisterView(TemplateView):
    template_name = 'main/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            kwargs['form'] = RegistrationForm()
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('home')
        else:
            return render_to_response(self.template_name, {'form': form})
