# Generated by Django 2.2.7 on 2019-11-27 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0007_rent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='client',
        ),
        migrations.AddField(
            model_name='rent',
            name='clientWhoHaveHouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='whohavehouse', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='rent',
            name='clientWhoRent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rentbyme', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='day',
            field=models.CharField(max_length=255, null=True, verbose_name='День'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='month',
            field=models.CharField(max_length=255, null=True, verbose_name='Месяц'),
        ),
    ]