# Generated by Django 5.0.7 on 2024-10-15 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0013_alter_group_options_alter_taskgroup_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='list_of_word',
            field=models.TextField(blank=True, null=True),
        ),
    ]
