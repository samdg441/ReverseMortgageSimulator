# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")
sys.path.append(".")

# Se importa el modulo donde se realizarán los procesos
from controller.Controlador_usuarios import ClientController
from Model.User import User

# Se le da una bienvenida al usuario y se le muestra un menú con las opciones
def Bienvenida():
    print("-------------------------------------------")
    print("    BIENVENIDO AL BANCO   ")
    print("¿Qué deseas hacer?")
    print(" 1. Obtener una hipoteca inversa \n 0. Salir")
    opcion = int(input("Elija una opción: "))
    print("--------------------------------------")
    # Se llama a la siguiente función y se le pasa como parametro la opción que el usuario eligió
    return desiciones(opcion)

def desiciones(opcion):
    try:
        while opcion != 0:
            if opcion < 0 or opcion > 1:
                print("------------------------------------------------------------------")
                print("                  EL BANCO            ")
                print("La opción ingresada no es correcta, intente de nuevo")
                print("-------------------------------------------------------------------")
                opcion = int(input("Elija una opción: "))  # Pedir nuevamente la opción en lugar de llamar a Bienvenida()

            if opcion == 1:
                print("---------------------------------------------------------------------")
                print("                     EL BANCO                 ")
                print("DATOS PERSONALES")
                cedula = int(input("Por favor ingrese su cédula: "))
                edad = int(input("Por favor ingrese su edad actual: "))
                estado_civil = input("Por favor ingrese su estado civil: ").title()
                
                # Verificar si está casado
                if estado_civil == "Casado" or estado_civil == "Casada":
                    edad_conyugue = int(input("Por favor ingrese la edad de su cónyuge: "))
                    sexo_conyugue = input("Por favor ingrese el género de su cónyuge: ")
                else:
                    edad_conyugue = None
                    sexo_conyugue = None
                
                # Pedir el valor de la propiedad
                valor_propiedad = float(input("Por favor ingrese el valor de su propiedad: "))
                # Pedir la tasa de interés
                tasa_interes = float(input("Por favor ingrese la tasa de interés: "))

                print("-------------------------------------------------------------------------")
                
                # Crear el usuario con los nuevos datos
                usuario = User(cedula, edad, estado_civil, edad_conyugue, sexo_conyugue, valor_propiedad, tasa_interes)
                ClientController.insert_client(usuario)
                opcion = 0  # Volvemos a la opción para salir o reiniciar

        print("------------------------------------------------------------------")
        print("                  EL BANCO            ")
        print("Gracias por visitarnos, vuelva pronto")
        print("-------------------------------------------------------------------")
        return
    except ValueError:
        print("------------------------------------------------------------------")
        print("                  EL BANCO            ")
        print("Hubo un ERROR, revisa que los datos ingresados sean correctos")
        print("-------------------------------------------------------------------")
    except Exception as exc:
        print("------------------------------------------------------------------")
        print("                  EL BANCO            ")
        print(f"{exc}, intentalo nuevamente")
        print("-------------------------------------------------------------------")

#Condicional para comprobar si la tabla "Usuarios" ya está creada
if ClientController.create_table == "Tabla Existente":
    # Si la condición anterior se cumple, solo se llama la funcion para dar inicio al programa
    Bienvenida()

else:
    #Si la condición anterior no se cumple, se crea la base de datos
    ClientController.create_table()
    # Se llama la funcion para dar inicio al programa
    Bienvenida()

if __name__ == "__main__":
    Bienvenida()
