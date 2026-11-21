import { getLabelDetails } from "../config/emailLabels";
import { formatPercent } from "../utils/formatting";

// Nje bar i rezultatit: emri i etiketes, vija me ngjyre dhe perqindja.
// "score" eshte probabiliteti nga 0 deri ne 1 (p.sh. 0.94 = 94%).
// Shfaqet ne karten "Result" te Scanner-it dhe ne shembullin e Homepage.
function LabelScoreBar({ label, score }) {
  const percent = formatPercent(score);

  return (
    <div className="flex items-center gap-3 text-sm">
      <span className="w-20 text-muted-text">{label}</span>

      {/* Vija gri eshte "binari"; vija me ngjyre brenda saj ka gjeresi sa perqindja */}
      <div className="flex-1 bg-raised-background rounded-full h-2">
        <div
          className={`h-2 rounded-full ${getLabelDetails(label).barClass}`}
          style={{ width: percent }}
        />
      </div>

      <span className="w-14 text-right text-main-text">{percent}</span>
    </div>
  );
}

export default LabelScoreBar;
