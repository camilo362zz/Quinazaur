console.log("Conectado a script.js")

// MENU PARA MOVIL

function Mostrar_menu(){
    document.querySelectorAll(".section").forEach(link=>{
        link.classList.add("section-movil");
    });
    document.querySelector(".links").classList.add("links-movil");
    document.querySelector(".cerrar-menu").classList.add("active");
    document.body.style.overflow='hidden';
}

function Cerrar_menu(){
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))
    document.querySelector(".links").classList.add("links-cerrar")
    setTimeout(() => {
    document.querySelectorAll(".section").forEach(section=>{
        section.classList.remove("section-movil");
    }
    );
    document.querySelector(".links").classList.remove("links-movil");
    document.querySelector(".cerrar-menu").classList.remove("active");
    document.body.style.overflow='auto';
    document.querySelector(".links").classList.remove("links-cerrar")
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

const menu = document.querySelector(".links");
const boton = document.querySelector(".abrir-menu");

document.addEventListener("click", function(event){

    if (!menu.contains(event.target) && !boton.contains(event.target) && menu.classList.contains("links-movil"))  {
        Cerrar_menu();
    }
});
//=================================================





