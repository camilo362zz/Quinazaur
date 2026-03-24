import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash
from Errors import *

class bd_postgres:
    def __init__(self,host,port,database,user,password):
        self.host=host
        self.port=port
        self.database=database
        self.user=user
        self.password=password
        self.connect()

    def connect(self):
        try:
            self.connection= psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
                                )
            print("✅ Conexión exitosa a PostgreSQL")

        except Exception as ex:
            print(f"Error al conectar")
            print(repr(ex))

        
    
    def disconnect(self):
        """Cierra la conexión."""
        if self.connection:
            # Verifica que exista una conexión activa.
            self.connection.close()
            # Cierra la conexión con la base de datos.
            print("Conexión cerrada.")   

    def execute_query(self,query,values=None,fetch=False):
        cursor=self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query,values)
            if fetch:
                return cursor.fetchall()
                # Si fetch es True, devuelve todos los resultados (para SELECT).
            else:
                self.connection.commit()  
            print("Acción Completada")
        except Exception as ex:
            self.connection.rollback()
            print (f"No se pudo completar la accion {ex}")
            return False
        

        if cursor:
            cursor.close()
            print("Cursor cerrado")

    def get_producto(self, id):
        query="SELECT p.id_producto, p.nombre_producto, p.descripcion_producto, p.precio_producto, p.stock, p.disponible, p.imagen_producto, ARRAY_AGG(a.nombre_atributo) as atributos FROM productos.productos p LEFT JOIN productos.atributos a ON p.id_producto=a.id_producto WHERE p.id_producto= %s GROUP BY p.id_producto"
        result=self.execute_query(query, (int(id),), fetch=True)
        return result  
    
    def select_productos(self):
        query="SELECT p.id_producto, p.nombre_producto, p.descripcion_producto, p.precio_producto, p.stock, p.disponible, p.imagen_producto, ARRAY_AGG(a.nombre_atributo) as atributos FROM productos.productos p LEFT JOIN productos.atributos a ON p.id_producto=a.id_producto WHERE p.disponible= True GROUP BY p.id_producto "
        result=self.execute_query(query, fetch=True)
        return result  
    
    def select_productos_admin(self):
        query="SELECT p.id_producto, p.nombre_producto, p.descripcion_producto, p.precio_producto, p.stock, p.disponible, p.imagen_producto, ARRAY_AGG(a.nombre_atributo) as atributos FROM productos.productos p LEFT JOIN productos.atributos a ON p.id_producto=a.id_producto GROUP BY p.id_producto"
        result=self.execute_query(query, fetch=True)
        return result 

    def cant_productos(self):
        query="SELECT COUNT(*) AS cantidad FROM productos.productos p WHERE p.disponible= True"
        result=self.execute_query(query, fetch=True)
        return result
    
    def cant_productos_admin(self):
        query="SELECT COUNT(*) AS cantidad FROM productos.productos "
        result=self.execute_query(query, fetch=True)
        return result
    
    def select_atributos(self):
        query="SELECT * FROM productos.atributos"
        result=self.execute_query(query, fetch=True)
        return result 
    
    def select_recetas(self):
        query="SELECT r.id_receta, r.nombre_receta, r.descripcion_receta, imagen_receta,(SELECT json_agg(json_build_object('ingrediente', i.nombre_ingrediente,'cantidad', ir.cantidad)) FROM recetas.ingrediente_receta ir JOIN recetas.ingredientes i  ON i.id_ingrediente = ir.id_ingrediente WHERE ir.id_receta = r.id_receta) AS ingredientes, (SELECT json_agg(p.descripcion ORDER BY p.orden asc) FROM recetas.pasos p WHERE p.id_receta = r.id_receta) AS pasos FROM recetas.recetas r order by r.nombre_receta"
        result=self.execute_query(query, fetch=True)
        return result 
    
    def buscar_receta(self,q):
        key=f"{q}"
        key=key.strip("+")
        query="SELECT r.id_receta, r.nombre_receta, r.descripcion_receta, imagen_receta,(SELECT json_agg(json_build_object('ingrediente', i.nombre_ingrediente,'cantidad', ir.cantidad)) FROM recetas.ingrediente_receta ir JOIN recetas.ingredientes i  ON i.id_ingrediente = ir.id_ingrediente WHERE ir.id_receta = r.id_receta) AS ingredientes, (SELECT json_agg(p.descripcion ORDER BY p.orden asc) FROM recetas.pasos p WHERE p.id_receta = r.id_receta) AS pasos FROM recetas.recetas r WHERE r.id_receta in (select distinct r.id_receta from recetas.recetas r join recetas.ingrediente_receta ir on r.id_receta =ir.id_receta join recetas.ingredientes i on i.id_ingrediente =ir.id_ingrediente where to_tsvector('spanish',r.nombre_receta) @@plainto_tsquery('spanish',%s) or to_tsvector('spanish',i.nombre_ingrediente) @@plainto_tsquery('spanish',%s) or to_tsvector('spanish',r.descripcion_receta) @@plainto_tsquery('spanish',%s))"
        result=self.execute_query(query,(q,q,q),fetch=True)
        return result
    
    def get_noticias(self):
        query="select n.titulo_noticia, n.descripcion_corta, n.descripcion_completa, n.fecha_publicacion, n.imagen_noticia from informacion.noticia n order by n.fecha_publicacion desc"
        result=self.execute_query(query, fetch=True)
        return result
    
    def buscar_noticia(self,buscar):
        b=f"%{buscar}%"
        query="select n.titulo_noticia, n.descripcion_corta, n.descripcion_completa, n.fecha_publicacion, n.imagen_noticia from informacion.noticia n where to_tsvector('spanish',n.titulo_noticia ) @@plainto_tsquery('spanish',%s) or to_tsvector('spanish', n.descripcion_completa) @@plainto_tsquery('spanish',%s) or n.fecha_publicacion::text ilike %s order by n.fecha_publicacion desc"
        result=self.execute_query(query, (buscar,buscar,b), fetch=True)
        return result
    
    def get_galeria(self):
        query="select i.titulo_imagen, i.ruta  from informacion.imagen i order by random()"
        result=self.execute_query(query, fetch=True)
        return result
    
    def verificar_user(self, email, telefono):
        valido=True
        query1="select u.email from usuarios.usuario u"
        query2="select u.telefono from usuarios.usuario u"
        emails=self.execute_query(query1,fetch=True)
        telefonos=self.execute_query(query2,fetch=True)
        for e in emails:
            if e["email"]==email:
                valido=False
                raise ErrorRegistro("Ese correo ya está registrado")
        for t in telefonos:
            if t["telefono"]==telefono:
                valido=False
                raise ErrorRegistro("Ese teléfono ya está registrado")        
        return valido


    def agregar_usuario(self,nombre,email,telefono,password):
        if self.verificar_user(email,telefono):
            query="insert  into usuarios.usuario (nombre, email, telefono, password) values (%s,%s,%s,%s)"
            self.execute_query(query,(nombre,email,telefono,password))
            print("Usuario registrado") 
        else:
            return   


    def validar_login(self, email, password):
        query="select u.password  from usuarios.usuario u where u.email = %s"
        key=self.execute_query(query, (email,) ,fetch=True)
        if key:
            key=key[0]["password"]
            if check_password_hash(key,password):
                return True
            else:
                raise ErrorLogin("Credenciales Incorrectas")
        raise ErrorLogin("Credenciales Incorrectas")     
        

    def obtener_id(self, email):
        query="select u.id_usuario from usuarios.usuario u where u.email = %s"
        id=self.execute_query(query, (email,), fetch=True)
        if id:
            id=id[0]["id_usuario"]
        else:
            id=None    
        return id
    
    def get_rol(self, email):
        query="select u.rol from usuarios.usuario u where u.email = %s"
        rol=self.execute_query(query, (email,), fetch=True)
        if rol:
            rol=rol[0]["rol"]
        else:
            rol=None    
        return rol
    

    def get_perfil(self,id):
        query="select u.nombre, u.email, u.telefono, u.rol from usuarios.usuario u where u.id_usuario= %s"
        result=self.execute_query(query,(id,), fetch=True)
        return result
    

    def validar_password(self, id, password):
        query="select u.password  from usuarios.usuario u where u.id_usuario = %s"
        key=self.execute_query(query, (id,) ,fetch=True)
        if not key:
            return ErrorLogin("Error")
        key=key[0]["password"]
        if check_password_hash(key,password):
            return True
        else:
            raise ErrorLogin("Contraseña Incorrecta") 
        

    def actualizar_user(self, id, nombre, telefono):
            query="update usuarios.usuario u set nombre=%s , telefono=%s where u.id_usuario =%s"
            result=self.execute_query(query,(nombre,telefono,id))
            return result
    

    def actualizar_password(self, id, password):
            query="update usuarios.usuario u set password=%s where u.id_usuario =%s"
            result=self.execute_query(query,(password,id))
            return result
    

    def validar_telefono(self, telefono):
            valido=True
            query="select u.telefono from usuarios.usuario u "
            telefonos=self.execute_query(query, fetch=True)
            for tel in telefonos:
                if tel["telefono"]==telefono:
                    valido=False
                    raise ErrorRegistro("Ese teléfono ya está en uso")
            return valido


    def subir_codigo(self, id, code, f_exp):
        query1="delete from usuarios.codigo_recuperacion cr where cr.id_usuario= %s"
        query2="insert into usuarios.codigo_recuperacion (id_usuario, code, fecha_exp) values (%s, %s, %s)" 
        query3="delete from usuarios.codigo_recuperacion cr where cr.fecha_exp < now()"
        self.execute_query(query1, (id,)) 
        result=self.execute_query(query2,(id,code,f_exp))
        self.execute_query(query3)
        return result 


    def verificar_code(self, id, code):
        query1="select cr.code from usuarios.codigo_recuperacion cr where id_usuario= %s and cr.fecha_exp > now()" 
        query2="delete from usuarios.codigo_recuperacion cr where cr.id_usuario= %s"
        codigo_valido=self.execute_query(query1,(id,), fetch=True)
        if not codigo_valido:
            return False
        if codigo_valido[0]["code"]==code:
            self.execute_query(query2,(id,))
            return True
        return False     
        

    def subir_codigo_verificacion(self, email, code, f_exp):
        query1="delete from usuarios.codigo_verificacion cv where cv.email= %s"
        query2="insert into usuarios.codigo_verificacion (email, code, fecha_exp) values (%s, %s, %s)" 
        query3="delete from usuarios.codigo_recuperacion cr where cr.fecha_exp < now()"
        self.execute_query(query1, (email,)) 
        result=self.execute_query(query2,(email,code,f_exp))
        self.execute_query(query3)
        return result     


    def verificar_code_email(self, email, code):
        query1="select cv.code from usuarios.codigo_verificacion cv where email= %s and cv.fecha_exp > now()" 
        query2="delete from usuarios.codigo_verificacion cv where cv.email= %s"
        codigo_valido=self.execute_query(query1,(email,), fetch=True)
        if not codigo_valido:
            return False
        if codigo_valido[0]["code"]==code:
            self.execute_query(query2,(email,))
            return True
        return False  
    
    def get_ruta(self,id_producto):
        query="select p.imagen_producto from productos.productos p where p.id_producto= %s"
        result=self.execute_query(query, (id_producto,), fetch=True)
        return result

    def update_product(self, id, nombre, descripcion, precio, imagen, disponible, stock):
        query="update productos.productos p set nombre_producto= %s, descripcion_producto= %s, precio_producto= %s, imagen_producto= %s, disponible= %s, stock= %s where p.id_producto= %s  " 
        result= self.execute_query(query, (nombre,descripcion,precio,imagen,disponible,stock,id))
        return result
    
    def update_atributos(self, id, newAtributos):
        drop=[]
        add=[]
        producto=self.get_producto(id)
        producto=producto[0]
        antAtributos=producto["atributos"]
        for a in antAtributos:
            if not a in newAtributos:
                drop.append(a)
        for a in newAtributos:
            if not a in antAtributos:
                add.append(a)    
        query1="delete from productos.atributos a where a.nombre_atributo= %s and a.id_producto= %s"
        query2="insert into productos.atributos (nombre_atributo, id_producto) values (%s, %s)"
        for a in drop:
            self.execute_query(query1, (a,id))
        for a in add:
            self.execute_query(query2, (a,id))    

    def delete_producto(self,id):
        query="delete from productos.productos p where p.id_producto= %s"
        result=self.execute_query(query, (id,))
        return result    

    def add_product(self, nombre, descripcion, precio, imagen, disponible, stock, atributos):
        query="insert into productos.productos  (nombre_producto, descripcion_producto, precio_producto, imagen_producto, disponible, stock) values (%s, %s, %s, %s, %s, %s) " 
        self.execute_query(query, (nombre,descripcion,precio,imagen,disponible,stock))
        query2="select p.id_producto from productos.productos p where p.nombre_producto= %s"
        id=self.execute_query(query2, (nombre,), fetch=True)
        if id:
            id=id[0]["id_producto"]
        self.update_atributos(id,atributos)

    def get_estadisticas(self):
        query1="select u.nombre, u.email, u.rol from usuarios.usuario u order by u.rol asc"
        query2="select  r.nombre_receta from recetas.recetas r"    
        query3="select p.nombre_producto, p.disponible from productos.productos p"  
        query4="select count(*) as total from usuarios.usuario " 
        query5="select count(*) as total from productos.productos "  
        query6="select count(*) as total from recetas.recetas "  

        datos=[]
        usuarios=self.execute_query(query1, fetch=True)
        productos=self.execute_query(query3, fetch=True)
        recetas=self.execute_query(query2, fetch=True)
        t_usuarios=self.execute_query(query4, fetch=True)[0]["total"]
        t_productos=self.execute_query(query5, fetch=True)[0]["total"]
        t_recetas=self.execute_query(query6, fetch=True)[0]["total"]

        datos.append(usuarios)
        datos.append(productos)
        datos.append(recetas)
        datos.append(t_usuarios)
        datos.append(t_productos)
        datos.append(t_recetas)
        return datos