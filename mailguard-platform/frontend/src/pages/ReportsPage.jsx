import { useEffect, useState } from "react";

import { createReport, getReports, getReport, previewReport } from "../services/reportService";
import LabelBadge from "../components/LabelBadge";

const REPORT_TYPES = [
  { value: "scan_summary", label: "Scan Summary" },
  { value: "label_distribution", label: "Label Distribution" },
  { value: "phishing_activity", label: "Phishing Activity" },
];

// Krijon dhe shfaq raporte dinamike
function ReportsPage() {
  const [reportType, setReportType] = useState("scan_summary");
  const [reportName, setReportName] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [label, setLabel] = useState("");
  const [data, setData] = useState(null);
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    getReports().then(setReports).catch(() => {});
  }, []);

  // Ndertimi i filtrave te dergueshem per raportin
  const buildParams = () => {
    // Dergohen vetem filtrat e plotesuar
    const params = { report_type: reportType };
    if (dateFrom) params.date_from = dateFrom;
    if (dateTo) params.date_to = dateTo;
    if (label) params.label = label;
    return params;
  };

  // Shikon te dhenat e raportit pa i ruajtur
  const handlePreview = async () => {
    setError("");
    setMessage("");
    try {
      const result = await previewReport(buildParams());
      setData(result.data);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Preview failed.");
    }
  };

  // Ruan raportin bashke me filtrat e perdorur
  const handleSave = async () => {
    setError("");
    setMessage("");
    if (!reportName) {
      setError("Give the report a name before saving.");
      return;
    }
    try {
      const saved = await createReport({ report_name: reportName, ...buildParams() });
      setData(saved.data);
      setMessage(`Report "${saved.report_name}" saved.`);
      setReportName("");
      setReports(await getReports());
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Saving the report failed.");
    }
  };

  // Hap nje raport te ruajtur (te dhenat rigjenerohen live)
  const handleOpenSaved = async (id) => {
    setError("");
    setMessage("");
    const report = await getReport(id).catch(() => null);
    if (report) {
      setData(report.data);
      setMessage(`Showing saved report "${report.report_name}" (data is regenerated live).`);
    }
  };

  // Vlerat e thjeshta shfaqen si karta, distribution si tabele
  const simpleEntries = data
    ? Object.entries(data).filter(([, value]) => typeof value !== "object" || value === null)
    : [];

  return (
    <div>
      <h1 className="page-title">Dynamic Reports</h1>

      <div className="card mb-6">
        {error && <p className="alert-error mb-4">{error}</p>}
        {message && <p className="alert-success mb-4">{message}</p>}

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="form-label">Report type</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="input-field"
            >
              {REPORT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="form-label">From date</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label className="form-label">To date</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label className="form-label">Label (optional)</label>
            <select
              value={label}
              onChange={(e) => setLabel(e.target.value)}
              className="input-field"
            >
              <option value="">All labels</option>
              <option value="safe">safe</option>
              <option value="spam">spam</option>
              <option value="phishing">phishing</option>
            </select>
          </div>
        </div>

        <div className="flex flex-wrap items-end gap-4">
          <button onClick={handlePreview} className="btn-secondary px-6">
            Preview
          </button>
          <div>
            <label className="form-label">Report name</label>
            <input
              value={reportName}
              onChange={(e) => setReportName(e.target.value)}
              placeholder="e.g. Monthly phishing report"
              className="input-field w-64"
            />
          </div>
          <button onClick={handleSave} className="btn-primary px-6">
            Save Report
          </button>
        </div>
      </div>

      {data && (
        <div className="mb-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            {simpleEntries.map(([key, value]) => (
              <div key={key} className="stat-card">
                <p className="stat-label">{key.replaceAll("_", " ")}</p>
                <p className="stat-value text-[var(--text)] break-words">
                  {value === null ? "-" : String(value)}
                </p>
              </div>
            ))}
          </div>

          {data.distribution && (
            <div className="card p-0 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="table-header">
                    <th className="px-4 py-3">Label</th>
                    <th className="px-4 py-3">Count</th>
                    <th className="px-4 py-3">Percentage</th>
                  </tr>
                </thead>
                <tbody>
                  {data.distribution.map((row) => (
                    <tr key={row.label} className="table-row">
                      <td className="px-4 py-3"><LabelBadge label={row.label} /></td>
                      <td className="px-4 py-3 text-[var(--text-dim)]">{row.count}</td>
                      <td className="px-4 py-3 text-[var(--text-dim)]">{row.percentage}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <h2 className="text-lg font-bold text-[var(--text)] mb-3">Saved reports</h2>
      {reports.length === 0 ? (
        <div className="empty-state">
          No saved reports yet. Choose filters above and click Save Report.
        </div>
      ) : (
        <ul className="card p-0 divide-y divide-[var(--border)]">
          {reports.map((report) => (
            <li key={report.id} className="px-4 py-3 flex items-center justify-between">
              <div>
                <p className="text-[var(--text)]">{report.report_name}</p>
                <p className="text-xs text-[var(--text-faint)]">
                  {report.report_type} · {new Date(report.created_at).toLocaleString()}
                </p>
              </div>
              <button
                onClick={() => handleOpenSaved(report.id)}
                className="text-sm text-[var(--accent)] hover:underline"
              >
                View
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ReportsPage;
