import { useEffect } from "react";
import AppRoutes from "./routes/AppRoutes";
import useAuthStore from "./store/authStore";

// Komponenti rrenje i aplikacionit
function App() {
  const { isCheckingLogin, checkLogin } = useAuthStore();

  // Kur hapet faqja, pyesim backend-in nese perdoruesi eshte ende i kycur
  useEffect(() => {
    checkLogin();
  }, []);

  // Presim pergjigjen, qe te mos shfaqet per nje cast faqja e vizitorit te nje perdoruesi te kycur
  if (isCheckingLogin) {
    return <p className="p-6 text-sm text-muted-text">Loading...</p>;
  }

  return <AppRoutes />;
}

export default App;
