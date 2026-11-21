// Si shfaqen datat dhe perqindjet ne te gjithe faqen (ndrysho ketu per t'i ndryshuar kudo)

// "2026-11-10T23:04:02" -> "11/10/2026, 11:04:02 PM" (sipas gjuhes se shfletuesit)
export function formatDateTime(isoDate) {
  return new Date(isoDate).toLocaleString();
}

// 0.9868 -> "98.7%"
export function formatPercent(score) {
  return `${(score * 100).toFixed(1)}%`;
}
