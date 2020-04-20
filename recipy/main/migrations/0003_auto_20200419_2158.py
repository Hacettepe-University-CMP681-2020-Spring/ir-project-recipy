# Generated by Django 2.2.12 on 2020-04-19 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200419_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='occasion',
        ),
        migrations.AddField(
            model_name='recipe',
            name='course',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Course'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Difficulty'),
        ),
    ]
