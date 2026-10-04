import { initApi } from "../utils/init_api.js";
export class AuthServices {
    async loginServices(email, password) {
        let endpoint = "/api/v1/auth/login";
        let params = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email,
                password
            })
        };
        let data = await initApi(endpoint, params);
        return data;
    }
}

export let authServices = new AuthServices();