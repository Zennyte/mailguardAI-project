import { Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

// Faqet e mbrojtura hapen vetem nese perdoruesi eshte i kycur
function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export default ProtectedRoute;
