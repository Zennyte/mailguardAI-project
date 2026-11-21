// Kerkesat e faqes CMS dhe te Homepage (backend: cms_controller.py)
// "Content page" = nje faqe permbajtjeje e krijuar ne CMS, e perbere nga blloqe teksti
import apiClient from "./apiClient";

// GET /cms/pages/{slug} - publike; Homepage e perdor me slug-un "home"
export async function getPublishedContentPage(slug) {
  const response = await apiClient.get(`/cms/pages/${slug}`);
  return response.data;
}

// GET /cms/manage/pages - te gjitha faqet, edhe draftet
export async function getAllContentPages() {
  const response = await apiClient.get("/cms/manage/pages");
  return response.data;
}

// POST /cms/pages - "pageForm" permban: title, slug, is_published
export async function createContentPage(pageForm) {
  const response = await apiClient.post("/cms/pages", pageForm);
  return response.data;
}

// PUT /cms/pages/{id}
export async function updateContentPage(pageId, pageForm) {
  const response = await apiClient.put(`/cms/pages/${pageId}`, pageForm);
  return response.data;
}

// DELETE /cms/pages/{id}
export async function deleteContentPage(pageId) {
  const response = await apiClient.delete(`/cms/pages/${pageId}`);
  return response.data;
}

// POST /cms/pages/{id}/blocks - "blockForm" permban: block_type, content, sort_order
export async function addContentBlock(pageId, blockForm) {
  const response = await apiClient.post(`/cms/pages/${pageId}/blocks`, blockForm);
  return response.data;
}

// PUT /cms/blocks/{id}
export async function updateContentBlock(blockId, blockForm) {
  const response = await apiClient.put(`/cms/blocks/${blockId}`, blockForm);
  return response.data;
}

// DELETE /cms/blocks/{id}
export async function deleteContentBlock(blockId) {
  const response = await apiClient.delete(`/cms/blocks/${blockId}`);
  return response.data;
}
