// Gjithcka rreth tri etiketave (safe, spam, phishing) ndryshohet ne kete skedar.

// ============================================================
// RENDITJA: ndrysho vetem kete rresht per te ndryshuar renditjen
// e etiketave kudo ne faqe (rezultati i Scanner-it, Homepage,
// Dashboard, dropdown-et ne Search dhe Reports).
// ============================================================
export const LABEL_ORDER = ["safe", "spam", "phishing"];

// Detajet e secilës etikete: tekstet dhe ngjyrat.
// Klasat e ngjyrave (p.sh. "bg-safe") duhet te shkruhen te plota ketu,
// qe Tailwind t'i gjeje; vete ngjyrat jane te percaktuara ne src/index.css.
export const LABEL_DETAILS = {
  safe: {
    title: "Safe",
    description: "Normal, legitimate emails that pose no risk.",
    resultMessage: "This email looks safe.",
    exampleScore: 0.01, // vlera e shfaqur ne shembullin e Homepage
    textClass: "text-safe", // numri ne Dashboard
    barClass: "bg-safe", // vija e rezultatit
    badgeClass: "bg-safe/10 text-safe-strong", // etiketa e vogel
    resultBorderClass: "border-safe/40", // korniza e kartes "Result"
    cardTopBorderClass: "border-t-safe", // vija ne krye te kartave te Homepage
  },
  spam: {
    title: "Spam",
    description: "Unwanted bulk or promotional emails.",
    resultMessage: "This email looks like spam.",
    exampleScore: 0.05,
    textClass: "text-spam",
    barClass: "bg-spam",
    badgeClass: "bg-spam/10 text-spam-strong",
    resultBorderClass: "border-spam/40",
    cardTopBorderClass: "border-t-spam",
  },
  phishing: {
    title: "Phishing",
    description: "Malicious emails that try to steal your information.",
    resultMessage: "Warning: this email looks like a phishing attempt!",
    exampleScore: 0.94,
    textClass: "text-phishing",
    barClass: "bg-phishing",
    badgeClass: "bg-phishing/10 text-phishing-strong",
    resultBorderClass: "border-phishing/40",
    cardTopBorderClass: "border-t-phishing",
  },
};

// Pamja neutrale per nje etikete te panjohur (nese modeli kthen dicka te re)
const UNKNOWN_LABEL_DETAILS = {
  title: "Unknown",
  description: "",
  resultMessage: "Scan completed.",
  exampleScore: 0,
  textClass: "text-main-text",
  barClass: "bg-accent",
  badgeClass: "bg-raised-background text-muted-text",
  resultBorderClass: "border-divider",
  cardTopBorderClass: "border-t-divider",
};

// Kthen detajet e nje etikete, p.sh. getLabelDetails("spam").barClass
export function getLabelDetails(label) {
  return LABEL_DETAILS[label] || UNKNOWN_LABEL_DETAILS;
}
