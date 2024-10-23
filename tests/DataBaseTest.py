import unittest
import sys
from psycopg2 import sql

# Lo importamos para poder incluir la ruta de búsqueda python
sys.path.append("src")
sys.path.append(".")

# Importar los módulos requeridos
from src.Model.User import User
from src.controller.Controlador_usuarios import ClientController, NoneException

class ControllerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Se ejecuta una vez antes de todas las pruebas para inicializar la base de datos y limpiar la tabla.
        """
        ClientController.clear_table()  # Asegúrate de usar el nombre correcto aquí

    def test_insert_usuario(self):
        usuario_prueba = User(
            id="1234657", 
            age="65", 
            marital_status="soltero",
            spouse_age=None, 
            spouse_gender=None, 
            property_value="100000000", 
            interest_rate="25"
        )
        
        print("Insertando usuario de prueba...")
        ClientController.insert_client(usuario_prueba)
        print("Usuario insertado. Buscando usuario...")

        usuario_buscado = ClientController.find_client(usuario_prueba.id)
        print(f"Usuario buscado: {usuario_buscado}")  # Esto debe mostrar detalles del usuario o 'None'

        self.assertIsNotNone(usuario_buscado, "El usuario no se encontró después de la inserción.")
        self.assertTrue(usuario_buscado.is_equal(usuario_prueba), "Los datos del usuario encontrado no coinciden.")



    def test_find_usuario(self):
        """
        Prueba que se pueda buscar un usuario después de haber sido insertado.
        """
        usuario_prueba = User(
            id="12346577", 
            age="65", 
            marital_status="soltero",
            spouse_age=None, 
            spouse_gender=None, 
            property_value="100000000", 
            interest_rate="25"
        )
        
        ClientController.insert_client(usuario_prueba)  # Inserción previa
        
        # Buscar el usuario insertado
        usuario_buscado = ClientController.find_client(usuario_prueba.id)
        self.assertIsNotNone(usuario_buscado, "El usuario no se encontró después de la inserción.")
        self.assertTrue(usuario_buscado.is_equal(usuario_prueba), "Los datos del usuario encontrado no coinciden.")

    def test_none_error(self):
        """
        Prueba que se lance la excepción None_Exception al intentar insertar un usuario con cédula nula.
        """
        usuario_prueba = User(
            id=None, 
            age="68", 
            marital_status="casada",
            spouse_age="62", 
            spouse_gender="hombre", 
            property_value="1000000000", 
            interest_rate="33"
        )

        with self.assertRaises(NoneException):
            ClientController.insert_client(usuario_prueba)  # Asegúrate de usar el nombre correcto aquí

    def test_update_usuario(self):
        """
        Prueba que se pueda actualizar correctamente un usuario.
        """
        # Supongamos que el usuario ya ha sido insertado previamente
        usuario_prueba = User(
            id="987654321",
            age="65",
            marital_status="Soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="120000000",
            interest_rate="30"
        )

        # Actualizar la edad
        usuario_actualizado = User(
            id="987654321",
            age="66",  # Actualizamos solo la edad
            marital_status="Married",
            spouse_age="64",
            spouse_gender="mujer",
            property_value="120000000",
            interest_rate="30"
        )

        ClientController.update_client(usuario_prueba.id, usuario_actualizado)

        usuario_buscado = ClientController.find_client(usuario_prueba.id)

        print("Datos del usuario buscado:", usuario_buscado)
        print("Datos del usuario actualizado:", usuario_actualizado)

        self.assertTrue(usuario_actualizado.is_equal(usuario_actualizado), "Los datos del usuario encontrado no coinciden con los datos actualizados.")




    def test_delete_usuario(self):
        """
        Prueba que se elimine un usuario correctamente.
        """
        # Crear un usuario de prueba y insertarlo
        usuario_prueba = User(
            id="1234658", 
            age="70", 
            marital_status="casado",
            spouse_age="68", 
            spouse_gender="mujer", 
            property_value="200000000", 
            interest_rate="35"
        )
        
        ClientController.insert_client(usuario_prueba)

        # Eliminar el usuario
        ClientController.delete_client(usuario_prueba.id)

        # Intentar buscar el usuario eliminado
        usuario_buscado = ClientController.find_client(usuario_prueba.id)
        self.assertIsNone(usuario_buscado, "El usuario no debería encontrarse después de ser eliminado.")
    # Repite para las demás funciones

if __name__ == '__main__':
    unittest.main()
