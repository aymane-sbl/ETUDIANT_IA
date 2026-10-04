import { initApi } from "../utils/init_api.js";

class MaterialsServices { 
    // add materials
    async addMaterial(formData) { 
        let endpoint = "/api/v1/admin/materials/";
        let token = window.localStorage.getItem("access_token");
        let tokenType = window.localStorage.getItem("token_type");
        let params = {
            method: "POST",
            headers: {
                
                "Authorization": `${tokenType} ${token}`,
            },
            body: formData
        }

        let data = await initApi(endpoint, params);
        return data;
    }
    // delete materials
    async deleteMaterial(materialId){
        let endpoint = `/api/v1/admin/materials/?id=${materialId}`;
        let params = {
          method: "DELETE",
        };
        let response = await initApi(endpoint, params);
        return response;
    }
}



export let materialsServices = new MaterialsServices();
