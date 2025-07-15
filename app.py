import gradio as gr
import subprocess
import os
import shutil

MODELS_MAPPING = {
    'English': 'en_US-lessac-medium',
    'Greek': 'el_GR-rapunzelina-low'
}


def generate_video(language, text, image):

    language_model = MODELS_MAPPING.get(language, 'en_US-lessac-medium')

    # Set paths
    driven_audio_path = 'examples/driven_audio/input_audio.wav'
    source_image_path = 'examples/source_image/input_image.png'

    # Save uploaded image to source path
    shutil.copy(image, source_image_path)

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
        '--source_image', source_image_path,
        '--result_dir', './results'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Construct expected output filename (latest .mp4 in results/)
    result_subdirs = sorted(os.listdir('./results'), reverse=True)
    for subdir in result_subdirs:
        path = os.path.join('./results', subdir, 'input_image##output.mp4')
        if os.path.exists(path):
            return path

    return "Error: No output video generated."


def launch():
    with gr.Blocks() as demo:
        gr.Markdown("# Avatar PoC")

        with gr.Row():
            language_input = gr.Dropdown(choices=list(MODELS_MAPPING.keys()), label="Select Language", value="English")
            text_input = gr.Textbox(lines=4, label="Enter Text")
            image_input = gr.Image(label="Upload Image", type="filepath")

        generate_button = gr.Button("Generate Video")

        video_output = gr.Video(label="Generated Video")

        generate_button.click(
            fn=generate_video,
            inputs=[language_input, text_input, image_input],
            outputs=video_output
        )

    demo.launch(share=True)
