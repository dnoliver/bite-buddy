import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from haystack import component
from haystack.components.audio import RemoteWhisperTranscriber
from openai import OpenAI

from src.database import Database
from src.intent_handling import (
    InventoryDeleteIntentHandling,
    InventoryEntryIntentHandling,
    InventoryQueryIntentHandling,
    ProductQueryIntentHandling,
    RecipeQueryIntentHandling,
)
from src.intent_matching import IntentMatching

load_dotenv(dotenv_path=Path(".") / ".env")

intent_matching = IntentMatching()
intent_handlers = {
    "InventoryQueryIntent": InventoryQueryIntentHandling,
    "InventoryEntryIntent": InventoryEntryIntentHandling,
    "InventoryDeleteIntent": InventoryDeleteIntentHandling,
    "ProductQueryIntent": ProductQueryIntentHandling,
    "RecipeQueryIntent": RecipeQueryIntentHandling,
}


@component
class RemoteOpenAITextToSpeech:
    def __init__(self):
        self.client = OpenAI()

    @component.output_types(file_path=Path)
    def run(self, text: str):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text,
        )

        os.makedirs(".tmp", exist_ok=True)
        response.write_to_file(".tmp/output.mp3")

        return {"file_path": ".tmp/output.mp3"}


transcriber = RemoteWhisperTranscriber()
talker = RemoteOpenAITextToSpeech()

with gr.Blocks() as demo:
    gr.Markdown("# Bite Buddy")
    gr.Markdown(
        """
        Hi! Welcome to Bite Buddy. I am Marcelo, your kitchen assistant.
        I can help you with your kitchen inventory, recipes, and more.

        You can ask me questions like:
        - What is in the pantry?
        - Put the milk in the pantry
        - Where is the milk?
        - Give me a meal recipe
        - Clear the pantry

        You can also ask me questions using your voice. Just use the record button and ask your question.
        Use the "Stop" button when you are done speaking.
        Then, click the "Run" button to get the answer.
        If you want me to read the answer to you, click the "Speak" button.

        Let's get started!
        """
    )
    audio = gr.Audio(label="Audio", sources=["microphone"], type="filepath")
    query = gr.Textbox(label="Your question:", placeholder="Type your question here")
    options = gr.Dropdown(
        label="or select a predefined question:",
        choices=[
            "What is in the pantry?",
            "Put the milk in the pantry",
            "Where is the milk?",
            "Give me a meal recipe",
            "Clear the pantry",
        ],
        value="What is in the pantry?",
        interactive=True,
        allow_custom_value=False,
    )
    run = gr.Button(value="Run")
    result = gr.Markdown()
    speak = gr.Button(value="Speak")
    speech = gr.Audio(label="Speech", interactive=False)

    def run_query(query, option):
        if not query and not option:
            return ""

        if not query and option:
            query = option

        print(f"Query: {query}")

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

    def reset_query(option, query):
        return "" if option else query

    # pylint: disable=no-member
    options.change(reset_query,inputs=[options, query],outputs=[query])
    audio.input(transcribe_audio, inputs=[audio], outputs=[query])
    run.click(run_query, inputs=[query, options], outputs=[result])
    speak.click(speak_answer, inputs=[result], outputs=[speech])
    # pylint: enable=no-member

if __name__ == "__main__":
    demo.launch(allowed_paths=[".tmp"])
