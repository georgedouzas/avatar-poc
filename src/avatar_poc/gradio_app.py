import gradio as gr
from pathlib import Path
from tempfile import mkdtemp
from importlib.resources import files

from avatar_poc.tts.pipper.main import TTS_MODELS_MAPPING, generate_audio
from avatar_poc.vidgen.sadtalker.main import generate_video

AVATARS_PER_PAGE = 10
IMAGE_CHOICES = [
    path
    for path in (Path(__file__).parent / 'avatars').iterdir()
    if path.suffix in ('.png', '.jpg', '.jpeg')
]


def get_gallery_page(page_idx):
    start = page_idx * AVATARS_PER_PAGE
    end = start + AVATARS_PER_PAGE
    return IMAGE_CHOICES[start:end]


def on_gallery_select(selected_path):
    return Path(selected_path).name


def set_selected_image(path=None):
    return [path or IMAGE_CHOICES[0]]


def check_ready(text, image_path):
    ready = bool(text.strip()) and bool(image_path)
    return gr.update(interactive=ready)


def generate(language, text, audio_path, image_path, video_path):
    generate_audio(language, text, audio_path)
    generate_video(audio_path, image_path, video_path)


def launch():
    avatar_dir = files('avatar_poc').joinpath('avatars')
    temp_dir = mkdtemp()
    audio_path = Path(temp_dir) / 'audio.wav'
    video_path = Path(temp_dir) / 'video.mp4'
    with gr.Blocks() as demo:

        gr.Markdown('# Avatar PoC')

        # Language and text selection
        with gr.Row():
            language = gr.Dropdown(
                choices=list(TTS_MODELS_MAPPING.keys()),
                label='Select Language',
                value='English',
            )
            text = gr.Textbox(lines=4, label='Enter Text')

        # Image selection
        gr.Markdown('### Select an Image')
        with gr.Row():
            gallery_prev_btn = gr.Button('⬅️ Prev Page')
            gallery_next_btn = gr.Button('Next Page ➡️')
        gallery = gr.Gallery(
            get_gallery_page(0), label='Avatar Gallery', columns=5, height='auto'
        )
        gallery_page_index = gr.State(0)
        gallery_prev_btn.click(
            fn=lambda page: (
                get_gallery_page(
                    (page - 1) % ((len(IMAGE_CHOICES) - 1) // AVATARS_PER_PAGE + 1)
                ),
                (page - 1) % ((len(IMAGE_CHOICES) - 1) // AVATARS_PER_PAGE + 1),
            ),
            inputs=gallery_page_index,
            outputs=[gallery, gallery_page_index],
        )
        gallery_next_btn.click(
            fn=lambda page: (
                get_gallery_page(
                    (page + 1) % ((len(IMAGE_CHOICES) - 1) // AVATARS_PER_PAGE + 1)
                ),
                (page + 1) % ((len(IMAGE_CHOICES) - 1) // AVATARS_PER_PAGE + 1),
            ),
            inputs=gallery_page_index,
            outputs=[gallery, gallery_page_index],
        )

        # Video generation
        generate_button = gr.Button('Generate Video', interactive=False)
        video_output = gr.Video(label='Generated Video', height=400)

        # Events
        selected_image_path = gr.State(IMAGE_CHOICES[0])
        gallery.select(fn=set_selected_image, outputs=[selected_image_path]).then(
            fn=check_ready, inputs=[text, selected_image_path], outputs=generate_button
        )
        generate_button.click(
            fn=lambda language, text, image_path: generate(
                language, text, audio_path, image_path, video_path
            ),
            inputs=[language, text, selected_image_path.value],
            outputs=video_output,
        )
        text.change(
            fn=check_ready, inputs=[text, selected_image_path], outputs=generate_button
        )

    demo.launch(share=True, allowed_paths=[avatar_dir])


if __name__ == '__main__':
    launch()
