import { useState } from "react";

import { importListFromFile } from "../../api/importExportApi";
import { getErrorMessage } from "../../api/apiClient";
import FormField from "../form/FormField";
import SelectField from "../form/SelectField";
import { IMPORTABLE_LISTS } from "../../config/dropdownOptions";

// Karta "Import data" ne te djathte te faqes Import/Export
function ImportCard({ onError }) {
  const [listName, setListName] = useState("email_messages");
  const [fileToImport, setFileToImport] = useState(null);
  const [importSummary, setImportSummary] = useState(null);
  const [isImporting, setIsImporting] = useState(false);

  const handleImport = async (event) => {
    event.preventDefault();
    onError("");
    setImportSummary(null);

    if (!fileToImport) {
      onError("Choose a file first (.csv, .json or .xlsx).");
      return;
    }

    setIsImporting(true);
    try {
      setImportSummary(await importListFromFile(listName, fileToImport));
    } catch (error) {
      onError(getErrorMessage(error, "Import failed."));
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <form onSubmit={handleImport} className="card">
      <h2 className="section-title">Import data</h2>
      <div className="space-y-4">
        <SelectField label="List" value={listName} onChange={setListName} options={IMPORTABLE_LISTS} />
        <FormField label="File (.csv / .json / .xlsx)">
          <input
            type="file"
            accept=".csv,.json,.xlsx"
            onChange={(event) => setFileToImport(event.target.files[0])}
            className="input-field text-sm"
          />
        </FormField>
        <button type="submit" disabled={isImporting} className="btn-primary px-6 w-full">
          {isImporting ? "Importing..." : "Import"}
        </button>
      </div>

      {/* Mesazhi i gjelber pas importit */}
      {importSummary && (
        <div className="alert-success mt-4">
          <p>{importSummary.message}</p>
          <p className="mt-1 text-muted-text">
            Imported: <span className="text-safe font-bold">{importSummary.imported_count}</span>
            {" · "}
            Skipped: <span className="text-spam font-bold">{importSummary.skipped_count}</span>
          </p>
        </div>
      )}
    </form>
  );
}

export default ImportCard;
