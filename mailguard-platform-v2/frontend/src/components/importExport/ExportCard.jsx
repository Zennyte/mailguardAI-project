import { useState } from "react";

import { downloadExportedList } from "../../api/importExportApi";
import SelectField from "../form/SelectField";
import { SEARCHABLE_LISTS, FILE_FORMATS } from "../../config/dropdownOptions";

// Karta "Export data" ne te majte te faqes Import/Export
function ExportCard({ onError }) {
  const [listName, setListName] = useState("scans");
  const [fileFormat, setFileFormat] = useState("csv");

  const handleExport = async () => {
    onError("");
    try {
      await downloadExportedList(listName, fileFormat);
    } catch {
      onError("Export failed. Is the backend running?");
    }
  };

  return (
    <div className="card">
      <h2 className="section-title">Export data</h2>
      <div className="space-y-4">
        <SelectField label="List" value={listName} onChange={setListName} options={SEARCHABLE_LISTS} />
        <SelectField label="Format" value={fileFormat} onChange={setFileFormat} options={FILE_FORMATS} />
        <button onClick={handleExport} className="btn-primary px-6 w-full">
          Export
        </button>
      </div>
      <p className="text-xs text-faint-text mt-3">
        The file downloads directly in the browser.
      </p>
    </div>
  );
}

export default ExportCard;
