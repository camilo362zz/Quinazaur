// EVITAR QUE LOS DATOS DE LOS FORMULARIOS SE PUEDAN RECUPERAR REGRESANDO 
window.addEventListener("pageshow", function(event) {
    if (event.persisted || performance.getEntriesByType("navigation")[0].type === "back_forward") {
        document.getElementById("formulario").reset();
    }
});

// BOTON CERRAR MENSAJE
document.getElementById("cerrar-msg").addEventListener('click',function(){
    document.getElementById("mensaje").style.display='none';
    document.body.classList.remove("inactivo");
    document.getElementById("section-registro").classList.remove("inactivo");
    document.getElementById("section-inicio-sesion").classList.remove("inactivo");
    document.getElementById("section").classList.remove("inactivo");

})
