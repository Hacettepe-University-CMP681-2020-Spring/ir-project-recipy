# Generated by Django 2.2.12 on 2020-05-12 21:10

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200419_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='words',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=16), null=True, size=None, verbose_name='Words'),
        ),
    ]
