import gradio as gr
from pathlib import Path
from tempfile import mkdtemp

from avatar_poc.tts.pipper.main import TTS_MODELS_MAPPING, generate_audio
from avatar_poc.vidgen.sadtalker.main import generate_video

IMAGE_CHOICES = [
    path
    for path in (Path(__file__).parent / 'avatars').iterdir()
    if path.suffix in (".png", ".jpg", ".jpeg")
]


def get_image(index):
    return IMAGE_CHOICES[index], index


def change_image(index, direction):
    new_index = (index + direction) % len(IMAGE_CHOICES)
    return get_image(new_index)


def generate(language, text, audio_path, image_path, video_path):
    generate_audio(language, text, audio_path)
    generate_video(audio_path, image_path, video_path)


def launch():
    temp_dir = mkdtemp()
    audio_path = Path(temp_dir) / "audio.wav"
    video_path = Path(temp_dir) / "video.mp4"
    with gr.Blocks() as demo:
        gr.Markdown("# Avatar PoC")

        with gr.Row():
            language = gr.Dropdown(choices=list(TTS_MODELS_MAPPING.keys()), label="Select Language", value="English")
            text = gr.Textbox(lines=4, label="Enter Text")
        
        gr.Markdown("### Select an Image")

        with gr.Row():
            prev_btn = gr.Button("⬅️ Previous")
            next_btn = gr.Button("Next ➡️")

        with gr.Row():
            image_display = gr.Image(type="filepath", label="Image Preview", height=300, width=300, value=IMAGE_CHOICES[0])
        
        image_index = gr.State(0)

        prev_btn.click(
            fn=lambda idx: change_image(idx, -1),
            inputs=image_index,
            outputs=[image_display, image_index]
        )

        next_btn.click(
            fn=lambda idx: change_image(idx, 1),
            inputs=image_index,
            outputs=[image_display, image_index]
        )

        generate_button = gr.Button("Generate Video")
        video_output = gr.Video(label="Generated Video", height=400)

        generate_button.click(
            fn=lambda lang, txt, idx: generate(lang, txt, audio_path, IMAGE_CHOICES[idx], video_path),
            inputs=[language, text, image_index],
            outputs=video_output
        )

    demo.launch(share=True)


if __name__ == '__main__':
    launch()
