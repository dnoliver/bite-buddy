# Local Voice Assistant

> A local voice assistant

To start the assistant, set your `OPENAI_API_KEY` in the `.env` file. Create a
virtual environment, install dependencies, and start the application:

```ps1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
doit
gradio app.py
```

The application will start in http://localhost:7860/

![Banner](banner.jpg)

## Links

- [Gradio - Quickstart](https://www.gradio.app/guides/quickstart)
- [Haystack - Get Started](https://haystack.deepset.ai/overview/quick-start)
- [OpenAI Platform - Text to speech](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI Platform - Speech to text](https://platform.openai.com/docs/guides/speech-to-text)
