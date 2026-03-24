from flask import Flask, render_template, request, redirect, url_for, session, flash
from bd_postgres import bd_postgres
import os
from dotenv import load_dotenv
from Datos import *
from Errors import *
import secrets
from datetime import datetime, timezone,timedelta 
from werkzeug.utils import secure_filename
# VARIABLES DE ENTORNO
load_dotenv()
h=os.getenv('HOST')
p=os.getenv('PORT')
d=os.getenv('DATABASE')
u=os.getenv('USER_DB')
pw=os.getenv('PASSWORD_DB')
key=os.getenv('SECRET_KEY')
sendgridKey=os.getenv('SENDGRID_API_KEY')

# API PARA ENVIAR EMAILS DE VERIFICACION ====================================================================================
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# FUNCION PARA ENVIAR EL CODIGO DEL RESET PASSWORD
def correo_reset(email,nombre,code,min):
    html = render_template("correos/tabla_code.html", nombre=nombre, codigo=code, minutos=min)
    message = Mail(
    from_email="pruebaquinazaur@gmail.com",
    to_emails=email,
    subject='Código de recuperación',
    html_content=html)
    try:
        sg = SendGridAPIClient(sendgridKey)
        # sg.set_sendgrid_data_residency("eu")
        # uncomment the above line if you are sending mail using a regional EU subuser
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


# FUNCION PARA ENVIAR EL CODE DE VERIFICACION DE EMAIL ================================================================================
def correo_verificacion(email,nombre,code,min):
    html = render_template("correos/tabla_verificacion.html", nombre=nombre, codigo=code, minutos=min)
    message = Mail(
    from_email="pruebaquinazaur@gmail.com",
    to_emails=email,
    subject='Código de verificación',
    html_content=html)
    try:
        sg = SendGridAPIClient(sendgridKey)
        # sg.set_sendgrid_data_residency("eu")
        # uncomment the above line if you are sending mail using a regional EU subuser
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)




# FUNCION PARA NO GUARDAR CACHE ====================================================================================
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
UPLOAD_FOLDER = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# PAGINA INICIO =============================================================================
@app.route("/")
def inicio():
    return render_template("index.html")


# PAGINA PRODUCTOS =============================================================================
@app.route("/productos")
def productos():
    db=bd_postgres(h,p,d,u,pw)
    if "user_id" in session:
        if session["user_rol"] == "admin":
            productos=db.select_productos_admin()
            cant_prod=db.cant_productos_admin()
            db.disconnect()
            return render_template("productos.html",productos=productos, cantidad=cant_prod)
    productos=db.select_productos()
    cant_prod=db.cant_productos() 
    db.disconnect()
    return render_template("productos.html",productos=productos, cantidad=cant_prod)


# PAGINA RECETAS =============================================================================
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


# PAGINA COMPROMISO VERDE =============================================================================
@app.route("/compromiso-verde")
def compromiso_verde():
    buscar=request.args.get("buscar")
    section=request.args.get("section")

    # PRESENTACION
    if not section:
        section="presentacion" 
        return render_template("compromiso_verde.html",section=section)
    if section=="presentacion":
        return render_template("compromiso_verde.html", section=section)

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

    return redirect(url_for("compromiso_verde",section="presentacion"))

# PAGINA REGISTRO =============================================================================
@app.route("/registro", methods=["GET","POST"])
@no_cache
def registro():
    # VERIFICA QUE ESTE HAYA SESION ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))
    
    # RECIBE DATOS    
    if request.method=="POST":
        nombre=request.form["nombre"]
        correo=request.form["correo"]
        telefono=request.form["telefono"]
        contraseña=request.form["contraseña"]

        # INTENTA GENERAR SESION DE REGISTRO
        try:
            user=Usuario(nombre,correo,telefono,contraseña)
            code=generar_codigo()
            db=bd_postgres(h,p,d,u,pw)
            valido=db.verificar_user(user.get_email(),user.get_telefono())
            db.subir_codigo_verificacion(correo,code[0],code[1])
            db.disconnect()
            correo_verificacion(correo,nombre,code[0],10)
            session["name"]=user.get_nombre()
            session["tel"]=user.get_telefono()
            session["password"]=user.get_password()
            session["email"]=user.get_email()
            session["try-verify"]=3
            return redirect (url_for("verify_email",email=user.get_email()))
        # MANDA ERROR
        except (ErrorRegistro, ErrorLogin) as ex:
            flash(str(ex),"error") 
            return redirect(url_for('registro'))
    
    return  render_template("formularios/registro.html")


