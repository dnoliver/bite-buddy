import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from haystack import component
from haystack.components.audio import RemoteWhisperTranscriber
from openai import OpenAI

from database import Database
from intent_handling import (
    InventoryDeleteIntentHandling,
    InventoryEntryIntentHandling,
    InventoryQueryIntentHandling,
)
from intent_matching import IntentMatching

load_dotenv(dotenv_path=Path(".") / ".env")

intent_matching = IntentMatching()
intent_handlers = {
    "InventoryQueryIntent": InventoryQueryIntentHandling,
    "InventoryEntryIntent": InventoryEntryIntentHandling,
    "InventoryDeleteIntent": InventoryDeleteIntentHandling,
}


@component
class RemoteOpenAISpeechToText:
    def __init__(self):
        self.client = OpenAI()

    @component.output_types(file_path=Path)
    def run(self, text: str):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )

        os.makedirs(".tmp", exist_ok=True)
        response.write_to_file(".tmp/output.mp3")

        return {"file_path": ".tmp/output.mp3"}


transcriber = RemoteWhisperTranscriber()
talker = RemoteOpenAISpeechToText()

with gr.Blocks() as demo:
    gr.Markdown("# Bite Buddy")
    gr.Markdown(
        """
        This is a voice assistant for the products in your kitchen. 
        You can ask a question by speaking into the microphone. 
        You can type the question in the text box as well.
        Then click "Run" to get the answer.
        """
    )
    audio = gr.Audio(label="Audio", sources=["microphone"], type="filepath")
    query = gr.Dropdown(
        label="Question",
        choices=[
            "What is in the pantry?",
            "Put the milk in the pantry",
            "Clear the pantry",
        ],
        interactive=True,
        allow_custom_value=True,
    )
    run = gr.Button(value="Run")
    result = gr.Textbox(label="Answer")
    speak = gr.Button(value="Speak")
    speech = gr.Audio(label="Speech", interactive=False)

    def run_query(query):
        if query is None:
            return ""

        result = intent_matching.run(query)
        intent_handler = intent_handlers[result]
        _handler_instance = intent_handler(Database("inventory.db"))
        return _handler_instance.run(query)

    def transcribe_audio(audio_file):
        if audio_file is None:
            return ""

        transcription = transcriber.run(sources=[audio_file])
        return transcription["documents"][0].content

    def speak_answer(answer):
        if answer is None:
            return ""

        result = talker.run(answer)
        return result["file_path"]

    # pylint: disable=no-member
    audio.input(transcribe_audio, inputs=[audio], outputs=[query])
    run.click(run_query, inputs=[query], outputs=[result])
    speak.click(speak_answer, inputs=[result], outputs=[speech])
    # pylint: enable=no-member

if __name__ == "__main__":
    demo.launch(allowed_paths=[".tmp"])
