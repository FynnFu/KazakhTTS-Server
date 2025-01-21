from django.urls import path, include

from .views import *

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('version/', VersionAPIView.as_view(), name='version'),
    path('generate-audio/', generate_audio, name='generate_audio'),
    path('get-modules/<int:age>/', ModulesAPIView.as_view(), name='get_modules'),
    path('get-module/<int:module_id>/', ModuleDetailAPIView.as_view(), name='get_module_byid'),
    path('get-sections/<int:module_id>/', SectionListAPIView.as_view(), name='get_section'),
    path('get-lessons/<int:section_id>/', LessonListAPIView.as_view(), name='get_lessons'),
    path('get-categories/', CategoryAPIView.as_view(), name='get_category'),
    path('get-groups/<int:age>/', GroupsAPIView.as_view(), name='get_group'),
    path('get-task-groups/<int:group_id>/', TaskGroupListAPIView.as_view(), name='get_task_groups'),
    path('get-tasks/<int:task_group_id>/', TaskListAPIView.as_view(), name='get_tasks'),
]