# VERIFICAR EMAIL ===============================================================================================================
@app.route('/verify-email', methods=["GET","POST"])
def verify_email():
    # VERIFICA QUE NO HAYA SESION ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))
    
    # VERIFICA QUE HAYA UNA SESION DE REGISTRO
    if not "email" in session or not "name" in session or not "password" in session or not "tel" in session:
        return redirect(url_for("registro"))
    
    # VERIFICA QUE TENGA INTENTOS
    if session["try-verify"]!=0:
        if request.method=="POST":
            # OBTIENE DATOS
            code=request.form.get("codigo-verificacion")
            # VERIFICA QUE EL CODIGO NO ESTÉ VACIO
            if code:
                # VERIFICA EL CODIGO
                email=session["email"]
                db=bd_postgres(h,p,d,u,pw)
                valido=db.verificar_code_email(email,code)
                db.disconnect()
                if valido:
                    db=bd_postgres(h,p,d,u,pw)
                    db.agregar_usuario(session["name"],session["email"],session["tel"],session["password"])
                    db.disconnect()
                    db=bd_postgres(h,p,d,u,pw)
                    user_id=db.obtener_id(session["email"])
                    db.disconnect()
                    session.clear()
                    session["user_id"]=user_id
                    return redirect(url_for("inicio"))
                # SI EL CODE NO ES VALIDO DISMINUYE INTENTOS
                session["try-verify"]-=1
                flash("Código incorrecto","error")
                return redirect(url_for("verify_email"))
            # SI ENVIA CODIGO VACIO DISMINUYE INTENTOS
            session["try-verify"]-=1
            flash("Código incorrecto","error")
            return redirect(url_for("verify_email"))
        
        return render_template("formularios/verify_email.html")
    # SIN INTENTOS CIERRA SESION Y REDIRIGE
    session.clear()
    flash("Demasiados intentos fallidos","error")
    return redirect(url_for("registro"))





# PAGINA LOGIN =============================================================================
@app.route("/login", methods=["GET","POST"])
@no_cache
def login():
    # VERIFICA QUE HAYA SESION ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))

    # SI ENVIA EL FORM
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
                rol=db.get_rol(email)
                db.disconnect()
                session.clear()
                session["user_id"]=user_id
                session["user_rol"]=rol
                return redirect(url_for("inicio"))
        # MANDA ERRROR    
        except (ErrorRegistro, ErrorLogin) as ex:
            flash(str(ex),"error")
            return redirect(url_for('login'))
    
    return  render_template("formularios/login.html")    
        

# PAGINA PERFIL =============================================================================
@app.route("/perfil")
def perfil():
    # VERIFICA SESION
    if not "user_id" in session:
        return redirect(url_for("login"))
    # OBTIENE DATOS Y LOS MANDA
    db=bd_postgres(h,p,d,u,pw)
    user=db.get_perfil(session["user_id"])
    db.disconnect()
    return render_template("formularios/perfil.html", user=user)


# PAGINA EDITAR PERFIL ==============================================================================
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
                flash("Se ha actualizado su información","aviso") 
                return redirect(url_for("perfil"))
            db.disconnect() 
        except (ErrorLogin, ErrorRegistro) as ex:
            # MANDA ERRROR
            flash(str(ex),"error")
            return redirect(url_for('editar_perfil'))
    
    return render_template("formularios/editar_perfil.html", user=user)



# PAGINA RESET PASSWORD (ENVIA CODIGO) ============================================================
@app.route("/reset-password", methods=["GET","POST"])
@no_cache
def reset_password():
    # VERIFICA QUE NO HAYA SESION DE USUARIO ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))

    # SI ENVIA FORMULARIO
    if request.method=="POST":
        # OBTIENE DATOS
        email=request.form.get("correo")
        db=bd_postgres(h,p,d,u,pw)
        id_usuario=db.obtener_id(email)
        db.disconnect()
        # VERIFICA QUE ESE EMAIL ESTE ASOCIADO A UN USER
        if id_usuario:
            
            # GENERA Y SUBE CODIGO
            code=generar_codigo()
            db=bd_postgres(h,p,d,u,pw)
            db.subir_codigo(id_usuario,code[0],code[1])
            nombre=db.get_perfil(id_usuario)
            nombre=nombre[0]["nombre"]
            db.disconnect()
            correo_reset(email,nombre,code[0],10)
            # CREA UNA SESION PARA VERIFICAR EL CODIGO
            session.clear()
            session["id_recuperacion"]=id_usuario
            # ESTABLECE INTENTOS PARA EL CODIGO
            session["try-code"]=3
            return redirect(url_for("verify_code"))
        # SI NO HAY USER ASOCIADO CREA UNA SESION NO VALIDA
        session.clear()
        session["id_recuperacion"]="ERROR"
        # ESTABLECE INTENTOS PARA EL CODIGO
        session["try-code"]=3
        return redirect(url_for("verify_code"))
    
    return render_template("formularios/reset_password.html")

