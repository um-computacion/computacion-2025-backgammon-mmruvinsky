from core.tablero import Tablero
from core.dados import Dados


class Backgammon:

    def __init__(self):
        self.__tablero__ = Tablero()
        self.__turno__ = 1  
      
    def cambiar_turno(self):
        self.__turno__ = -1 if self.__turno__ == 1 else -1

    def obtener_turno(self):
        return self.__turno__

    def mover(self, origen, valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras):
            jugador = self.__turno__  # 1 = blancas, -1 = negras
            indice_origen = origen - 1
            destino = indice_origen + jugador * valor_dado

            # Validaciones iniciales
            if indice_origen < 0 or indice_origen > 23:
                return False, "origen inválido", posiciones, fichas_barra_blancas, fichas_barra_negras

            if posiciones[indice_origen] * jugador <= 0:
                return False, "no hay fichas del jugador en el origen", posiciones, fichas_barra_blancas, fichas_barra_negras

            if destino < 0 or destino > 23:
                return False, "movimiento fuera del tablero", posiciones, fichas_barra_blancas, fichas_barra_negras

            valor_destino = posiciones[destino]

            # Movimiento permitido si está libre o ocupado por fichas del mismo jugador
            if abs(valor_destino) <= 1 or valor_destino * jugador >= 0:
                posiciones[indice_origen] -= jugador
                posiciones[destino] += jugador
                return True, "movió", posiciones, fichas_barra_blancas, fichas_barra_negras

            # Comer ficha contraria si solo hay una
            elif abs(valor_destino) == 1 and valor_destino * jugador < 0:
                posiciones[indice_origen] -= jugador
                posiciones[destino] = jugador
                if jugador == 1:
                    fichas_barra_negras += 1
                else:
                    fichas_barra_blancas += 1
                return True, "movió y comió", posiciones, fichas_barra_blancas, fichas_barra_negras

            # Bloqueado
            else:
                return False, "bloqueado", posiciones, fichas_barra_blancas, fichas_barra_negras



    


    