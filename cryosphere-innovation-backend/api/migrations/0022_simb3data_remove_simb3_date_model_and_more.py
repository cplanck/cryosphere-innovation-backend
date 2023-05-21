# Generated by Django 4.2 on 2023-05-19 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_datamodel_field_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIMB3Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='simb3',
            name='date_model',
        ),
        migrations.AddField(
            model_name='simb3deployment',
            name='data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.simb3data'),
        ),
    ]