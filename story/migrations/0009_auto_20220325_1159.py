# Generated by Django 3.2.12 on 2022-03-25 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0008_alter_comment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
    ]