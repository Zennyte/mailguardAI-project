import { useEffect, useState } from "react";

import { previewReport, saveReport, getSavedReports, openSavedReport } from "../api/reportApi";
import { getErrorMessage } from "../api/apiClient";
import ReportForm from "../components/reports/ReportForm";
import ReportNumbers from "../components/reports/ReportNumbers";
import SavedReportsList from "../components/reports/SavedReportsList";

// Faqja Reports (/reports) - tri pjese nga lart poshte:
// 1. forma e raportit, 2. numrat e raportit, 3. lista "Saved reports"
function ReportsPage() {
  const [reportData, setReportData] = useState(null); // numrat e raportit aktual (null = asnje)
  const [savedReports, setSavedReports] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    getSavedReports().then(setSavedReports).catch(() => {});
  }, []);

  const clearMessages = () => {
    setErrorMessage("");
    setSuccessMessage("");
  };

  // Butoni "Preview": shfaq numrat pa ruajtur asgje
  const handlePreview = async (reportOptions) => {
    clearMessages();
    try {
      const preview = await previewReport(reportOptions);
      setReportData(preview.report_data);
    } catch (error) {
      setErrorMessage(getErrorMessage(error, "Preview failed."));
    }
  };

  // Butoni "Save Report": ruan raportin dhe rifreskon listen. Kthen true nese u ruajt.
  const handleSave = async (reportName, reportOptions) => {
    clearMessages();
    if (!reportName) {
      setErrorMessage("Give the report a name before saving.");
      return false;
    }
    try {
      const savedReport = await saveReport(reportName, reportOptions);
      setReportData(savedReport.report_data);
      setSuccessMessage(`Report "${savedReport.report_name}" saved.`);
      setSavedReports(await getSavedReports());
      return true;
    } catch (error) {
      setErrorMessage(getErrorMessage(error, "Saving the report failed."));
      return false;
    }
  };

  // Butoni "View": backend-i i llogarit numrat nga e para me filtrat e ruajtur
  const handleOpenReport = async (reportId) => {
    clearMessages();
    try {
      const report = await openSavedReport(reportId);
      setReportData(report.report_data);
      setSuccessMessage(`Showing saved report "${report.report_name}" (data is regenerated live).`);
    } catch (error) {
      setErrorMessage(getErrorMessage(error, "Could not open the report."));
    }
  };

  return (
    <div>
      <h1 className="page-title">Dynamic Reports</h1>

      <ReportForm
        onPreview={handlePreview}
        onSave={handleSave}
        errorMessage={errorMessage}
        successMessage={successMessage}
      />

      {reportData && <ReportNumbers reportData={reportData} />}

      <SavedReportsList savedReports={savedReports} onOpenReport={handleOpenReport} />
    </div>
  );
}

export default ReportsPage;
