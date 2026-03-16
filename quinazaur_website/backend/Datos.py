from werkzeug.security import generate_password_hash
from Errors import *

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
        
        if not e.endswith(".com") or not "@" in e:
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
        
        if not e.endswith(".com") or not "@" in e:
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