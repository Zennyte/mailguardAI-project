import api from "./api";

export async function register(data) {
  const response = await api.post("/auth/register", data);
  return response.data;
}

export async function login(email, password) {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get("/auth/me");
  return response.data;
}

export async function logout(refreshToken) {
  const response = await api.post("/auth/logout", { refresh_token: refreshToken });
  return response.data;
}
