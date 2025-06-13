# Local Translator

This project provides a simple translation service built with [FastAPI](https://fastapi.tiangolo.com/). It uses the OpenRouter API to translate text between different languages through a web interface or a REST endpoint.

## Features

- **/translate** – translate arbitrary text to a specified target language.
- **/languages** – list supported language codes and names.
- **/health** – basic health check.
- Web UI available at the root endpoint (`/`).

## Setup

1. Install Python 3.10 or newer.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Provide your OpenRouter API key. Edit `server.py` and replace the placeholder `"your_key"` with your key or set the environment variable `OPENAI_API_KEY` and modify the code accordingly.

4. Run the server using Uvicorn:

```bash
uvicorn server:app --reload
```

The service will start on `http://127.0.0.1:8000` by default.

## Requirements

Dependencies are listed in `requirements.txt`.

