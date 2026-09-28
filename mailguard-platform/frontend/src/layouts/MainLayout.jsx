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
  { to: "/cms", label: "CMS", role: "Admin" },
];

// Layout i perbashket: navbar per vizitore, sidebar per perdorues te kycur
function MainLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  // Del nga llogaria dhe ridrejton te homepage
  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  // Faqet publike (Home/Login/Register) marrin nje navbar te thjeshte, pa menu anesore
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-[var(--bg)] flex flex-col">
        <nav className="bg-[var(--surface)] border-b border-[var(--border)] sticky top-0 z-20">
          <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
            <Link to="/" className="font-bold text-lg text-[var(--text)]">
              MailGuard <span className="text-[var(--accent)]">AI</span>
            </Link>
            <div className="flex items-center gap-4 text-sm">
              <NavLink to="/login" className="nav-tab">
                Login
              </NavLink>
              <Link to="/register" className="btn-primary px-4 py-1.5 text-sm">
                Register
              </Link>
            </div>
          </div>
        </nav>

        <main className="flex-1 w-full px-6 py-10">
          <Outlet />
        </main>

        <footer className="border-t border-[var(--border)] py-4 text-center text-xs text-[var(--text-faint)]">
          MailGuard AI Platform — Lab Course 2 project
        </footer>
      </div>
    );
  }

  // Percakton klasen CSS te linkut sipas faqes aktive
  const sidebarLinkClass = ({ isActive }) =>
    isActive ? "sidebar-link sidebar-link-active" : "sidebar-link";

  // CMS shfaqet vetem per perdoruesit qe kane rolin Admin
  const visibleNavItems = NAV_ITEMS.filter(
    (item) => !item.role || user?.roles?.includes(item.role),
  );

  // Faqet e brendshme (pas login) marrin nje layout me sidebar, si nje aplikacion i vertete
  return (
    <div className="min-h-screen bg-[var(--bg)] flex">
      <aside className="w-56 shrink-0 hidden md:flex flex-col bg-[var(--surface)] border-r border-[var(--border)]">
        <div className="h-14 flex items-center px-4 border-b border-[var(--border)]">
          <Link to="/" className="font-bold text-[var(--text)]">
            MailGuard <span className="text-[var(--accent)]">AI</span>
          </Link>
        </div>

        <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
          {visibleNavItems.map(({ to, label }) => (
            <NavLink key={to} to={to} className={sidebarLinkClass}>
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="px-3 py-3 border-t border-[var(--border)]">
          {user && (
            <p className="px-1 mb-2 text-xs text-[var(--text-dim)] truncate">
              {user.first_name} {user.last_name}
            </p>
          )}
          <button onClick={handleLogout} className="btn-secondary w-full text-xs py-1.5">
            Logout
          </button>
        </div>
      </aside>

      <div className="flex-1 min-w-0 flex flex-col">
        <header className="h-14 shrink-0 flex items-center justify-between px-4 md:px-8 border-b border-[var(--border)] bg-[var(--surface)] sticky top-0 z-20">
          <Link to="/" className="font-bold text-[var(--text)] md:hidden">
            MailGuard <span className="text-[var(--accent)]">AI</span>
          </Link>
          <div className="hidden md:block" />
          <div className="flex items-center gap-3">
            <NotificationBell />
          </div>
        </header>

        {/* Meny horizontale per ekranet e vegjel, kur sidebar-i fshihet */}
        <nav className="md:hidden flex flex-wrap gap-x-4 gap-y-2 px-4 py-3 border-b border-[var(--border)] bg-[var(--surface)]">
          {visibleNavItems.map(({ to, label }) => (
            <NavLink key={to} to={to} className={({ isActive }) => (isActive ? "nav-tab nav-tab-active" : "nav-tab")}>
              {label}
            </NavLink>
          ))}
        </nav>

        <main className="flex-1 w-full px-4 md:px-8 py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default MainLayout;
