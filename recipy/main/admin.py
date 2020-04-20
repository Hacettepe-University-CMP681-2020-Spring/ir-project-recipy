from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from main.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        'title',
        'type_of_dish',
        'course',
        'total_time',
    )
