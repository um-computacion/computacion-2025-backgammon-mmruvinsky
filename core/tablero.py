
from core.constantes import CASILLEROS

class Tablero:
    def __init__(self):
        self.__posiciones__ = self.inicializar_posiciones()
        self.__barra__ = { 'blancas': 0, 'negras': 0 }
        self.__fichas_fuera__ = { 'blancas': 0, 'negras': 0 }

    def inicializar_posiciones(self):
        posiciones = [0] * CASILLEROS
        posiciones[0] = 2   # blancas
        posiciones[11] = 5
        posiciones[16] = 3
        posiciones[18] = 5

        posiciones[23] = -2   # negras
        posiciones[12] = -5
        posiciones[7]  = -3
        posiciones[5]  = -5
        return posiciones
    
            # Numeración del tablero 0-indexada
        # (vista desde el jugador blanco)
        #
        #  23 22 21 20 19 18 | 17 16 15 14 13 12
        #  -2                | -5
        #                    |
        # -------------------|-------------------
        #                    |
        #  0  1  2  3  4  5  |  6  7  8  9 10 11
        #  +2                | +5

    