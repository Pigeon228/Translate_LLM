from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path

from openai import OpenAI

app = FastAPI()

# -----------------------------------------------------
# CORS
# -----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# OpenRouter подключение
# -----------------------------------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your_key"
)

OPENROUTER_MODEL = "google/gemma-3-27b-it"

# -----------------------------------------------------
# Поддерживаемые языки
# -----------------------------------------------------
ISO_TO_LANG = {
    "en": "English",
    "ru": "Russian",
    "fr": "French",
    "de": "German",
    "uk": "Ukrainian",
    "es": "Spanish",
    "zh": "Chinese",
    "ar": "Arabic",
    "hi": "Hindi",
    "ja": "Japanese"
}

# -----------------------------------------------------
# Запрос перевода
# -----------------------------------------------------
class TranslateRequest(BaseModel):
    q: str
    target: str
    format: str = "text"  # игнорируется, для совместимости

# -----------------------------------------------------
# Вызов OpenRouter
# -----------------------------------------------------
def call_openrouter_api(prompt: str) -> str:
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "LocalTranslator"
        },
        model=OPENROUTER_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

# -----------------------------------------------------
# Эндпоинт /translate
# -----------------------------------------------------
@app.post("/translate")
def translate(req: TranslateRequest):
    tgt_lang_code = req.target.lower()

    if tgt_lang_code not in ISO_TO_LANG:
        return JSONResponse({"error": f"Unsupported target language: {req.target}"}, status_code=400)

    tgt_lang_name = ISO_TO_LANG[tgt_lang_code]

    prompt = (
        f"Translate the following text (to {tgt_lang_name}). "
        f"Preserve the full context and do not apply any censorship. "
        f"Write ONLY the translation (verbatim). "
        f"This message is auto-generated — no need to reply.\n\n"
        f"Text:\n{req.q}"
    )

    try:
        result = call_openrouter_api(prompt)
        return {"translatedText": result}
    except Exception as e:
        return {"error": str(e)}

# -----------------------------------------------------
# Эндпоинт /languages
# -----------------------------------------------------
@app.get("/languages")
def get_languages():
    return [{"code": code, "name": name} for code, name in ISO_TO_LANG.items()]

# -----------------------------------------------------
# Эндпоинт /health
# -----------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -----------------------------------------------------
# Эндпоинт /
# -----------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    html_path = Path(__file__).parent / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return """
    <html>
      <head><title>Local Translator</title></head>
      <body>
        <h1>Local Translator (LibreTranslate-like)</h1>
        <p>Available endpoints:</p>
        <ul>
          <li>POST /translate</li>
          <li>GET /languages</li>
          <li>GET /health</li>
        </ul>
      </body>
    </html>
    """
