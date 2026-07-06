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
    { title: "Total scans", value: stats?.total_scans, color: "text-white", border: "border-t-slate-500/60" },
    { title: "Safe", value: stats?.safe_count, color: "text-green-400", border: "border-t-green-500/60" },
    { title: "Spam", value: stats?.spam_count, color: "text-yellow-400", border: "border-t-yellow-500/60" },
    { title: "Phishing", value: stats?.phishing_count, color: "text-red-400", border: "border-t-red-500/60" },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-1">Dashboard</h1>
      {user && (
        <p className="text-slate-400 mb-8">
          Welcome, {user.first_name} {user.last_name}!
        </p>
      )}

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
        {statCards.map((card) => (
          <div key={card.title} className={`card border-t-2 ${card.border} p-5`}>
            <p className="text-sm text-slate-400 mb-1">{card.title}</p>
            <p className={`text-3xl font-bold ${card.color}`}>
              {card.value ?? "-"}
            </p>
          </div>
        ))}

        <div className="card border-t-2 border-t-emerald-500/60 p-5">
          <p className="text-sm text-slate-400 mb-2">Latest scan</p>
          {stats?.latest_scan_label ? (
            <LabelBadge label={stats.latest_scan_label} />
          ) : (
            <p className="text-slate-500 text-sm">No scans yet</p>
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
