import { useEffect, useState } from "react";

import { getAllContentPages, deleteContentPage } from "../api/cmsApi";
import ContentPageList from "../components/cms/ContentPageList";
import NewContentPageForm from "../components/cms/NewContentPageForm";
import ContentPageEditor from "../components/cms/ContentPageEditor";

// Faqja CMS (/cms) - vetem per perdoruesit me lejen "manage_cms" (Admin).
// "Content page" = nje faqe permbajtjeje e krijuar ketu, e perbere nga blloqe teksti.
// Majtas: lista e faqeve + forma "New page". Djathtas: editimi i faqes se zgjedhur.
function CmsManagementPage() {
  const [contentPages, setContentPages] = useState([]);
  const [selectedPageId, setSelectedPageId] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  // Thirret ne fillim dhe pas cdo ndryshimi, qe ekrani te tregoje gjendjen e databazes
  const reloadContentPages = async () => {
    setContentPages(await getAllContentPages().catch(() => []));
  };

  useEffect(() => {
    reloadContentPages();
  }, []);

  // null nese asnje faqe nuk eshte zgjedhur (ose faqja e zgjedhur sapo u fshi)
  const selectedPage = contentPages.find((contentPage) => contentPage.id === selectedPageId) || null;

  const handleDeletePage = async (pageId) => {
    setErrorMessage("");
    await deleteContentPage(pageId).catch(() => setErrorMessage("Could not delete the page."));
    await reloadContentPages();
  };

  return (
    <div>
      <h1 className="page-title mb-1">Simple CMS</h1>
      <p className="text-muted-text mb-6 text-sm">
        Manage static content pages like the homepage text and phishing tips.
      </p>

      {errorMessage && <p className="alert-error mb-4">{errorMessage}</p>}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Kolona e majte */}
        <div className="space-y-6">
          <ContentPageList
            contentPages={contentPages}
            selectedPageId={selectedPageId}
            onSelectPage={setSelectedPageId}
            onDeletePage={handleDeletePage}
          />
          <NewContentPageForm onPageCreated={reloadContentPages} onError={setErrorMessage} />
        </div>

        {/* Kolona e djathte */}
        {selectedPage ? (
          <ContentPageEditor
            contentPage={selectedPage}
            onPageChanged={reloadContentPages}
            onError={setErrorMessage}
          />
        ) : (
          <div className="empty-state self-start">Select a page on the left to edit it.</div>
        )}
      </div>
    </div>
  );
}

export default CmsManagementPage;
