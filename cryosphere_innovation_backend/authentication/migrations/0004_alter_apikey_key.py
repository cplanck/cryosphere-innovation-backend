# Generated by Django 4.2 on 2023-06-12 22:12

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_apikey_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(default=authentication.models.APIKey.generate_key, max_length=64, unique=True),
        ),
    ]
