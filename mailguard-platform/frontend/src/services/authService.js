import api from "./api";

// POST /auth/register - regjistron nje perdorues te ri
export async function register(data) {
  const response = await api.post("/auth/register", data);
  return response.data;
}

// POST /auth/login - kthen access + refresh token
export async function login(email, password) {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
}

// GET /auth/me - te dhenat e perdoruesit te kycur
export async function getCurrentUser() {
  const response = await api.get("/auth/me");
  return response.data;
}

// POST /auth/logout - revokon refresh tokenin
export async function logout(refreshToken) {
  const response = await api.post("/auth/logout", { refresh_token: refreshToken });
  return response.data;
}
