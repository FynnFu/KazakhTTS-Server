import os
from django.conf import settings
from tts1.synthesize import synthesize  # Импорт функции синтеза


def generate(obj, obj_audio, text, path):
    # Генерация аудио для слова
    audio_path = os.path.join(settings.MEDIA_ROOT, f'{path}', f'{obj.id}.wav')
    synthesize(text, audio_path)
    obj_audio.name = f'{path}{obj.id}.wav'

    # Сохраняем изменения
    obj.save()
    