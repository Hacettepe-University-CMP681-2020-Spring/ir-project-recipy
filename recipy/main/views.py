from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView, DetailView

from main.forms import RegistrationForm
from main.models import Recipe


class HomePageView(TemplateView):
    template_name = 'main/home.html'

    def get(self, request, *args, **kwargs):
        kwargs['recipes'] = Recipe.objects.order_by('id')
        return super().get(request, *args, **kwargs)


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


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'main/recipe_detail.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
