
/* Oculta / Mostra Menu lateral */
// const toggler = document.querySelector(".btn");
// toggler.addEventListener("click",function(){
    //     document.querySelector("#sidebar").classList.toggle("collapsed");
    // });
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector("#sidebar");
    let  sidebarState = localStorage.getItem("sidebarState");
    console.log(sidebarState);

    if (!sidebarState) {
        sidebarState = "expanded";
        localStorage.setItem("sidebarState", "expanded");
    }

     // Define a classe da barra lateral com base no valor do localStorage
    if (sidebarState === "collapsed") {
        sidebar.classList.add("collapsed");
    }
    // localStorage.setItem("sidebarState", "expanded");    
    // console.log(localStorage);
});
    
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

// document.addEventListener("DOMContentLoaded", () => {
//     const sidebar = document.querySelector("#sidebar");


// });
