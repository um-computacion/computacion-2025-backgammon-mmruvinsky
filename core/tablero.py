
from core.constantes import CASILLEROS

class Tablero:
    def __init__(self):
        self.__posiciones__ = self.inicializar_posiciones()

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
    


