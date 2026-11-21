import { Navigate, Outlet } from "react-router-dom";
import useAuthStore, { userHasPermission } from "../store/authStore";

// Roja e faqeve te mbrojtura (perdoret ne AppRoutes.jsx).
// - Pa kycje: perdoruesi dergohet te /login.
// - Me "requiredPermission": faqja hapet vetem nese perdoruesi e ka ate leje.
function RequireLogin({ requiredPermission }) {
  const user = useAuthStore((state) => state.user);

  if (user === null) {
    return <Navigate to="/login" replace />;
  }

  if (requiredPermission && !userHasPermission(user, requiredPermission)) {
    return <Navigate to="/dashboard" replace />;
  }

  // Outlet = faqja e kerkuar
  return <Outlet />;
}

export default RequireLogin;
