import { create } from "zustand";
import * as authApi from "../api/authApi";
import { setSessionExpiredHandler } from "../api/apiClient";

// Gjendja globale e kycjes: kush eshte i kycur dhe veprimet login/register/logout.
// Tokenat nuk ruhen ketu (as ne localStorage): jane cookie "httpOnly" qe i menaxhon backend-i.
// "user" eshte null kur nuk ka kycje; kur ka kycje permban
// { id, first_name, last_name, email, roles, permissions }.
const useAuthStore = create((set, get) => ({
  user: null,
  isCheckingLogin: true, // true derisa faqja te pyese backend-in nese perdoruesi eshte i kycur
  isLoading: false, // true sa kohe pritet pergjigjja e login/register

  // Thirret nje here kur hapet faqja (App.jsx). Nese cookie-t jane ende te vlefshme,
  // backend-i kthen perdoruesin dhe mbetet i kycur edhe pas rifreskimit te faqes.
  checkLogin: async () => {
    try {
      set({ user: await authApi.getLoggedInUser() });
    } catch {
      set({ user: null });
    } finally {
      set({ isCheckingLogin: false });
    }
  },

  login: async (email, password) => {
    set({ isLoading: true });
    try {
      set({ user: await authApi.login(email, password) });
    } finally {
      set({ isLoading: false });
    }
  },

  // Pas regjistrimit perdoruesi kycet automatikisht
  register: async (registrationForm) => {
    set({ isLoading: true });
    try {
      await authApi.register(registrationForm);
      await get().login(registrationForm.email, registrationForm.password);
    } finally {
      set({ isLoading: false });
    }
  },

  logout: async () => {
    try {
      await authApi.logout();
    } catch {
      // Edhe nese kerkesa deshton, perdoruesi del nga llogaria ne frontend
    }
    set({ user: null });
  },
}));

// Nese kycja skadon ndersa perdoruesi punon, e nxjerrim nga llogaria (faqet e mbrojtura e coje te /login)
setSessionExpiredHandler(() => useAuthStore.setState({ user: null }));

// Lejet vijne nga backend-i (p.sh. "manage_cms", "import_data") dhe perdoren
// per te fshehur pjeset e faqes qe perdoruesi nuk ka te drejte t'i perdore
export function userHasPermission(user, permissionName) {
  return user?.permissions?.includes(permissionName) === true;
}

export default useAuthStore;
