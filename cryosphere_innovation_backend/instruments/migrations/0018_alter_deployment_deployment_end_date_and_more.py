# Generated by Django 4.2 on 2023-05-22 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0017_deployment_deployment_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='deployment_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='deployment_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
