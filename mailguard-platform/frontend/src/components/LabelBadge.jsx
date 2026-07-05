const LABEL_STYLES = {
  safe: "bg-green-500/20 text-green-400",
  spam: "bg-yellow-500/20 text-yellow-400",
  phishing: "bg-red-500/20 text-red-400",
};

// Etiketa me ngjyre sipas rezultatit (safe/spam/phishing)
function LabelBadge({ label }) {
  const style = LABEL_STYLES[label] || "bg-slate-600 text-slate-200";
  return (
    <span className={`px-2 py-0.5 rounded text-sm font-medium ${style}`}>
      {label}
    </span>
  );
}

export default LabelBadge;
