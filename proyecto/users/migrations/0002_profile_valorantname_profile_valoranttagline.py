# Generated by Django 4.0.8 on 2023-02-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='valorantName',
            field=models.TextField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='valorantTagline',
            field=models.TextField(blank=True, max_length=5),
        ),
    ]
