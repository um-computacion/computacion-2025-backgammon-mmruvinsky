from core.tablero import Tablero
from core.dados import Dados


class Backgammon:

    def __init__(self):
        self.__tablero__ = Tablero()
        self.__turno__ = 1  
      
    def cambiar_turno(self):
        self.__turno__ = 2 if self.__turno__ == 1 else 1

    def obtener_turno(self):
        return self.__turno__
    
    def entrar_desde_barra_blancas(valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras):
    # posiciones: lista de 24 ints (0-index). + = blancas, - = negras.
    # valor_dado ∈ {1..6}
        destino = valor_dado - 1         # índices 23..18  (puntos 24..19)
        valor_destino = posiciones[destino]

        if  4 >= valor_destino >= 0:
            # libre o ocupado por blancas
            posiciones[destino] = valor_destino + 1
            fichas_barra_blancas -= 1
            return True, "entró", posiciones, fichas_barra_blancas, fichas_barra_negras

        elif valor_destino == -1:
            # comer negro
            posiciones[destino] = 1        # ahora hay 1 blanca
            fichas_barra_blancas -= 1
            fichas_barra_negras += 1       # la negra va a la barra
            return True, "entró y comió", posiciones, fichas_barra_blancas, fichas_barra_negras

        else:
            # valor_destino <= -2: punto bloqueado por negras
            return False, "bloqueado", posiciones, fichas_barra_blancas, fichas_barra_negras

    def entrar_desde_barra_negras(valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras):
        # posiciones: lista de 24 ints (0-index). + = blancas, - = negras.
        # valor_dado ∈ {1..6}
            destino = 24 - valor_dado          # índices 23..18  (puntos 24..19)
            valor_destino = posiciones[destino]

            if  -4 <= valor_destino <= 0:
                # libre o ocupado por negras
                posiciones[destino] = valor_destino + 1
                fichas_barra_negras -= 1
                return True, "entró", posiciones, fichas_barra_blancas, fichas_barra_negras

            elif valor_destino == 1:
                # comer blanca
                posiciones[destino] = -1        # ahora hay 1 negra
                fichas_barra_blancas += 1
                fichas_barra_negras -= 1       # la blanca va a la barra
                return True, "entró y comió", posiciones, fichas_barra_blancas, fichas_barra_negras

            else:
                # valor_destino >= 2: punto bloqueado por blancas
                return False, "bloqueado", posiciones, fichas_barra_blancas, fichas_barra_negras
            
    def mover_blancas(origen, valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras):
        # posiciones: lista de 24 ints (0-index). + = blancas, - = negras.
        # origen ∈ {1..24}
        # valor_dado ∈ {1..6}
        indice_origen = origen - 1
        destino = origen + valor_dado - 1
        if indice_origen < 0 or indice_origen > 23:
            return False, "origen inválido", posiciones, fichas_barra_blancas, fichas_barra_negras
        if posiciones[indice_origen] <= 0:
            return False, "no hay blancas en el origen", posiciones, fichas_barra_blancas, fichas_barra_negras
        if destino > 23:
            return False, "movimiento fuera del tablero", posiciones, fichas_barra_blancas, fichas_barra_negras
        valor_destino = posiciones[destino]
        if 4 >= valor_destino >= 0:
            # libre o ocupado por blancas
            posiciones[indice_origen] -= 1
            posiciones[destino] = valor_destino + 1
            return True, "movió", posiciones, fichas_barra_blancas, fichas_barra_negras
        elif valor_destino == -1:
            posiciones[indice_origen] -= 1
            posiciones[destino] = 1        # ahora hay 1 blanca
            fichas_barra_negras += 1       # la negra va a la barra
            return True, "movió y comió", posiciones, fichas_barra_blancas, fichas_barra_negras
        else:
            # valor_destino <= -2: punto bloqueado por negras
            return False, "bloqueado", posiciones, fichas_barra_blancas, fichas_barra_negras    


    def mover_negras(origen, valor_dado, posiciones, fichas_barra_blancas, fichas_barra_negras):
        # posiciones: lista de 24 ints (0-index). + = blancas, - = negras.
        # origen ∈ {1..24}
        # valor_dado ∈ {1..6}
        indice_origen = origen - 1
        destino = origen - valor_dado - 1
        if indice_origen < 0 or indice_origen > 23:
            return False, "origen inválido", posiciones, fichas_barra_blancas, fichas_barra_negras
        if posiciones[indice_origen] >= 0:
            return False, "no hay negras en el origen", posiciones, fichas_barra_blancas, fichas_barra_negras
        if destino < 0:
            return False, "movimiento fuera del tablero", posiciones, fichas_barra_blancas, fichas_barra_negras
        valor_destino = posiciones[destino]
        if -4 <= valor_destino <= 0:
            # libre o ocupado por negras
            posiciones[indice_origen] += 1
            posiciones[destino] = valor_destino - 1
            return True, "movió", posiciones, fichas_barra_blancas, fichas_barra_negras
        elif valor_destino == 1:
            posiciones[indice_origen] += 1
            posiciones[destino] = -1        # ahora hay 1 negra
            fichas_barra_blancas += 1       # la blanca va a la barra
            return True, "movió y comió", posiciones, fichas_barra_blancas, fichas_barra_negras
        else:
            # valor_destino >= 2: punto bloqueado por blancas
            return False, "bloqueado", posiciones, fichas_barra_blancas, fichas_barra_negras





    


    