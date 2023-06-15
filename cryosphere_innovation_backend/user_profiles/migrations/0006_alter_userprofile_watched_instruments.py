# Generated by Django 4.2 on 2023-06-07 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0018_alter_deployment_deployment_end_date_and_more'),
        ('user_profiles', '0005_alter_userprofile_watched_instruments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='watched_instruments',
            field=models.ManyToManyField(blank=True, to='instruments.deployment'),
        ),
    ]