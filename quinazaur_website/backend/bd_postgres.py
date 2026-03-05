import psycopg2
from psycopg2.extras import RealDictCursor

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

    def select_productos(self):
        query="SELECT p.id_producto, p.nombre_producto, p.descripcion_producto, p.precio_producto, p.stock, p.disponible, p.imagen_producto, ARRAY_AGG(a.nombre_atributo) as atributos FROM productos.productos p LEFT JOIN productos.atributos a ON p.id_producto=a.id_producto GROUP BY p.id_producto"
        result=self.execute_query(query, fetch=True)
        return result  
    
    def cant_productos(self):
        query="SELECT COUNT(*) AS cantidad FROM productos.productos"
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