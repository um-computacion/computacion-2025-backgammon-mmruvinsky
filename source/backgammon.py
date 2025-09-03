from source.tablero import Tablero
from source.dados import Dados


class Backgammon:

    def __init__(self):
        self.__tablero__ = Tablero()
        self.__turno__ = 1  
        self.__fichas_barra_blancas__ = 0
        self.__fichas_barra_negras__ = 0
        self.__dados__ = Dados()
        self.__movimientos_pendientes__ = []
      
    def cambiar_turno(self):
        self.__turno__ = -1 if self.__turno__ == 1 else 1

    def obtener_turno(self):
        return self.__turno__
    
    # ---------- Helpers internos ----------
    def __indice_entrada__(self, jugador: int, valor_dado: int) -> int:
        if not 1 <= valor_dado <= 6:
            raise ValueError("dado inválido (1..6)")
        return valor_dado - 1 if jugador == 1 else 24 - valor_dado

    def __hay_en_barra__(self, jugador: int) -> bool:
        return (self.__fichas_barra_blancas__ > 0) if jugador == 1 else (self.__fichas_barra_negras__ > 0)
    
    #---------------Lógica dados----------------------
    def tirar_dados(self) -> tuple[int, int]:
        d1, d2 = self.__dados__.tirar()

        # Validación 1: Dobles
        if d1 == d2:
            self.__movimientos_pendientes__ = [d1] * 4
        else:
            self.__movimientos_pendientes__ = [d1, d2]

        return d1, d2
    
    def obtener_movimientos_pendientes(self) -> list[int]:
        #getter movimientos disponibles
        return list(self.__movimientos_pendientes__)
    
    def consumir_movimiento(self, valor: int) -> bool:
        # Validación: el valor está en los movimientos pendientes
        if valor in self.__movimientos_pendientes__:
            self.__movimientos_pendientes__.remove(valor)
            return True
        return False
    
    def movimientos_disponibles(self) -> bool:
       return bool(self.__movimientos_pendientes__)

    def finalizar_tirada(self):
        # Limpiar movimientos pendientes y cambiar turno
        self.__movimientos_pendientes__.clear()
        self.cambiar_turno()
    
    #---------------Lógica movimiento----------------------
    def mover(self, origen: int, valor_dado: int):
        jugador = self.__turno__ 
        posiciones = self.__tablero__.__posiciones__  

        # Validación 0: Validar que el dado esté disponible en esta tirada
        if valor_dado not in self.__movimientos_pendientes__:
           return False, "dado no disponible"

        # Validación 1: existen fichas en barra?
        if self.__hay_en_barra__(jugador):
            ok, msg = self.entrar_desde_barra(valor_dado)
            if ok:
                self.consumir_movimiento(valor_dado)
            return ok, msg
            
        origen_idx = origen - 1
        destino_idx = origen_idx + jugador * valor_dado

        # Validación 2: origen dentro del tablero
        if not (0 <= origen_idx < 24):
                raise ValueError("origen inválido (1..24)")

        # Validación 3: Turno y fichas en origen compatibles
        if posiciones[origen_idx] * jugador <= 0:
                return False, "no hay fichas del jugador en el origen"

        # Validación 4: destino dentro del tablero
        if not (0 <= destino_idx < 24):
                return False, "movimiento fuera del tablero"

        valor_destino = posiciones[destino_idx]

        # Validación 5: Destino bloqueado (2+ fichas rivales)
        if valor_destino * jugador < 0 and abs(valor_destino) >= 2:
                return False, "posición de destino bloqueada"

        # COMER: exactamente 1 ficha rival en destino
        if valor_destino * jugador < 0 and abs(valor_destino) == 1:
            posiciones[origen_idx] -= jugador
            posiciones[destino_idx] = jugador
            if jugador == 1:
                self.__fichas_barra_negras__ += 1
            else:
                self.__fichas_barra_blancas__ += 1
            self.consumir_movimiento(valor_dado)
            return True, "movió y comió"

        # MOVER NORMAL: destino vacío (0) o con fichas propias (mismo signo)
        posiciones[origen_idx] -= jugador
        posiciones[destino_idx] += jugador
        self.consumir_movimiento(valor_dado)
        return True, "movió"


    def entrar_desde_barra(self, valor_dado: int):
        jugador = self.__turno__
        posiciones = self.__tablero__.__posiciones__
        destino_idx = self.__indice_entrada__(jugador, valor_dado)

        # (Asume que ya existen fichas en la barra por la validación previa)

        # Validación 1: Destino dentro del tablero
        if not (0 <= destino_idx < 24):
            return False, "movimiento fuera del tablero"

        valor_destino = posiciones[destino_idx]

        # Validación 2: Destino bloqueado (2+ fichas rivales)
        if valor_destino * jugador < 0 and abs(valor_destino) >= 2:
            return False, "posición de destino bloqueada"

        # COMER: exactamente 1 ficha rival en destino
        if valor_destino * jugador < 0 and abs(valor_destino) == 1:
            if jugador == 1:
               self.__fichas_barra_negras__ += 1
            else:
                self.__fichas_barra_blancas__ += 1                     
            posiciones[destino_idx] = jugador 
        else:
            posiciones[destino_idx] += jugador

        # Decrementar la barra del que entra
        if jugador == 1:
            self.__fichas_barra_blancas__ -= 1
        else:
            self.__fichas_barra_negras__ -= 1

        return True, "entró"
    









    