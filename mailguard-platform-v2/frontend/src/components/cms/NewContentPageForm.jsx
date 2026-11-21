import { useState } from "react";

import { createContentPage } from "../../api/cmsApi";
import { getErrorMessage } from "../../api/apiClient";

const EMPTY_PAGE_FORM = { title: "", slug: "", is_published: false };

// Karta "New page" ne faqen CMS (kolona e majte, poshte)
function NewContentPageForm({ onPageCreated, onError }) {
  const [pageForm, setPageForm] = useState(EMPTY_PAGE_FORM);

  const handleCreatePage = async (event) => {
    event.preventDefault();
    onError("");
    try {
      await createContentPage(pageForm);
      setPageForm(EMPTY_PAGE_FORM);
      await onPageCreated();
    } catch (error) {
      onError(getErrorMessage(error, "Could not create the page."));
    }
  };

  return (
    <form onSubmit={handleCreatePage} className="card">
      <h2 className="section-title">New page</h2>
      <div className="space-y-3">
        <input
          value={pageForm.title}
          onChange={(event) => setPageForm({ ...pageForm, title: event.target.value })}
          placeholder="Title"
          required
          className="input-field"
        />
        {/* Slug = pjesa e adreses qe e identifikon faqen, p.sh. "home" */}
        <input
          value={pageForm.slug}
          onChange={(event) => setPageForm({ ...pageForm, slug: event.target.value })}
          placeholder="Slug (e.g. home, phishing-tips)"
          required
          className="input-field"
        />
        <label className="flex items-center gap-2 text-sm text-muted-text">
          <input
            type="checkbox"
            checked={pageForm.is_published}
            onChange={(event) => setPageForm({ ...pageForm, is_published: event.target.checked })}
          />
          Published
        </label>
        <button type="submit" className="btn-primary px-6">
          Create Page
        </button>
      </div>
    </form>
  );
}

export default NewContentPageForm;
