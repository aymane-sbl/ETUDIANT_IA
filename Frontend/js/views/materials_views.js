import { createCardAdmin } from "../component/card.js";
import { search, showHiddenSearchInput, showHideMenu } from "../component/header.js";
import { homeServices } from "../services/home_services.js";
import { materialsServices } from "../services/materials_services.js";
import { subjectsServices } from "../services/subjects_services.js";
import { showSweetalert, showSweetalertConfirmed } from "../utils/sweetalert.js";

export async function materialsViews() { 

    // header
    // Menu
    showHideMenu();

    

    // main content

    // subjects selects
    let subjectsSelect = document.getElementById("subjects_select");
    subjectsSelect.addEventListener("focus",async (e) => {
        try {
            let response = await subjectsServices.getSubjects();
            let data = response["data"];
            subjectsSelect.innerHTML = "";
            data.forEach(element => {
                subjectsSelect.innerHTML += ` <option value="${element["id"]}">${element["subject_name"]}</option>`;
            });
        } catch (error) {
            console.error(error)
        }
    })
    // form
    let form = document.getElementById("add-materials-form");
    
    form.addEventListener("submit", async (e) => {
        try {
            e.preventDefault();
            let formData = new FormData(form);
            let data = await materialsServices.addMaterial(formData);
            await showSweetalert(data["message"], "success");

        } catch (error) { 
            let result = await showSweetalertConfirmed(error["message"], "error");
            if (result && error["status"] === 401) {
              window.location.replace("/pages/auth/login.html");
            }
            return;
        }
    });

    // materials list
    let adminCards = document.querySelector(".admin-cards");
    
    try {
        let response = await homeServices.home();
        let materials = response["data"];
        
        materials.forEach((element) => {
            let card = document.createElement("section");
            card.className = "admin-card";

            let adminCardsForm = document.createElement("form");
            adminCardsForm.className = "admin-cards-form";
            card.appendChild(adminCardsForm);
            adminCardsForm.innerHTML += createCardAdmin(element);
            
            adminCards.appendChild(card);

            adminCardsForm.addEventListener("submit", async (e) => {
              e.preventDefault();
              try {
                  let response =await materialsServices.deleteMaterial(element.id);
                  await showSweetalert(response["message"], "success");
                  window.location.reload();
              } catch (error) {
                  await showSweetalert(error.message, "error");
              }
            });
        });
        
    } catch (error) {
        await showSweetalert(error.message,"error")
    }

}