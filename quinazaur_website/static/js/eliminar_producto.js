console.log("Conectado a script.js")

// BOTON DE ELIMINAR PRODUCTO

document.querySelectorAll(".drop-button").forEach(boton => {
    boton.addEventListener("click", function(){
        const confirmacion = document.getElementById("confirmacion");
        const mensaje = document.querySelector(".mensaje");
        const id = this.dataset.id
        const cancelar = document.getElementById("cancelar")
        mensaje.action = `/delete-product/${id}`;
        confirmacion.style.display = "flex";
        mensaje.style.animation = "slidey 0.25s ease";
        document.body.style.overflow="hidden";

        cancelar.addEventListener("click",function(){
            document.body.style.overflow="auto";
            mensaje.style.animation="hidey 0.25s ease";
            setTimeout(() => {
                confirmacion.style.display="none";
            }, 200);
            
        })
    })
});
    