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
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-white mb-6">Import / Export</h1>

      {error && (
        <p className="bg-red-900/50 text-red-300 text-sm rounded px-3 py-2 mb-4">{error}</p>
      )}

      <div className="bg-slate-800 rounded-lg p-6 mb-6">
        <h2 className="text-lg font-semibold text-white mb-4">Export data</h2>
        <div className="flex flex-wrap items-end gap-4">
          <div>
            <label className="block text-sm text-slate-300 mb-1">List</label>
            <select
              value={exportEntity}
              onChange={(e) => setExportEntity(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            >
              {EXPORT_ENTITIES.map((e) => <option key={e} value={e}>{e}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Format</label>
            <select
              value={exportFormat}
              onChange={(e) => setExportFormat(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            >
              {FORMATS.map((f) => <option key={f} value={f}>{f}</option>)}
            </select>
          </div>
          <button
            onClick={handleExport}
            className="bg-emerald-600 hover:bg-emerald-500 px-6 py-2 rounded text-white font-medium"
          >
            Export
          </button>
        </div>
        <p className="text-xs text-slate-500 mt-3">
          The file downloads directly in the browser.
        </p>
      </div>

      <form onSubmit={handleImport} className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Import data</h2>
        <div className="flex flex-wrap items-end gap-4">
          <div>
            <label className="block text-sm text-slate-300 mb-1">List</label>
            <select
              value={importEntity}
              onChange={(e) => setImportEntity(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            >
              {IMPORT_ENTITIES.map((e) => <option key={e} value={e}>{e}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">File (.csv / .json / .xlsx)</label>
            <input
              type="file"
              accept=".csv,.json,.xlsx"
              onChange={(e) => setImportFile(e.target.files[0])}
              className="text-sm text-slate-300"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 px-6 py-2 rounded text-white font-medium"
          >
            {loading ? "Importing..." : "Import"}
          </button>
        </div>

        {summary && (
          <div className="mt-4 bg-slate-900 rounded p-4 text-sm">
            <p className="text-slate-200">{summary.message}</p>
            <p className="text-slate-400 mt-1">
              Imported: <span className="text-green-400">{summary.imported_count}</span>
              {" · "}
              Skipped: <span className="text-yellow-400">{summary.skipped_count}</span>
            </p>
          </div>
        )}
      </form>
    </div>
  );
}

export default ImportExportPage;
