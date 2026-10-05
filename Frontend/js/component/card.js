export function createCard(title, type, year, semester, session, fileUrl) {
    return `
              <div class="card">
                   <div class="card-header" title="${title}">
                     <h3>${title}</h3>
                   </div>
                   <div class="card-content">
                        <p >type : ${type}</p>
                        <p>année : ${year}</p>
                        <p>semestre : ${semester}</p>
                        <p>session : ${session}</p>
                   </div>
                   <a href="${fileUrl}" download target="_blank">
                        <button type="button" class="download-btn">Télécharger le fichier</button>
                   </a>
                </div>`;
}

export function getCards(data, cards) { 
    data.forEach((element) => {
      let card = createCard(
        element.subject_name,
        element.type,
        element.year_academic,
        element.semester,
        element.session === "none" ? "Cours" : element.session,
        element.file_url,
      );

      cards.innerHTML += card;
    });
}

export function createCardAdmin(element) {
  return `<div class="card-header" title="${element.subject_name}">
                             <h3>${element.subject_name}</h3>
                        </div>

                        <div class="card-content">
                            <p>type : ${element.type}</p>
                            <p>année : ${element.year_academic}</p>
                            <p>semestre : ${element.semester}</p>
                            <p>session : ${element.session === "none" ? "Cours" : element.session}</p>
                        </div>

                        <div class="utils">
                            <button type="submit" id = "delete-btn"><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#EA3323"><path d="m376-300 104-104 104 104 56-56-104-104 104-104-56-56-104 104-104-104-56 56 104 104-104 104 56 56Zm-96 180q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520Zm-400 0v520-520Z"/></svg> </button>
                        </div>`;
}