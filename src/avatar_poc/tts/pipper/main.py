import subprocess
import os
from tempfile import mkdtemp
from pathlib import Path

TTS_MODELS_MAPPING = {
    'English': 'en_US-lessac-medium',
    'Greek': 'el_GR-rapunzelina-low'
}


def generate_audio(language, text, audio_path):
    language_model = TTS_MODELS_MAPPING.get(language, 'en_US-lessac-medium')
    subprocess.run([
        'python3.9', '-m', 'piper',
        '-m', language_model,
        '-f', audio_path,
        '--', text
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)