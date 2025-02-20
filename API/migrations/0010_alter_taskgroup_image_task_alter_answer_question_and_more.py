# Generated by Django 5.0.7 on 2024-09-09 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_remove_section_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskgroup',
            name='image',
            field=models.ImageField(upload_to='task_groups/'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='tasks/')),
                ('audio', models.FileField(blank=True, null=True, upload_to='tasks/audio/')),
                ('task_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.taskgroup')),
            ],
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='API.task'),
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
