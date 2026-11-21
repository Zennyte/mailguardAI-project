import { Link, NavLink, Outlet } from "react-router-dom";
import AppLogo from "../components/AppLogo";
import { SITE_TEXT } from "../config/siteText";

// Korniza e faqeve publike (Home, Login, Register): navbar lart + footer poshte
function VisitorLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar: logo majtas, Login dhe Register djathtas */}
      <nav className="bg-card-background/90 backdrop-blur border-b border-divider sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-4 md:px-6 h-16 flex items-center justify-between">
          <AppLogo className="text-lg" />
          <div className="flex items-center gap-2">
            <NavLink
              to="/login"
              className={({ isActive }) => (isActive ? "nav-link nav-link-active" : "nav-link")}
            >
              Login
            </NavLink>
            <Link to="/register" className="btn-primary px-4 py-1.5 text-sm">
              Register
            </Link>
          </div>
        </div>
      </nav>

      {/* Outlet = faqja aktuale */}
      <main className="flex-1 w-full px-4 md:px-6 py-10">
        <Outlet />
      </main>

      <footer className="border-t border-divider bg-card-background py-6 text-center text-xs text-faint-text">
        {SITE_TEXT.footer}
      </footer>
    </div>
  );
}

export default VisitorLayout;
