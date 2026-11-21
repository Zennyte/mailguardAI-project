import { formatDateTime } from "../../utils/formatting";

// Lista "Saved reports" ne fund te faqes Reports; "View" e hap nje raport te ruajtur
function SavedReportsList({ savedReports, onOpenReport }) {
  return (
    <div>
      <h2 className="section-title">Saved reports</h2>

      {savedReports.length === 0 ? (
        <div className="empty-state">
          No saved reports yet. Choose filters above and click Save Report.
        </div>
      ) : (
        <ul className="card p-0 divide-y divide-divider">
          {savedReports.map((savedReport) => (
            <li key={savedReport.id} className="px-4 py-3 flex items-center justify-between">
              <div>
                <p className="text-main-text">{savedReport.report_name}</p>
                <p className="text-xs text-faint-text">
                  {savedReport.report_type} · {formatDateTime(savedReport.created_at)}
                </p>
              </div>
              <button
                onClick={() => onOpenReport(savedReport.id)}
                className="text-sm text-accent hover:underline"
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

export default SavedReportsList;
