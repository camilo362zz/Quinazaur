console.log("Conectado a script.js")

// MENU PARA MOVIL

const menu = document.querySelector(".links");
const btnAbrirMenu = document.querySelector(".abrir-menu");
const btnCerrarMenu = document.querySelector(".cerrar-menu");


function Mostrar_menu(){
    document.querySelectorAll(".section").forEach(link=>{
        link.classList.add("section-movil");
    });
    menu.classList.add("links-movil");
    btnCerrarMenu.classList.add("active");
    document.body.style.overflow='hidden';
}

function Cerrar_menu(){
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))
    menu.classList.add("links-cerrar")
    setTimeout(() => {
    document.querySelectorAll(".section").forEach(section=>{
        section.classList.remove("section-movil");
    }
    );
    menu.classList.remove("links-movil");
    btnCerrarMenu.classList.remove("active");
    document.body.style.overflow='auto';
    menu.classList.remove("links-cerrar")
    }, 190);
    
}

document.querySelectorAll(".abrir-menu").forEach(abrir=>{
    abrir.addEventListener('click',function(){
        Mostrar_menu();
    })
})

document.querySelectorAll(".cerrar-menu").forEach(cerrar=>{
    cerrar.addEventListener('click',function(){
        Cerrar_menu();
    })
})


document.addEventListener("click", function(event){
    if (!menu.contains(event.target) && !btnAbrirMenu.contains(event.target) && menu.classList.contains("links-movil"))  {
        Cerrar_menu();
    }
});
//=================================================





