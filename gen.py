# import os
# import pandas as pd
# from tts1.synthesize import synthesize  # Импорт функции синтеза
#
# BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'KazakhTTS-Server/audio')
#
# articles_split_data = pd.read_csv('data/articles_split_data.csv')
# print(articles_split_data)
#
# # Initialize an empty list to store the audio file paths
# audio_paths = []
#
# # Process and save audio for the first 50 sentences
# for idx, sentence in enumerate(articles_split_data['sentence'][:50]):
#     # Define a unique audio path using the index
#     audio_path = os.path.join(BASE_DIR, f'article_kz_{idx}.wav')
#
#     # Generate audio for each sentence
#     synthesize(sentence, audio_path)
#
#     # Append the audio path to the list
#     audio_paths.append(audio_path)
#
#     # Output the path of the generated audio file
#     print(audio_path)
#
# # Add the audio paths as a new column to the DataFrame
# articles_split_data.loc[:49, 'audio_kz_wav'] = audio_paths
#
# # Save the updated DataFrame back to CSV if needed
# articles_split_data.to_csv('data/articles_with_kz_audio.csv', index=False)
# import pandas as pd

# import pandas as pd
# from datasets import Dataset, DatasetDict, Audio
#
# # Load your CSV data
# data = pd.read_csv('data/articles_with_kz_audio.csv')
#
# # Convert the DataFrame into a Hugging Face Dataset
# hf_dataset = Dataset.from_pandas(data)
#
# hf_dataset = hf_dataset.cast_column("audio_kz_wav", Audio())
#
# dataset_name = "FynnFu/audio"
#
# hf_dataset.push_to_hub(dataset_name)


# from datasets import load_dataset
#
# dataset = load_dataset("FynnFu/audio")


# import pandas as pd
#
# data = pd.read_csv('data/articles_with_kz_audio.csv')
# print(len(data))

import os
from pydub import AudioSegment

# Путь к папке с аудиофайлами
audio_folder = 'audio'

# Инициализируем переменную для общего времени в миллисекундах
total_duration = 0

# Перебираем все файлы в папке
for filename in os.listdir(audio_folder):
    # Проверяем, что файл имеет формат .wav
    if filename.endswith('.wav'):
        file_path = os.path.join(audio_folder, filename)

        # Загружаем аудиофайл
        audio = AudioSegment.from_wav(file_path)

        # Добавляем длительность файла к общему времени
        total_duration += len(audio)

# Переводим общее время из миллисекунд в секунды
total_duration_seconds = total_duration / 1000
total_minutes, total_seconds = divmod(total_duration_seconds, 60)

print(f"Общее время аудиофайлов: {int(total_minutes)} минут {int(total_seconds)} секунд")
