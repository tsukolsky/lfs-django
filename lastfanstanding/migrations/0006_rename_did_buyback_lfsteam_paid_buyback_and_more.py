# Generated by Django 5.2 on 2025-04-10 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastfanstanding', '0005_lfsteam_lfs_game'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lfsteam',
            old_name='did_buyback',
            new_name='paid_buyback',
        ),
        migrations.AddField(
            model_name='lfsteam',
            name='paid_intitial',
            field=models.BooleanField(default=False),
        ),
    ]
