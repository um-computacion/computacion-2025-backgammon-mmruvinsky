from core.tablero import Tablero
from core.dados import Dados


class Backgammon:

    def __init__(self):
        self.__tablero__ = Tablero()
        self.__turno__ = 1  
      
    def cambiar_turno(self):
        self.__turno__ = -1 if self.__turno__ == 1 else 1

    def obtener_turno(self):
        return self.__turno__
    


    def mover(self, origen, valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras):
        jugador = self.__turno__  # 1 = blancas, -1 = negras

        # Regla: si hay fichas en barra, primero hay que entrar
        if (jugador == 1 and fichas_barra_blancas > 0) or (jugador == -1 and fichas_barra_negras > 0):
            return self.entrar_desde_barra(valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras)
        
        origen_idx = origen - 1
        destino_idx = origen_idx + jugador * valor_dado

        # 1) Validaciones de rango y presencia en origen
        if not (0 <= origen_idx < 24):
            return False, "origen inválido", posiciones, fichas_barra_blancas, fichas_barra_negras

        # En el origen debe haber fichas del jugador actual (signo compatible)
        if posiciones[origen_idx] * jugador <= 0:
            return False, "no hay fichas del jugador en el origen", posiciones, fichas_barra_blancas, fichas_barra_negras

        # Destino dentro del tablero
        if not (0 <= destino_idx < 24):
            return False, "movimiento fuera del tablero", posiciones, fichas_barra_blancas, fichas_barra_negras

        valor_destino = posiciones[destino_idx]

        # 2) BLOQUEADO: hay 2 o más fichas del rival en destino
        if valor_destino * jugador < 0 and abs(valor_destino) >= 2:
            return False, "bloqueado", posiciones, fichas_barra_blancas, fichas_barra_negras

        # 3) COMER: exactamente 1 ficha rival en destino
        if valor_destino * jugador < 0 and abs(valor_destino) == 1:
            # sacar del origen una del jugador
            posiciones[origen_idx] -= jugador
            # en destino queda 1 del jugador (la rival va a la barra)
            posiciones[destino_idx] = jugador
            if jugador == 1:
                fichas_barra_negras += 1
            else:
                fichas_barra_blancas += 1
            return True, "movió y comió", posiciones, fichas_barra_blancas, fichas_barra_negras

        # 4) MOVER NORMAL: destino vacío (0) o con fichas propias (mismo signo)
        posiciones[origen_idx] -= jugador
        posiciones[destino_idx] += jugador
        return True, "movió", posiciones, fichas_barra_blancas, fichas_barra_negras
    


    def entrar_desde_barra(self, valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras):
        jugador = self.__turno__
        fb, fn = fichas_barra_blancas, fichas_barra_negras

        # 1) Verificar que haya fichas del jugador en barra
        if jugador == 1 and fb <= 0:
            return False, "sin_fichas_en_barra", posiciones, fb, fn
        if jugador == -1 and fn <= 0:
            return False, "sin_fichas_en_barra", posiciones, fb, fn

        # 2) Calcular punto de entrada según el dado
        destino_idx = self._indice_entrada(jugador, valor_dado)
        if not (0 <= destino_idx < 24):
            return False, "movimiento fuera del tablero", posiciones, fb, fn

        valor_destino = posiciones[destino_idx]

        # 3) Bloqueado si hay 2+ rivales en destino
        if valor_destino * jugador < 0 and abs(valor_destino) >= 2:
            return False, "Bloqueado barra", posiciones, fb, fn

        # 4) Entrar: comer si hay 1 rival, si no apilar/colocar
        if valor_destino * jugador < 0 and abs(valor_destino) == 1:
            # comer
            if jugador == 1:
                fn += 1                       
            else:
                fb += 1                       
            posiciones[destino_idx] = jugador 
        else:
            # vacío o propias
            posiciones[destino_idx] += jugador

        # 5) Decrementar la barra del que entra
        if jugador == 1:
            fb -= 1
        else:
            fn -= 1

        return True, "entró", posiciones, fb, fn
    

    
    def _indice_entrada(self, jugador, valor_dado):

        if jugador == 1:
            # Blancas entran desde el punto 1 al 6 (índices 0 a 5)
            return valor_dado - 1
        else:
            # Negras entran desde el punto 24 al 19 (índices 23 a 18)
            return 24 - valor_dado



    