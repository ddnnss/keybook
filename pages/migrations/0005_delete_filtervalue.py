# Generated by Django 2.2.7 on 2019-11-24 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_remove_categoryfilter_values'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FilterValue',
        ),
    ]
