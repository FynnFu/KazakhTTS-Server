# Generated by Django 5.0.7 on 2024-09-04 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_task'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Task',
            new_name='TaskGroup',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
