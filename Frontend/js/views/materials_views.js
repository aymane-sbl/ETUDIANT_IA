import { showHideMenu } from "../component/header.js";
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
            adminCardsForm.innerHTML += ` 
                        <div class="card-header" title="${element.subject_name}">
                             <h3>${element.subject_name}</h3>
                        </div>

                        <div class="card-content">
                            <p>type : ${element.type}</p>
                            <p>année : ${element.year_academic}</p>
                            <p>semestre : ${element.semester}</p>
                            <p>session : ${element.session}</p>
                        </div>

                        <div class="utils">
                            <button type="submit" id = "delete-btn"><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#EA3323"><path d="m376-300 104-104 104 104 56-56-104-104 104-104-56-56-104 104-104-104-56 56 104 104-104 104 56 56Zm-96 180q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520Zm-400 0v520-520Z"/></svg> </button>
                        </div>`;
            
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