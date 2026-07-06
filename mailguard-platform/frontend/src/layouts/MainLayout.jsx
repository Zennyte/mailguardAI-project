import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import NotificationBell from "../components/NotificationBell";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/scanner", label: "Scanner" },
  { to: "/history", label: "History" },
  { to: "/search", label: "Search" },
  { to: "/import-export", label: "Import/Export" },
  { to: "/reports", label: "Reports" },
  { to: "/cms", label: "CMS" },
];

function MainLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  // Linku aktiv theksohet me ngjyre jeshile
  const navLinkClass = ({ isActive }) =>
    isActive ? "nav-link nav-link-active" : "nav-link";

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <nav className="bg-slate-800/95 border-b border-slate-700 sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-y-2">
          <Link to="/" className="text-lg font-bold text-white">
            MailGuard <span className="text-emerald-400">AI</span>
          </Link>

          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm">
            {isAuthenticated ? (
              <>
                {NAV_ITEMS.map((item) => (
                  <NavLink key={item.to} to={item.to} className={navLinkClass}>
                    {item.label}
                  </NavLink>
                ))}
                <NotificationBell />
                {user && (
                  <span className="text-slate-400 hidden sm:inline">
                    {user.first_name}
                  </span>
                )}
                <button onClick={handleLogout} className="btn-secondary px-3 py-1.5 text-sm">
                  Logout
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login" className={navLinkClass}>
                  Login
                </NavLink>
                <Link to="/register" className="btn-primary px-3 py-1.5 text-sm">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <main className="max-w-6xl w-full mx-auto px-4 py-10 flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-slate-800 py-4 text-center text-xs text-slate-500">
        MailGuard AI Platform — Lab Course 2 project
      </footer>
    </div>
  );
}

export default MainLayout;
