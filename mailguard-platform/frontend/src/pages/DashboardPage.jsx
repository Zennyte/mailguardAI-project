import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import useAuthStore from "../store/authStore";
import { getScanStats } from "../services/scanService";
import LabelBadge from "../components/LabelBadge";

function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getScanStats().then(setStats).catch(() => {});
  }, []);

  const statCards = [
    { title: "Total scans", value: stats?.total_scans, color: "text-[var(--text)]" },
    { title: "Safe", value: stats?.safe_count, color: "text-[var(--safe)]" },
    { title: "Spam", value: stats?.spam_count, color: "text-[var(--warn)]" },
    { title: "Phishing", value: stats?.phishing_count, color: "text-[var(--danger)]" },
  ];

  return (
    <div>
      <h1 className="page-title mb-1">Dashboard</h1>
      {user && (
        <p className="text-[var(--text-dim)] mb-8 text-sm">
          Welcome, {user.first_name} {user.last_name}
        </p>
      )}

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
        {statCards.map((card) => (
          <div key={card.title} className="stat-card">
            <p className="stat-label">{card.title}</p>
            <p className={`stat-value ${card.color}`}>{card.value ?? "-"}</p>
          </div>
        ))}

        <div className="stat-card">
          <p className="stat-label">Latest scan</p>
          {stats?.latest_scan_label ? (
            <LabelBadge label={stats.latest_scan_label} />
          ) : (
            <p className="text-[var(--text-faint)] text-sm">No scans yet</p>
          )}
        </div>
      </div>

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
