from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os, json

app = FastAPI(title="Hebrew Recipe Recommender", version="0.2.0")

# בזמן פיתוח מותר מכל כתובת; בפרודקשן נצמצם (ראו שלב הפריסה)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV ONLY
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "recipes.json")

class RecommendRequest(BaseModel):
    meal_type: str = Field(pattern="^(breakfast|lunch|dinner)$")
    target_calories: int = Field(ge=100, le=1200)
    diet_tags: Optional[List[str]] = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/recipes/count")
def count_recipes():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return {"count": len(json.load(f))}

@app.post("/recommend")
def recommend(req: RecommendRequest):
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="recipes data not found")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    cands = [r for r in recipes if r.get("meal_type") == req.meal_type]

    if req.diet_tags:
        req_set = set(req.diet_tags)
        cands = [r for r in cands if req_set.issubset(set(r.get("tags", [])))]

    if not cands:
        return {"results": [], "message": "לא נמצאו מתכונים מתאימים"}

    for r in cands:
        r["_score"] = -abs(r.get("calories", 0) - req.target_calories)

    cands.sort(key=lambda x: x["_score"], reverse=True)
    results = [{k: v for k, v in r.items() if k != "_score"} for r in cands[:3]]
    return {"results": results}
