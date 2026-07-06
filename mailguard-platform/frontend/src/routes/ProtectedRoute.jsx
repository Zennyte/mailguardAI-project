import { Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

// Faqet e mbrojtura hapen vetem nese perdoruesi eshte i kycur.
// Nese jepet "role", faqja kerkon qe perdoruesi te kete ate rol specifik.
function ProtectedRoute({ children, role }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const user = useAuthStore((state) => state.user);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  if (role && !user?.roles?.includes(role)) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
}

export default ProtectedRoute;
