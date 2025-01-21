from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Lesson, Task


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.word_audio:
            audio_html = format_html(f'''
                        <audio controls style="height: 50px; vertical-align: middle;">
                            <source src="{self.instance.word_audio.url}" type="audio/wav">
                            Your browser does not support the audio element.
                        </audio>
                    ''')
            self.fields['word_audio'].help_text = audio_html

        if self.instance and self.instance.list_of_word_audio:
            audio_html = format_html(f'''
                        <audio controls style="height: 50px; vertical-align: middle;">
                            <source src="{self.instance.list_of_word_audio.url}" type="audio/wav">
                            Your browser does not support the audio element.
                        </audio>
                    ''')
            self.fields['list_of_word_audio'].help_text = audio_html


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.audio:
            audio_html = format_html(f'''
                        <audio controls style="height: 50px; vertical-align: middle;">
                            <source src="{self.instance.audio.url}" type="audio/wav">
                            Your browser does not support the audio element.
                        </audio>
                    ''')
            self.fields['audio'].help_text = audio_html

