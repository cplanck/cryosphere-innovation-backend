# Generated by Django 4.2 on 2023-05-19 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_simb3data_deployment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simb3deployment',
            name='deployment_notes',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
