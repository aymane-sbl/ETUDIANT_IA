export async function initApi(endpoint, params = {"Method": "GET","cache": 'no-store',}) {
    let loader = document.getElementById("loader");
    loader.style.display = "block";
    try {
      const subdomaine = "https://api--etudiant-ia--4rb7wvfyhphp.code.run/";
      // const subdomaine = "http://127.0.0.1:8000";

      let response = await fetch(`${subdomaine}${endpoint}`, params);

      if (!response.ok) {
        let error = await response.json();
        let errorMessage = new Error(
          error["detail"] ??
            "Une erreur s'est produite lors de la requête API.",
        );
        errorMessage.status = response.status;
        throw errorMessage;
      }
      let data = await response.json();
      return data;
    } finally { 
        loader.style.display = "none";
    }
} 