import { useState } from "react";

import { exportData, importData } from "../services/dataTransferService";

const EXPORT_ENTITIES = ["scans", "email_messages", "notifications", "reports", "cms_pages"];
const IMPORT_ENTITIES = ["email_messages", "cms_pages", "user_feedback", "settings", "notifications"];
const FORMATS = ["csv", "json", "xlsx"];

function ImportExportPage() {
  const [exportEntity, setExportEntity] = useState("scans");
  const [exportFormat, setExportFormat] = useState("csv");
  const [importEntity, setImportEntity] = useState("email_messages");
  const [importFile, setImportFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setError("");
    try {
      await exportData(exportEntity, exportFormat);
    } catch {
      setError("Export failed. Is the backend running?");
    }
  };

  const handleImport = async (event) => {
    event.preventDefault();
    setError("");
    setSummary(null);
    if (!importFile) {
      setError("Choose a file first (.csv, .json or .xlsx).");
      return;
    }
    setLoading(true);
    try {
      const result = await importData(importEntity, importFile);
      setSummary(result);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Import failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="page-title">Import / Export</h1>

      {error && <p className="alert-error mb-4">{error}</p>}

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-bold text-[var(--text)] mb-4">Export data</h2>
          <div className="space-y-4">
            <div>
              <label className="form-label">List</label>
              <select
                value={exportEntity}
                onChange={(e) => setExportEntity(e.target.value)}
                className="input-field"
              >
                {EXPORT_ENTITIES.map((e) => <option key={e} value={e}>{e}</option>)}
              </select>
            </div>
            <div>
              <label className="form-label">Format</label>
              <select
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value)}
                className="input-field"
              >
                {FORMATS.map((f) => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>
            <button onClick={handleExport} className="btn-primary px-6 w-full">
              Export
            </button>
          </div>
          <p className="text-xs text-[var(--text-faint)] mt-3">
            The file downloads directly in the browser.
          </p>
        </div>

        <form onSubmit={handleImport} className="card">
          <h2 className="text-lg font-bold text-[var(--text)] mb-4">Import data</h2>
          <div className="space-y-4">
            <div>
              <label className="form-label">List</label>
              <select
                value={importEntity}
                onChange={(e) => setImportEntity(e.target.value)}
                className="input-field"
              >
                {IMPORT_ENTITIES.map((e) => <option key={e} value={e}>{e}</option>)}
              </select>
            </div>
            <div>
              <label className="form-label">File (.csv / .json / .xlsx)</label>
              <input
                type="file"
                accept=".csv,.json,.xlsx"
                onChange={(e) => setImportFile(e.target.files[0])}
                className="input-field text-sm"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary px-6 w-full">
              {loading ? "Importing..." : "Import"}
            </button>
          </div>

          {summary && (
            <div className="alert-success mt-4">
              <p>{summary.message}</p>
              <p className="mt-1 text-[var(--text-dim)]">
                Imported: <span className="text-[var(--safe)] font-bold">{summary.imported_count}</span>
                {" · "}
                Skipped: <span className="text-[var(--warn)] font-bold">{summary.skipped_count}</span>
              </p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default ImportExportPage;
