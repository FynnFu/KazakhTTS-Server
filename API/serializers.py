from rest_framework import serializers

from API.models import Module, Category, Group, Section, Lesson, TaskGroup, Task, Answer


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module

        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'lesson_count']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
