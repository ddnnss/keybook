# Generated by Django 2.2.7 on 2019-11-24 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_delete_filtervalue'),
        ('filter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filtervalue',
            name='filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat_filter', to='pages.CategoryFilter', verbose_name='Фильтр'),
        ),
    ]
