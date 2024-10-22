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
    print(" 1. Obtener una hipoteca inversa")
    print(" 2. Buscar cliente")
    print(" 3. Actualizar cliente")
    print(" 4. Eliminar cliente")
    print(" 0. Salir")
    opcion = int(input("Elija una opción: "))
    print("--------------------------------------")
    # Se llama a la siguiente función y se le pasa como parametro la opción que el usuario eligió
    return desiciones(opcion)


def desiciones(opcion):
    try:
        while opcion != 0:
            if opcion < 0 or opcion > 4:
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
                if estado_civil in ["Casado", "Casada"]:
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



            elif opcion == 3:
                cedula = input("Ingrese la cédula del cliente a actualizar: ")
                print("Ingrese los nuevos datos (dejar en blanco para no modificar):")
                new_id = input("Nuevo ID (actual: {}): ".format(cedula)) or cedula
                edad = input("Nueva edad (actual: {}): ".format(client.age)) or client.age
                estado_civil = input("Nuevo estado civil (actual: {}): ".format(client.marital_status)) or client.marital_status
                edad_conyugue = input("Nueva edad del cónyuge (actual: {}): ".format(client.spouse_age)) or client.spouse_age
                sexo_conyugue = input("Nuevo género del cónyuge (actual: {}): ".format(client.spouse_gender)) or client.spouse_gender
                valor_propiedad = input("Nuevo valor de la propiedad (actual: {}): ".format(client.property_value)) or client.property_value
                tasa_interes = input("Nueva tasa de interés (actual: {}): ".format(client.interest_rate)) or client.interest_rate

                updated_data = User(
                    id=new_id,
                    age=edad,
                    marital_status=estado_civil,
                    spouse_age=edad_conyugue,
                    spouse_gender=sexo_conyugue,
                    property_value=valor_propiedad,
                    interest_rate=tasa_interes
                )
                ClientController.update_client(cedula, updated_data)

            elif opcion == 4:
                cedula = input("Ingrese la cédula del cliente a eliminar: ")
                ClientController.delete_client(cedula)

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


# Condicional para comprobar si la tabla "Usuarios" ya está creada
if ClientController.create_table == "Tabla Existente":
    # Si la condición anterior se cumple, solo se llama la funcion para dar inicio al programa
    Bienvenida()

else:
    # Si la condición anterior no se cumple, se crea la base de datos
    ClientController.create_table()
    # Se llama la funcion para dar inicio al programa
    Bienvenida()

if __name__ == "__main__":
    Bienvenida()