# FUNCION PARA GENERAR EL CODE DE RECUPERACION
def generar_codigo():
    code = str(secrets.randbelow(900000) + 100000)
    exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    codigo=[code,exp]
    return codigo 




# PAGINA VERIFICAR CODIGO ===============================================================
@app.route("/verify-code", methods=["GET","POST"])
@no_cache
def verify_code():
    # VERIFICA QUE NO HAYA SESION DE USUARIO ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))

    # VERIFICA QUE HAYA UNA SESION DE RECUPERACION DE CODIGO
    if not "id_recuperacion" in session:
        return redirect(url_for("reset_password"))

    # VERIFICA QUE TENGA INTENTOS
    if session["try-code"]!=0:
        if request.method=="POST":
            # OBTIENE DATOS
            code=request.form.get("codigo-recuperacion")
            # VERIFICA QUE EL CODIGO NO ESTÉ VACIO
            if code:
                # VERIFICA EL CODIGO
                id=session["id_recuperacion"]
                db=bd_postgres(h,p,d,u,pw)
                valido=db.verificar_code(id,code)
                db.disconnect()
                if valido:
                    # ESTABLECE UN NUMERO DE INTENTOS PARA RESTABLECER PASSWORD
                    session["try-password"]=3
                    return redirect(url_for("nueva_contraseña"))
                # SI EL CODE NO ES VALIDO DISMINUYE INTENTOS
                session["try-code"]-=1
                flash("Código incorrecto","error")
                return redirect(url_for("verify_code"))
            # SI ENVIA CODIGO VACIO DISMINUYE INTENTOS
            session["try-code"]-=1
            flash("Código incorrecto","error")
            return redirect(url_for("verify_code"))
        
        return render_template("formularios/verify_code.html")
    # SIN INTENTOS CIERRA SESION Y REDIRIGE
    session.clear()
    flash("Demasiados intentos fallidos","error")
    return redirect(url_for("reset_password"))




# PAGINA ESTABLECER NUEVA PASSWORD =============================================================================
@app.route("/new-password", methods=["GET","POST"] )
@no_cache
def nueva_contraseña():
    # VERIFICA QUE NO HAYA SESION DE USUARIO ACTIVA
    if "user_id" in session:
        return redirect(url_for("inicio"))
    # VERIFICA QUE HAYA SESION DE RECUPERACION
    if not "id_recuperacion" in session:
        return redirect(url_for("reset_password"))
    
    # VERIFICA QUE TENGA INTENTOS DISPONIBLES
    if session["try-password"]!=0:
        # SI ENVIA EL FORMULARIO
        if request.method=="POST":
            #OBTIENE DATOS
            new=request.form["nueva-password"]
            confirmation=request.form["confirmacion"]
            try:
                #INTENTA REESTABLECER PASSWORD
                newPassword=ResetPassword(new,confirmation)
                id=session["id_recuperacion"]
                db=bd_postgres(h,p,d,u,pw)
                db.actualizar_password(id,newPassword.get_password_nueva())
                db.disconnect()
                session.clear()
                flash("Tu contraseña se ha restablecido correctamente. Ya puedes iniciar sesión con tu nueva contraseña.","aviso")
                return redirect (url_for("login"))
            # MANDA ERROR
            except (ErrorLogin, ErrorRegistro) as ex:
                # DISMINUYE INTENTOS
                session["try-password"]-=1
                flash(str(ex),"error")
                return redirect(url_for("nueva_contraseña"))
        
        return render_template("formularios/new_password.html")
    # SIN INTENTOS, REDIRIGE Y CIERRA SESION DE RECUPERACION
    session.clear()
    flash("Demasiados intentos fallidos","error")
    return redirect(url_for("reset_password"))



# PANEL DE EDICION DE PRODUCTO ===========================================================================================

