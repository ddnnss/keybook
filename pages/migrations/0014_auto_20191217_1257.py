# Generated by Django 2.2.7 on 2019-12-17 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0013_message_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='message',
            name='messageFrom',
        ),
        migrations.RemoveField(
            model_name='message',
            name='messageTo',
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Сообщение от'),
        ),
        migrations.AlterField(
            model_name='message',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('users', models.ManyToManyField(blank=True, null=True, related_name='chatusers', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.Chat', verbose_name='В чате'),
        ),
    ]
