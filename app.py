import gradio as gr
import subprocess
import os

MODELS_MAPPING = {
    'English': 'en_US-lessac-medium',
    'Greek': 'el_GR-rapunzelina-low'
}
IMAGE_DIR = "examples/source_image"
IMAGE_CHOICES = [
    os.path.join(IMAGE_DIR, f)
    for f in sorted(os.listdir(IMAGE_DIR))
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]


def generate_video(language, text, image_path):

    language_model = MODELS_MAPPING.get(language, 'en_US-lessac-medium')

    # Set paths
    driven_audio_path = 'examples/driven_audio/input_audio.wav'

    # Run TTS to generate audio
    subprocess.run([
        'python3.9', '-m', 'piper',
        '-m', language_model,
        '-f', driven_audio_path,
        '--', text
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Run inference
    subprocess.run([
        'python3.8', 'inference.py',
        '--driven_audio', driven_audio_path,
        '--source_image', image_path,
        '--result_dir', './results'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Construct expected output filename (latest .mp4 in results/)
    results_path = sorted(os.listdir('./results'), reverse=True)
    return max([os.path.join('./results', path) for path in results_path], key=os.path.getctime)


def get_image(index):
    return IMAGE_CHOICES[index], index


def change_image(index, direction):
    new_index = (index + direction) % len(IMAGE_CHOICES)
    return get_image(new_index)


def launch():
    with gr.Blocks() as demo:
        gr.Markdown("# Avatar PoC")

        with gr.Row():
            language = gr.Dropdown(choices=list(MODELS_MAPPING.keys()), label="Select Language", value="English")
            text = gr.Textbox(lines=4, label="Enter Text")
        
        gr.Markdown("### Select an Image")

        with gr.Row():
            prev_btn = gr.Button("⬅️ Previous")
            next_btn = gr.Button("Next ➡️")

        with gr.Row():
            image_display = gr.Image(type="filepath", label="Image Preview", height=300, width=300)
        
        image_index = gr.State(0)

        prev_btn.click(fn=change_image, inputs=[image_index, gr.Number(-1)], outputs=[image_display, image_index])
        next_btn.click(fn=change_image, inputs=[image_index, gr.Number(1)], outputs=[image_display, image_index])

        generate_button = gr.Button("Generate Video")
        video_output = gr.Video(label="Generated Video", height=300)

        generate_button.click(
            fn=lambda lang, txt, idx: generate_video(lang, txt, IMAGE_CHOICES[idx]),
            inputs=[language, text, image_index],
            outputs=video_output
        )

    demo.launch(share=True)
