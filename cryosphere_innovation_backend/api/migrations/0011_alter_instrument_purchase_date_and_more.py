# Generated by Django 4.2 on 2023-04-30 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_instrument_avatar_alter_instrument_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='purchase_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='starred_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
