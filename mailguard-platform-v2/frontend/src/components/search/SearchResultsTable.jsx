import EmailLabelBadge from "../EmailLabelBadge";
import { formatDateTime } from "../../utils/formatting";

// Vendos si shfaqet nje qelize sipas kolones dhe llojit te vleres
function formatCell(columnName, value) {
  if (value === null || value === undefined) return "-";
  if (columnName === "predicted_label") return <EmailLabelBadge label={value} />;
  if (columnName === "created_at") return formatDateTime(value);
  if (typeof value === "boolean") return value ? "yes" : "no";
  return String(value);
}

// Tabela e rezultateve te kerkimit. "rows" eshte nje liste objektesh.
// Cdo liste ka kolona te ndryshme, prandaj kolonat merren nga celesat e rreshtit te pare
// (p.sh. "subject", "created_at").
function SearchResultsTable({ rows }) {
  if (rows.length === 0) {
    return (
      <div className="empty-state">
        No results found. Try different filters or another list.
      </div>
    );
  }

  const columnNames = Object.keys(rows[0]);

  return (
    <div className="card p-0 overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="table-header">
            {columnNames.map((columnName) => (
              <th key={columnName} className="table-cell">{columnName.replaceAll("_", " ")}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex} className="table-row">
              {columnNames.map((columnName) => (
                <td key={columnName} className="table-cell text-main-text">
                  {formatCell(columnName, row[columnName])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SearchResultsTable;
