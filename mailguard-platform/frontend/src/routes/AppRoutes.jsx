import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "./ProtectedRoute";

// Cdo faqe ngarkohet vetem kur perdoruesi hyn ne rrugen (route) e saj (code splitting)
const HomePage = lazy(() => import("../pages/HomePage"));
const LoginPage = lazy(() => import("../pages/LoginPage"));
const RegisterPage = lazy(() => import("../pages/RegisterPage"));
const DashboardPage = lazy(() => import("../pages/DashboardPage"));
const ScannerPage = lazy(() => import("../pages/ScannerPage"));
const ScanHistoryPage = lazy(() => import("../pages/ScanHistoryPage"));
const SearchPage = lazy(() => import("../pages/SearchPage"));
const ImportExportPage = lazy(() => import("../pages/ImportExportPage"));
const ReportsPage = lazy(() => import("../pages/ReportsPage"));
const CmsPage = lazy(() => import("../pages/CmsPage"));

// Shfaqet sa kohe nje faqe (lazy) po ngarkohet
function PageLoader() {
  return <p className="text-[var(--text-dim)] text-sm">Loading...</p>;
}

// Percakton te gjitha rruget e aplikacionit
function AppRoutes() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route element={<MainLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/scanner"
              element={
                <ProtectedRoute>
                  <ScannerPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/history"
              element={
                <ProtectedRoute>
                  <ScanHistoryPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/search"
              element={
                <ProtectedRoute>
                  <SearchPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/import-export"
              element={
                <ProtectedRoute>
                  <ImportExportPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/reports"
              element={
                <ProtectedRoute>
                  <ReportsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/cms"
              element={
                <ProtectedRoute role="Admin">
                  <CmsPage />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default AppRoutes;
