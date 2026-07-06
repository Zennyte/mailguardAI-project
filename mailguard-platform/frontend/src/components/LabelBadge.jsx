const LABEL_CLASS = {
  safe: "badge badge-safe",
  spam: "badge badge-spam",
  phishing: "badge badge-phishing",
};

// Etiketa me ngjyre sipas rezultatit (safe/spam/phishing)
function LabelBadge({ label }) {
  const className = LABEL_CLASS[label] || "badge text-[var(--text-dim)] bg-[var(--surface-2)]";

  return <span className={className}>{label}</span>;
}

export default LabelBadge;
