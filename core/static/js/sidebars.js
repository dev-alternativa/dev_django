
/* Armazena o estado da sidebar no localstorage do navegador */
/* Inicializa com a barra expandida */
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector("#sidebar");
    let  sidebarState = localStorage.getItem("sidebarState");

    if (!sidebarState) {
        sidebarState = "expanded";
        localStorage.setItem("sidebarState", "expanded");
    }

     // Define a classe da barra lateral com base no valor do localStorage
    if (sidebarState === "collapsed") {
        sidebar.classList.add("collapsed");
    }
    // localStorage.setItem("sidebarState", "expanded");    
});
    
/* Manipula o localstorage para manter o estado da barra, oculta / aparecendo */
const toggler = document.querySelector(".btn");
toggler.addEventListener("click",function(){
    const sidebar = document.querySelector("#sidebar");
    sidebar.classList.toggle("collapsed");

    // Salva o estado do sidebar no localStorage
    if (sidebar.classList.contains("collapsed")){
        localStorage.setItem("sidebarState", "collapsed");
    }else{
        localStorage.setItem("sidebarState", "expanded");
    }
});




/* Função para permitir manter o estado de expansed/collapsed nos menus da barra lateral */
$(document).ready( () => {

  // Função para salvar o estado de expansão no localStorage
  function saveState(id, isExpanded) {
    localStorage.setItem(id + "Expanded", isExpanded);
}

// Restaurar o estado de expansão para cada um dos itens do menu ao carregar a página
$('a.sidebar-link[data-menu]').each(function() {
    var targetId = $(this).data('menu');
    var savedState = localStorage.getItem(targetId + "Expanded");
    var targetElement = $("#" + targetId);

    if (savedState === "true") {
        targetElement.addClass("show");
        $(this).removeClass("collapsed");
        $(this).attr("aria-expanded", "true");
    } else {
        targetElement.removeClass("show");
        $(this).addClass("collapsed");
        $(this).attr("aria-expanded", "false");
    }

    // Adicionar evento de clique para salvar o estado de expansão
    $(this).on("click", function() {
        var isExpanded = targetElement.hasClass("show");
        saveState(targetId, !isExpanded);
    });

    // Adicionar evento de transição (hide/show) para garantir que o estado seja salvo corretamente
    targetElement.on("shown.bs.collapse", function () {
        saveState(targetId, true);
    });

    targetElement.on("hidden.bs.collapse", function () {
        saveState(targetId, false);
    });
});

});


// $(document).ready( () => {
//     let cadastroLink = $("#cadastrosLink");
//     let cadastros = $("#cadastros");

//     // Salva o estado de expansão no localStorage
//     const saveStateCadastro = (isExpanded) => {
//         localStorage.setItem("cadastroExpanded", isExpanded);
//     };

//     // restaura o estado de expansão ao carregar a página
//     let saveState = localStorage.getItem("cadastroExpanded");
//     if (saveState === "true") {
//         cadastros.addClass("show");
//         cadastroLink.removeClass("collapsed");
//         cadastroLink.attr("aria-expansed", "true");
//     }else{
//         cadastros.removeClass("show");
//         cadastroLink.addClass("collapsed");
//         cadastroLink.attr("aria-expansed", "false");
//     }

//     // adiciona evento de clique para salvar o estado de expansão
//     cadastroLink.on("click", () => {
//         let isExpanded = cadastros.hasClass("show");
//         saveStateCadastro(!isExpanded);
//     });

//     // adiciona evento de transição para garantir que o estado seja salvo corretamente
//     cadastros.on("show.bs.collapse", () => {
//         saveStateCadastro(true);
//     });

//     cadastros.on("hidden.bs.collapse", () => {
//         saveStateCadastro(false);
//     });
// });