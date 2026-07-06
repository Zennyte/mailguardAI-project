import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import useAuthStore from "../store/authStore";
import { getPageBySlug } from "../services/cmsService";

const LABEL_CARDS = [
  {
    name: "Safe",
    color: "text-green-400",
    border: "border-t-green-500/60",
    text: "Normal, legitimate emails that pose no risk.",
  },
  {
    name: "Spam",
    color: "text-yellow-400",
    border: "border-t-yellow-500/60",
    text: "Unwanted bulk or promotional emails.",
  },
  {
    name: "Phishing",
    color: "text-red-400",
    border: "border-t-red-500/60",
    text: "Malicious emails that try to steal your information.",
  },
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
    <div className="text-center max-w-3xl mx-auto">
      <h1 className="text-4xl font-bold text-white mb-3">MailGuard AI Platform</h1>
      <p className="text-lg text-slate-300 mb-12">
        Full-stack email scanning platform powered by Machine Learning
      </p>

      <div className="grid sm:grid-cols-3 gap-4 mb-12 text-left">
        {LABEL_CARDS.map((card) => (
          <div key={card.name} className={`card border-t-2 ${card.border}`}>
            <p className={`font-semibold mb-1 ${card.color}`}>{card.name}</p>
            <p className="text-sm text-slate-400">{card.text}</p>
          </div>
        ))}
      </div>

      {cmsBlocks && cmsBlocks.length > 0 ? (
        <div className="mb-10 space-y-3">
          {cmsBlocks.map((block) => (
            <p key={block.id} className="text-slate-300">{block.content}</p>
          ))}
        </div>
      ) : (
        <p className="text-slate-300 mb-10">
          Paste an email and our Machine Learning model tells you instantly if it
          is safe, spam, or a phishing attempt — with a confidence score. After
          logging in, every scan is saved so you can review your scan history at
          any time.
        </p>
      )}

      {isAuthenticated ? (
        <Link to="/dashboard" className="btn-primary px-6 py-3">
          Go to Dashboard
        </Link>
      ) : (
        <div className="flex justify-center gap-4">
          <Link to="/login" className="btn-secondary px-6 py-3">
            Login
          </Link>
          <Link to="/register" className="btn-primary px-6 py-3">
            Register
          </Link>
        </div>
      )}
    </div>
  );
}

export default HomePage;
