// EVITAR QUE LOS DATOS DE LOS FORMULARIOS SE PUEDAN RECUPERAR REGRESANDO 

console.log("Conectado")

window.addEventListener("pageshow", function(event) {
    if (event.persisted || performance.getEntriesByType("navigation")[0].type === "back_forward") {
        document.getElementById("formulario").reset();
    }
});

