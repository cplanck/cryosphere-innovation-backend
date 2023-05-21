# Generated by Django 4.2 on 2023-05-19 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_simb3_sensor_suite_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(blank=True, max_length=100, null=True)),
                ('field_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='simb3',
            name='data_model',
        ),
        migrations.AddField(
            model_name='simb3',
            name='data_model',
            field=models.ManyToManyField(to='api.datamodel'),
        ),
    ]