import { useEffect } from "react";
import AppRoutes from "./routes/AppRoutes";
import useAuthStore from "./store/authStore";

// Komponenti rrenje - rifreskon perdoruesin nese ka token te ruajtur
function App() {
  const { isAuthenticated, user, loadCurrentUser, logout } = useAuthStore();

  // Nese ka token te ruajtur, ngarkojme perdoruesin; nese tokeni ka skaduar, dalim
  useEffect(() => {
    if (isAuthenticated && !user) {
      loadCurrentUser().catch(() => logout());
    }
  }, []);

  return <AppRoutes />;
}

export default App;
