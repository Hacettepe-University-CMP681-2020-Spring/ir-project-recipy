import operator
import random
from functools import reduce

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView, DetailView, ListView

from main.forms import RegistrationForm
from main.models import Recipe
from recipy.settings import STOP_WORDS


class HomePageView(ListView):
    model = Recipe
    paginate_by = 15
    ordering = ['id']
    context_object_name = 'recipes'
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


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'main/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Remove stopwords from the title
        cleaned_title = set(self.get_object().title.lower().split()) - STOP_WORDS

        # Query the elements
        context['related_recipes'] = Recipe.objects.filter(
            reduce(operator.or_, (Q(title__icontains=w) for w in cleaned_title))
        )

        # Get random 4 of them if the population size is larger than the sample size
        if len(context['related_recipes']) > 4:
            context['related_recipes'] = random.sample(list(context['related_recipes']), 4)

        return context
