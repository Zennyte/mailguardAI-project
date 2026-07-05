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

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-2">Dashboard</h1>
      {user && (
        <p className="text-slate-300 mb-6">
          Welcome, {user.first_name} {user.last_name}!
        </p>
      )}

      <div className="grid sm:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-800 rounded-lg p-5">
          <p className="text-sm text-slate-400">Total scans</p>
          <p className="text-3xl font-bold text-white">{stats ? stats.total_scans : "-"}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-5">
          <p className="text-sm text-slate-400">Safe</p>
          <p className="text-3xl font-bold text-green-400">{stats ? stats.safe_count : "-"}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-5">
          <p className="text-sm text-slate-400">Spam</p>
          <p className="text-3xl font-bold text-yellow-400">{stats ? stats.spam_count : "-"}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-5">
          <p className="text-sm text-slate-400">Phishing</p>
          <p className="text-3xl font-bold text-red-400">{stats ? stats.phishing_count : "-"}</p>
        </div>
      </div>

      {stats?.latest_scan_label && (
        <p className="text-slate-300 mb-8">
          Latest scan result: <LabelBadge label={stats.latest_scan_label} />
        </p>
      )}

      <div className="flex gap-4">
        <Link
          to="/scanner"
          className="bg-emerald-600 hover:bg-emerald-500 px-6 py-3 rounded text-white font-medium"
        >
          Go to Scanner
        </Link>
        <Link
          to="/history"
          className="bg-slate-700 hover:bg-slate-600 px-6 py-3 rounded text-white font-medium"
        >
          View Scan History
        </Link>
      </div>
    </div>
  );
}

export default DashboardPage;
