import api from "./api";

export async function searchData(params) {
  const response = await api.get("/search", { params });
  return response.data;
}
