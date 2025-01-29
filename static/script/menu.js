function toggleDropdown(menuId) {
    // Fecha todos os dropdowns antes de abrir o atual
    document.querySelectorAll('.dropdown-content').forEach(menu => {
        if (menu.id !== menuId) {
            menu.classList.remove("show");
        }
    });

    // Abre ou fecha o dropdown clicado
    document.getElementById(menuId).classList.toggle("show");
}

// Fechar dropdowns ao clicar fora
document.addEventListener("click", function(event) {
    if (!event.target.closest(".dropdown")) {
        document.querySelectorAll('.dropdown-content').forEach(menu => {
            menu.classList.remove("show");
        });
    }
});