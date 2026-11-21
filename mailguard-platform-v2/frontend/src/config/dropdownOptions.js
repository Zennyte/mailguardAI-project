// Opsionet e dropdown-eve ne faqet Search, Import/Export dhe Reports.
// Cdo opsion ka "value" (ajo qe i dergohet backend-it) dhe "title" (ajo qe sheh perdoruesi).
// Per te shtuar ose hequr nje opsion, ndrysho listen perkatese.
import { LABEL_ORDER, getLabelDetails } from "./emailLabels";

// Listat qe mund te kerkohen (Search) dhe te eksportohen (Import/Export)
export const SEARCHABLE_LISTS = [
  { value: "scans", title: "Scans" },
  { value: "email_messages", title: "Email Messages" },
  { value: "notifications", title: "Notifications" },
  { value: "reports", title: "Reports" },
  { value: "cms_pages", title: "CMS Pages" },
];

// Listat qe mund te importohen nga nje skedar (Import/Export)
export const IMPORTABLE_LISTS = [
  { value: "email_messages", title: "Email Messages" },
  { value: "cms_pages", title: "CMS Pages" },
  { value: "user_feedback", title: "User Feedback" },
  { value: "settings", title: "Settings" },
  { value: "notifications", title: "Notifications" },
];

export const FILE_FORMATS = [
  { value: "csv", title: "csv" },
  { value: "json", title: "json" },
  { value: "xlsx", title: "xlsx" },
];

export const REPORT_TYPES = [
  { value: "scan_summary", title: "Scan Summary" },
  { value: "label_distribution", title: "Label Distribution" },
  { value: "phishing_activity", title: "Phishing Activity" },
];

export const SORT_OPTIONS = [
  { value: "newest", title: "Newest first" },
  { value: "oldest", title: "Oldest first" },
];

// Dropdown-i "Label" ne Search dhe Reports: "All labels" + tri etiketat sipas LABEL_ORDER
export const LABEL_FILTER_OPTIONS = [
  { value: "", title: "All labels" },
  ...LABEL_ORDER.map((label) => ({ value: label, title: getLabelDetails(label).title })),
];
