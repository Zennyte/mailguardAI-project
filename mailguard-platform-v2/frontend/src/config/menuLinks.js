// Linqet e menyse (sidebar-i dhe menyja ne telefon) pas kycjes.
// Per te shtuar, hequr ose rirenditur nje link, ndrysho vetem kete liste.
// "requiredPermission" e fsheh linkun nga perdoruesit qe s'e kane ate leje.
export const MENU_LINKS = [
  { path: "/dashboard", title: "Dashboard" },
  { path: "/scanner", title: "Scanner" },
  { path: "/history", title: "History" },
  { path: "/search", title: "Search" },
  { path: "/import-export", title: "Import/Export" },
  { path: "/reports", title: "Reports" },
  { path: "/cms", title: "CMS", requiredPermission: "manage_cms" },
];
