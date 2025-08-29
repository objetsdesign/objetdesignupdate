/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {
    // Sélectionne le modal par son ID
    let loginModal = document.getElementById('loginModal');

    if (loginModal) {
        loginModal.addEventListener('shown.bs.modal', function () {
            let modalContent = document.getElementById("loginModalContent");

            // Vérifie si le formulaire n'a pas déjà été chargé
            if (!modalContent.dataset.loaded) {
                fetch("/web/login")
                    .then(response => response.text())
                    .then(html => {
                        let tempDiv = document.createElement("div");
                        tempDiv.innerHTML = html;
                        let form = tempDiv.querySelector(".o_login_form");

                        if (form) {
                            modalContent.innerHTML = "";
                            modalContent.appendChild(form);
                            modalContent.dataset.loaded = "true"; // Empêche le rechargement multiple
                        } else {
                            modalContent.innerHTML = "<p class='text-danger text-center'>Erreur de chargement du formulaire.</p>";
                        }
                    })
                    .catch(error => {
                        console.error("Erreur lors du chargement du formulaire :", error);
                        modalContent.innerHTML = "<p class='text-danger text-center'>Erreur de connexion au serveur.</p>";
                    });
            }
        });

        // Réinitialise le modal à la fermeture pour permettre un rechargement si besoin
        loginModal.addEventListener('hidden.bs.modal', function () {
            let modalContent = document.getElementById("loginModalContent");
            modalContent.innerHTML = "<p class='text-center text-muted'>Chargement...</p>";
            delete modalContent.dataset.loaded;
        });
    }
});
