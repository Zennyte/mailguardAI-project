import { NavLink, Outlet, useNavigate } from "react-router-dom";
import useAuthStore, { userHasPermission } from "../store/authStore";
import AppLogo from "../components/AppLogo";
import NotificationBell from "../components/NotificationBell";
import { MENU_LINKS } from "../config/menuLinks";

// Korniza e faqeve pas kycjes: navbar lart me linqet, kambanen dhe Logout.
// Linqet e menyse vijne nga src/config/menuLinks.js
function LoggedInLayout() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  // Linqet qe perdoruesi ka te drejte t'i shohe (p.sh. "CMS" vetem per Admin)
  const visibleMenuLinks = MENU_LINKS.filter(
    (menuLink) => !menuLink.requiredPermission || userHasPermission(user, menuLink.requiredPermission),
  );

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-card-background/90 backdrop-blur border-b border-divider sticky top-0 z-20">
        {/* Rreshti i pare: logo majtas, kambana dhe perdoruesi djathtas */}
        <div className="max-w-6xl mx-auto px-4 md:px-6 h-16 flex items-center justify-between gap-4">
          <AppLogo />

          <div className="flex items-center gap-3">
            <NotificationBell />
            <span className="hidden sm:inline text-sm font-medium text-muted-text">
              {user.first_name} {user.last_name}
            </span>
            <button onClick={handleLogout} className="btn-secondary text-xs px-4 py-1.5">
              Logout
            </button>
          </div>
        </div>

        {/* Rreshti i dyte: linqet e menyse (rreshqasin horizontalisht ne telefon) */}
        <nav className="max-w-6xl mx-auto px-4 md:px-6 pb-3 flex items-center gap-1 overflow-x-auto">
          {visibleMenuLinks.map((menuLink) => (
            <NavLink
              key={menuLink.path}
              to={menuLink.path}
              className={({ isActive }) => (isActive ? "nav-link nav-link-active" : "nav-link")}
            >
              {menuLink.title}
            </NavLink>
          ))}
        </nav>
      </header>

      {/* Outlet = faqja aktuale */}
      <main className="flex-1 w-full max-w-6xl mx-auto px-4 md:px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}

export default LoggedInLayout;
