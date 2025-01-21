document.addEventListener('DOMContentLoaded', function () {
    const lessonId = document.querySelector('input[name="_save"]').value; // Получаем ID урока

    // Создаем кнопку для генерации аудио для Word
    const generateWordAudioButton = document.createElement('button');
    generateWordAudioButton.textContent = 'Сгенерировать аудио для Word';
    generateWordAudioButton.type = 'button';
    generateWordAudioButton.classList.add('btn', 'btn-primary');
    generateWordAudioButton.style.margin = '10px 0';

    // Создаем кнопку для генерации аудио для List of Words
    const generateListOfWordsAudioButton = document.createElement('button');
    generateListOfWordsAudioButton.textContent = 'Сгенерировать аудио для List of Words';
    generateListOfWordsAudioButton.type = 'button';
    generateListOfWordsAudioButton.classList.add('btn', 'btn-primary');
    generateListOfWordsAudioButton.style.margin = '10px 0';

    // Вставляем кнопки перед кнопкой сохранения
    const saveButton = document.querySelector('.submit-row');
    if (saveButton) {
        saveButton.insertAdjacentElement('beforebegin', generateWordAudioButton);
        saveButton.insertAdjacentElement('beforebegin', generateListOfWordsAudioButton);
    }

    // Обработчик для кнопки генерации аудио для Word
    generateWordAudioButton.addEventListener('click', function () {
        const wordField = document.querySelector('#id_word').value;

        if (wordField) {
            fetch('api/generate-audio/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    field: 'word',
                    word: wordField,
                    lesson_id: lessonId  // Передаем ID урока
                })
            })
            .then(response => response.json())
            .then(data => {
                alert('Аудио для слова сгенерировано.');
            })
            .catch(error => {
                alert('Ошибка при генерации аудио.');
            });
        } else {
            alert('Поле Word пустое. Введите слово для генерации аудио.');
        }
    });

    // Обработчик для кнопки генерации аудио для List of Words
    generateListOfWordsAudioButton.addEventListener('click', function () {
        const listOfWordsField = document.querySelector('#id_list_of_word').value;

        if (listOfWordsField) {
            fetch('api/generate-audio/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    field: 'list_of_word',
                    list_of_word: listOfWordsField,
                    lesson_id: lessonId  // Передаем ID урока
                })
            })
            .then(response => response.json())
            .then(data => {
                alert('Аудио для списка слов сгенерировано.');
            })
            .catch(error => {
                alert('Ошибка при генерации аудио.');
            });
        } else {
            alert('Поле List of Words пустое. Введите список слов для генерации аудио.');
        }
    });
});
