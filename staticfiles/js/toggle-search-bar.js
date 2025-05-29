import clearSearchHandler from './clear-search-handler.js';

export default function toggleSearchBar() {
    // Toggle the visibility of the search bar when the reveal button is clicked
    // This function is used to show or hide the search bar in the text search form
    // when the user clicks on the "reveal" button.
    const revealBtn = document.getElementById('text-search-reveal');
    const searchBar = document.getElementById('search-location');
    searchBar.classList.toggle('hidden');
    revealBtn.classList.toggle('button-active');
    // Clear the search input and reset the search icon
    clearSearchHandler();
}