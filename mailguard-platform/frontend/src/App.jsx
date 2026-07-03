import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [backendStatus, setBackendStatus] = useState("checking");

  // Kontrollojme nese backend-i eshte duke punuar
  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "ok") {
          setBackendStatus("online");
        } else {
          setBackendStatus("offline");
        }
      })
      .catch(() => setBackendStatus("offline"));
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-4xl font-bold text-white mb-3">
        MailGuard AI Platform
      </h1>
      <p className="text-lg text-slate-300 mb-8">
        Full-stack email scanning platform powered by Machine Learning
      </p>

      <div className="bg-slate-800 rounded-lg px-6 py-4">
        <p className="text-sm text-slate-400 mb-1">Backend status</p>
        {backendStatus === "checking" && (
          <p className="text-yellow-400 font-medium">Checking...</p>
        )}
        {backendStatus === "online" && (
          <p className="text-green-400 font-medium">Online</p>
        )}
        {backendStatus === "offline" && (
          <p className="text-red-400 font-medium">Offline</p>
        )}
      </div>
    </div>
  );
}

export default App;
