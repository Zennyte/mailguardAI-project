import { getLabelDetails } from "../config/emailLabels";

// Etiketa e vogel me ngjyre (safe, spam ose phishing).
// Shfaqet ne Homepage, Dashboard, History, Search, Reports dhe ne karten e rezultatit.
// Ngjyrat vijne nga src/config/emailLabels.js
function EmailLabelBadge({ label }) {
  return <span className={`label-badge ${getLabelDetails(label).badgeClass}`}>{label}</span>;
}

export default EmailLabelBadge;
