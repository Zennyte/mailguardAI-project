import { useState } from "react";

import { searchData } from "../services/searchService";
import LabelBadge from "../components/LabelBadge";

const ENTITIES = [
  { value: "scans", label: "Scans" },
  { value: "email_messages", label: "Email Messages" },
  { value: "notifications", label: "Notifications" },
  { value: "reports", label: "Reports" },
  { value: "cms_pages", label: "CMS Pages" },
];

function SearchPage() {
  const [entity, setEntity] = useState("scans");
  const [q, setQ] = useState("");
  const [label, setLabel] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      // Dergohen vetem filtrat e plotesuar
      const params = { entity };
      if (q) params.q = q;
      if (label && entity === "scans") params.label = label;
      if (dateFrom) params.date_from = dateFrom;
      if (dateTo) params.date_to = dateTo;
      const data = await searchData(params);
      setResults(data.results);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Search failed.");
    } finally {
      setLoading(false);
    }
  };

  const columns = results && results.length > 0 ? Object.keys(results[0]) : [];

  const renderValue = (column, value) => {
    if (column === "predicted_label" && value) return <LabelBadge label={value} />;
    if (column === "created_at" && value) return new Date(value).toLocaleString();
    if (typeof value === "boolean") return value ? "yes" : "no";
    if (value === null || value === undefined) return "-";
    return String(value);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">Advanced Search</h1>

      <form onSubmit={handleSearch} className="bg-slate-800 rounded-lg p-6 mb-6">
        {error && (
          <p className="bg-red-900/50 text-red-300 text-sm rounded px-3 py-2 mb-4">{error}</p>
        )}

        <div className="grid sm:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm text-slate-300 mb-1">Search in</label>
            <select
              value={entity}
              onChange={(e) => { setEntity(e.target.value); setResults(null); }}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            >
              {ENTITIES.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>

          <div className="sm:col-span-2">
            <label className="block text-sm text-slate-300 mb-1">Text query</label>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search text..."
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            />
          </div>
        </div>

        <div className="grid sm:grid-cols-3 gap-4 mb-4">
          {entity === "scans" && (
            <div>
              <label className="block text-sm text-slate-300 mb-1">Label</label>
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
          )}
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
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 px-6 py-2 rounded text-white font-medium"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {results !== null && (
        results.length === 0 ? (
          <div className="bg-slate-800 rounded-lg p-6 text-slate-400">No results found.</div>
        ) : (
          <div className="bg-slate-800 rounded-lg overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-400 border-b border-slate-700">
                  {columns.map((column) => (
                    <th key={column} className="px-4 py-3">{column}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, index) => (
                  <tr key={index} className="border-b border-slate-700/50">
                    {columns.map((column) => (
                      <td key={column} className="px-4 py-3 text-slate-200">
                        {renderValue(column, row[column])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      )}
    </div>
  );
}

export default SearchPage;
