# Generated by Django 5.0.4 on 2024-05-04 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_generator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='youtute_link',
            new_name='youtube_link',
        ),
        migrations.RenameField(
            model_name='blogpost',
            old_name='youtute_title',
            new_name='youtube_title',
        ),
    ]
