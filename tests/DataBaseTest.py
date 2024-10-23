import unittest
import sys
from psycopg2 import sql

# Lo importamos para poder incluir la ruta de búsqueda python
sys.path.append("src")
sys.path.append(".")
sys.path.append("..")

# Importar los módulos requeridos
from src.Model.User import User
from src.controller.Controlador_usuarios import (ClientNotUpdatedException, ClientNotInsertedException, ClientNotDeletedException, AgeException, NoneException, PropertyValueException,
                                                 InterestRateException,insert_client,find_client,delete_client,update_client)


class ControllerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Se ejecuta una vez antes de todas las pruebas para inicializar la base de datos y limpiar la tabla.
        """
        Controlador_usuarios.create_table()
        Controlador_usuarios.clear_table()

    def test_insert_and_select_usuario_1(self):
        """
        Prueba que se inserte correctamente un usuario y se pueda buscar.
        """
        usuario_prueba = User(
            cedula="1234657", 
            edad="65", 
            estado_civil="soltero",
            edad_conyugue=None, 
            sexo_conyugue=None, 
            valor_inmueble="100000000", 
            tasa_interes="25"
        )
        
        Controlador_Usuarios.insert_client(usuario_prueba)
        
        usuario_buscado = Controlador_Usuarios.find_client(usuario_prueba.cedula)
        self.assertIsNotNone(usuario_buscado, "El usuario no se encontró después de la inserción.")
        self.assertTrue(usuario_buscado.es_Igual(usuario_prueba), "Los datos del usuario encontrado no coinciden.")

    def test_update_usuario(self):
        """
        Prueba que se actualicen correctamente los datos de un usuario.
        """
        datos_actualizar = User(
            cedula=None, 
            edad=None, 
            estado_civil="casado",
            edad_conyugue="66", 
            sexo_conyugue="mujer", 
            valor_inmueble=None, 
            tasa_interes=None
        )
        
        Controlador_Usuarios.update_client(cedula_buscada="1234657", datos_actualizar=datos_actualizar)
        usuario_actualizado = Controlador_Usuarios.find_client("1234657")
        
        self.assertEqual(usuario_actualizado.edad_conyugue, "66")
        self.assertEqual(usuario_actualizado.estado_civil, "casado")

    def test_delete_usuario(self):
        """
        Prueba que se elimine correctamente un usuario de la base de datos.
        """
        Controlador_Usuarios.delete_client(cedula_buscada="55555555")
        usuario_buscado = Controlador_Usuarios.find_client("55555555")
        
        self.assertIsNone(usuario_buscado, "El usuario no fue eliminado correctamente.")

    def test_none_error(self):
        """
        Prueba que se lance la excepción None_Exception al intentar insertar un usuario con cédula nula.
        """
        usuario_prueba = User(
            cedula=None, 
            edad="68", 
            estado_civil="casada",
            edad_conyugue="62", 
            sexo_conyugue="hombre", 
            valor_inmueble="1000000000", 
            tasa_interes="33"
        )

        with self.assertRaises(None_Exception):
            Controlador_Usuarios.insert_client(usuario_prueba)

    def test_edad_error(self):
        """
        Prueba que se lance la excepción Edad_Exception al intentar insertar un usuario con edad no permitida.
        """
        usuario_prueba = User(
            cedula="1038867289", 
            edad="55", 
            estado_civil="soltero",
            edad_conyugue=None, 
            sexo_conyugue=None, 
            valor_inmueble="84000000", 
            tasa_interes="35"
        )

        with self.assertRaises(Edad_Exception):
            Controlador_Usuarios.insert_client(usuario_prueba)

    def test_valor_inmueble_error(self):
        """
        Prueba que se lance la excepción Valor_Inmueble_Exception al intentar insertar un usuario con valor de inmueble no permitido.
        """
        usuario_prueba = User(
            cedula="1038867289", 
            edad="66", 
            estado_civil="soltero",
            edad_conyugue=None, 
            sexo_conyugue=None, 
            valor_inmueble="7000000", 
            tasa_interes="40"
        )

        with self.assertRaises(Valor_Inmueble_Exception):
            Controlador_Usuarios.insert_client(usuario_prueba)

    def test_tasa_interes_error(self):
        """
        Prueba que se lance la excepción Tasa_Exception al intentar insertar un usuario con tasa de interés no permitida.
        """
        usuario_prueba = User(
            cedula="1038867289", 
            edad="66", 
            estado_civil="soltero",
            edad_conyugue=None, 
            sexo_conyugue=None, 
            valor_inmueble="125000000000", 
            tasa_interes="48"
        )

        with self.assertRaises(Tasa_Exception):
            Controlador_Usuarios.Insertar_Usuario(usuario_prueba)

if __name__ == '__main__':
    unittest.main()
