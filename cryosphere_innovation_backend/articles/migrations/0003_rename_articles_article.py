# Generated by Django 4.2 on 2023-05-29 13:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0002_remove_articles_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Articles',
            new_name='Article',
        ),
    ]
