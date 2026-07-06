import { useState } from "react";

import { analyzeEmail } from "../services/scanService";
import LabelBadge from "../components/LabelBadge";

// Ngjyrat e njejta si LabelBadge: safe=jeshile, spam=verdhe, phishing=kuqe
const RESULT_BORDERS = {
  safe: "border-green-500/60",
  spam: "border-yellow-500/60",
  phishing: "border-red-500/60",
};

const BAR_COLORS = {
  safe: "bg-green-500",
  spam: "bg-yellow-500",
  phishing: "bg-red-500",
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
      <h1 className="page-title">Email Scanner</h1>

      <form onSubmit={handleSubmit} className="card space-y-4">
        {error && <p className="alert-error">{error}</p>}

        <div>
          <label className="form-label">Subject (optional)</label>
          <input
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="input-field"
          />
        </div>

        <div>
          <label className="form-label">Email body</label>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
            rows={8}
            placeholder="Paste the email content here..."
            className="input-field"
          />
        </div>

        <button type="submit" disabled={loading} className="btn-primary px-6">
          {loading ? "Scanning..." : "Scan Email"}
        </button>
      </form>

      {result && (
        <div className={`card mt-6 border-2 ${RESULT_BORDERS[result.predicted_label] || "border-slate-700"}`}>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-white">Result</h2>
            <LabelBadge label={result.predicted_label} />
          </div>

          <p className="text-slate-200 mb-1">{result.message}</p>
          <p className="text-3xl font-bold text-white mb-1">
            {(result.confidence_score * 100).toFixed(1)}%
          </p>
          <p className="text-sm text-slate-400 mb-5">confidence</p>

          <div className="space-y-2">
            {result.scores.map((score) => (
              <div key={score.label} className="flex items-center gap-3 text-sm">
                <span className="w-20 text-slate-400">{score.label}</span>
                <div className="flex-1 bg-slate-900 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${BAR_COLORS[score.label] || "bg-emerald-500"}`}
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
