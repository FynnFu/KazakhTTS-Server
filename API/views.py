import json
from pathlib import Path

from django.core import serializers
from django.db.models import Count
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Lesson, Answer
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

from .models import Category, Group, TaskGroup, Module, Section, Task
from KazakhTTS import settings

from tts1.synthesize import synthesize
from .serializers import ModuleSerializer, CategorySerializer, GroupSerializer, SectionSerializer, LessonSerializer, \
    TaskGroupSerializer, TaskSerializer


def get_objects_with_file_urls(queryset, request, fields_to_process=['image']):
    objects_with_urls = []
    for obj in queryset:
        for field in fields_to_process:
            file_url = None
            if obj[field]:  # Проверяем, если файл существует
                file_url = request.build_absolute_uri(default_storage.url(obj[field]))
                # file_url = file_url.replace('http://', 'https://')
            obj[field] = file_url
        objects_with_urls.append(obj)
    return objects_with_urls


class VersionAPIView(APIView):
    def get(self, request):
        return JsonResponse({'version': settings.VERSION})


@csrf_exempt
def generate_audio(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        field = data.get('field')
        lesson_id = data.get('lesson_id')  # Передаем ID урока для обновления записи

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Lesson not found'}, status=404)

        folder_to_save = Path("media/lessons/audio")
        folder_to_save.mkdir(parents=True, exist_ok=True)  # Создаем папку, если её нет

        if field == 'word':
            word = data.get('word')
            if word:
                output_wav_file = folder_to_save / f"word_audio_{lesson_id}.wav"
                synthesize(word, output_wav_file)
                lesson.word_audio = output_wav_file  # Сохраняем путь к аудиофайлу в модели
                lesson.save()
                return JsonResponse({'status': 'success', 'message': 'Audio for word generated'})

            return JsonResponse({'status': 'error', 'message': 'Word is empty'}, status=400)

        elif field == 'list_of_word':
            list_of_word = data.get('list_of_word')
            if list_of_word:
                output_wav_file = folder_to_save / f"list_of_word_audio_{lesson_id}.wav"
                synthesize(list_of_word, output_wav_file)
                lesson.list_of_word_audio = output_wav_file  # Сохраняем путь к аудиофайлу в модели
                lesson.save()
                return JsonResponse({'status': 'success', 'message': 'Audio for list of words generated'})
            return JsonResponse({'status': 'error', 'message': 'List of words is empty'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


class ModulesAPIView(generics.ListAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        age = self.kwargs.get('age')
        auth_header = self.request.headers.get("Authorization")
        print(f"Authorization Header: {auth_header}")
        return Module.objects.filter(age=age)


class ModuleDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ModuleSerializer

    def get(self, request, *args, **kwargs):
        module_id = self.kwargs.get('module_id')
        module = get_object_or_404(Module, id=module_id)
        serializer = self.get_serializer(module)
        return Response(serializer.data)


class SectionListAPIView(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        module_id = self.kwargs.get('module_id')
        get_object_or_404(Module, id=module_id)
        # Аннотируем количество уроков в каждой секции
        return Section.objects.filter(module_id=module_id).annotate(
            lesson_count=Count('lessons')  # Используем 'lessons' для подсчета связанных уроков
        )


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        get_object_or_404(Section, id=section_id)
        return Lesson.objects.filter(section__id=section_id)


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()

    serializer_class = CategorySerializer


class GroupsAPIView(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        age = self.kwargs.get('age')

        category = get_object_or_404(Category, age=age)

        return Group.objects.filter(category=category)


class TaskGroupListAPIView(generics.ListAPIView):
    serializer_class = TaskGroupSerializer

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        return TaskGroup.objects.filter(group=group)


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        task_group_id = self.kwargs.get('task_group_id')
        task_group = get_object_or_404(TaskGroup, id=task_group_id)
        return Task.objects.filter(task_group=task_group).prefetch_related('answers')
