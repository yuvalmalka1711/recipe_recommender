import { useState } from "react";

function App() {
  const [mealType, setMealType] = useState("lunch");
  const [calories, setCalories] = useState(600);
  const [dietTags, setDietTags] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleTagChange = (tag) => {
    setDietTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const fetchRecommendations = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          meal_type: mealType,
          target_calories: Number(calories),
          diet_tags: dietTags,
        }),
      });
      if (!res.ok) throw new Error("שגיאה מהשרת");
      const data = await res.json();
      setResults(data.results || []);
    } catch (e) {
      setError("לא הצלחתי להביא המלצות. ודאי שהשרת מאחור רץ.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-8 font-sans">
      <h1 className="text-3xl font-bold mb-6 text-center">🍽️ מערכת המלצות למתכונים</h1>

      <div className="max-w-md mx-auto bg-white p-6 rounded-2xl shadow-md space-y-4">
        <label className="block">
          <span>סוג ארוחה:</span>
          <select
            value={mealType}
            onChange={(e) => setMealType(e.target.value)}
            className="w-full border p-2 rounded mt-1"
          >
            <option value="breakfast">ארוחת בוקר</option>
            <option value="lunch">ארוחת צהריים</option>
            <option value="dinner">ארוחת ערב</option>
          </select>
        </label>

        <label className="block">
          <span>יעד קלוריות:</span>
          <input
            type="number"
            value={calories}
            onChange={(e) => setCalories(e.target.value)}
            className="w-full border p-2 rounded mt-1"
            min={100}
          />
        </label>

        <fieldset className="space-y-2">
          <legend>העדפות תזונתיות:</legend>
          {["כשר", "צמחוני", "טבעוני", "ללא-גלוטן", "חלבי", "פרווה"].map((tag) => (
            <label key={tag} className="block">
              <input
                type="checkbox"
                checked={dietTags.includes(tag)}
                onChange={() => handleTagChange(tag)}
                className="ml-2"
              />
              {tag}
            </label>
          ))}
        </fieldset>

        <button
          onClick={fetchRecommendations}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold py-2 rounded-lg transition"
        >
          {loading ? "מחפש..." : "הצג המלצות"}
        </button>

        {error && <p className="text-red-600 text-sm">{error}</p>}
      </div>

      {results.length > 0 && (
        <div className="max-w-2xl mx-auto mt-10 grid gap-4">
          {results.map((r) => (
            <div key={r.id} className="bg-white shadow p-4 rounded-xl">
              <h2 className="text-xl font-bold mb-1">{r.name_he}</h2>
              <p className="text-sm text-gray-500 mb-2">
                {r.calories} קלוריות | {r.tags.join(", ")}
              </p>
              <p className="text-sm mb-2">
                <b>מרכיבים:</b> {r.ingredients_he.join(", ")}
              </p>
              <p className="text-sm">
                <b>אופן הכנה:</b> {r.instructions_he}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
