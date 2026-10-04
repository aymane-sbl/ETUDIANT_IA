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