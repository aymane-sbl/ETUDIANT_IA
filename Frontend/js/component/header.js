export function showHideMenu() { 
        let menuBtn = document.getElementById("menu-btn");
        let logoNav = document.querySelector(".logo-nav");
        menuBtn.addEventListener("click", (e) => {
          e.preventDefault();
          logoNav.classList.toggle("hidden");
          
        });
}

export function showHiddenSearchInput() {
    let searchBtn = document.getElementById("search-btn");
    let search = document.querySelector(".search");
    searchBtn.addEventListener("click", (e) => {
      e.preventDefault();
      search.classList.toggle("hidden");
    });
}

export function search(cards, searchServices,getCards) {
  let searchInput = document.getElementById("search-input");
  let searchForm = document.getElementById("search-form");
  searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    cards.innerHTML = "";
    try {
      let response = await searchServices(searchInput.value);
      let data = response["data"];
      getCards(data, cards);
    } catch (error) {
      cards.innerHTML = "";
      cards.innerHTML = `<p id = "error-message">${error.message}</p>`;
    }
  });
}