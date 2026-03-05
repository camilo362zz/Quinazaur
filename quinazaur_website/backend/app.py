from flask import Flask, render_template
from __init__ import BD_CONFIG
from bd_postgres import bd_postgres


app=Flask(__name__,template_folder="../templates", static_folder="../static")
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/productos")
def productos():
    db=bd_postgres(**BD_CONFIG)
    productos=db.select_productos()
    cant_prod=db.cant_productos()
    db.disconnect()
    return render_template("productos.html",productos=productos, cantidad=cant_prod)

@app.route("/recetas")
def recetas():
    db=bd_postgres(**BD_CONFIG)
    recetas=db.select_recetas()
    db.disconnect()
    return render_template("recetas.html",recetas=recetas)

if __name__=="__main__":
    app.run()