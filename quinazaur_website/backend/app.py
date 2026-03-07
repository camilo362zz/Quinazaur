from flask import Flask, render_template, request
from bd_postgres import bd_postgres
import os
from dotenv import load_dotenv

load_dotenv()
h=os.getenv('HOST')
p=os.getenv('PORT')
d=os.getenv('DATABASE')
u=os.getenv('USER_DB')
pw=os.getenv('PASSWORD_DB')


app=Flask(__name__,template_folder="../templates", static_folder="../static")
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/productos")
def productos():
    db=bd_postgres(h,p,d,u,pw)
    productos=db.select_productos()
    cant_prod=db.cant_productos()
    db.disconnect()
    return render_template("productos.html",productos=productos, cantidad=cant_prod)

@app.route("/recetas")
def recetas():
    search=request.args.get("search")
    db=bd_postgres(h,p,d,u,pw)
    if search:
        recetas=db.buscar_receta(search)
        db.disconnect()
    else:
        recetas=db.select_recetas()
        db.disconnect()
    return render_template("recetas.html",recetas=recetas)

if __name__=="__main__":
    app.run(debug=True)