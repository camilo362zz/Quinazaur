from werkzeug.security import generate_password_hash
from Errors import *
from random import randint
#///////////////////////////////////////////////////////////////////
# ESTA CLASE SE USA PAARA VALIDAR LOS DATOS AL HACER UN RESGISTRO
#///////////////////////////////////////////////////////////////////

class Usuario:
    __nombre=""
    __email=""
    __telefono=""
    __password=""

    def __init__(self,nombre,email,telefono,password):
        self.set_nombre(nombre)
        self.set_email(email)
        self.set_telefono(telefono)
        self.set_password(password)

    def set_nombre(self,nombre):
        n=nombre.strip()

        if len(n)==0:
            raise ErrorRegistro("El nombre no debe estar vacío")
        
        if not n.replace(" ","").isalpha():
            raise ErrorRegistro("El nombre no debe contener numeros o caracteres especiales")
        
        if len(n)<3:
            raise ErrorRegistro("Nombre muy corto")
        
        if len(n)>50:
            raise ErrorRegistro("Nombre muy largo")
        
        self.__nombre=n

    def set_email(self,email):
        e=email.strip()
        
        if len(e)==0:
            raise ErrorRegistro("El correo no debe estar vacío")
        
        if " " in e:
            raise ErrorRegistro("El correo no debe contener espacios")
        
        if len(e)<6:
            raise ErrorRegistro("Correo muy corto")
        
        if len(e)>50:
            raise ErrorRegistro("Correo muy largo")
        
        if not (e.endswith(".com") or e.endswith(".co")) or not "@" in e:
            raise ErrorRegistro("Formato de correo incorrecto")
        
        self.__email=e
        
    def set_telefono(self,telefono):
        t=telefono.strip()
        t=t.replace(" ","")

        if len(t)==0:
            raise ErrorRegistro("El teléfono no debe estar vacío")
        
        if not t.isdigit():
            raise ErrorRegistro("El teléfono solo debe contener números")

        if len(t)!=10:
            raise ErrorRegistro("El teléfono debe ser de Colombia")

        self.__telefono=t

    def set_password(self,password):
        p=password.strip()

        if p!=password:
            raise ErrorRegistro("La contraseña no debe tener espacios al inicio o al final")

        if len(p)<8:
            raise ErrorRegistro("La contraseña debe tener al menos 8 caracteres")
        
        
        if len(p)>100:
            raise ErrorRegistro("Contraseña demasiado larga")

        self.__password=generate_password_hash(p)

    def get_nombre(self):
        return self.__nombre    

    def get_email(self):
        return self.__email  

    def get_telefono(self):
        return self.__telefono 

    def get_password(self):
        return self.__password    
    
#///////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////    




#///////////////////////////////////////////////////////////////////
# ESTA CLASE SE USA PARA VALIDAR LOS DATOS EN EL LOGIN
#///////////////////////////////////////////////////////////////////

class Login:

    __email=""
    __password=""
    
    def __init__(self,email,password):
        
        self.set_email(email)
        self.set_password(password)

    def set_email(self,email):
        e=email.strip()
        msg="Credenciales Incorrectas"
        
        if len(e)==0:
            raise ErrorLogin(msg)
        
        if " " in e:
            raise ErrorLogin(msg)
        
        if len(e)<6:
            raise ErrorLogin(msg)
        
        if len(e)>50:
            raise ErrorLogin(msg)
        
        if not (e.endswith(".com") or e.endswith(".co")) or not "@" in e:
            raise ErrorLogin(msg)
        
        self.__email=e
        

    def set_password(self,password):
        p=password.strip()
        msg="Credenciales Incorrectas"
        
        if p!=password:
            raise ErrorLogin(msg)

        if len(p)<8:
            raise ErrorLogin(msg)
        
        if len(p)>100:
            raise ErrorLogin(msg)

        self.__password=p

    def get_email(self):
        return self.__email  

    def get_password(self):
        return self.__password    

