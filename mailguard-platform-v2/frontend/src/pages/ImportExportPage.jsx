import { useState } from "react";

import useAuthStore, { userHasPermission } from "../store/authStore";
import ExportCard from "../components/importExport/ExportCard";
import ImportCard from "../components/importExport/ImportCard";

// Faqja Import/Export (/import-export) - karta "Export data" majtas, "Import data" djathtas
function ImportExportPage() {
  const user = useAuthStore((state) => state.user);
  const [errorMessage, setErrorMessage] = useState("");

  // Importi lejohet vetem per Admin dhe Manager (leja "import_data" ne database/seed.sql)
  const canImport = userHasPermission(user, "import_data");

  return (
    <div>
      <h1 className="page-title">Import / Export</h1>

      {errorMessage && <p className="alert-error mb-4">{errorMessage}</p>}

      <div className="grid lg:grid-cols-2 gap-6">
        <ExportCard onError={setErrorMessage} />

        {canImport ? (
          <ImportCard onError={setErrorMessage} />
        ) : (
          <div className="card">
            <h2 className="section-title">Import data</h2>
            <p className="text-sm text-muted-text">
              Importing data requires the Admin or Manager role.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ImportExportPage;
