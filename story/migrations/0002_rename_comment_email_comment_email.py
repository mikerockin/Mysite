# Generated by Django 4.0 on 2022-02-14 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_email',
            new_name='email',
        ),
    ]
