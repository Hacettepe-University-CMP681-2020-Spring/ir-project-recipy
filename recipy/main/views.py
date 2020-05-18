import operator
import random
from collections import defaultdict
from functools import reduce

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView, DetailView, ListView

from main.forms import RegistrationForm
from main.models import Recipe
from main.utils import clean_text_and_tokenize
from recipy.settings import STOP_WORDS


#
INDEX = defaultdict(set)


def reload_index():
    """
    This function fetches recipes from database and indexes them to a global variable
    :return: None
    """
    global INDEX

    for recipe_pk, words in Recipe.objects.values_list('pk', 'words'):
        for word in words:
            INDEX[word].add(recipe_pk)


class HomePageView(ListView):
    model = Recipe
    paginate_by = 12
    ordering = ['id']
    context_object_name = 'recipes'
    template_name = 'main/home.html'

    def get(self, request, *args, **kwargs):
        params = request.GET
        if 'page' not in params and ('search' in params or 'include' in params or 'exclude' in params):
            self.template_name = 'main/recipe_list.html'

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({'search': self.request.GET.get('search', None)})

        return context

    def get_queryset(self):
        if self.request.GET.get('search'):
            # Clean text and tokenize.
            word_set = clean_text_and_tokenize(self.request.GET['search'])

            # Retrieve documents from index with using OR operator (union the documents)
            doc_set = set()
            for word in word_set:
                doc_set = doc_set.union(INDEX[word])

            # Filter the resultant recipes
            return super().get_queryset().filter(pk__in=doc_set).order_by(*self.ordering)

        elif self.request.GET.get('include') or self.request.GET.get('exclude'):
            include_set = clean_text_and_tokenize(self.request.GET.get('include'))
            exclude_set = clean_text_and_tokenize(self.request.GET.get('exclude'))

            # TODO: Preprocess the query-terms

            # Combine include query-terms with AND operator (intersect the documents)
            include_docs = INDEX[include_set.pop()] if include_set else set()
            for w in include_set:
                include_docs = include_docs.intersection(INDEX[w])

            # Combine exclude query-terms with OR operator (union the documents)
            exclude_docs = set()
            for w in exclude_set:
                exclude_docs = exclude_docs.union(INDEX[w])

            # Filter the resultant recipes
            return super().get_queryset().filter(pk__in=(include_docs - exclude_docs)).order_by(*self.ordering)

        else:
            return super().get_queryset()


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
