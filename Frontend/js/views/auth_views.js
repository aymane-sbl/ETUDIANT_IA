import { authServices } from "../services/auth_services.js";
import { checkRegex, showHiddePassword } from "../utils/auth_utils.js";
import { showSweetalert } from "../utils/sweetalert.js";

export async function loginViews() {
    // form
    let emailInput = document.getElementById("email");
    let passwordInput = document.getElementById("password");
    let passwordIcon = document.getElementById("password_icon");
    let btnIcon = document.querySelector(".btn-icon");

    // show hide password
    passwordIcon.addEventListener("click", (e) => {
        e.preventDefault();
        showHiddePassword(passwordInput, btnIcon)
    });


    // check email passwords 
    let invalidEmail = document.querySelector(".invalid-email");
    emailInput.addEventListener("blur", (e) => {
        if (!checkRegex(emailInput.value, /^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            invalidEmail.style.display = "block";
        }else {
            invalidEmail.style.display = "none";
        }
        
    })

    let invalidPassword = document.querySelector(".invalid-password");
    passwordInput.addEventListener("input", (e) => {
      if (!checkRegex(passwordInput.value, /^.{8,}$/)) {
        invalidPassword.style.display = "block";
      } else {
        invalidPassword.style.display = "none";
      }
    });
    
    // send form data to the server
    let form = document.getElementById("auth_form");
    form.addEventListener("submit",async (e) => {
        e.preventDefault();
        try {
            let response = await authServices.loginServices(emailInput.value, passwordInput.value);
            // showSweetalert(response["message"], "success");
            if (response["role"] === "admin") {
                window.location.replace("/pages/admin/materials.html");
            } else {
                window.location.replace("/")
            }
            window.localStorage.setItem("access_token", response["access_token"]);
            window.localStorage.setItem("token_type", response["token_type"]);

    } catch (error) {
            showSweetalert(error.message, "error");
            
    }
    })
}