
console.log("Conectado")

const usuarios = document.querySelector(".usuarios");
const productos = document.querySelector(".productos");
const recetas = document.querySelector(".recetas");
const btn_usuarios = document.getElementById("usuarios");
const btn_productos = document.getElementById("productos");
const btn_recetas = document.getElementById("recetas");

function MostrarUsuarios(){
    btn_usuarios.classList.add("activo")
    btn_productos.classList.remove("activo")
    btn_recetas.classList.remove("activo")

    usuarios.classList.add("mostrar")
    productos.classList.remove("mostrar")
    recetas.classList.remove("mostrar")
}

function MostrarProductos(){
    btn_productos.classList.add("activo")
    btn_usuarios.classList.remove("activo")
    btn_recetas.classList.remove("activo")

    productos.classList.add("mostrar")
    usuarios.classList.remove("mostrar")
    recetas.classList.remove("mostrar")
}

function MostrarRecetas(){
    btn_recetas.classList.add("activo")
    btn_productos.classList.remove("activo")
    btn_usuarios.classList.remove("activo")
    
    recetas.classList.add("mostrar")
    productos.classList.remove("mostrar")
    usuarios.classList.remove("mostrar")  

}

btn_usuarios.addEventListener("click",MostrarUsuarios)
btn_productos.addEventListener("click",MostrarProductos)
btn_recetas.addEventListener("click",MostrarRecetas)
