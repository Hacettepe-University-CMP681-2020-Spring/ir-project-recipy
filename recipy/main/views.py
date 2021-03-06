import operator
import random
from functools import reduce

from django.contrib.auth import authenticate, login
from django.db.models import Q, When, Case
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView, DetailView, ListView

from main.forms import RegistrationForm
from main.models import Recipe
from main.utilities.text_operations import clean_text_and_tokenize
from recipy.settings import STOP_WORDS, INDEX, ALL_DOCUMENTS, STATISTICAL_THESAURUS


class HomePageView(ListView):
    model = Recipe
    paginate_by = 12
    # ordering = ['id']
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
        context.update({'include': self.request.GET.get('include', None)})
        context.update({'exclude': self.request.GET.get('exclude', None)})

        return context

    def get_queryset(self):
        if self.request.GET.get('search'):
            word_set = clean_text_and_tokenize(self.request.GET['search'])

            # Retrieve documents from index with using OR operator (union the documents)
            doc_set = set()
            for word in word_set:
                doc_set = doc_set.union(INDEX[word])

            # Filter the resultant recipes
            return super().get_queryset().filter(pk__in=doc_set).order_by('id')

        elif self.request.GET.get('include') or self.request.GET.get('exclude'):
            include_set = clean_text_and_tokenize(self.request.GET.get('include'))
            exclude_set = clean_text_and_tokenize(self.request.GET.get('exclude'))

            # Expand include query
            expansion_include_set = set()
            for query_term in include_set:
                expansion_include_set.update(STATISTICAL_THESAURUS[query_term])

            # Expand exclude query
            expanded_exclude_set = set()
            for query_term in exclude_set:
                expanded_exclude_set.add(query_term)
                expanded_exclude_set.update(STATISTICAL_THESAURUS[query_term])

            # To prevent some terms gone missing
            expanded_exclude_set = expanded_exclude_set.difference(include_set)
            expansion_include_set = expansion_include_set.difference(exclude_set)

            # Combine include query-term results with AND operator (intersect the documents)
            include_docs = ALL_DOCUMENTS.copy()
            for w in include_set:
                include_docs.intersection_update(INDEX[w])

            # Combine expansion query-term results with OR operator (union the documents)
            expansion_docs = set()
            for w in expansion_include_set:
                expansion_docs = expansion_docs.union(INDEX[w])

            # Combine exclude query-term results with OR operator (union the documents)
            exclude_docs = set()
            for w in expanded_exclude_set:
                exclude_docs = exclude_docs.union(INDEX[w])

            # Put recipes in order
            ordered_include_docs = sorted(include_docs - exclude_docs, reverse=True) + sorted(expansion_docs - exclude_docs)

            # Get only the recipes which will be displayed
            ordered_include_docs = ordered_include_docs[:self.paginate_by * (int(self.request.GET.get('page', 1)) + 1)]

            # Filter the resultant recipes
            return super().get_queryset().filter(
                pk__in=ordered_include_docs
            ).order_by(
                Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ordered_include_docs)])
            )

        else:
            return super().get_queryset().order_by('id')


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
