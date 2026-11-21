import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Te gjitha kerkesat drejt backend-it kalojne nga ky klient.
// Tokenat e kycjes ruhen nga backend-i ne cookie "httpOnly": JavaScript nuk i sheh kurre,
// shfletuesi i dergon vetem (withCredentials: true) me cdo kerkese.
const apiClient = axios.create({ baseURL: API_URL, withCredentials: true });

// Funksioni qe thirret kur kycja skadon plotesisht; authStore e vendos (shiko setSessionExpiredHandler)
let onSessionExpired = () => {};

export function setSessionExpiredHandler(handler) {
  onSessionExpired = handler;
}

// Nese disa kerkesa deshtojne njekohesisht, te gjitha presin te njejtin refresh
let tokenRefreshInProgress = null;

// Kerkon cookie te reja nga backend-i duke perdorur refresh tokenin (POST /auth/refresh)
function refreshTokens() {
  if (!tokenRefreshInProgress) {
    tokenRefreshInProgress = axios
      .post(`${API_URL}/auth/refresh`, null, { withCredentials: true })
      .finally(() => {
        tokenRefreshInProgress = null;
      });
  }
  return tokenRefreshInProgress;
}

// Kerkesat e kycjes nuk duhet te provojne refresh kur deshtojne (p.sh. fjalekalim i gabuar)
const URLS_WITHOUT_REFRESH = ["/auth/login", "/auth/register", "/auth/refresh", "/auth/logout"];

// Pas cdo pergjigjeje: nese access tokeni ka skaduar (401), kerkojme token te ri
// dhe e perserisim kerkesen njehere, pa e vene re perdoruesi
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const failedRequest = error.config;
    const accessTokenMayHaveExpired =
      error.response?.status === 401 &&
      !URLS_WITHOUT_REFRESH.includes(failedRequest.url) &&
      !failedRequest.wasRetried;

    if (!accessTokenMayHaveExpired) {
      throw error;
    }

    try {
      await refreshTokens();
    } catch {
      // Edhe refresh tokeni ka skaduar (ose s'ka kycje fare): perdoruesi duhet te kycet perseri
      onSessionExpired();
      throw error;
    }

    failedRequest.wasRetried = true;
    return apiClient(failedRequest);
  },
);

// Nxjerr mesazhin e gabimit qe ktheu backend-i ({"detail": "..."});
// nese nuk ka, perdoret mesazhi rezerve
export function getErrorMessage(error, fallbackMessage) {
  const detail = error.response?.data?.detail;
  return typeof detail === "string" ? detail : fallbackMessage;
}

export default apiClient;
