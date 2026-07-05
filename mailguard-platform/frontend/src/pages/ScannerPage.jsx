import { useState } from "react";

import { analyzeEmail } from "../services/scanService";
import LabelBadge from "../components/LabelBadge";

const RESULT_STYLES = {
  safe: "border-green-500/50",
  spam: "border-yellow-500/50",
  phishing: "border-red-500/50",
};

function ScannerPage() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = await analyzeEmail({ subject, body, input_type: "manual" });
      setResult(data);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Scan failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-white mb-6">Email Scanner</h1>

      <form onSubmit={handleSubmit} className="bg-slate-800 rounded-lg p-6 space-y-4">
        {error && (
          <p className="bg-red-900/50 text-red-300 text-sm rounded px-3 py-2">{error}</p>
        )}

        <div>
          <label className="block text-sm text-slate-300 mb-1">Subject (optional)</label>
          <input
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-300 mb-1">Email body</label>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
            rows={8}
            placeholder="Paste the email content here..."
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 px-6 py-2 rounded text-white font-medium"
        >
          {loading ? "Scanning..." : "Scan Email"}
        </button>
      </form>

      {result && (
        <div className={`mt-6 bg-slate-800 rounded-lg p-6 border-2 ${RESULT_STYLES[result.predicted_label] || "border-slate-700"}`}>
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-semibold text-white">Result</h2>
            <LabelBadge label={result.predicted_label} />
          </div>

          <p className="text-slate-300 mb-1">{result.message}</p>
          <p className="text-sm text-slate-400 mb-4">
            Confidence: {(result.confidence_score * 100).toFixed(1)}%
          </p>

          <div className="space-y-2">
            {result.scores.map((score) => (
              <div key={score.label} className="flex items-center gap-3 text-sm">
                <span className="w-20 text-slate-400">{score.label}</span>
                <div className="flex-1 bg-slate-900 rounded h-2">
                  <div
                    className="bg-emerald-500 h-2 rounded"
                    style={{ width: `${score.score * 100}%` }}
                  />
                </div>
                <span className="w-14 text-right text-slate-300">
                  {(score.score * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ScannerPage;
