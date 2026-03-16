from flask import Flask, render_template, request, redirect, url_for, session
from bd_postgres import bd_postgres
import os
from dotenv import load_dotenv
from Datos import *
from Errors import *

# VARIABLES DE ENTORNO
load_dotenv()
h=os.getenv('HOST')
p=os.getenv('PORT')
d=os.getenv('DATABASE')
u=os.getenv('USER_DB')
pw=os.getenv('PASSWORD_DB')
key=os.getenv('SECRET_KEY')

# FUNCION PARA NO GUARDAR CACHE 
from functools import wraps
from flask import make_response

def no_cache(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return wrapped
#==============================================================================================


# APP PRINCIPAL
app=Flask(__name__,template_folder="../templates", static_folder="../static")

app.config["SECRET_KEY"]=key
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True

# PAGINA INICIO
@app.route("/")
def inicio():
    return render_template("index.html")


# PAGINA PRODUCTOS
@app.route("/productos")
def productos():
    db=bd_postgres(h,p,d,u,pw)
    productos=db.select_productos()
    cant_prod=db.cant_productos()
    db.disconnect()
    return render_template("productos.html",productos=productos, cantidad=cant_prod)


# PAGINA RECETAS
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


# PAGINA COMPROMISO VERDE
@app.route("/compromiso-verde")
def compromiso_verde():
    buscar=request.args.get("buscar")
    section=request.args.get("section")

    # PRESENTACION
    if not section:
        section="presentacion" 
        return render_template("compromiso_verde.html",section=section)
    
    # NOTICIAS
    if section=="noticias":
        if not buscar:
            db=bd_postgres(h,p,d,u,pw)
            noticias=db.get_noticias()
            db.disconnect()
            return render_template("compromiso_verde.html",section=section, noticias=noticias)
        else:
            db=bd_postgres(h,p,d,u,pw)
            noticias=db.buscar_noticia(buscar)
            db.disconnect()
            return render_template("compromiso_verde.html",section=section, noticias=noticias)     
    
    # GALERIA
    if section=="galeria":
        db=bd_postgres(h,p,d,u,pw)
        imgs=db.get_galeria()
        db.disconnect()
        return render_template("compromiso_verde.html",section=section, img=imgs) 


# PAGINA REGISTRO
@app.route("/registro", methods=["GET","POST"])
@no_cache
def registro():
    # VERIFICA QUE ESTE HAYA SESION ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))
    
    else:
        # RECIBE DATOS    
        error=request.args.get("error")
        if request.method=="POST":
            nombre=request.form["nombre"]
            correo=request.form["correo"]
            telefono=request.form["telefono"]
            contraseña=request.form["contraseña"]

            # INTENTA AGREGAR
            try:
                user=Usuario(nombre,correo,telefono,contraseña)
                db=bd_postgres(h,p,d,u,pw)
                db.agregar_usuario(user.get_nombre(),user.get_email(),user.get_telefono(),user.get_password())
                db.disconnect()
                db=bd_postgres(h,p,d,u,pw)
                user_id=db.obtener_id(user.get_email())
                db.disconnect()
                session.clear()
                session["user_id"]=user_id
                return redirect(url_for("inicio"))
            # MANDA ERROR
            except (ErrorRegistro, ErrorLogin) as ex: 
                return redirect(url_for('registro',error=str(ex)))
        # MUESTRA ERROR
        if error:
            return render_template("registro.html",error=error)
        
        return  render_template("registro.html")


# PAGINA LOGIN
@app.route("/login", methods=["GET","POST"])
@no_cache
def login():
    # VERIFICA QUE ESTE HAYA SESION ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))
    
    else:    
        error=request.args.get("error")
        if request.method=="POST":
            # RECIBE DATOS
            email=request.form["correo"]
            password=request.form["contraseña"]
            # INTENTA LOGIN
            try:
                login=Login(email,password)
                db=bd_postgres(h,p,d,u,pw)
                valido=db.validar_login(login.get_email(),login.get_password())
                db.disconnect()
                if valido:
                    db=bd_postgres(h,p,d,u,pw)
                    user_id=db.obtener_id(email)
                    db.disconnect()
                    session.clear()
                    session["user_id"]=user_id
                    return redirect(url_for("inicio"))
            # MANDA ERRROR    
            except (ErrorRegistro, ErrorLogin) as ex:
                return redirect(url_for('login',error=str(ex)))
        # MUESTRA ERRROR
        if error:
            return render_template("login.html", error=error)
        return  render_template("login.html")    
        

# PAGINA PERFIL
@app.route("/perfil")
def perfil():
    # VERIFICA SESION
    if not "user_id" in session:
        return redirect(url_for("login"))
    # OBTIENE DATOS Y LOS MANDA
    db=bd_postgres(h,p,d,u,pw)
    user=db.get_perfil(session["user_id"])
    db.disconnect()
    return render_template("perfil.html", user=user)


# PAGINA EDITAR PERFIL
@app.route("/editar-perfil",methods=["POST","GET"])
@no_cache
def editar_perfil():
    # VERIFICA SESION
    if not "user_id" in session:
        return redirect(url_for("login"))
    
    # OBTIENE ID USUARIO
    db=bd_postgres(h,p,d,u,pw)
    user=db.get_perfil(session["user_id"])
    db.disconnect()
    error=request.args.get("error")

    if request.method=="POST":
        # RECIBE DATOS DEL FORMULARIO
        nombre=request.form["nombre"]
        telefono_actual=user[0]["telefono"]
        telefono_nuevo=request.form["telefono"]
        actual=request.form["p_actual"]
        nueva=request.form["p_nueva"]
        try:
            #INTENTA ACTUALIZAR DATOS
            datos=Modificar(nombre,telefono_nuevo,actual,nueva)
            db=bd_postgres(h,p,d,u,pw)
            tel_valido=True

            # VERIFICA QUE EL TELEFONO Y PASSWORD SEAN VALIDOS
            if telefono_actual!=telefono_nuevo: # VERIFICA SI EL TELEFONO QUE VA A AGREGAR ES EL MISMO
                tel_valido=db.validar_telefono(telefono_nuevo) # SI ES NUEVO VALIDA QUE NO SE REPITA EN LA DB
            password_valido=db.validar_password(session["user_id"],actual) #VALIDA PASSWORD PARA GUARDAR CAMBIOS
            
            if password_valido and tel_valido:
                db.actualizar_user(session["user_id"],datos.get_nombre(),datos.get_telefono()) # ACTUALIZA DATOS
                # VERIFICA SI SE VA A ACTUALIZAR PASSWORD
                if nueva!="":
                    db.actualizar_password(session["user_id"],datos.get_password_nueva())
                    db.disconnect() 
                    return redirect(url_for("logout"))
                db.disconnect() 
                return redirect(url_for("perfil"))
            db.disconnect() 
        except (ErrorLogin, ErrorRegistro) as ex:
            # MANDA ERRROR
            return redirect(url_for('editar_perfil', error=str(ex)))

    # MUESTRA ERRROR
    if error:
        return render_template("editar_perfil.html",error=error)
    return render_template("editar_perfil.html", user=user)


# CERRAR SESION
@app.route("/logout")
def logout():
    if "user_id" in session:
        session.clear()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("inicio")) 


# EJECUTA APP
if __name__=="__main__":
    app.run(debug=True)