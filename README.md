# 🍴 Hebrew Recipe Recommender

מערכת המלצות למתכונים חכמים – לפי סוג הארוחה, ערך קלורי ותגים תזונתיים.  
המערכת פותחה כפרויקט אישי לתיק עבודות, ומספקת חוויית משתמש מלאה בעברית.

---

## 🌐 דמו חי
- **Frontend (Vercel):** [https://recipe-recommender-theta.vercel.app](https://recipe-recommender-theta.vercel.app)  
- **Backend (Render):** [https://recipe-recommender-t3nz.onrender.com](https://recipe-recommender-t3nz.onrender.com)

---

## 🧠 על הפרויקט
המערכת מאפשרת להזין סוג ארוחה (בוקר, צהריים, ערב), טווח קלוריות ותגים כמו *כשר*, *צמחוני* או *נטול גלוטן* — ולקבל מתכונים תואמים מתוך מאגר מתכונים מובנה.

---

## ⚙️ טכנולוגיות
**Frontend:**
- React (Vite)
- TailwindCSS

**Backend:**
- FastAPI (Python)
- JSON data storage

**Deployment:**
- Vercel (Frontend)
- Render (Backend)

---

## 🚀 הרצה מקומית
```bash
# הרצת שרת ה-Backend
cd backend
uvicorn main:app --reload

# הרצת ממשק ה-Frontend
cd ../frontend/vite-project
npm install
npm run dev
# recipe_recommender