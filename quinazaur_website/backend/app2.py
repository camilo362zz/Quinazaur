from flask import Flask, render_template, request, redirect, url_for, session

app=Flask(__name__,template_folder="../templates", static_folder="../static")

@app.route("/")
def inicio():
    return render_template("edicion/editar_producto.html")


if __name__=="__main__":
    app.run(debug=True)