import { useState } from "react";

import { analyzeEmail } from "../services/scanService";
import LabelBadge from "../components/LabelBadge";

// Ngjyrat e njejta si LabelBadge: safe=jeshile, spam=verdhe, phishing=kuqe
const RESULT_BORDERS = {
  safe: "border-[var(--safe)]/40",
  spam: "border-[var(--warn)]/40",
  phishing: "border-[var(--danger)]/40",
};

const BAR_COLORS = {
  safe: "bg-[var(--safe)]",
  spam: "bg-[var(--warn)]",
  phishing: "bg-[var(--danger)]",
};

// Forma e skanimit + rezultati (etikete, score-t, shpjegimi AI)
function ScannerPage() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Dergon emailin per skanim dhe shfaq rezultatin
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
    <div>
      <h1 className="page-title">Email Scanner</h1>

      <div className="grid lg:grid-cols-2 gap-6 items-start">
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
              rows={12}
              placeholder="Paste the email content here..."
              className="input-field"
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary px-6">
            {loading ? "Scanning..." : "Scan Email"}
          </button>
        </form>

        {result ? (
          <div className={`card border-2 ${RESULT_BORDERS[result.predicted_label] || "border-[var(--border)]"}`}>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-bold text-[var(--text)]">Result</h2>
              <LabelBadge label={result.predicted_label} />
            </div>

            <p className="text-[var(--text)] mb-1">{result.message}</p>
            <p className="text-3xl font-bold text-[var(--text)] mb-1">
              {(result.confidence_score * 100).toFixed(1)}%
            </p>
            <p className="text-xs uppercase tracking-wide text-[var(--text-faint)] mb-5">
              confidence
            </p>

            <div className="space-y-2">
              {result.scores.map((score) => (
                <div key={score.label} className="flex items-center gap-3 text-sm">
                  <span className="w-20 text-[var(--text-dim)]">{score.label}</span>
                  <div className="flex-1 bg-[var(--surface-2)] rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${BAR_COLORS[score.label] || "bg-[var(--accent)]"}`}
                      style={{ width: `${score.score * 100}%` }}
                    />
                  </div>
                  <span className="w-14 text-right text-[var(--text)]">
                    {(score.score * 100).toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>

            {result.ai_explanation && (
              <div className="mt-5 pt-4 border-t border-[var(--border)]">
                <p className="text-xs uppercase tracking-wide text-[var(--text-faint)] mb-2">
                  Why? (AI explanation)
                </p>
                <p className="text-sm text-[var(--text-dim)]">{result.ai_explanation}</p>
              </div>
            )}
          </div>
        ) : (
          <div className="empty-state h-full flex items-center justify-center">
            Scan an email to see the result here.
          </div>
        )}
      </div>
    </div>
  );
}

export default ScannerPage;
