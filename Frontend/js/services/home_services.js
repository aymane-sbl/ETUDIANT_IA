import { initApi } from "../utils/init_api.js";

class HomeServices {

    async  home(page = 1) { 
        let endpoint = `/api/v1/materials/?page=${page}&limit=20`;
        let params = {
            "method": 'GET',
            "cache": 'no-store',
            "headers" : {"Content-Type": "application/json"}
        }
        let data = await initApi(endpoint, params);
        return data;
    }

    async  search(title) {
        let endpoint = `/api/v1/materials/search?subject_name=${title}`;
        let data = await initApi(endpoint);
        return data;
    }

    async  filter(type, semester) { 
        let endpoint = `/api/v1/materials/filter?type=${type}&semester=${semester}`;
        let data = await initApi(endpoint);
        return data;
    }
}

export let homeServices = new HomeServices();