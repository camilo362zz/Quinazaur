from flask import Flask, render_template
from __init__ import BD_CONFIG
from bd_postgres import bd_postgres
db=bd_postgres(**BD_CONFIG)

app=Flask(__name__,template_folder="../templates", static_folder="../static")
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/productos")
def productos():
    productos=db.select_productos()
    cant_prod=db.cant_productos()
    return render_template("productos.html",productos=productos, cantidad=cant_prod)

@app.route("/recetas")
def recetas():
    recetas=db.select_recetas()
    return render_template("recetas.html",recetas=recetas)

if __name__=="__main__":
    app.run()