@app.route("/edit-product/<string:id>", methods=["GET","POST"])
def edit_product(id):
    if not "user_id" in session or not session["user_rol"]=="admin":
        return redirect(url_for("login"))
    
    if request.method=="POST":
        nombre=request.form.get("nombre-producto")
        descripcion=request.form.get("descripcion-producto")
        atributos=request.form.get("atributos")
        precio=request.form.get("precio-producto") 
        stock=request.form.get("stock-producto")
        disponible=request.form.get("disponible")
        print(f"Disponible recibido de html: {disponible}")
        imagen=request.files["imagen-producto"]
        if not imagen:
            filename="none"
            db=bd_postgres(h,p,d,u,pw)
            ruta=db.get_ruta(id)
            db.disconnect()
            ruta=ruta[0]["imagen_producto"]
        else:
            filename=imagen.filename    
        try:
            producto=Producto(nombre,descripcion,atributos,precio,stock,disponible,filename)
            if imagen:
                nombre = secure_filename(producto.get_name_img())
                #ruta completa
                ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre)
                #guardar
                imagen.save(ruta)
                ruta=producto.get_ruta()
            db=bd_postgres(h,p,d,u,pw)
            db.update_product(id,producto.get_nombre(),producto.get_descripción(),producto.get_precio(),ruta,producto.get_disponible(),producto.get_stock())
            db.update_atributos(id,producto.get_atributos())
            db.disconnect()
            return redirect(url_for("productos"))

        except (ErrorLogin, ErrorRegistro) as ex:
            flash(str(ex),"error")  
            return redirect(url_for("edit_product", id=id))  
        

    db=bd_postgres(h,p,d,u,pw)
    producto=db.get_producto(id)
    db.disconnect()
    if not producto:
        return redirect(url_for("productos"))
    producto=producto[0]
    atributos=""
    for a in producto["atributos"]:
        atributos+=f"{a},"
    atributos=atributos.strip(",")
    producto["atributos"]=atributos 
    return render_template("edicion/editar_producto.html",producto=producto)


# AGREGAR PRODUCTO ====================================================================================================

@app.route("/add-product", methods=["GET","POST"])
def add_product():
    if not "user_id" in session or not session["user_rol"]=="admin":
        return redirect(url_for("login"))
    
    if request.method=="POST":
        nombre=request.form.get("nombre-producto")
        descripcion=request.form.get("descripcion-producto")
        atributos=request.form.get("atributos")
        precio=request.form.get("precio-producto") 
        stock=request.form.get("stock-producto")
        disponible=request.form.get("disponible")
        imagen=request.files["imagen-producto"]
        if not imagen:
            flash("Seleccione una imagen", "error")
            return redirect(url_for("add_product"))
        else:
            filename=imagen.filename    
        try:
            producto=Producto(nombre,descripcion,atributos,precio,stock,disponible,filename)
            if imagen:
                nombre = secure_filename(producto.get_name_img())
                #ruta completa
                ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre)
                #guardar
                imagen.save(ruta)
                ruta=producto.get_ruta()
            db=bd_postgres(h,p,d,u,pw)
            db.add_product(producto.get_nombre(),producto.get_descripción(),producto.get_precio(),ruta,producto.get_disponible(),producto.get_stock(),producto.get_atributos())
            db.disconnect()
            return redirect(url_for("productos"))

        except (ErrorLogin, ErrorRegistro) as ex:
            flash(str(ex),"error")  
            return redirect(url_for("add_product"))  
        
    return render_template("edicion/agregar_producto.html")


# ESTADÍSITCAS ======================================================================================================
@app.route("/resumen")
def estadisticas():

    if not "user_id" in session or not session["user_rol"]=="admin":
        return redirect(url_for("login"))

    db=bd_postgres(h,p,d,u,pw)
    datos=db.get_estadisticas()
    db.disconnect()
    return render_template("/dashboard/dashboard.html",datos=datos)



#   ELIMINAR PRODUCTO ===============================================================================================

@app.route("/delete-product/<int:id>", methods=["POST"])
def delete_product(id):
    if not "user_id" in session or not session["user_rol"]=="admin":
        return redirect(url_for("login"))
    db=bd_postgres(h,p,d,u,pw)
    db.delete_producto(id)
    db.disconnect()
    return redirect(url_for("productos"))
    


# CERRAR SESION =============================================================================
@app.route("/logout")
def logout():
    if "user_id" in session:
        session.clear()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("inicio")) 


# EJECUTA APP =============================================================================
if __name__=="__main__":
    app.run()
    