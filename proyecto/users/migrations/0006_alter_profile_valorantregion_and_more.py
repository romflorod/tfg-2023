# Generated by Django 4.1.6 on 2023-02-10 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_valorantregion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='valorantRegion',
            field=models.TextField(blank=True, choices=[('NA', 'NA'), ('EU', 'EU'), ('AP', 'AP'), ('KR', 'KRU')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='valorantTagline',
            field=models.TextField(blank=True, max_length=4),
        ),
    ]
