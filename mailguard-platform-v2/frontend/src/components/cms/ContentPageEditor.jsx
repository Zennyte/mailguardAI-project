import { useEffect, useState } from "react";

import {
  updateContentPage, addContentBlock, updateContentBlock, deleteContentBlock,
} from "../../api/cmsApi";
import { getErrorMessage } from "../../api/apiClient";

// Karta "Edit page" ne faqen CMS (kolona e djathte). Ka tri pjese:
// 1. titulli/slug/published i faqes, 2. blloqet ekzistuese, 3. shtimi i nje blloku te ri
function ContentPageEditor({ contentPage, onPageChanged, onError }) {
  // Kopje e faqes qe ndryshohet gjate shkrimit; ruhet ne databaze vetem me butonat Save
  const [editedPage, setEditedPage] = useState(contentPage);
  const [newBlockContent, setNewBlockContent] = useState("");

  // Kur zgjidhet nje faqe tjeter ose te dhenat rifreskohen, fillojme nga kopja e re
  useEffect(() => {
    setEditedPage(contentPage);
  }, [contentPage]);

  // ---------- 1. Te dhenat e faqes ----------

  const handleSavePage = async () => {
    onError("");
    try {
      await updateContentPage(editedPage.id, {
        title: editedPage.title,
        slug: editedPage.slug,
        is_published: editedPage.is_published,
      });
      await onPageChanged();
    } catch (error) {
      onError(getErrorMessage(error, "Could not update the page."));
    }
  };

  // ---------- 2. Blloqet ekzistuese ----------

  // Ndryshon nje fushe ("content" ose "sort_order") te nje blloku ne kopjen lokale
  const handleBlockFieldChange = (blockId, fieldName, newValue) => {
    setEditedPage({
      ...editedPage,
      blocks: editedPage.blocks.map((block) =>
        block.id === blockId ? { ...block, [fieldName]: newValue } : block,
      ),
    });
  };

  const handleSaveBlock = async (block) => {
    onError("");
    try {
      await updateContentBlock(block.id, {
        block_type: block.block_type,
        content: block.content,
        sort_order: Number(block.sort_order) || 0,
      });
      await onPageChanged();
    } catch (error) {
      onError(getErrorMessage(error, "Could not save the block."));
    }
  };

  const handleDeleteBlock = async (blockId) => {
    onError("");
    try {
      await deleteContentBlock(blockId);
      await onPageChanged();
    } catch (error) {
      onError(getErrorMessage(error, "Could not delete the block."));
    }
  };

  // ---------- 3. Blloku i ri ----------

  const handleAddBlock = async (event) => {
    event.preventDefault();
    onError("");
    try {
      await addContentBlock(editedPage.id, {
        block_type: "text",
        content: newBlockContent,
        sort_order: editedPage.blocks.length, // blloku i ri shkon ne fund
      });
      setNewBlockContent("");
      await onPageChanged();
    } catch (error) {
      onError(getErrorMessage(error, "Could not add the block."));
    }
  };

  return (
    <div className="card self-start">
      {/* 1. Te dhenat e faqes */}
      <h2 className="section-title">Edit page</h2>
      <div className="space-y-3 mb-6">
        <input
          value={editedPage.title}
          onChange={(event) => setEditedPage({ ...editedPage, title: event.target.value })}
          className="input-field"
        />
        <input
          value={editedPage.slug}
          onChange={(event) => setEditedPage({ ...editedPage, slug: event.target.value })}
          className="input-field"
        />
        <label className="flex items-center gap-2 text-sm text-muted-text">
          <input
            type="checkbox"
            checked={editedPage.is_published}
            onChange={(event) => setEditedPage({ ...editedPage, is_published: event.target.checked })}
          />
          Published
        </label>
        <button onClick={handleSavePage} className="btn-primary px-6">
          Save Page
        </button>
      </div>

      {/* 2. Blloqet ekzistuese: secili me tekstin, renditjen dhe butonat Save / Delete */}
      <h3 className="text-sm font-bold text-muted-text mb-2">Content blocks</h3>
      {editedPage.blocks.length === 0 && (
        <p className="text-sm text-muted-text mb-3">No blocks yet.</p>
      )}
      <div className="space-y-3 mb-6">
        {editedPage.blocks.map((block) => (
          <div key={block.id} className="bg-raised-background border border-divider rounded p-3 space-y-2">
            <textarea
              value={block.content || ""}
              onChange={(event) => handleBlockFieldChange(block.id, "content", event.target.value)}
              rows={2}
              className="input-field text-sm"
            />
            <div className="flex items-center gap-3 text-sm">
              <label className="text-muted-text">
                Order:{" "}
                <input
                  type="number"
                  value={block.sort_order}
                  onChange={(event) => handleBlockFieldChange(block.id, "sort_order", event.target.value)}
                  className="w-16 bg-card-background border border-divider rounded px-2 py-1 text-main-text"
                />
              </label>
              <button onClick={() => handleSaveBlock(block)} className="text-accent hover:underline">
                Save
              </button>
              <button onClick={() => handleDeleteBlock(block.id)} className="text-phishing hover:underline">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* 3. Shtimi i nje blloku te ri */}
      <form onSubmit={handleAddBlock} className="space-y-2">
        <textarea
          value={newBlockContent}
          onChange={(event) => setNewBlockContent(event.target.value)}
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
  );
}

export default ContentPageEditor;
