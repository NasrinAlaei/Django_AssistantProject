# Generated by Django 4.2.4 on 2023-11-08 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessionn', '0004_remove_session_attachfile_session_attachfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='time_end',
            field=models.DateTimeField(),
        ),
    ]
