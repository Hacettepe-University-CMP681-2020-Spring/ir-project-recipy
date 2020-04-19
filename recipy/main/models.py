from django.urls import reverse
from django.utils.text import slugify
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models


class Recipe(models.Model):
    slug = models.SlugField(max_length=250, unique=True, editable=False)
    title = models.CharField(max_length=250, verbose_name='Title', db_index=True)
    type_of_dish = models.CharField(max_length=100, verbose_name='Type of Dish', null=True, blank=True)
    photo_url = models.URLField(max_length=500, verbose_name='Photo URL')
    occasion = models.CharField(max_length=250, verbose_name='Occasion', null=True, blank=True)
    ingredients = ArrayField(models.CharField(max_length=150), verbose_name='Ingredients')
    description = models.TextField(verbose_name='Description')
    instructions = ArrayField(models.TextField(), verbose_name='Instructions')
    total_time = models.CharField(max_length=100, verbose_name='Total Time', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) if not self.slug else self.slug
        return super().save(*args, **kwargs)
