import re
import string

from django.urls import reverse
from django.utils.text import slugify
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models

from recipy.settings import LEMMATIZER, STOP_WORDS, CLEANED_STOP_WORDS


class Recipe(models.Model):
    slug = models.SlugField(max_length=250, unique=True, editable=False)
    title = models.CharField(max_length=250, verbose_name='Title', db_index=True)
    course = models.CharField(max_length=50, verbose_name='Course', null=True, blank=True)
    type_of_dish = models.CharField(max_length=100, verbose_name='Type of Dish', null=True, blank=True)
    difficulty = models.CharField(max_length=50, verbose_name='Difficulty', null=True, blank=True)
    ingredients = ArrayField(models.CharField(max_length=150), verbose_name='Ingredients')
    description = models.TextField(verbose_name='Description')
    instructions = ArrayField(models.TextField(), verbose_name='Instructions')
    photo_url = models.URLField(max_length=500, verbose_name='Photo URL')
    total_time = models.CharField(max_length=100, verbose_name='Total Time', null=True, blank=True)

    # Index related attributes
    words = ArrayField(models.CharField(max_length=16), verbose_name='Words', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) if not self.slug else self.slug

        # Build the whole string and remove digits from it
        whole_string = re.sub(r'\d+', '', ' '.join(self.instructions).lower())

        # Remove punctuations from the string
        cleaned_string = whole_string.translate(str.maketrans('', '', string.punctuation))

        # Tokenize and remove the stop-words from the instructions
        tokens = set(w for w in re.split(r'[-\s\n]', cleaned_string) if w) - CLEANED_STOP_WORDS

        # Lemmatize the string and save the results to the DB
        self.words = sorted(set(LEMMATIZER.lemmatize(token) for token in tokens))

        return super().save(*args, **kwargs)
