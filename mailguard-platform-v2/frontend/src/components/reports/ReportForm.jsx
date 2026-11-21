import { useState } from "react";

import FormField from "../form/FormField";
import SelectField from "../form/SelectField";
import { REPORT_TYPES, LABEL_FILTER_OPTIONS } from "../../config/dropdownOptions";

// Forma ne krye te faqes Reports: lloji, datat, etiketa dhe butonat Preview / Save Report.
// "message" eshte teksti i gabimit ose i suksesit qe shfaqet mbi formen.
function ReportForm({ onPreview, onSave, errorMessage, successMessage }) {
  const [reportType, setReportType] = useState("scan_summary");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [label, setLabel] = useState("");
  const [reportName, setReportName] = useState("");

  // Mbledh zgjedhjet e formes; backend-it i dergohen vetem filtrat e plotesuar
  const getReportOptions = () => {
    const reportOptions = { report_type: reportType };
    if (dateFrom) reportOptions.date_from = dateFrom;
    if (dateTo) reportOptions.date_to = dateTo;
    if (label) reportOptions.label = label;
    return reportOptions;
  };

  const handleSave = async () => {
    const wasSaved = await onSave(reportName, getReportOptions());
    if (wasSaved) {
      setReportName("");
    }
  };

  return (
    <div className="card mb-6">
      {errorMessage && <p className="alert-error mb-4">{errorMessage}</p>}
      {successMessage && <p className="alert-success mb-4">{successMessage}</p>}

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        <SelectField label="Report type" value={reportType} onChange={setReportType} options={REPORT_TYPES} />
        <FormField label="From date">
          <input
            type="date"
            value={dateFrom}
            onChange={(event) => setDateFrom(event.target.value)}
            className="input-field"
          />
        </FormField>
        <FormField label="To date">
          <input
            type="date"
            value={dateTo}
            onChange={(event) => setDateTo(event.target.value)}
            className="input-field"
          />
        </FormField>
        <SelectField label="Label (optional)" value={label} onChange={setLabel} options={LABEL_FILTER_OPTIONS} />
      </div>

      <div className="flex flex-wrap items-end gap-4">
        <button onClick={() => onPreview(getReportOptions())} className="btn-secondary px-6">
          Preview
        </button>
        <FormField label="Report name">
          <input
            value={reportName}
            onChange={(event) => setReportName(event.target.value)}
            placeholder="e.g. Monthly phishing report"
            className="input-field w-64"
          />
        </FormField>
        <button onClick={handleSave} className="btn-primary px-6">
          Save Report
        </button>
      </div>
    </div>
  );
}

export default ReportForm;
