import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getScanHistory } from "../services/scanService";
import LabelBadge from "../components/LabelBadge";

function ScanHistoryPage() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getScanHistory()
      .then(setScans)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1 className="page-title">Scan History</h1>

      {loading ? (
        <p className="text-slate-400">Loading...</p>
      ) : scans.length === 0 ? (
        <div className="empty-state">
          <p className="mb-3">No scans yet.</p>
          <Link to="/scanner" className="btn-primary inline-block">
            Scan your first email
          </Link>
        </div>
      ) : (
        <div className="card p-0 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="table-header">
                <th className="px-4 py-3">Subject</th>
                <th className="px-4 py-3">Result</th>
                <th className="px-4 py-3">Confidence</th>
                <th className="px-4 py-3">Date</th>
              </tr>
            </thead>
            <tbody>
              {scans.map((scan) => (
                <tr key={scan.scan_request_id} className="table-row">
                  <td className="px-4 py-3 text-slate-200">
                    {scan.subject || <span className="text-slate-500">(no subject)</span>}
                  </td>
                  <td className="px-4 py-3">
                    <LabelBadge label={scan.predicted_label} />
                  </td>
                  <td className="px-4 py-3 text-slate-300">
                    {(scan.confidence_score * 100).toFixed(1)}%
                  </td>
                  <td className="px-4 py-3 text-slate-400">
                    {new Date(scan.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ScanHistoryPage;
