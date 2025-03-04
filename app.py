import os

from haystack import Pipeline
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.components.audio import RemoteWhisperTranscriber
from dotenv import load_dotenv
from pathlib import Path

from pathlib import Path
from openai import OpenAI

import gradio as gr

from haystack import component

load_dotenv(dotenv_path=Path(".") / ".env")


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

        response.write_to_file(".tmp/output.mp3")

        return {"file_path": ".tmp/output.mp3"}


fetcher = LinkContentFetcher()
converter = HTMLToDocument()
prompt_template = [
    ChatMessage.from_user(
        """
      According to the contents of this website:
      {% for document in documents %}
        {{document.content}}
      {% endfor %}
      Answer the given question: {{query}}
      Answer:
      """
    )
]

prompt_builder = ChatPromptBuilder(template=prompt_template)
llm = OpenAIChatGenerator()
transcriber = RemoteWhisperTranscriber()
talker = RemoteOpenAISpeechToText()

pipeline = Pipeline()
pipeline.add_component("fetcher", fetcher)
pipeline.add_component("converter", converter)
pipeline.add_component("prompt", prompt_builder)
pipeline.add_component("llm", llm)

pipeline.connect("fetcher.streams", "converter.sources")
pipeline.connect("converter.documents", "prompt.documents")
pipeline.connect("prompt.prompt", "llm")

with gr.Blocks() as demo:
    gr.Markdown("# Local Voice Assistant")
    gr.Markdown(
        """
        This is a voice assistant that can answer questions based on the contents of a website. 
        You can ask a question by speaking into the microphone. 
        You can type the question in the text box as well.
        Then click "Run" to get the answer.
        """
    )
    audio = gr.Audio(label="Audio", sources=["microphone"], type="filepath")
    url = gr.Textbox(
        label="URL", placeholder="https://haystack.deepset.ai/overview/quick-start"
    )
    query = gr.Textbox(label="Question")
    run = gr.Button(value="Run")
    result = gr.Textbox(label="Answer")
    speak = gr.Button(value="Speak")
    speech = gr.Audio(label="Speech", interactive=False)

    def run_query(url, query):
        response = pipeline.run(
            {"fetcher": {"urls": [url]}, "prompt": {"query": query}}
        )
        return response["llm"]["replies"][0].text

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

    audio.input(transcribe_audio, inputs=[audio], outputs=[query])
    query.submit(run_query, inputs=[url, query], outputs=[result])
    run.click(run_query, inputs=[url, query], outputs=[result])
    speak.click(speak_answer, inputs=[result], outputs=[speech])

if __name__ == "__main__":
    demo.launch(allowed_paths=[".tmp"])
