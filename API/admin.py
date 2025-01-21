import requests
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import Token

from .forms import LessonAdminForm, TaskAdminForm
from .audio_generate import generate
from .models import Category, Group, TaskGroup, Section, Module, Lesson, Answer, Task


# Register your models here.
class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'order')
    list_filter = ('age', )

    list_editable = ('order', 'age')

    ordering = ('order',)

    inlines = [SectionInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['word', 'image', 'list_of_word']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'get_module_age')
    list_filter = ('module__name', 'module__age' )

    def get_module_age(self, obj):
        return obj.module.age

    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ('word', 'section', 'image_thumbnail', 'word_audio_player', 'list_of_word_audio_player')
    list_filter = ('section__name', 'section__module__name', 'section__module__age')

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height:50px;" />',
            )
        return "Изображение не загружено"

    def word_audio_player(self, obj):
        if obj.word_audio:
            return mark_safe(
                '<audio controls>'
                f'<source src="{obj.word_audio.url}" type="audio/wav">'
                'Your browser does not support the audio element.'
                '</audio>'
            )
        return "Аудио не загружено"

    def list_of_word_audio_player(self, obj):
        if obj.list_of_word_audio:
            return mark_safe(
                '<audio controls>'
                f'<source src="{obj.list_of_word_audio.url}" type="audio/wav">'
                'Your browser does not support the audio element.'
                '</audio>'
            )
        return "Аудио не загружено"

    word_audio_player.short_description = 'Word Audio'
    list_of_word_audio_player.short_description = 'List of Word Audio'

    def save_model(self, request, obj, form, change):
        # Сначала сохраняем объект, чтобы был доступен его ID для использования в именах файлов
        super().save_model(request, obj, form, change)

        if '_continue' in request.POST:
            # Генерируем аудио
            generate(obj, obj.word_audio, obj.word, 'lessons/audio/word/')

            generate(obj, obj.list_of_word_audio, obj.list_of_word, 'lessons/audio/list_of_word/')

            # Отправляем сообщение пользователю
            self.message_user(request, 'Аудио успешно сгенерировано и сохранено.')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')
    list_filter = ('category__name', )
    list_editable = ('order',)

    ordering = ('order',)


@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'category', 'order')
    list_filter = ('group__name', 'group__category__name')
    list_editable = ('order',)

    ordering = ('order',)

    def category(self, obj):
        return obj.group.category.name

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height:50px;" />',
            )


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Количество дополнительных пустых строк для ответов


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm

    list_display = ('text', 'image_thumbnail', 'audio_player')
    list_filter = ('task_group__name', )
    inlines = [AnswerInline]

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height:50px;" />',
            )

    def audio_player(self, obj):
        if obj.audio:
            return mark_safe(
                '<audio controls>'
                f'<source src="{obj.audio.url}" type="audio/wav">'
                'Your browser does not support the audio element.'
                '</audio>'
            )
        return "Аудио не загружено"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if '_continue' in request.POST:

            generate(obj, obj.audio, obj.text, 'tasks/audio/')

            self.message_user(request, 'Аудио успешно сгенерировано и сохранено.')


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('question', 'text_or_image', 'is_correct')
#
#     def text_or_image(self, obj):
#         if obj.text:
#             return obj.text[:50]  # Возвращаем текст, если он есть
#         elif obj.image:
#             return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
#         return "No answer"

