import { loginViews } from "./views/auth_views.js";
import { homeViews } from "./views/home_views.js";
import {materialsViews} from "./views/materials_views.js";
let roots = {
  index: async () => await homeViews(),
  materials: async () => await materialsViews(),
  login : async ()=> await loginViews()
};

let currentPage = window.location.pathname.split("/").at(-1);
currentPage = currentPage.split(".")[0];

if (currentPage === "") {
  currentPage = "index";
}

for (let root in roots) {
  if (root === currentPage) {
    roots[root]();
  }
}
