import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini Client using environment API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class OutfitRequest(BaseModel):
    query: str
    bottom: str
    occasion: str
    budget: str

@app.post("/generate-outfit")
async def generate_outfit(req: OutfitRequest):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing on Render environment variables!")

        prompt = f"""
        You are a professional fashion stylist. A user needs an outfit recommendation.
        - Bottom Wear: {req.bottom}
        - Occasion/Vibe: {req.occasion}
        - Target Budget Tier: {req.budget}
        - User Custom Note/Preferences: {req.query}

        Provide a complete styling recommendation matching the bottom wear and budget.
        Format your response EXACTLY in these four lines, starting with these prefixes:
        TOP: [Color and specific style of topwear, e.g., Oversized Solid Black Cotton T-Shirt]
        SHOES: [Specific matching footwear, e.g., White Casual Sneakers]
        ACCESSO: [Minimal matching accessories like watch, chain, or cap]
        TIP: [A short 1-sentence styling pro-tip for this look]
        """

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )

        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "FitMatch AI Backend is Live!"}