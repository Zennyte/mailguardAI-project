import { useState } from "react";

import { scanEmail } from "../api/scanApi";
import { getErrorMessage } from "../api/apiClient";
import ScanResultCard from "../components/ScanResultCard";

// Faqja Scanner (/scanner) - forma majtas, rezultati djathtas
function ScannerPage() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [scanResult, setScanResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isScanning, setIsScanning] = useState(false);

  const handleScan = async (event) => {
    event.preventDefault();
    setErrorMessage("");
    setScanResult(null);
    setIsScanning(true);
    try {
      setScanResult(await scanEmail(subject, body));
    } catch (error) {
      setErrorMessage(getErrorMessage(error, "Scan failed. Is the backend running?"));
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div>
      <h1 className="page-title">Email Scanner</h1>

      <div className="grid lg:grid-cols-2 gap-6 items-start">
        {/* Majtas: forma ku ngjitet emaili */}
        <form onSubmit={handleScan} className="card space-y-4">
          {errorMessage && <p className="alert-error">{errorMessage}</p>}

          <div>
            <label className="form-label">Subject (optional)</label>
            <input
              value={subject}
              onChange={(event) => setSubject(event.target.value)}
              className="input-field"
            />
          </div>

          <div>
            <label className="form-label">Email body</label>
            <textarea
              value={body}
              onChange={(event) => setBody(event.target.value)}
              required
              rows={12}
              placeholder="Paste the email content here..."
              className="input-field"
            />
          </div>

          <button type="submit" disabled={isScanning} className="btn-primary px-6">
            {isScanning ? "Scanning..." : "Scan Email"}
          </button>
        </form>

        {/* Djathtas: rezultati i skanimit (ose nje kuti bosh para skanimit te pare) */}
        {scanResult ? (
          <ScanResultCard scanResult={scanResult} />
        ) : (
          <div className="empty-state">Scan an email to see the result here.</div>
        )}
      </div>
    </div>
  );
}

export default ScannerPage;
