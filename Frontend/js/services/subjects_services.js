class SubjectsServices { 
    async  getSubjects() { 
        let endpoint = "/api/v1/admin/subjects/";
        let data = await initApi(endpoint);
        return data;
    }
}

export let subjectsServices = new SubjectsServices();