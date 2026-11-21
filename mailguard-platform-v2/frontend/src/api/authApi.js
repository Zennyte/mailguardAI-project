// Kerkesat e faqeve Login dhe Register (backend: auth_controller.py)
import apiClient from "./apiClient";

// POST /auth/register
export async function register(registrationForm) {
  const response = await apiClient.post("/auth/register", registrationForm);
  return response.data;
}

// POST /auth/login - backend-i vendos tokenat ne cookie dhe kthen perdoruesin
export async function login(email, password) {
  const response = await apiClient.post("/auth/login", { email, password });
  return response.data;
}

// GET /auth/me - perdoruesi i kycur me rolet dhe lejet e tij (401 nese s'ka kycje)
export async function getLoggedInUser() {
  const response = await apiClient.get("/auth/me");
  return response.data;
}

// POST /auth/logout - backend-i revokon refresh tokenin dhe fshin cookie-t
export async function logout() {
  const response = await apiClient.post("/auth/logout");
  return response.data;
}
