from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os, json

app = FastAPI(title="Hebrew Recipe Recommender", version="0.1.0")

# לאפשר פניות מה-frontend בהמשך
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # בשלב פיתוח
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "recipes.json")

class RecommendRequest(BaseModel):
    meal_type: str            # "breakfast" | "lunch" | "dinner"
    target_calories: int      # יעד קלורי
    diet_tags: Optional[List[str]] = None  # לדוגמה: ["כשר","טבעוני"]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(req: RecommendRequest):
    # טוענים מתכונים
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    # סינון לפי סוג ארוחה
    cands = [r for r in recipes if r.get("meal_type") == req.meal_type]

    # סינון לפי תגים (אם ביקשו)
    if req.diet_tags:
        req_set = set(req.diet_tags)
        cands = [r for r in cands if req_set.issubset(set(r.get("tags", [])))]

    # ניקוד לפי מרחק מהיעד הקלורי (ככל שקרוב יותר—טוב יותר)
    for r in cands:
        r["_score"] = -abs(r.get("calories", 0) - req.target_calories)

    # מיון והחזרת שלוש המובילים
    cands.sort(key=lambda x: x["_score"], reverse=True)
    results = [{k: v for k, v in r.items() if k != "_score"} for r in cands[:3]]
    return {"results": results}
