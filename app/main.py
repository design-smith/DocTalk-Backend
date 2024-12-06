from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import translate_v2 as translate
import json
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your Vercel domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslateRequest(BaseModel):
    text: str
    target_language: str

@app.get("/")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/translate")
async def translate_text(request: TranslateRequest):
    try:
        # Initialize the Translation client
        client = translate.Client()
        
        # Perform translation
        result = client.translate(
            request.text,
            target_language=request.target_language
        )
        
        return {
            "success": True,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))