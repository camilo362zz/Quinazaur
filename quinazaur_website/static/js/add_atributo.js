
console.log("Conectado a add_atributo.js")


const inpu = document.querySelector("input[type='file']");

inpu.addEventListener("change", () => {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const maxFiles = 1;


    for (let file of inpu.files) {
        if (file.size > maxSize) {
            alert("Archivo demasiado grande");
            inpu.value = "";
        }else{
            if (inpu.files.length > maxFiles) {
                alert("Máximo 1 archivo");
                inpu.value = "";
            }else{
                alert("Archivo Subido")
            }
            
        }
    }

    
});


// ===============================================================================

const btn = document.getElementById("btn-cambio");
const cont = document.getElementById("cont-estado")
const texto = cont.querySelector("p");
const disponible = document.getElementById("disponible");

btn.addEventListener("click", function(){
    btn.classList.toggle("estado-activo");
    btn.classList.toggle("estado-inactivo");
    texto.classList.toggle("dis");
    texto.classList.toggle("no-dis");


    if (btn.classList.contains("estado-activo")) {
        texto.textContent = "Disponible";
        
    } else {
        texto.textContent = "No disponible";
        
    };

    if(disponible.value == 1){
        disponible.value = 0;
    }else{
        disponible.value = 1;
    }
});

// ====================================================================================

const input = document.getElementById("atributo-input");
const contenedor = document.getElementById("container-atributos");
const hidden = document.getElementById("atributos-hidden");

const maxTags = 5;

let tags = hidden.value ? hidden.value.split(",") : [];

input.addEventListener("keydown", function(e) {
    const cantTags = tags.length

    if (e.key === "Enter" || e.key === ",") {
        e.preventDefault();

        if (cantTags < maxTags){
            let valor = input.value.trim();

            if (valor !== "") {
                tags.push(valor);
                crearTag(valor);
                actualizarHidden();
            }
        }
        

        input.value = "";
    }
});

document.querySelectorAll(".atributo").forEach(atributo => {
    atributo.querySelectorAll(".eliminar-atributo").forEach(boton => {
        boton.onclick = () => {
        let texto = atributo.firstChild.textContent.trim();

        tags = tags.filter(t => t !== texto);
        atributo.remove();
        actualizarHidden();
    };
    });   
});

function crearTag(texto) {
    const tag = document.createElement("span");
    tag.textContent = texto;
    tag.classList.add("atributo")

    const boton = document.createElement("button");
    boton.textContent = "x";
    boton.classList.add("eliminar-atributo")

    boton.onclick = () => {
        tags = tags.filter(t => t !== texto);
        tag.remove();
        actualizarHidden();
    };

    tag.appendChild(boton);
    contenedor.appendChild(tag);
}

function actualizarHidden() {
    hidden.value = tags.join(",");
}





