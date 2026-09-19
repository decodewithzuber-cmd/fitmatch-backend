import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Frontend se request allow karne ke liye CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Client setup (Render par environment variable se key uthayega)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

class OutfitRequest(BaseModel):
    query: str
    bottom: str
    occasion: str
    budget: str

@app.post("/generate-outfit")
def generate_outfit(data: OutfitRequest):
    system_instruction = (
        "You are an elite AI fashion stylist and color-matching expert. "
        "The user will provide their bottom wear, occasion, budget tier, and custom text prompt. "
        "Analyze their request and return the response strictly in this exact plain text layout (do not use markdown headers like ###): "
        "TOP: [Specific top wear name and color matching the prompt/budget]\n"
        "SHOES: [Best matching footwear]\n"
        "ACCESSO: [Watch, belt, or jewelry details]\n"
        "TIP: [One short professional stylist rule for this look]"
    )

    full_prompt = (
        f"{system_instruction}\n\n"
        f"Bottom Wear: {data.bottom}\n"
        f"Custom Request: {data.query}\n"
        f"Occasion: {data.occasion}\n"
        f"Budget Tier: {data.budget}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return {"result": response.text}