#///////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////





#///////////////////////////////////////////////////////////////////
# ESTA CLASE SE USA PAARA VALIDAR LOS DATOS PARA ACTUALIZAR UN USER
#///////////////////////////////////////////////////////////////////

class Modificar:
    __nombre=""
    __telefono=""
    __password_nueva=""

    def __init__(self,nombre,telefono,password,password_nueva):
        self.set_nombre(nombre)
        self.set_telefono(telefono)
        self.set_password(password)
        self.set_password_nueva(password_nueva)

    def set_nombre(self,nombre):
        n=nombre.strip()

        if len(n)==0:
            raise ErrorRegistro("El nombre no debe estar vacío")
        
        if not n.replace(" ","").isalpha():
            raise ErrorRegistro("El nombre no debe contener numeros o caracteres especiales")
        
        if len(n)<3:
            raise ErrorRegistro("Nombre muy corto")
        
        if len(n)>50:
            raise ErrorRegistro("Nombre muy largo")
        
        self.__nombre=n

        
    def set_telefono(self,telefono):
        t=telefono.strip()
        t=t.replace(" ","")

        if len(t)==0:
            raise ErrorRegistro("El teléfono no debe estar vacío")
        
        if not t.isdigit():
            raise ErrorRegistro("El teléfono solo debe contener números")

        if len(t)!=10:
            raise ErrorRegistro("El teléfono debe ser de Colombia")

        self.__telefono=t

    def set_password(self,password):
        p=password.strip()

        if p!=password:
            raise ErrorRegistro("Contraseña Incorrecta")

        if len(p)<8:
            raise ErrorRegistro("Contraseña Incorrecta")
        
        
        if len(p)>100:
            raise ErrorRegistro("Contraseña Incorrecta")
        

    def set_password_nueva(self,password_nueva):
        
        if password_nueva=="":
            self.__password_nueva=""
            return
        
        p=password_nueva.strip()
        if p!=password_nueva:
            raise ErrorRegistro("La nueva contraseña no debe tener espacios al inicio o al final")

        if len(p)<8:
            raise ErrorRegistro("La nueva contraseña debe tener al menos 8 caracteres")
        
        if len(p)>100:
            raise ErrorRegistro("Nueva contraseña demasiado larga")

        self.__password_nueva=generate_password_hash(p)    

    def get_nombre(self):
        return self.__nombre    

    def get_telefono(self):
        return self.__telefono 

    def get_password_nueva(self):
        return self.__password_nueva       
    


#////////////////////////////////////////////////////////////////
# CLASE PARA VALIDAR PASSWORD CUANDO SE OLVIDA 
#////////////////////////////////////////////////////////////////

class ResetPassword:
    __password_nueva=""

    def __init__(self,password_nueva, confirmacion):
        self.set_password_nueva(password_nueva, confirmacion)


    def set_password_nueva(self,password_nueva, confirmacion):

        if password_nueva!=confirmacion:
            raise ErrorRegistro("Los campos no coinciden")
        
        p=password_nueva.strip()
        if p!=password_nueva:
            raise ErrorRegistro("La nueva contraseña no debe tener espacios al inicio o al final")

        if len(p)<8:
            raise ErrorRegistro("La nueva contraseña debe tener al menos 8 caracteres")
        
        if len(p)>100:
            raise ErrorRegistro("Nueva contraseña demasiado larga")

        self.__password_nueva=generate_password_hash(p)     


    def get_password_nueva(self):
        return self.__password_nueva    


#/////////////////////////////////////////////////////////////////////////////////////////////////////////
# ESTA CLASE VALIDA LOS DATOS DEL PRODUCTO QUE SE VA A SUBIR
#/////////////////////////////////////////////////////////////////////////////////////////////////////////

