import EmailLabelBadge from "../EmailLabelBadge";

// Numrat e raportit (pas Preview, Save Report ose View).
// "reportData" permban numra te thjeshte (p.sh. total_scans: 12), qe shfaqen si karta,
// dhe ndonjehere listen "distribution", qe shfaqet si tabele.
function ReportNumbers({ reportData }) {
  const numberCards = Object.entries(reportData).filter(([name]) => name !== "distribution");

  return (
    <div className="mb-8">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        {numberCards.map(([name, value]) => (
          <div key={name} className="stat-card">
            <p className="stat-label">{name.replaceAll("_", " ")}</p>
            <p className="stat-value break-words">{value === null ? "-" : String(value)}</p>
          </div>
        ))}
      </div>

      {reportData.distribution && (
        <div className="card p-0 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="table-header">
                <th className="table-cell">Label</th>
                <th className="table-cell">Count</th>
                <th className="table-cell">Percentage</th>
              </tr>
            </thead>
            <tbody>
              {reportData.distribution.map((distributionRow) => (
                <tr key={distributionRow.label} className="table-row">
                  <td className="table-cell"><EmailLabelBadge label={distributionRow.label} /></td>
                  <td className="table-cell text-muted-text">{distributionRow.count}</td>
                  <td className="table-cell text-muted-text">{distributionRow.percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ReportNumbers;
