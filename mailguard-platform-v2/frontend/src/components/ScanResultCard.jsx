import EmailLabelBadge from "./EmailLabelBadge";
import LabelScoreBar from "./LabelScoreBar";
import { LABEL_ORDER, getLabelDetails } from "../config/emailLabels";
import { formatPercent } from "../utils/formatting";

// Karta "Result" ne te djathte te faqes Scanner.
// "scanResult" eshte pergjigjja e POST /scans/analyze.
function ScanResultCard({ scanResult }) {
  const predictedLabelDetails = getLabelDetails(scanResult.predicted_label);

  // Bar-et shfaqen sipas LABEL_ORDER (config/emailLabels.js), jo sipas renditjes qe vjen nga modeli
  const orderedLabelScores = [...scanResult.label_scores].sort(
    (a, b) => LABEL_ORDER.indexOf(a.label) - LABEL_ORDER.indexOf(b.label),
  );

  return (
    <div className={`card border-2 ${predictedLabelDetails.resultBorderClass}`}>
      {/* Titulli dhe etiketa e parashikuar */}
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-bold text-main-text">Result</h2>
        <EmailLabelBadge label={scanResult.predicted_label} />
      </div>

      {/* Fjalia permbledhese dhe besueshmeria e modelit */}
      <p className="text-main-text mb-1">{predictedLabelDetails.resultMessage}</p>
      <p className="text-3xl font-bold text-main-text mb-1">
        {formatPercent(scanResult.confidence_score)}
      </p>
      <p className="text-xs uppercase tracking-wide text-faint-text mb-5">confidence</p>

      {/* Nga nje bar per secilen etikete */}
      <div className="space-y-2">
        {orderedLabelScores.map((labelScore) => (
          <LabelScoreBar key={labelScore.label} label={labelScore.label} score={labelScore.score} />
        ))}
      </div>

      {/* Shpjegimi me fjale nga AI (shfaqet vetem nese backend-i ka GROQ_API_KEY) */}
      {scanResult.ai_explanation && (
        <div className="mt-5 pt-4 border-t border-divider">
          <p className="text-xs uppercase tracking-wide text-faint-text mb-2">
            Why? (AI explanation)
          </p>
          <p className="text-sm text-muted-text">{scanResult.ai_explanation}</p>
        </div>
      )}
    </div>
  );
}

export default ScanResultCard;
