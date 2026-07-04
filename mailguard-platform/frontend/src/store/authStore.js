import { create } from "zustand";
import * as authService from "../services/authService";

const useAuthStore = create((set, get) => ({
  user: null,
  accessToken: localStorage.getItem("accessToken"),
  refreshToken: localStorage.getItem("refreshToken"),
  isAuthenticated: localStorage.getItem("accessToken") !== null,
  loading: false,

  login: async (email, password) => {
    set({ loading: true });
    try {
      const tokens = await authService.login(email, password);
      localStorage.setItem("accessToken", tokens.access_token);
      localStorage.setItem("refreshToken", tokens.refresh_token);
      set({
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        isAuthenticated: true,
      });
      await get().loadCurrentUser();
    } finally {
      set({ loading: false });
    }
  },

  register: async (data) => {
    set({ loading: true });
    try {
      await authService.register(data);
      // Pas regjistrimit behet login automatik
      await get().login(data.email, data.password);
    } finally {
      set({ loading: false });
    }
  },

  loadCurrentUser: async () => {
    const user = await authService.getCurrentUser();
    set({ user });
  },

  logout: async () => {
    try {
      await authService.logout(get().refreshToken);
    } catch {
      // Edhe nese kerkesa deshton, perdoruesi del nga llogaria ne frontend
    }
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false });
  },
}));

export default useAuthStore;
