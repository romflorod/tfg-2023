# Generated by Django 4.0.8 on 2023-02-21 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_profile_valorantregion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='valorantAssists',
            field=models.TextField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='profile',
            name='valorantBodyshots',
            field=models.TextField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='profile',
            name='valorantDeaths',
            field=models.TextField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='profile',
            name='valorantHeadshots',
            field=models.TextField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='profile',
            name='valorantKills',
            field=models.TextField(blank=True, max_length=40),
        ),
    ]
