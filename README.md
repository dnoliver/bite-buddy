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
