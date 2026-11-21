import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getScanHistory } from "../api/scanApi";
import EmailLabelBadge from "../components/EmailLabelBadge";
import { formatDateTime, formatPercent } from "../utils/formatting";

// Faqja History (/history) - tabela e skanimeve te meparshme, me te rejat te parat
function ScanHistoryPage() {
  const [scans, setScans] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getScanHistory()
      .then(setScans)
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div>
      <h1 className="page-title">Scan History</h1>

      {isLoading && <p className="text-muted-text">Loading...</p>}

      {/* Asnje skanim ende */}
      {!isLoading && scans.length === 0 && (
        <div className="empty-state">
          <p className="mb-3">No scans yet.</p>
          <Link to="/scanner" className="btn-primary inline-block">
            Scan your first email
          </Link>
        </div>
      )}

      {/* Tabela e skanimeve */}
      {!isLoading && scans.length > 0 && (
        <div className="card p-0 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="table-header">
                <th className="table-cell">Subject</th>
                <th className="table-cell">Result</th>
                <th className="table-cell">Confidence</th>
                <th className="table-cell">Date</th>
              </tr>
            </thead>
            <tbody>
              {scans.map((scan) => (
                <tr key={scan.scan_request_id} className="table-row">
                  <td className="table-cell text-main-text">
                    {scan.subject || <span className="text-faint-text">(no subject)</span>}
                  </td>
                  <td className="table-cell">
                    <EmailLabelBadge label={scan.predicted_label} />
                  </td>
                  <td className="table-cell text-muted-text">
                    {formatPercent(scan.confidence_score)}
                  </td>
                  <td className="table-cell text-faint-text text-xs">
                    {formatDateTime(scan.created_at)}
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
