# Generated by Django 4.2.2 on 2023-06-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]