class Producto:
    __nombre=""
    __descripcion=""
    __atributos=[]
    __precio=0
    __stock=0
    __disponible=True
    __name_img=""
    __ruta=""

    def __init__(self,nombre,descripcion,atributos,precio,stock,disponible,imagen):
        self.set_nombre(nombre)
        self.set_descripcion(descripcion)
        self.set_atributos(atributos)
        self.set_precio(precio)
        self.set_stock(stock)
        self.set_disponible(disponible)
        self.set_imagen(imagen,nombre)


    def set_nombre(self,nombre):
        n=nombre.strip()

        if len(n)==0:
            raise ErrorRegistro("El nombre no debe estar vacío")
        
        if len(n)<3:
            raise ErrorRegistro("Nombre muy corto")
        
        if len(n)>150:
            raise ErrorRegistro("Nombre muy largo")
        
        self.__nombre=n

    def set_descripcion(self,descripcion):
        d=descripcion.strip()

        if len(d)==0:
            raise ErrorRegistro("La descripcion no debe estar vacía")
        
        if len(d)<10:
            raise ErrorRegistro("Descripción muy corta")
        
        if len(d)>500:
            raise ErrorRegistro("Descripción muy larga")
        
        self.__descripcion=d
        
    def set_atributos(self,atributos):
        a = [item.strip() for item in atributos.split(",")]
        
        if len(a)<1:
            raise ErrorRegistro("Debe incluir al menos un atributo")

        if len(a)>5:
            raise ErrorRegistro("Máximo 5 atributos")

        for i in a:
            i=i.strip()
            if len(i)==0:
                raise ErrorRegistro("No debe haber atributos vacíos")
            
            if len(i)<3:
                raise ErrorRegistro("Hay un atributo demasiado corto")

            if len(i)>50:
                raise ErrorRegistro("Hay un atributo demasiado largo")
            
        self.__atributos=a

    def set_precio(self,precio):
        char=["1","2","3","4","5","6","7","8","9","0",",",".","-","+"]
        for p in precio:
            if not p in char:
                raise ErrorRegistro("Precio solo admite números")
        p=float(precio)
        if p<=0:
            raise ErrorRegistro("El precio no puede ser negativo o cero")
        self.__precio=p
        
    def set_stock(self,stock):
        char=["1","2","3","4","5","6","7","8","9","0",]
        for s in stock:
            if not s in char:
                raise ErrorRegistro("Stock solo admite números")
        s=int(stock)
        if s<0:
            raise ErrorRegistro("El stock no puede ser negativo")
        self.__stock=s

    def set_disponible(self, disponible):
        disponible=int(disponible)
        if disponible!=1 and disponible!=0:
            raise ErrorRegistro("Estado solo admite True o False")
        
        if disponible==1:
            self.__disponible=True
        if disponible==0:
            self.__disponible=False        

    def set_imagen(self,ruta, name):

        if ruta=="none":
            return
        n=name.strip()
        r=ruta.strip()
        if len(r)==0:
            raise ErrorRegistro("El nombre del archivo no puede estar vacío")
        
        if not r.endswith(".jpg") and not r.endswith(".png") and not r.endswith(".webp") and not r.endswith(".jpeg"):
            raise ErrorRegistro("Formato de archivo no válido")
        
        newRuta="/images/"
        digits=[1,2,3,4,5,6,7,8,9,0]
        id=""
        for i in range(3):
            id+=str(digits[randint(0,9)])
        n=n.replace(" ","_")
        id+="_"
        self.__name_img=id+n  
        newRuta+=(id+r) 

        self.__ruta=newRuta

    def get_nombre(self):
        return self.__nombre
    
    def get_descripción(self):
        return self.__descripcion
    
    def get_atributos(self):
        return self.__atributos
    
    def get_precio(self):
        return self.__precio
    
    def get_stock(self):
        return self.__stock
    
    def get_disponible(self):
        return self.__disponible
    
    def get_ruta(self):
        return self.__ruta
    
    def get_name_img(self):
        return self.__name_img  