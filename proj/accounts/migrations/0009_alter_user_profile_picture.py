# Generated by Django 4.2.4 on 2023-11-12 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='avatar.jpg', upload_to='pics'),
        ),
    ]
