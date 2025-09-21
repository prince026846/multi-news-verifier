import { useState } from "react";

export default function VerifierForm() {
  const [newsText, setNewsText] = useState("");
  const [targetLang, setTargetLang] = useState("auto");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("news_text", newsText);
    formData.append("target_lang", targetLang);
    if (file) formData.append("file_upload", file);

    try {
      const res = await fetch("http://localhost:5000/api/verify", {
        method: "POST",
        body: formData,
        mode: "cors", // ✅ allow CORS
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "Server error");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Error:", err);
      setResult({ error: err.message || "Something went wrong" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow">
      <h1 className="text-2xl font-bold mb-4">📰 Multi-Media News Verifier</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={newsText}
          onChange={(e) => setNewsText(e.target.value)}
          placeholder="Type or paste forward messages here..."
          className="w-full min-h-[150px] border rounded-lg p-3"
        />

        <div>
          <label className="block font-semibold">Upload file:</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            accept="image/*,audio/*,video/*,.pdf,.docx,.txt"
          />
        </div>

        <div className="flex items-center gap-3">
          <label>Output language:</label>
          <select
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
            className="border rounded p-2"
          >
            <option value="auto">Auto</option>
            <option value="en">English</option>
            <option value="hi">हिंदी (Hindi)</option>
            <option value="gu">ગુજરાતી (Gujarati)</option>
            <option value="bn">বাংলা (Bengali)</option>
            <option value="mr">मराठी (Marathi)</option>
            <option value="ta">தமிழ் (Tamil)</option>
            <option value="te">తెలుగు (Telugu)</option>
            <option value="pa">ਪੰਜਾਬੀ (Punjabi)</option>
            <option value="kn">ಕನ್ನಡ (Kannada)</option>
          </select>
        </div>

        <button
          type="submit"
          className="bg-indigo-600 text-white px-6 py-2 rounded-lg"
          disabled={loading}
        >
          {loading ? "Checking..." : "Check News"}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 bg-indigo-50 rounded-lg whitespace-pre-line">
          {result.error ? (
            <p className="text-red-600">{result.error}</p>
          ) : (
            <>
              <h2 className="font-bold text-lg">
                🎯 Verdict: {result.verdict}
              </h2>
              <p className="mt-2">{result.analysis}</p>
              <p className="mt-2 text-gray-600">{result.evidence}</p>
              {result.original_text && (
                <p className="mt-2 text-sm text-gray-500">
                  📝 Extracted Text: {result.original_text}
                </p>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
