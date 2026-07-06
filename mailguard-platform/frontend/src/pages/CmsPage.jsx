import { useEffect, useState } from "react";

import {
  getPages, createPage, updatePage, deletePage,
  addBlock, updateBlock, deleteBlock,
} from "../services/cmsService";

function CmsPage() {
  const [pages, setPages] = useState([]);
  const [selected, setSelected] = useState(null);
  const [newPage, setNewPage] = useState({ title: "", slug: "", is_published: false });
  const [newBlock, setNewBlock] = useState({ block_type: "text", content: "", sort_order: 0 });
  const [error, setError] = useState("");

  const loadPages = async () => {
    const data = await getPages().catch(() => []);
    setPages(data);
    // Rifreskojme edhe faqen e zgjedhur nese ekziston akoma
    if (selected) {
      setSelected(data.find((p) => p.id === selected.id) || null);
    }
  };

  useEffect(() => {
    loadPages();
  }, []);

  const showError = (err, fallback) => {
    const detail = err.response?.data?.detail;
    setError(typeof detail === "string" ? detail : fallback);
  };

  const handleCreatePage = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await createPage(newPage);
      setNewPage({ title: "", slug: "", is_published: false });
      await loadPages();
    } catch (err) {
      showError(err, "Could not create the page.");
    }
  };

  const handleUpdatePage = async () => {
    setError("");
    try {
      await updatePage(selected.id, {
        title: selected.title,
        slug: selected.slug,
        is_published: selected.is_published,
      });
      await loadPages();
    } catch (err) {
      showError(err, "Could not update the page.");
    }
  };

  const handleDeletePage = async (id) => {
    setError("");
    await deletePage(id).catch(() => {});
    if (selected?.id === id) setSelected(null);
    await loadPages();
  };

  const handleAddBlock = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await addBlock(selected.id, newBlock);
      setNewBlock({ block_type: "text", content: "", sort_order: 0 });
      await loadPages();
    } catch (err) {
      showError(err, "Could not add the block.");
    }
  };

  const handleBlockChange = (blockId, field, value) => {
    setSelected({
      ...selected,
      blocks: selected.blocks.map((b) =>
        b.id === blockId ? { ...b, [field]: value } : b,
      ),
    });
  };

  const handleSaveBlock = async (block) => {
    setError("");
    try {
      await updateBlock(block.id, {
        block_type: block.block_type,
        content: block.content,
        sort_order: Number(block.sort_order) || 0,
      });
      await loadPages();
    } catch (err) {
      showError(err, "Could not save the block.");
    }
  };

  const handleDeleteBlock = async (blockId) => {
    setError("");
    await deleteBlock(blockId).catch(() => {});
    await loadPages();
  };

  return (
    <div>
      <h1 className="page-title mb-1">Simple CMS</h1>
      <p className="text-[var(--text-dim)] mb-6 text-sm">
        Manage static content pages like the homepage text and phishing tips.
      </p>

      {error && <p className="alert-error mb-4">{error}</p>}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Lista e faqeve + krijimi */}
        <div>
          <div className="card mb-6">
            <h2 className="text-lg font-bold text-[var(--text)] mb-3">Pages</h2>
            {pages.length === 0 ? (
              <p className="text-sm text-[var(--text-dim)]">
                No CMS pages yet. Create the first one below — try the slug{" "}
                <span className="text-[var(--accent)]">home</span> to change the homepage text.
              </p>
            ) : (
              <ul className="divide-y divide-[var(--border)]">
                {pages.map((page) => (
                  <li key={page.id} className="py-2 flex items-center justify-between gap-2">
                    <button
                      onClick={() => setSelected(page)}
                      className={`text-left hover:text-[var(--accent)] ${
                        selected?.id === page.id ? "text-[var(--accent)]" : "text-[var(--text)]"
                      }`}
                    >
                      {page.title}
                      <span className="text-xs text-[var(--text-faint)] ml-2">/{page.slug}</span>
                      {!page.is_published && (
                        <span className="text-xs bg-[var(--surface-2)] text-[var(--warn)] rounded px-1.5 py-0.5 ml-2">
                          draft
                        </span>
                      )}
                    </button>
                    <button
                      onClick={() => handleDeletePage(page.id)}
                      className="text-xs text-[var(--danger)] hover:underline shrink-0"
                    >
                      Delete
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <form onSubmit={handleCreatePage} className="card">
            <h2 className="text-lg font-bold text-[var(--text)] mb-3">New page</h2>
            <div className="space-y-3">
              <input
                value={newPage.title}
                onChange={(e) => setNewPage({ ...newPage, title: e.target.value })}
                placeholder="Title"
                required
                className="input-field"
              />
              <input
                value={newPage.slug}
                onChange={(e) => setNewPage({ ...newPage, slug: e.target.value })}
                placeholder="Slug (e.g. home, phishing-tips)"
                required
                className="input-field"
              />
              <label className="flex items-center gap-2 text-sm text-[var(--text-dim)]">
                <input
                  type="checkbox"
                  checked={newPage.is_published}
                  onChange={(e) => setNewPage({ ...newPage, is_published: e.target.checked })}
                />
                Published
              </label>
              <button type="submit" className="btn-primary px-6">
                Create Page
              </button>
            </div>
          </form>
        </div>

        {/* Editimi i faqes se zgjedhur */}
        <div>
          {selected === null ? (
            <div className="empty-state">
              Select a page on the left to edit it.
            </div>
          ) : (
            <div className="card">
              <h2 className="text-lg font-bold text-[var(--text)] mb-3">Edit page</h2>
              <div className="space-y-3 mb-6">
                <input
                  value={selected.title}
                  onChange={(e) => setSelected({ ...selected, title: e.target.value })}
                  className="input-field"
                />
                <input
                  value={selected.slug}
                  onChange={(e) => setSelected({ ...selected, slug: e.target.value })}
                  className="input-field"
                />
                <label className="flex items-center gap-2 text-sm text-[var(--text-dim)]">
                  <input
                    type="checkbox"
                    checked={selected.is_published}
                    onChange={(e) => setSelected({ ...selected, is_published: e.target.checked })}
                  />
                  Published
                </label>
                <button onClick={handleUpdatePage} className="btn-primary px-6">
                  Save Page
                </button>
              </div>

              <h3 className="text-sm font-bold text-[var(--text-dim)] mb-2">
                Content blocks
              </h3>
              {selected.blocks.length === 0 && (
                <p className="text-sm text-[var(--text-dim)] mb-3">No blocks yet.</p>
              )}
              <div className="space-y-3 mb-6">
                {selected.blocks.map((block) => (
                  <div key={block.id} className="bg-[var(--surface-2)] border border-[var(--border)] rounded p-3 space-y-2">
                    <textarea
                      value={block.content || ""}
                      onChange={(e) => handleBlockChange(block.id, "content", e.target.value)}
                      rows={2}
                      className="input-field text-sm"
                    />
                    <div className="flex items-center gap-3 text-sm">
                      <label className="text-[var(--text-dim)]">
                        Order:{" "}
                        <input
                          type="number"
                          value={block.sort_order}
                          onChange={(e) => handleBlockChange(block.id, "sort_order", e.target.value)}
                          className="w-16 bg-[var(--surface)] border border-[var(--border)] rounded px-2 py-1 text-[var(--text)]"
                        />
                      </label>
                      <button
                        onClick={() => handleSaveBlock(block)}
                        className="text-[var(--accent)] hover:underline"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => handleDeleteBlock(block.id)}
                        className="text-[var(--danger)] hover:underline"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <form onSubmit={handleAddBlock} className="space-y-2">
                <textarea
                  value={newBlock.content}
                  onChange={(e) => setNewBlock({ ...newBlock, content: e.target.value })}
                  placeholder="New block content..."
                  rows={2}
                  required
                  className="input-field text-sm"
                />
                <button type="submit" className="btn-secondary px-4 py-2 text-sm">
                  Add Block
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CmsPage;
