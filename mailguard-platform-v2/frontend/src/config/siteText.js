// Tekstet kryesore te faqes qe shfaqen ne shume vende.
// Ndrysho ketu dhe ndryshon kudo (navbar, sidebar, Homepage, footer).
// Shenim: titulli i tab-it te shfletuesit ndodhet ne frontend/index.html.
export const SITE_TEXT = {
  // Logoja: "MailGuard" ne ngjyre normale, "AI" ne ngjyren e theksit
  brandName: "MailGuard",
  brandAccent: "AI",

  // Homepage
  heroBadge: "Machine Learning email protection", // etiketa e vogel mbi titull
  tagline: "Full-stack email scanning platform powered by Machine Learning.",
  // Shfaqet nese Admin nuk ka publikuar faqen CMS me slug "home"
  defaultIntro:
    "Paste an email and our Machine Learning model tells you instantly if it " +
    "is safe, spam, or a phishing attempt — with a confidence score. After " +
    "logging in, every scan is saved so you can review your scan history at " +
    "any time.",
  exampleEmailSubject: "Verify your account now",
  exampleEmailLabel: "phishing", // etiketa e shfaqur ne shembullin e Homepage

  // Footer-i i faqeve publike
  footer: "MailGuard AI Platform — Lab Course 2 project",
};
