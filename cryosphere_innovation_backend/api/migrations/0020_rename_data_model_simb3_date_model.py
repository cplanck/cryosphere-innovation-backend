# Generated by Django 4.2 on 2023-05-19 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_datamodel_remove_simb3_data_model_simb3_data_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simb3',
            old_name='data_model',
            new_name='date_model',
        ),
    ]
