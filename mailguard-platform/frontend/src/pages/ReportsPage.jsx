import { useEffect, useState } from "react";

import { createReport, getReports, getReport, previewReport } from "../services/reportService";

const REPORT_TYPES = [
  { value: "scan_summary", label: "Scan Summary" },
  { value: "label_distribution", label: "Label Distribution" },
  { value: "phishing_activity", label: "Phishing Activity" },
];

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

  const buildParams = () => {
    // Dergohen vetem filtrat e plotesuar
    const params = { report_type: reportType };
    if (dateFrom) params.date_from = dateFrom;
    if (dateTo) params.date_to = dateTo;
    if (label) params.label = label;
    return params;
  };

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
      <h1 className="text-2xl font-bold text-white mb-6">Dynamic Reports</h1>

      <div className="bg-slate-800 rounded-lg p-6 mb-6">
        {error && (
          <p className="bg-red-900/50 text-red-300 text-sm rounded px-3 py-2 mb-4">{error}</p>
        )}
        {message && (
          <p className="bg-emerald-900/50 text-emerald-300 text-sm rounded px-3 py-2 mb-4">{message}</p>
        )}

        <div className="grid sm:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-sm text-slate-300 mb-1">Report type</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            >
              {REPORT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">From date</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">To date</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Label (optional)</label>
            <select
              value={label}
              onChange={(e) => setLabel(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            >
              <option value="">All labels</option>
              <option value="safe">safe</option>
              <option value="spam">spam</option>
              <option value="phishing">phishing</option>
            </select>
          </div>
        </div>

        <div className="flex flex-wrap items-end gap-4">
          <button
            onClick={handlePreview}
            className="bg-slate-700 hover:bg-slate-600 px-6 py-2 rounded text-white font-medium"
          >
            Preview
          </button>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Report name</label>
            <input
              value={reportName}
              onChange={(e) => setReportName(e.target.value)}
              placeholder="e.g. Monthly phishing report"
              className="bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white w-64"
            />
          </div>
          <button
            onClick={handleSave}
            className="bg-emerald-600 hover:bg-emerald-500 px-6 py-2 rounded text-white font-medium"
          >
            Save Report
          </button>
        </div>
      </div>

      {data && (
        <div className="mb-8">
          <div className="grid sm:grid-cols-4 gap-4 mb-4">
            {simpleEntries.map(([key, value]) => (
              <div key={key} className="bg-slate-800 rounded-lg p-5">
                <p className="text-sm text-slate-400">{key.replaceAll("_", " ")}</p>
                <p className="text-2xl font-bold text-white break-words">
                  {value === null ? "-" : String(value)}
                </p>
              </div>
            ))}
          </div>

          {data.distribution && (
            <div className="bg-slate-800 rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-slate-400 border-b border-slate-700">
                    <th className="px-4 py-3">Label</th>
                    <th className="px-4 py-3">Count</th>
                    <th className="px-4 py-3">Percentage</th>
                  </tr>
                </thead>
                <tbody>
                  {data.distribution.map((row) => (
                    <tr key={row.label} className="border-b border-slate-700/50">
                      <td className="px-4 py-3 text-slate-200">{row.label}</td>
                      <td className="px-4 py-3 text-slate-300">{row.count}</td>
                      <td className="px-4 py-3 text-slate-300">{row.percentage}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <h2 className="text-lg font-semibold text-white mb-3">Saved reports</h2>
      {reports.length === 0 ? (
        <div className="bg-slate-800 rounded-lg p-6 text-slate-400">
          No saved reports yet. Choose filters above and click Save Report.
        </div>
      ) : (
        <ul className="bg-slate-800 rounded-lg divide-y divide-slate-700/50">
          {reports.map((report) => (
            <li key={report.id} className="px-4 py-3 flex items-center justify-between">
              <div>
                <p className="text-slate-200">{report.report_name}</p>
                <p className="text-xs text-slate-500">
                  {report.report_type} · {new Date(report.created_at).toLocaleString()}
                </p>
              </div>
              <button
                onClick={() => handleOpenSaved(report.id)}
                className="text-sm text-emerald-400 hover:underline"
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
