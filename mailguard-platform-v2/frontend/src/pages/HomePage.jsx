import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import useAuthStore from "../store/authStore";
import { getPublishedContentPage } from "../api/cmsApi";
import EmailLabelBadge from "../components/EmailLabelBadge";
import LabelScoreBar from "../components/LabelScoreBar";
import { LABEL_ORDER, getLabelDetails } from "../config/emailLabels";
import { SITE_TEXT } from "../config/siteText";

// Homepage (/) - faqja publike e prezantimit.
// Tekstet vijne nga src/config/siteText.js, etiketat nga src/config/emailLabels.js
function HomePage() {
  const isLoggedIn = useAuthStore((state) => state.user !== null);
  const [introBlocks, setIntroBlocks] = useState([]);

  // Nese Admin ka publikuar ne CMS nje faqe me slug "home", blloqet e saj
  // zevendesojne tekstin hyres. Perndryshe mbetet teksti i paracaktuar.
  useEffect(() => {
    getPublishedContentPage("home")
      .then((contentPage) => setIntroBlocks(contentPage.blocks))
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid lg:grid-cols-2 gap-10 items-center py-10">
        {/* Ana e majte: titulli, teksti hyres dhe butonat */}
        <div>
          <span className="inline-block mb-4 px-3 py-1 rounded-full text-xs font-semibold bg-accent/10 text-accent">
            {SITE_TEXT.heroBadge}
          </span>
          <h1 className="text-5xl font-extrabold tracking-tight text-main-text mb-4 leading-tight">
            {SITE_TEXT.brandName} <span className="text-accent">{SITE_TEXT.brandAccent}</span>
          </h1>
          <p className="text-lg text-muted-text mb-8">{SITE_TEXT.tagline}</p>

          {introBlocks.length > 0 ? (
            <div className="mb-8 space-y-3">
              {introBlocks.map((block) => (
                <p key={block.id} className="text-muted-text">{block.content}</p>
              ))}
            </div>
          ) : (
            <p className="text-muted-text mb-8">{SITE_TEXT.defaultIntro}</p>
          )}

          {isLoggedIn ? (
            <Link to="/dashboard" className="btn-primary px-6 py-3 inline-block">
              Go to Dashboard
            </Link>
          ) : (
            <div className="flex gap-4">
              <Link to="/register" className="btn-primary px-6 py-3">
                Get started
              </Link>
              <Link to="/login" className="btn-secondary px-6 py-3">
                Login
              </Link>
            </div>
          )}
        </div>

        {/* Ana e djathte: nje shembull si duket rezultati i nje skanimi */}
        <div className="card shadow-xl shadow-accent/10">
          <p className="stat-label mb-3">Example scan result</p>
          <div className="flex items-center justify-between mb-3">
            <span className="text-main-text font-medium">{SITE_TEXT.exampleEmailSubject}</span>
            <EmailLabelBadge label={SITE_TEXT.exampleEmailLabel} />
          </div>
          <div className="space-y-2">
            {LABEL_ORDER.map((label) => (
              <LabelScoreBar key={label} label={label} score={getLabelDetails(label).exampleScore} />
            ))}
          </div>
        </div>
      </div>

      {/* Tri kartat shpjeguese, nga nje per etikete */}
      <div className="grid sm:grid-cols-3 gap-4 py-10">
        {LABEL_ORDER.map((label) => {
          const labelDetails = getLabelDetails(label);
          return (
            <div key={label} className={`stat-card ${labelDetails.cardTopBorderClass}`}>
              <p className="font-bold mb-1 text-main-text">{labelDetails.title}</p>
              <p className="text-sm text-muted-text">{labelDetails.description}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default HomePage;
