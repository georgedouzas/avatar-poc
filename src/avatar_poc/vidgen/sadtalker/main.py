import subprocess
from pathlib import Path


def generate_video(audio_path, image_path, video_path):
    video_dir_path = Path(video_path).parent
    subprocess.run(
        [
            'python3.8',
            'inference.py',
            '--driven_audio',
            audio_path,
            '--source_image',
            image_path,
            '--result_dir',
            video_dir_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    list(video_dir_path.iterdir())[0].rename(video_path)
