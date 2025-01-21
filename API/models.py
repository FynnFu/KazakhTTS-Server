import os
import asyncio
from django.db import models
from django.core.files.storage import default_storage


# Create your models here.
class Module(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='module/')
    age = models.IntegerField()

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} - {self.age} жыл'


class Section(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.module}'


class Lesson(models.Model):
    section = models.ForeignKey(Section, related_name='lessons', on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lessons/', blank=True, null=True)
    list_of_word = models.TextField(null=True, blank=True)
    word_audio = models.FileField(upload_to='lessons/audio/word/', blank=True, null=True)
    list_of_word_audio = models.FileField(upload_to='lessons/audio/list_of_word/', blank=True, null=True)

    def __str__(self):
        return self.word


class Category(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Group(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class TaskGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='task_groups/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} - {self.group.name} - {self.group.category.name}'


class Task(models.Model):
    task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='tasks/', blank=True, null=True)
    audio = models.FileField(upload_to='tasks/audio/', blank=True, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    task = models.ForeignKey(Task, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='answers/', blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.task.text}: {self.text[:50]}..." if self.text else "Image answer"
