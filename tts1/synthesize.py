import os
import time, argparse, sys

import numpy as np
import torch
from espnet2.bin.tts_inference import Text2Speech
from parallel_wavegan.utils import download_pretrained_model
from parallel_wavegan.utils import load_model, read_hdf5
from scipy.io.wavfile import write
from pathlib import Path

from KazakhTTS import settings


def synthesize(text, output_wav_file):
    fs = 22050  # Частота дискретизации

    vocoder_checkpoint = os.path.join(settings.BASE_DIR, 'tts1/exp/vocoder/checkpoint-400000steps.pkl')
    vocoder = load_model(vocoder_checkpoint).to("cpu").eval()
    vocoder.remove_weight_norm()

    config_file = os.path.join(settings.BASE_DIR, 'tts1/exp/tts_train_raw_char/config.yaml')
    model_path = os.path.join(settings.BASE_DIR, 'tts1/exp/tts_train_raw_char/train.loss.ave_5best.pth')

    text2speech = Text2Speech(
        config_file,
        model_path,
        device="cpu",
        # Only for Tacotron 2
        threshold=0.5,
        minlenratio=0.0,
        maxlenratio=10.0,
        use_att_constraint=True,
        backward_window=1,
        forward_window=3,
        # Only for FastSpeech & FastSpeech2
        speed_control_alpha=1.0,
    )
    text2speech.spc2wav = None  # Disable griffin-lim

    timer = time.perf_counter()
    with torch.no_grad():
        output_dict = text2speech(text.lower())
        feat_gen = output_dict['feat_gen']
        wav = vocoder.inference(feat_gen)

    # Сохраняем аудио файл
    write(str(output_wav_file), fs, (wav.view(-1).cpu().numpy() * 32767).astype(np.int16))

    return output_wav_file, round(time.perf_counter() - timer, 3)


