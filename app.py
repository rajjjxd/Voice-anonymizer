# -*- coding: utf-8 -*-
"""Audio_anonymizer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PHkTlJr9PcIl2VKUh-lH6JPHzMXCutDi
"""

import os
os.system('apt-get update && apt-get install -y ffmpeg')
import torch
import torchaudio
import gradio as gr
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
import tempfile

class VoiceAnonymizer:
    def __init__(self):
        self.sample_rate = 16000

    def load_audio(self, audio_path):
        """Load and preprocess audio file"""
        waveform, sr = librosa.load(audio_path, sr=self.sample_rate)
        return waveform

    def anonymize(self, input_path, pitch_shift=2):
        """Main function to anonymize voice"""
        # Load audio
        waveform = self.load_audio(input_path)

        # Simple pitch shifting
        anonymized_audio = librosa.effects.pitch_shift(
            waveform,
            sr=self.sample_rate,
            n_steps=pitch_shift
        )

        # Normalize audio
        anonymized_audio = librosa.util.normalize(anonymized_audio)

        # Save as MP3
        output_path = "anonymized_output.mp3"

        # First save as WAV (temporary)
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        sf.write(temp_wav.name, anonymized_audio, self.sample_rate)

        # Convert to MP3
        audio = AudioSegment.from_wav(temp_wav.name)
        audio.export(output_path, format="mp3", bitrate="192k")  # High quality MP3

        # Clean up temporary file
        os.unlink(temp_wav.name)

        return output_path

def create_gradio_interface():
    anonymizer = VoiceAnonymizer()

    def process_file(audio_file, pitch_amount=2):
        if audio_file is None:
            return None
        return anonymizer.anonymize(audio_file, pitch_shift=pitch_amount)

    interface = gr.Interface(
        fn=process_file,
        inputs=[
            gr.Audio(type="filepath", label="Input Audio"),
            gr.Slider(minimum=1, maximum=4, value=2, step=0.5,
                     label="Pitch Shift (higher = more anonymized)")
        ],
        outputs=gr.Audio(label="Anonymized Audio (MP3)"),
        title="Voice Anonymizer",
        description="Upload an audio file to anonymize the voice. Adjust the pitch slider to control the level of anonymization.",
    )
    return interface

if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch()


