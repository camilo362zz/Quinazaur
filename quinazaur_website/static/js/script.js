console.log("Conected to JS")
function AbrirModal(){
    document.getElementById("modal_card").style.display="flex";
    document.getElementById("md-c").style.animation="slidey 0.25s ease";
    
    document.body.style.overflow="hidden";
}

function CerrarModal(){
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))
    
    document.getElementById("md-c").style.animation="hidey 0.25s ease";
    setTimeout(() => {
    document.getElementById("modal_card").style.display="none";
    }, 200);
    
    document.body.style.overflow="auto";
}

document.querySelectorAll(".btn_vermas").forEach(boton => {
    boton.addEventListener('click',function(){
        const nombre= this.dataset.nombre;
        const descripcion= this.dataset.descripcion;
        const precio= this.dataset.precio
        const img= this.dataset.img;
        const atributos =JSON.parse(this.dataset.atributos);
        const saludo = "\u{1F44B}";
        const sonrisa = "\u{1F60A}";
        const mensaje = `Hola ${saludo}

Estoy interesado(a) en recibir más información sobre la *${nombre}*.

Me gustaría conocer detalles como presentación, precio, beneficios nutricionales y disponibilidad.

Quedo atento(a) a tu amable respuesta. Muchas gracias ${sonrisa}`
;
        console.log(mensaje)
    
        document.getElementById("img-producto").src=img;
        document.getElementById("nombre-producto").textContent=nombre;
        document.getElementById("descripcion-producto").textContent=descripcion;
        document.getElementById("btn-comprar").href="https://wa.me/573167821523?text="+encodeURIComponent(mensaje)
        

        const contenedor= document.getElementById("cont-atributos");
        contenedor.innerHTML = ""; // limpiar antes
        atributos.forEach(tag => {
            const h3 = document.createElement("h3");
            h3.textContent = tag;
            contenedor.appendChild(h3);
            });
        document.getElementById("precio-producto").textContent=" $" + Number(precio).toLocaleString("es-CO", {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
            });
        AbrirModal();
    })
});

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