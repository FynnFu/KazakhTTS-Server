# Generated by Django 5.0.7 on 2024-10-08 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_rename_question_answer_task_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='module',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
