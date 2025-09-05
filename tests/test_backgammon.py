from unittest import TestCase
from source.backgammon import Backgammon

class TestBackgammon(TestCase):
    def setUp(self):
        self.juego = Backgammon()
        self.pos = self.juego.__tablero__.__posiciones__
        for i in range(24):
            self.pos[i] = 0
        self.juego.__tablero__.__barra__['blancas'] = 0
        self.juego.__tablero__.__barra__['negras'] = 0
        # turno por defecto: blancas (1)

    def test_turno_inicial(self):
        self.assertEqual(self.juego.obtener_turno(), 1)

    def test_cambiar_turno(self):
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), -1)
        self.juego.cambiar_turno()
        self.assertEqual(self.juego.obtener_turno(), 1)

    def test_mover_a_casilla_vacia_blancas(self):
        self.pos[0] = 1
        self.juego.__turno__ = 1
        self.juego.__movimientos_pendientes__ = [3]  

        ok, msg = self.juego.mover(origen=1, valor_dado=3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)  
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 0)  


    def test_mover_a_casilla_con_ficha_propia_blancas(self):
        self.pos[0] = 1
        self.pos[3] = 2
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(1, 3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 3)

    def test_mover_y_comer_blancas(self):
        self.pos[0] = 1
        self.pos[3] = -1
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(1, 3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[0], 0)
        self.assertEqual(self.pos[3], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 1)

    def test_mover_a_posicion_bloqueada_blancas(self):
        self.pos[0] = 1
        self.pos[3] = -3
        self.juego.__turno__ = 1

        ok, msg = self.juego.mover(1, 3)

        self.assertFalse(ok)
        self.assertEqual(msg, "posición de destino bloqueada")
        self.assertEqual(self.pos[0], 1)
        self.assertEqual(self.pos[3], -3)

    def test_mover_a_casilla_vacia_negras(self):
        self.pos[23] = -1
        self.juego.__turno__ = -1

        ok, msg = self.juego.mover(origen=24, valor_dado=3)  

        self.assertTrue(ok)
        self.assertEqual(msg, "movió")
        self.assertEqual(self.pos[23], 0)
        self.assertEqual(self.pos[20], -1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 0)

    def test_mover_y_comer_negras(self):
        self.pos[23] = -1
        self.pos[20] = 1
        self.juego.__turno__ = -1

        ok, msg = self.juego.mover(24, 3)

        self.assertTrue(ok)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[23], 0)
        self.assertEqual(self.pos[20], -1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 1)

    def test_bloqueo_negras(self):
        self.pos[23] = -1
        self.pos[20] = 3
        self.juego.__turno__ = -1

        ok, msg = self.juego.mover(24, 3)

        self.assertFalse(ok)
        self.assertEqual(msg, "posición de destino bloqueada")
        self.assertEqual(self.pos[23], -1)
        self.assertEqual(self.pos[20], 3)

    def test_entrar_desde_barra_blancas_libre(self):
        self.juego.__turno__ = 1
        self.juego.__tablero__.__barra__['blancas'] = 1

        ok, msg = self.juego.entrar_desde_barra(3)  # índice 2

        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)

    def test_entrar_desde_barra_blancas_bloqueado(self):
        self.juego.__turno__ = 1
        self.juego.__tablero__.__barra__['blancas'] = 1
        self.pos[2] = -2  # bloqueado

        ok, msg = self.juego.entrar_desde_barra(3)

        self.assertFalse(ok)
        self.assertEqual(msg, "posición de destino bloqueada")
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 1)

    def test_entrar_desde_barra_blancas_comer(self):
        self.juego.__turno__ = 1
        self.juego.__tablero__.__barra__['blancas'] = 1
        self.pos[2] = -1  # blot

        ok, msg = self.juego.entrar_desde_barra(3)

        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 1)

    def test_entrar_desde_barra_negras_libre(self):
        self.juego.__turno__ = -1
        self.juego.__tablero__.__barra__['negras'] = 1

        ok, msg = self.juego.entrar_desde_barra(3)  # 24-3 = 21

        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[21], -1)
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 0)

    def test_mover_con_fichas_en_barra_deriva_a_entrar(self):
        self.juego.__turno__ = 1
        self.juego.__tablero__.__barra__['blancas'] = 1
        self.juego.__movimientos_pendientes__ = [3]  # dado disponible
        # destino índice 2 libre por defecto
        ok, msg = self.juego.mover(origen=1, valor_dado=3)

        self.assertTrue(ok)
        self.assertEqual(msg, "entró")
        self.assertEqual(self.pos[2], 1)
        self.assertEqual(self.juego.__tablero__.__barra__['blancas'], 0)

    def test_consumir_movimiento_no_existente(self):
        self.juego.__movimientos_pendientes__ = [2, 5]
        resultado = self.juego.consumir_movimiento(3)   
        self.assertFalse(resultado)                   
        self.assertEqual(self.juego.__movimientos_pendientes__, [2, 5]) 

    def test_finalizar_tirada(self):
        self.juego.__movimientos_pendientes__ = [3, 5]
        turno_inicial = self.juego.obtener_turno()
        self.juego.finalizar_tirada()
        self.assertEqual(self.juego.__movimientos_pendientes__, [])
        turno_final = self.juego.obtener_turno()
        self.assertNotEqual(turno_inicial, turno_final)
        self.assertIn(turno_final, [1, -1]) 

    def test_mover_origen_invalido_o_sin_fichas(self):
        # Turno de blancas (1) pero origen está vacío
        self.juego.__turno__ = 1
        self.pos[0] = 0  # sin fichas en origen

        ok, msg = self.juego.mover(origen=1, valor_dado=3)

        self.assertFalse(ok)
        self.assertEqual(msg, "origen inválido o sin fichas del jugador")

        # Turno de blancas (1) pero en origen hay ficha negra
        self.pos[0] = -1
        ok, msg = self.juego.mover(origen=1, valor_dado=3)

        self.assertFalse(ok)
        self.assertEqual(msg, "origen inválido o sin fichas del jugador")

    def test_mover_y_comer_consumiendo_movimiento(self):
        # Blancas atacan con un dado 3
        self.juego.__turno__ = 1
        self.juego.__movimientos_pendientes__ = [3]  # dado disponible

        self.pos[0] = 1   # ficha blanca en origen
        self.pos[3] = -1  # blot negro en destino

        ok, msg = self.juego.mover(origen=1, valor_dado=3)

        # Validaciones
        self.assertTrue(ok)
        self.assertEqual(msg, "movió y comió")
        self.assertEqual(self.pos[0], 0)   # origen vacío
        self.assertEqual(self.pos[3], 1)   # destino ahora blanco

        # En el tablero: una ficha negra fue a la barra
        self.assertEqual(self.juego.__tablero__.__barra__['negras'], 1)

        # El dado ya no está disponible
        self.assertNotIn(3, self.juego.__movimientos_pendientes__)

    def test_bear_off_blancas_valido(self):
        self.juego.__turno__ = 1
        self.pos[20] = 1  # Poner una ficha blanca en punto 21 (índice 20)
        self.juego.__tablero__.__fichas_fuera__['blancas'] = 0
        self.juego.__tablero__.__fichas_fuera__['negras'] = 0
        ok, msg = self.juego.mover(origen=21, valor_dado=5)
        self.assertTrue(ok)
        self.assertEqual(msg, "sacó ficha")
        self.assertEqual(self.pos[20], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['blancas'], 1)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['negras'], 0)

    def test_bear_off_negras_valido(self):
        self.juego.__turno__ = -1
        self.pos[3] = -1  # Poner una ficha negra en punto 3 (índice 2)
        self.juego.__tablero__.__fichas_fuera__['blancas'] = 0
        self.juego.__tablero__.__fichas_fuera__['negras'] = 0
        ok, msg = self.juego.mover(origen=4, valor_dado=5)
        self.assertTrue(ok)
        self.assertEqual(msg, "sacó ficha")
        self.assertEqual(self.pos[3], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['blancas'], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['negras'], 1)

    def test_bear_off_negras_invalido(self):
        self.juego.__turno__ = -1
        self.pos[3] = -1 
        self.pos[20] = -1 # Poner una ficha negra en punto 3 (índice 2)
        self.juego.__tablero__.__fichas_fuera__['blancas'] = 0
        self.juego.__tablero__.__fichas_fuera__['negras'] = 0
        ok, msg = self.juego.mover(origen=4, valor_dado=5)
        self.assertFalse(ok)
        self.assertEqual(msg, "para sacar, todas las fichas deben estar en home")
        self.assertEqual(self.pos[3], -1)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['blancas'], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['negras'], 0)

    def test_bear_off_blancas_invalido(self):
        self.juego.__turno__ = 1
        self.pos[20] = 1
        self.pos[10] = 1
        self.juego.__tablero__.__fichas_fuera__['blancas'] = 0
        self.juego.__tablero__.__fichas_fuera__['negras'] = 0
        ok, msg = self.juego.mover(origen=21, valor_dado=5)
        self.assertFalse(ok)
        self.assertEqual(msg, "para sacar, todas las fichas deben estar en home")
        self.assertEqual(self.pos[20], 1)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['blancas'], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['negras'], 0)

    def test_bear_off_ganar(self):
        self.juego.__turno__ = 1
        self.pos[20] = 1  
        self.juego.__tablero__.__fichas_fuera__['blancas'] = 14
        self.juego.__tablero__.__fichas_fuera__['negras'] = 0
        ok, msg = self.juego.mover(origen=21, valor_dado=5)
        self.assertTrue(ok)
        self.assertEqual(msg, "juego terminado! Blancas ganaron")
        self.assertEqual(self.pos[20], 0)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['blancas'], 15)
        self.assertEqual(self.juego.__tablero__.__fichas_fuera__['negras'], 0)

    def test_valor_dado_no_disponible(self):
        self.pos[0] = 1
        self.juego.__turno__ = 1
        self.juego.__movimientos_pendientes__ = [3, 4]

        ok, msg = self.juego.mover(origen=1, valor_dado=5)

        self.assertFalse(ok)
        self.assertEqual(msg, "dado no disponible")
        self.assertEqual(self.pos[0], 1)
        self.assertEqual(self.pos[4], 0)

    def test_indice_entrada_dado_fuera_de_rango(self):
        # dado = 0 -> debe levantar ValueError
        with self.assertRaises(ValueError) as cm:
            self.juego.__indice_entrada__(jugador=1, valor_dado=0)
        self.assertEqual(str(cm.exception), "dado inválido (1..6)")

        # dado = 7 -> debe levantar ValueError
        with self.assertRaises(ValueError):
            self.juego.__indice_entrada__(jugador=-1, valor_dado=7)

    def test_obtener_movimientos_pendientes_vacio(self):
        # Al inicio no hay movimientos
        self.juego.__movimientos_pendientes__ = []
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [])

    def test_obtener_movimientos_pendientes_con_valores(self):
        # Simulamos tirada de dados = [3, 5]
        self.juego.__movimientos_pendientes__ = [3, 5]
        pendientes = self.juego.obtener_movimientos_pendientes()

        # Debe devolver copia de la lista
        self.assertEqual(pendientes, [3, 5])
        self.assertIsNot(pendientes, self.juego.__movimientos_pendientes__) 

    def test_movimientos_disponibles_false(self):
        # No hay movimientos pendientes
        self.juego.__movimientos_pendientes__ = []
        self.assertFalse(self.juego.movimientos_disponibles())

    def test_movimientos_disponibles_true(self):
        # Simulamos que hay movimientos pendientes
        self.juego.__movimientos_pendientes__ = [3, 5]
        self.assertTrue(self.juego.movimientos_disponibles())

    class StubDados:
        def __init__(self, d1, d2):
            self._d1 = d1
            self._d2 = d2
        def tirar(self):
            return (self._d1, self._d2)
        
    def test_tirar_dados_normales(self):
        self.juego.__dados__ = self.StubDados(3, 5)
        d1, d2 = self.juego.tirar_dados()
        self.assertEqual((d1, d2), (3, 5))
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [3, 5])

    def test_tirar_dados_dobles(self):
        self.juego.__dados__ = self.StubDados(4, 4)
        d1, d2 = self.juego.tirar_dados()
        self.assertEqual((d1, d2), (4, 4))
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [4, 4, 4, 4])

    def test_consumir_movimiento_valido(self):
        self.juego.__movimientos_pendientes__ = [3, 5]
        resultado = self.juego.consumir_movimiento(3)
        self.assertTrue(resultado)
        self.assertEqual(self.juego.obtener_movimientos_pendientes(), [5])



if __name__ == '__main__':
    import unittest
    unittest.main()