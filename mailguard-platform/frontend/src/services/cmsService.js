import api from "./api";

// Lista e plote per panelin e menaxhimit (perfshin draftet)
export async function getPages() {
  const response = await api.get("/cms/pages/manage");
  return response.data;
}

// Endpoint publik - vetem faqet e publikuara
export async function getPageBySlug(slug) {
  const response = await api.get(`/cms/pages/${slug}`);
  return response.data;
}

export async function createPage(data) {
  const response = await api.post("/cms/pages", data);
  return response.data;
}

export async function updatePage(id, data) {
  const response = await api.put(`/cms/pages/${id}`, data);
  return response.data;
}

export async function deletePage(id) {
  const response = await api.delete(`/cms/pages/${id}`);
  return response.data;
}

export async function addBlock(pageId, data) {
  const response = await api.post(`/cms/pages/${pageId}/blocks`, data);
  return response.data;
}

export async function updateBlock(blockId, data) {
  const response = await api.put(`/cms/blocks/${blockId}`, data);
  return response.data;
}

export async function deleteBlock(blockId) {
  const response = await api.delete(`/cms/blocks/${blockId}`);
  return response.data;
}
