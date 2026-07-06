import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import useAuthStore from "../store/authStore";
import { getPageBySlug } from "../services/cmsService";

const LABEL_CARDS = [
  { name: "Safe", accent: "var(--safe)", text: "Normal, legitimate emails that pose no risk." },
  { name: "Spam", accent: "var(--warn)", text: "Unwanted bulk or promotional emails." },
  { name: "Phishing", accent: "var(--danger)", text: "Malicious emails that try to steal your information." },
];

function HomePage() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const [cmsBlocks, setCmsBlocks] = useState(null);

  // Nese ekziston faqja CMS "home" e publikuar, teksti i saj perdoret ketu.
  // Nese jo, mbetet teksti statik i meposhtem.
  useEffect(() => {
    getPageBySlug("home")
      .then((page) => setCmsBlocks(page.blocks))
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero */}
      <div className="grid lg:grid-cols-2 gap-10 items-center py-10">
        <div>
          <h1 className="text-5xl font-bold text-[var(--text)] mb-4 leading-tight">
            MailGuard <span className="text-[var(--accent)]">AI</span>
          </h1>
          <p className="text-lg text-[var(--text-dim)] mb-8">
            Full-stack email scanning platform powered by Machine Learning.
          </p>

          {cmsBlocks && cmsBlocks.length > 0 ? (
            <div className="mb-8 space-y-3">
              {cmsBlocks.map((block) => (
                <p key={block.id} className="text-[var(--text-dim)]">{block.content}</p>
              ))}
            </div>
          ) : (
            <p className="text-[var(--text-dim)] mb-8">
              Paste an email and our Machine Learning model tells you instantly if it
              is safe, spam, or a phishing attempt — with a confidence score. After
              logging in, every scan is saved so you can review your scan history at
              any time.
            </p>
          )}

          {isAuthenticated ? (
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

        <div className="card">
          <p className="stat-label mb-3">Example scan result</p>
          <div className="flex items-center justify-between mb-2">
            <span className="text-[var(--text)] font-medium">Verify your account now</span>
            <span className="badge badge-phishing">phishing</span>
          </div>
          <div className="flex items-center gap-3 text-sm mb-1">
            <span className="w-20 text-[var(--text-dim)]">phishing</span>
            <div className="flex-1 bg-[var(--surface-2)] rounded-full h-2">
              <div className="h-2 rounded-full bg-[var(--danger)]" style={{ width: "94%" }} />
            </div>
            <span className="w-10 text-right text-[var(--text-dim)] text-xs">94%</span>
          </div>
          <div className="flex items-center gap-3 text-sm mb-1">
            <span className="w-20 text-[var(--text-dim)]">spam</span>
            <div className="flex-1 bg-[var(--surface-2)] rounded-full h-2">
              <div className="h-2 rounded-full bg-[var(--warn)]" style={{ width: "5%" }} />
            </div>
            <span className="w-10 text-right text-[var(--text-dim)] text-xs">5%</span>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <span className="w-20 text-[var(--text-dim)]">safe</span>
            <div className="flex-1 bg-[var(--surface-2)] rounded-full h-2">
              <div className="h-2 rounded-full bg-[var(--safe)]" style={{ width: "1%" }} />
            </div>
            <span className="w-10 text-right text-[var(--text-dim)] text-xs">1%</span>
          </div>
        </div>
      </div>

      {/* Feature cards */}
      <div className="grid sm:grid-cols-3 gap-4 py-10">
        {LABEL_CARDS.map((card) => (
          <div key={card.name} className="stat-card" style={{ borderTopColor: card.accent }}>
            <p className="font-bold mb-1 text-[var(--text)]">{card.name}</p>
            <p className="text-sm text-[var(--text-dim)]">{card.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
