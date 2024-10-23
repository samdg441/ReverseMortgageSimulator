import unittest
import sys
from psycopg2 import sql

# Lo importamos para poder incluir la ruta de búsqueda python
sys.path.append("src")
sys.path.append(".")

# Importar los módulos requeridos
from src.Model.User import User
from src.controller.Controlador_usuarios import ClientController, NoneException , AgeException, PropertyValueException, InterestRateException, MIN_AGE, MAX_INTEREST_RATE, MIN_INTEREST_RATE, MIN_PROPERTY_VALUE, MAX_LIFE_EXPECTANCY_MALES

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
    def test_age_exception(self):
        """
        Prueba que se lance la excepción AgeException para una edad inválida.
        """
        age_invalid = 15  # Edad menor al mínimo permitido
        usuario_prueba = User(
            id="1234567",
            age=age_invalid,
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="100000000",
            interest_rate="25"
        )

        with self.assertRaises(AgeException) as context:
            ClientController.insert_client(usuario_prueba)  # Asegúrate de que esto verifique la edad
        self.assertEqual(str(context.exception), f"The age: {age_invalid} is invalid; to apply for a reverse mortgage, one must be between {MIN_AGE} and {MAX_LIFE_EXPECTANCY_MALES}")

    def test_none_exception(self):
        """
        Prueba que se lance la excepción NoneException al intentar insertar un usuario con campos nulos.
        """
        usuario_prueba = User(
            id=None, 
            age="68", 
            marital_status="casada",
            spouse_age=None,  # Campo nulo
            spouse_gender="hombre", 
            property_value="1000000000", 
            interest_rate="33"
        )

        with self.assertRaises(NoneException):
            ClientController.insert_client(usuario_prueba)

    def test_property_value_exception(self):
        """
        Prueba que se lance la excepción PropertyValueException para un valor de propiedad inválido.
        """
        usuario_prueba = User(
            id="1234567",
            age="65",
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="50000",  # Valor por debajo del mínimo permitido
            interest_rate="25"
        )

        with self.assertRaises(PropertyValueException) as context:
            ClientController.insert_client(usuario_prueba)
        self.assertEqual(str(context.exception), "Property value cannot be below the minimum")

    def test_interest_rate_exception_above_maximum(self):
        """
        Prueba que se lance la excepción InterestRateException para una tasa de interés mayor que el máximo.
        """
        interest_rate_too_high = 50.0  # Asegúrate de usar un número decimal
        usuario_prueba_high = User(
            id="1234567",
            age="65",
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="100000000",
            interest_rate=interest_rate_too_high
        )

        with self.assertRaises(InterestRateException) as context_high:
            ClientController.insert_client(usuario_prueba_high)

        # Ajusta el mensaje esperado para incluir el valor con punto decimal
        self.assertEqual(str(context_high.exception), f"The interest rate: {interest_rate_too_high} is invalid; it should not be less than {MIN_INTEREST_RATE} or greater than {MAX_INTEREST_RATE}")



    def test_interest_rate_valid(self):
        """
        Prueba que se pueda insertar un usuario con una tasa de interés válida.
        """
        interest_rate_valid = 30  # Tasa de interés válida, dentro de los límites permitidos
        usuario_prueba = User(
            id="1234567",
            age="65",
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="100000000",
            interest_rate=interest_rate_valid
        )

        try:
            ClientController.insert_client(usuario_prueba)  # Debería pasar sin lanzar excepción
        except InterestRateException:
            self.fail("InterestRateException should not have been raised for a valid interest rate")


if __name__ == '__main__':
    unittest.main()
