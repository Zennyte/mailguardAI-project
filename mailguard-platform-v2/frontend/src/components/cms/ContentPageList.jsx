// Karta "Pages" ne faqen CMS (kolona e majte, lart):
// lista e te gjitha faqeve te permbajtjes, me butonin Delete prane secilit
function ContentPageList({ contentPages, selectedPageId, onSelectPage, onDeletePage }) {
  return (
    <div className="card">
      <h2 className="section-title">Pages</h2>

      {contentPages.length === 0 ? (
        <p className="text-sm text-muted-text">
          No CMS pages yet. Create the first one below — try the slug{" "}
          <span className="text-accent">home</span> to change the homepage text.
        </p>
      ) : (
        <ul className="divide-y divide-divider">
          {contentPages.map((contentPage) => (
            <li key={contentPage.id} className="py-2 flex items-center justify-between gap-2">
              {/* Klikimi mbi titull e hap faqen per editim ne kolonen e djathte */}
              <button
                onClick={() => onSelectPage(contentPage.id)}
                className={`text-left hover:text-accent ${
                  contentPage.id === selectedPageId ? "text-accent" : "text-main-text"
                }`}
              >
                {contentPage.title}
                <span className="text-xs text-faint-text ml-2">/{contentPage.slug}</span>
                {!contentPage.is_published && (
                  <span className="text-xs bg-raised-background text-spam rounded px-1.5 py-0.5 ml-2">
                    draft
                  </span>
                )}
              </button>
              <button
                onClick={() => onDeletePage(contentPage.id)}
                className="text-xs text-phishing hover:underline shrink-0"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ContentPageList;
