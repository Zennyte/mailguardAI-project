import { useState } from "react";

import { searchList } from "../api/searchApi";
import { getErrorMessage } from "../api/apiClient";
import SearchForm from "../components/search/SearchForm";
import SearchResultsTable from "../components/search/SearchResultsTable";

// Faqja Search (/search) - forma e filtrave lart, tabela e rezultateve poshte
function SearchPage() {
  // null = ende nuk eshte bere asnje kerkim; [] = kerkimi nuk gjeti asgje
  const [resultRows, setResultRows] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (listName, filters) => {
    setErrorMessage("");
    setIsSearching(true);
    try {
      const searchResponse = await searchList(listName, filters);
      setResultRows(searchResponse.rows);
    } catch (error) {
      setErrorMessage(getErrorMessage(error, "Search failed."));
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div>
      <h1 className="page-title">Advanced Search</h1>

      {errorMessage && <p className="alert-error mb-4">{errorMessage}</p>}

      <SearchForm
        onSearch={handleSearch}
        onListChange={() => setResultRows(null)}
        isSearching={isSearching}
      />

      {resultRows !== null && <SearchResultsTable rows={resultRows} />}
    </div>
  );
}

export default SearchPage;
