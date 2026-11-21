import { useState } from "react";

import FormField from "../form/FormField";
import SelectField from "../form/SelectField";
import { SEARCHABLE_LISTS, LABEL_FILTER_OPTIONS, SORT_OPTIONS } from "../../config/dropdownOptions";

// Forma e filtrave ne krye te faqes Search.
// Mban vete vlerat e fushave; kur shtypet "Search" thote onSearch(listName, filters).
function SearchForm({ onSearch, onListChange, isSearching }) {
  const [listName, setListName] = useState("scans");
  const [searchText, setSearchText] = useState("");
  const [label, setLabel] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [sortOrder, setSortOrder] = useState("newest");

  // Filtri "Label" ka kuptim vetem per listen e skanimeve
  const canFilterByLabel = listName === "scans";

  const handleListChange = (newListName) => {
    setListName(newListName);
    onListChange(); // rezultatet e vjetra i perkasin listes tjeter, prandaj fshihen
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Backend-it i dergohen vetem filtrat e plotesuar
    const filters = { newest_first: sortOrder === "newest" };
    if (searchText) filters.search_text = searchText;
    if (label && canFilterByLabel) filters.label = label;
    if (dateFrom) filters.date_from = dateFrom;
    if (dateTo) filters.date_to = dateTo;

    onSearch(listName, filters);
  };

  return (
    <form onSubmit={handleSubmit} className="card mb-6">
      {/* Rreshti i pare: ku te kerkohet dhe cfare teksti */}
      <div className="grid sm:grid-cols-3 gap-4 mb-4">
        <SelectField
          label="Search in"
          value={listName}
          onChange={handleListChange}
          options={SEARCHABLE_LISTS}
        />
        <FormField label="Text query" className="sm:col-span-2">
          <input
            value={searchText}
            onChange={(event) => setSearchText(event.target.value)}
            placeholder="Search text..."
            className="input-field"
          />
        </FormField>
      </div>

      {/* Rreshti i dyte: etiketa, datat dhe renditja */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        {canFilterByLabel && (
          <SelectField label="Label" value={label} onChange={setLabel} options={LABEL_FILTER_OPTIONS} />
        )}
        <FormField label="From date">
          <input
            type="date"
            value={dateFrom}
            onChange={(event) => setDateFrom(event.target.value)}
            className="input-field"
          />
        </FormField>
        <FormField label="To date">
          <input
            type="date"
            value={dateTo}
            onChange={(event) => setDateTo(event.target.value)}
            className="input-field"
          />
        </FormField>
        <SelectField label="Sort" value={sortOrder} onChange={setSortOrder} options={SORT_OPTIONS} />
      </div>

      <button type="submit" disabled={isSearching} className="btn-primary px-6">
        {isSearching ? "Searching..." : "Search"}
      </button>
    </form>
  );
}

export default SearchForm;
