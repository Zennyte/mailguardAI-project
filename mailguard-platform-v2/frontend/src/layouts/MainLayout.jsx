import useAuthStore from "../store/authStore";
import VisitorLayout from "./VisitorLayout";
import LoggedInLayout from "./LoggedInLayout";

// Korniza rreth cdo faqeje: vizitoret shohin nje navbar te thjeshte,
// perdoruesit e kycur shohin menyne anesore (sidebar)
function MainLayout() {
  const user = useAuthStore((state) => state.user);
  const isLoggedIn = user !== null;

  return isLoggedIn ? <LoggedInLayout /> : <VisitorLayout />;
}

export default MainLayout;
