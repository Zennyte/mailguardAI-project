import api from "./api";

// GET /search - kerkim i avancuar mbi listat e ndryshme
export async function searchData(params) {
  const response = await api.get("/search", { params });
  return response.data;
}
