# Generated by Django 4.2 on 2023-05-19 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0014_remove_deployment_instrument_delete_instrument'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIMB3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('serial_number', models.CharField(max_length=100, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('data_model', models.JSONField(null=True)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('notes', models.TextField(blank=True, max_length=5000, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('transmission_interval', models.CharField(choices=[('1', '1 Hour'), ('4', '4 Hours'), ('0', 'Other')], default='4', max_length=20)),
                ('build_date', models.DateField(blank=True, null=True)),
                ('fetch_data', models.BooleanField(default=True)),
                ('decode', models.BooleanField(default=True)),
                ('post_to_database', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
