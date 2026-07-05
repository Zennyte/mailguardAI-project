import { Link, Outlet, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import NotificationBell from "../components/NotificationBell";

function MainLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <nav className="bg-slate-800 border-b border-slate-700">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-lg font-bold text-white">
            MailGuard <span className="text-emerald-400">AI</span>
          </Link>

          <div className="flex items-center gap-4 text-sm">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="hover:text-emerald-400">
                  Dashboard
                </Link>
                <Link to="/scanner" className="hover:text-emerald-400">
                  Scanner
                </Link>
                <Link to="/history" className="hover:text-emerald-400">
                  History
                </Link>
                <Link to="/search" className="hover:text-emerald-400">
                  Search
                </Link>
                <Link to="/import-export" className="hover:text-emerald-400">
                  Import/Export
                </Link>
                <Link to="/reports" className="hover:text-emerald-400">
                  Reports
                </Link>
                <Link to="/cms" className="hover:text-emerald-400">
                  CMS
                </Link>
                <NotificationBell />
                {user && <span className="text-slate-400">{user.first_name}</span>}
                <button
                  onClick={handleLogout}
                  className="bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="hover:text-emerald-400">
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-emerald-600 hover:bg-emerald-500 px-3 py-1.5 rounded text-white"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 py-10">
        <Outlet />
      </main>
    </div>
  );
}

export default MainLayout;
