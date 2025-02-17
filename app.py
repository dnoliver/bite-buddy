import os

from haystack import Pipeline
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage

import gradio as gr

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

pipeline = Pipeline()
pipeline.add_component("fetcher", fetcher)
pipeline.add_component("converter", converter)
pipeline.add_component("prompt", prompt_builder)
pipeline.add_component("llm", llm)

pipeline.connect("fetcher.streams", "converter.sources")
pipeline.connect("converter.documents", "prompt.documents")
pipeline.connect("prompt.prompt", "llm")

def ask_question(query):
    result = pipeline.run({
        "fetcher": {"urls": ["https://haystack.deepset.ai/overview/quick-start"]},
        "prompt": {"query": query}
    })
    return result["llm"]["replies"][0].text

iface = gr.Interface(
    fn=ask_question,
    inputs="text",
    outputs="text",
    title="Ask Questions to LLM",
    description="Enter a question to get an answer from the LLM based on the content of the provided URL."
)
iface.launch()

