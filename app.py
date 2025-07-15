import gradio as gr
import subprocess
import os
import shutil

MODELS_MAPPING = {
    'English': 'en_US-lessac-medium',
    'Greek': 'el_GR-rapunzelina-low'
}


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
    result_subdirs = sorted(os.listdir('./results'), reverse=True)
    for subdir in result_subdirs:
        for video_path in os.listdir(os.path.join('./results', subdir)):
            if video_path.endswith('.mp4'):
                return video_path

    return "Error: No output video generated."


def get_image_choices():
    """List all .png and .jpg files in examples/source_image"""
    image_dir = "examples/source_image"
    return sorted([
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])


def launch():
    with gr.Blocks() as demo:
        gr.Markdown("# Avatar PoC")

        with gr.Row():
            language = gr.Dropdown(choices=list(MODELS_MAPPING.keys()), label="Select Language", value="English")
            text = gr.Textbox(lines=4, label="Enter Text")
            image_path = gr.Dropdown(choices=get_image_choices(), label="Select Image")

        generate_button = gr.Button("Generate Video")

        video_output = gr.Video(label="Generated Video")

        generate_button.click(
            fn=generate_video,
            inputs=[language, text, image_path],
            outputs=video_output
        )

    demo.launch(share=True)
