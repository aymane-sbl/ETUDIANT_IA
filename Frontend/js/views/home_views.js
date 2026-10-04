import { getCards } from "../component/card.js";
import { search, showHiddenSearchInput, showHideMenu } from "../component/header.js";
import { homeServices } from "../services/home_services.js";



export async function homeViews() {
  // cards section
  let cards = document.querySelector(".cards");
  // header
  // menu
  showHideMenu();

  // search
   showHiddenSearchInput();
  search(cards,  homeServices.search, getCards);
  
  // administration button
  let adminBtn = document.getElementById("admin-btn");
  adminBtn.addEventListener("click", (e) => {
    e.preventDefault();
    let accessToken = localStorage.getItem("access_token");

    if (accessToken) {
      window.location.href = "/pages/admin/materials.html";
    } else {
      window.location.href = "/pages/auth/login.html";
    }
  });

  // main content 

  // filter
  let filterForm = document.getElementById("filter-form");
  let typeSelect = document.getElementById("type-select");
  let semesterSelect = document.getElementById("semester-select");
  
  filterForm.addEventListener("submit", async (e) => { 
    try {
          e.preventDefault();
          // value of the select elements
          cards.innerHTML = "";

          let type = typeSelect.value;
          let semester = semesterSelect.value;

          let response = await homeServices.filter(type, semester);
          let data = response["data"];
          getCards(data, cards);
    } catch (error) {

      cards.innerHTML = "";
      cards.innerHTML = `<p id = "error-message">${error.message}</p>`;
    }
  })
  

  // create cards
  
  let query = new URLSearchParams(window.location.search);
  let page = query.get("page") ?? 1;
    try {
        
      cards.innerHTML = "";
        let response = await homeServices.home(page);
        let data = response["data"];
        getCards(data, cards);
      
    } catch (error) { 
      cards.innerHTML = "";
      cards.innerHTML = `<p id = "error-message">${error.message}</p>`;
      
    }
  
    // footer 
  let nextBtn = document.getElementById("next-btn");
  let prevBtn = document.getElementById("prev-btn");

  nextBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    let response = await homeServices.home(page);
    if (page >= response["pagination"]["total_pages"]) {
      return;
    }
    page++;
    window.location.href = `?page=${page}`;
  });

  prevBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (page <= 1) {
      return;
    }

    page--;
    window.location.href = `?page=${page}`;
  });

}






