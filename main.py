import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class OutfitRequest(BaseModel):
    query: str
    bottom: str
    upper: str
    shoes: str
    occasion: str
    budget: str

class QuickQueryRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    feedback: str

@app.post("/generate-outfit")
async def generate_outfit(req: OutfitRequest):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing on Render environment variables!")

        prompt = f"""
        You are a professional fashion stylist. A user needs a complete matching outfit recommendation based on their chosen items.
        - Selected Upper Wear: {req.upper}
        - Selected Bottom Wear: {req.bottom}
        - Selected Footwear: {req.shoes}
        - Occasion/Vibe: {req.occasion}
        - Target Budget Tier: {req.budget}
        - User Custom Note/Preferences: {req.query}

        Provide a refined styling recommendation matching these choices and budget.
        Format your response EXACTLY in these five lines, starting with these prefixes:
        TOP: [Refined color and style of topwear]
        SHOES: [Refined matching footwear style]
        ACCESSO: [Minimal matching accessories like watch, chain, or cap]
        TIP: [A short 1-sentence styling pro-tip for this look]
        SCORE: [Style match percentage and synergy vibe, e.g., 95% - Sharp Monochromatic Synergy]
        """

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )

        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quick-ask")
async def quick_ask(req: QuickQueryRequest):
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"You are a direct and concise fashion stylist. Answer this specific user question directly, short, and to the point without extra formatting clutter: {req.question}"
        )
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-feedback")
async def submit_feedback(req: FeedbackRequest):
    try:
        print(f"New User Feedback: {req.feedback}")
        return {"message": "Feedback received successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "FitMatch AI Backend is Live!"}