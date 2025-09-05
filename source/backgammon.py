from source.tablero import Tablero
from source.dados import Dados


class Backgammon:

    def __init__(self):
        self.__tablero__ = Tablero()
        self.__turno__ = 1  # 1 = blancas, -1 = negras
        self.__dados__ = Dados() 
        self.__movimientos_pendientes__ = []

    # ---------- Lógica turnos ---------- 
    def cambiar_turno(self):
        self.__turno__ = -1 if self.__turno__ == 1 else 1

    def obtener_turno(self):
        return self.__turno__
    
    # ---------- Helpers internos ----------
    def __indice_entrada__(self, jugador: int, valor_dado: int) -> int:
        # Convierte el valor del dado (1..6) en el índice de la posición de entrada (0..23) según el jugador
        if not 1 <= valor_dado <= 6:
            raise ValueError("dado inválido (1..6)")
        return valor_dado - 1 if jugador == 1 else 24 - valor_dado

    def __hay_en_barra__(self, jugador: int) -> bool:
        # Verifica si hay fichas en la barra del jugador actual
        barra = self.__tablero__.__barra__
        return (barra['blancas'] > 0) if jugador == 1 else (barra['negras'] > 0)
    
    def __todas_en_home__(self, jugador: int) -> bool:
        # Verifica si todas las fichas del jugador están en su zona de home para poder hacer bear off
        pos = self.__tablero__.__posiciones__
        if jugador == 1:  # blancas: home 18..23
            return all(x <= 0 for x in pos[:18])  # antes de 18 no hay blancas
        else:            # negras: home 0..5
            return all(x >= 0 for x in pos[6:])   # después de 5 no hay negras
        
    def obtener_movimientos_pendientes(self) -> list[int]:
        # Getter movimientos disponibles
        return list(self.__movimientos_pendientes__)
    
    def movimientos_disponibles(self) -> bool:
       # Indica si quedan movimientos pendientes en la tirada actual
       return bool(self.__movimientos_pendientes__)
    
    def _es_fuera(self, idx: int) -> bool:
        # True si el índice está fuera del tablero (0..23)
        return not (0 <= idx < 24)

    def _destino_bloqueado(self, valor_destino: int, jugador: int) -> bool:
        # True si hay 2+ fichas rivales en el destino
        return (valor_destino * jugador < 0) and (abs(valor_destino) >= 2)

    def _destino_es_blot_rival(self, valor_destino: int, jugador: int) -> bool:
        # True si hay exactamente 1 ficha rival en el destino (blot)
        return (valor_destino * jugador < 0) and (abs(valor_destino) == 1)
    
    def _origen_valido(self, posiciones: list[int], origen_idx: int, jugador: int) -> bool:
        # True si el índice es válido y hay fichas del jugador en el origen."""
        return (0 <= origen_idx < 24) and (posiciones[origen_idx] * jugador > 0)
    
    #---------------Lógica dados----------------------
    def tirar_dados(self) -> tuple[int, int]:
        d1, d2 = self.__dados__.tirar()

        # Validación dobles
        if d1 == d2: 
            self.__movimientos_pendientes__ = [d1] * 4
        else:
            self.__movimientos_pendientes__ = [d1, d2]

        return d1, d2
    
    def consumir_movimiento(self, valor: int) -> bool:
        # Validación: el valor está en los movimientos pendientes
        if valor in self.__movimientos_pendientes__:
            self.__movimientos_pendientes__.remove(valor)
            return True
        return False
    
    #---------------Lógica movimiento----------------------
    def finalizar_tirada(self):
        # Limpiar movimientos pendientes y cambiar turno
        self.__movimientos_pendientes__.clear()
        self.cambiar_turno()
    
    def mover(self, origen: int, valor_dado: int):
        jugador = self.__turno__ 
        posiciones = self.__tablero__.__posiciones__  

        # Validación prioridad fichas en barra
        if self.__hay_en_barra__(jugador):
            ok, msg = self.entrar_desde_barra(valor_dado)
            if ok:
                self.consumir_movimiento(valor_dado)
            return ok, msg
            
        origen_idx = origen - 1
        destino_idx = origen_idx + jugador * valor_dado

        # Validación origen válido
        if not self._origen_valido(posiciones, origen_idx, jugador): 
            return False, "origen inválido o sin fichas del jugador"

        # INTENTAR BEAR OFF (sacar ficha)
        if destino_idx < 0 or destino_idx >= 24:
            ok, msg = self.__intentar_bear_off__(origen_idx, valor_dado)
            return ok, msg

        # Validación destino dentro del tablero 
        if self._es_fuera(destino_idx):  
            return False, "movimiento fuera del tablero"

        valor_destino = posiciones[destino_idx]

        # Validación destino bloqueado (2+ fichas rivales)
        if self._destino_bloqueado(valor_destino, jugador): 
            return False, "posición de destino bloqueada"
        
        # Validación que el dado esté disponible en esta tirada
        if self.__movimientos_pendientes__ and (valor_dado not in self.__movimientos_pendientes__):
            return False, "dado no disponible"
        
        # COMER: exactamente 1 ficha rival en destino 
        if self._destino_es_blot_rival(valor_destino, jugador): 
            posiciones[origen_idx] -= jugador
            posiciones[destino_idx] = jugador
            barra = self.__tablero__.__barra__          
            if jugador == 1:
                barra['negras'] += 1
            else:
                barra['blancas'] += 1

            if self.__movimientos_pendientes__:
                self.consumir_movimiento(valor_dado)
            return True, "movió y comió"

        # MOVER NORMAL: destino vacío (0) o con fichas propias (mismo signo)
        posiciones[origen_idx] -= jugador
        posiciones[destino_idx] += jugador
        if self.__movimientos_pendientes__:
            self.consumir_movimiento(valor_dado)
        return True, "movió"

    def entrar_desde_barra(self, valor_dado: int):
        #Lógica para entrar desde la barra
        jugador = self.__turno__
        posiciones = self.__tablero__.__posiciones__
        destino_idx = self.__indice_entrada__(jugador, valor_dado)

        # (Asume que ya existen fichas en la barra por la validación previa)
        # Validación: destino dentro del tablero
        if self._es_fuera(destino_idx): 
            return False, "movimiento fuera del tablero"

        valor_destino = posiciones[destino_idx]

        # Validación destino bloqueado (2+ fichas rivales)
        if self._destino_bloqueado(valor_destino, jugador): 
            return False, "posición de destino bloqueada"

        barra = self.__tablero__.__barra__
        # COMER: exactamente 1 ficha rival en destino 
        if self._destino_es_blot_rival(valor_destino, jugador):
            if jugador == 1:
                barra['negras'] += 1
            else:
                barra['blancas'] += 1
            posiciones[destino_idx] = jugador
        else:
            posiciones[destino_idx] += jugador

        # Decrementar la barra del que entra
        if jugador == 1:
            barra['blancas'] -= 1
        else:
            barra['negras'] -= 1

        return True, "entró"
    
    def __intentar_bear_off__(self, origen_idx: int, valor_dado: int) -> tuple[bool, str]:
        # Lógica para sacar ficha (bear off)
        jugador = self.__turno__
        pos = self.__tablero__.__posiciones__

        if not self.__todas_en_home__(jugador):
            return False, "para sacar, todas las fichas deben estar en home"

        # Ejecutar sacar ficha
        pos[origen_idx] -= jugador
        color = "blancas" if jugador == 1 else "negras"
        self.__tablero__.__fichas_fuera__[color] += 1

        if self.__movimientos_pendientes__ and valor_dado in self.__movimientos_pendientes__:
            self.consumir_movimiento(valor_dado)

        if self.__tablero__.__fichas_fuera__[color] == 15:
            return True, f"juego terminado! {color.capitalize()} ganaron"

        return True, "sacó ficha"
    
    
    

    


    









    