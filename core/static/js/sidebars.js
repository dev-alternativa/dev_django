
/* Oculta / Mostra Menu lateral */
// const toggler = document.querySelector(".btn");
// toggler.addEventListener("click",function(){
    //     document.querySelector("#sidebar").classList.toggle("collapsed");
    // });
    
    
    
/* Oculta / Mostra Menu lateral */
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