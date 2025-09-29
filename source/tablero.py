
from source.constantes import CASILLEROS

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

    def obtener_posiciones(self) -> list[int]:
        return list(self.__posiciones__)
    
    def obtener_barra(self) -> dict:
        return dict(self.__barra__)
    
    def obtener_fichas_fuera(self) -> dict:
        return dict(self.__fichas_fuera__)
    
    def hay_fichas_en_barra(self, color: str) -> bool:
        if color not in ['blancas', 'negras']:
            raise ValueError(f"Color inválido: {color}")
        return self.__barra__[color] > 0
    
    def obtener_ficha_en_posicion(self, posicion: int) -> int:
        if not 0 <= posicion < CASILLEROS:
            raise IndexError(f"Posición {posicion} fuera de rango [0, 23]")
        return self.__posiciones__[posicion]
    
    def _obtener_posiciones_ref(self) -> list[int]:
        """
        MÉTODO PROTEGIDO: Retorna REFERENCIA directa a posiciones.
        ⚠️ SOLO para uso interno de Backgammon.
        NO usar desde código externo.
        """
        return self.__posiciones__

    def _obtener_barra_ref(self) -> dict:
        """
        MÉTODO PROTEGIDO: Retorna REFERENCIA directa a barra.
        ⚠️ SOLO para uso interno de Backgammon.
        """
        return self.__barra__

    def _obtener_fichas_fuera_ref(self) -> dict:
        """
        MÉTODO PROTEGIDO: Retorna REFERENCIA directa a fichas fuera.
        ⚠️ SOLO para uso interno de Backgammon.
        """
        return self.__fichas_fuera__
    