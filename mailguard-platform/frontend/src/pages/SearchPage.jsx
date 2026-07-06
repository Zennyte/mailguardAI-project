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
      <h1 className="page-title">Advanced Search</h1>

      <form onSubmit={handleSearch} className="card mb-6">
        {error && <p className="alert-error mb-4">{error}</p>}

        <div className="grid sm:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="form-label">Search in</label>
            <select
              value={entity}
              onChange={(e) => { setEntity(e.target.value); setResults(null); }}
              className="input-field"
            >
              {ENTITIES.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>

          <div className="sm:col-span-2">
            <label className="form-label">Text query</label>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search text..."
              className="input-field"
            />
          </div>
        </div>

        <div className="grid sm:grid-cols-3 gap-4 mb-4">
          {entity === "scans" && (
            <div>
              <label className="form-label">Label</label>
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
          )}
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
        </div>

        <button type="submit" disabled={loading} className="btn-primary px-6">
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {results !== null && (
        results.length === 0 ? (
          <div className="empty-state">
            No results found. Try different filters or another list.
          </div>
        ) : (
          <div className="card p-0 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="table-header">
                  {columns.map((column) => (
                    <th key={column} className="px-4 py-3">{column.replaceAll("_", " ")}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, index) => (
                  <tr key={index} className="table-row">
                    {columns.map((column) => (
                      <td key={column} className="px-4 py-3 text-[var(--text)]">
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
