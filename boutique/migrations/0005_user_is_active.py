# Generated by Django 4.1.7 on 2023-05-14 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0004_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
