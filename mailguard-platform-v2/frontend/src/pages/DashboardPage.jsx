import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import useAuthStore from "../store/authStore";
import { getScanStats } from "../api/scanApi";
import EmailLabelBadge from "../components/EmailLabelBadge";
import { LABEL_ORDER, getLabelDetails } from "../config/emailLabels";

// Faqja Dashboard (/dashboard) - permbledhja e skanimeve te perdoruesit
function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const [scanStats, setScanStats] = useState(null); // null derisa te vije pergjigjja

  useEffect(() => {
    getScanStats().then(setScanStats).catch(() => {});
  }, []);

  // Karta "Total scans" para, pastaj nje karte per cdo etikete sipas LABEL_ORDER
  const numberCards = [
    { title: "Total scans", number: scanStats?.total_scans, numberColor: "text-main-text" },
    ...LABEL_ORDER.map((label) => ({
      title: getLabelDetails(label).title,
      number: scanStats?.scans_per_label[label],
      numberColor: getLabelDetails(label).textClass,
    })),
  ];

  return (
    <div>
      <h1 className="page-title mb-1">Dashboard</h1>
      <p className="text-muted-text mb-8 text-sm">
        Welcome, {user.first_name} {user.last_name}
      </p>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
        {numberCards.map((card) => (
          <div key={card.title} className="stat-card">
            <p className="stat-label">{card.title}</p>
            <p className={`stat-value ${card.numberColor}`}>{card.number ?? "-"}</p>
          </div>
        ))}

        {/* Karta e fundit: etiketa e skanimit me te fundit */}
        <div className="stat-card">
          <p className="stat-label">Latest scan</p>
          {scanStats?.latest_scan_label ? (
            <EmailLabelBadge label={scanStats.latest_scan_label} />
          ) : (
            <p className="text-faint-text text-sm">No scans yet</p>
          )}
        </div>
      </div>

      {/* Shkurtore drejt faqeve kryesore */}
      <div className="flex flex-wrap gap-4">
        <Link to="/scanner" className="btn-primary px-6 py-3">
          Go to Scanner
        </Link>
        <Link to="/history" className="btn-secondary px-6 py-3">
          View Scan History
        </Link>
      </div>
    </div>
  );
}

export default DashboardPage;
