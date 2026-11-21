import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import RequireLogin from "./RequireLogin";

// Cdo faqe ngarkohet vetem kur perdoruesi e hap per here te pare (code splitting)
const HomePage = lazy(() => import("../pages/HomePage"));
const LoginPage = lazy(() => import("../pages/LoginPage"));
const RegisterPage = lazy(() => import("../pages/RegisterPage"));
const DashboardPage = lazy(() => import("../pages/DashboardPage"));
const ScannerPage = lazy(() => import("../pages/ScannerPage"));
const ScanHistoryPage = lazy(() => import("../pages/ScanHistoryPage"));
const SearchPage = lazy(() => import("../pages/SearchPage"));
const ImportExportPage = lazy(() => import("../pages/ImportExportPage"));
const ReportsPage = lazy(() => import("../pages/ReportsPage"));
const CmsManagementPage = lazy(() => import("../pages/CmsManagementPage"));

// Harta e faqes: cila adrese (URL) hap cilen faqe
function AppRoutes() {
  return (
    <BrowserRouter>
      <Suspense fallback={<p className="p-6 text-sm text-muted-text">Loading...</p>}>
        <Routes>
          <Route element={<MainLayout />}>
            {/* Faqet publike */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Faqet qe kerkojne kycje */}
            <Route element={<RequireLogin />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/scanner" element={<ScannerPage />} />
              <Route path="/history" element={<ScanHistoryPage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/import-export" element={<ImportExportPage />} />
              <Route path="/reports" element={<ReportsPage />} />
            </Route>

            {/* Faqja qe kerkon edhe lejen "manage_cms" (vetem Admin) */}
            <Route element={<RequireLogin requiredPermission="manage_cms" />}>
              <Route path="/cms" element={<CmsManagementPage />} />
            </Route>
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default AppRoutes;
