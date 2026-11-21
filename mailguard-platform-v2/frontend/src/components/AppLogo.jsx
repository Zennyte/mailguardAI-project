import { Link } from "react-router-dom";
import { SITE_TEXT } from "../config/siteText";

// Logoja ne navbar: ikona e mburojes + emri; klikimi te con te Homepage.
// Teksti vjen nga src/config/siteText.js
function AppLogo({ className = "" }) {
  return (
    <Link to="/" className={`flex items-center gap-2 font-extrabold tracking-tight text-main-text ${className}`}>
      <span className="flex items-center justify-center w-8 h-8 rounded-xl bg-accent text-on-accent">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2"
          strokeLinecap="round" strokeLinejoin="round" className="w-4.5 h-4.5">
          <path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6l-7-3Z" />
          <path d="m9 12 2 2 4-4" />
        </svg>
      </span>
      <span>
        {SITE_TEXT.brandName} <span className="text-accent">{SITE_TEXT.brandAccent}</span>
      </span>
    </Link>
  );
}

export default AppLogo;
