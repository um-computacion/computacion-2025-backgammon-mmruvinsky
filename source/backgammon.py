from source.tablero import Tablero
from source.dados import Dados
from source.excepciones import *
from source.constantes import CASILLEROS

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
        if self.__turno__ == 1:
            return "blancas"
        else:   
            return "negras"
    
    # ---------- Helpers internos ----------
    def __indice_entrada__(self, jugador: int, valor_dado: int) -> int:
        # Convierte el valor del dado (1..6) en el índice de la posición de entrada (0..23) según el jugador
        if not 1 <= valor_dado <= 6:
            raise ValueError("dado inválido (1..6)")
        return valor_dado - 1 if jugador == 1 else CASILLEROS - valor_dado

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
        return not (0 <= idx < CASILLEROS)

    def _destino_bloqueado(self, valor_destino: int, jugador: int) -> bool:
        # True si hay 2+ fichas rivales en el destino
        return (valor_destino * jugador < 0) and (abs(valor_destino) >= 2)

    def _destino_es_blot_rival(self, valor_destino: int, jugador: int) -> bool:
        # True si hay exactamente 1 ficha rival en el destino (blot)
        return (valor_destino * jugador < 0) and (abs(valor_destino) == 1)
    
    def _origen_valido(self, posiciones: list[int], origen_idx: int, jugador: int) -> bool:
        # True si el índice es válido y hay fichas del jugador en el origen."""
        return (0 <= origen_idx < CASILLEROS) and (posiciones[origen_idx] * jugador > 0)
    
    def _simular_mejor_movimiento(self, valor_dado: int) -> bool:
        # Simula el mejor movimiento posible con un dado
        jugador = self.__turno__
        pos = self.__tablero__.__posiciones__
        
        # Prioridad: barra
        if self.__hay_en_barra__(jugador):
            try:
                destino_idx = self.__indice_entrada__(jugador, valor_dado)
                if not self._es_fuera(destino_idx):
                    val_dest = pos[destino_idx]
                    if not self._destino_bloqueado(val_dest, jugador):
                        self._ejecutar_entrada_simulada(destino_idx)
                        return True
            except:
                pass
            return False
        
        # Buscar primer movimiento válido
        for origen_idx in range(CASILLEROS):
            if pos[origen_idx] * jugador <= 0:
                continue
                
            destino_idx = origen_idx + jugador * valor_dado
            
            if 0 <= destino_idx < CASILLEROS:
                val_dest = pos[destino_idx]
                if not self._destino_bloqueado(val_dest, jugador):
                    self._ejecutar_movimiento_simulado(origen_idx, destino_idx)
                    return True
            
            elif self.__todas_en_home__(jugador) and self._puede_hacer_bear_off(origen_idx, valor_dado):
                pos[origen_idx] -= jugador
                return True
        
        return False

    def _puede_hacer_bear_off(self, origen_idx: int, valor_dado: int) -> bool:
        # Verifica si se puede hacer bear-off desde una posición
        jugador = self.__turno__
        pos = self.__tablero__.__posiciones__
        
        needed = (CASILLEROS - origen_idx) if jugador == 1 else (origen_idx + 1)
        
        if valor_dado == needed:
            return True
        
        if valor_dado > needed:
            # Overshoot: solo si no hay fichas más adelantadas
            if jugador == 1:
                return all(pos[i] <= 0 for i in range(origen_idx + 1, CASILLEROS))
            else:
                return all(pos[i] >= 0 for i in range(0, origen_idx))
        
        return False

    def _ejecutar_entrada_simulada(self, destino_idx: int):
            # Ejecuta entrada desde barra en simulación
            jugador = self.__turno__
            pos = self.__tablero__.__posiciones__
            barra = self.__tablero__.__barra__
            
            if self._destino_es_blot_rival(pos[destino_idx], jugador):
                if jugador == 1:
                    barra['negras'] += 1
                else:
                    barra['blancas'] += 1
                pos[destino_idx] = jugador
            else:
                pos[destino_idx] += jugador
            
            if jugador == 1:
                barra['blancas'] -= 1
            else:
                barra['negras'] -= 1

    def _ejecutar_movimiento_simulado(self, origen_idx: int, destino_idx: int):
            # Ejecuta movimiento normal en simulación
            jugador = self.__turno__
            pos = self.__tablero__.__posiciones__
            barra = self.__tablero__.__barra__
            
            if self._destino_es_blot_rival(pos[destino_idx], jugador):
                if jugador == 1:
                    barra['negras'] += 1
                else:
                    barra['blancas'] += 1
                pos[destino_idx] = jugador
            else:
                pos[destino_idx] += jugador
            
            pos[origen_idx] -= jugador
        
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
    
    def puede_usar_ambos_dados(self) -> bool:
        # Verifica si es posible usar ambos dados en la tirada actual
        if len(self.__movimientos_pendientes__) != 2:
            return True  # Dobles o un solo dado - no aplica
        
        if self.__movimientos_pendientes__[0] == self.__movimientos_pendientes__[1]:
            return True  # Son dobles - no aplica
        
        # Verificar si puede usar ambos dados en cualquier orden
        dado1, dado2 = self.__movimientos_pendientes__
        
        return (self._puede_usar_dado(dado1) and self._puede_usar_dado_tras_simular(dado1, dado2)) or \
            (self._puede_usar_dado(dado2) and self._puede_usar_dado_tras_simular(dado2, dado1))

    def _puede_usar_dado(self, valor_dado: int) -> bool:
        # Verifica si se puede usar un dado específico en el estado actual
        jugador = self.__turno__
        pos = self.__tablero__.__posiciones__
        
        # Prioridad: fichas en barra
        if self.__hay_en_barra__(jugador):
            try:
                destino_idx = self.__indice_entrada__(jugador, valor_dado)
                if not self._es_fuera(destino_idx):
                    val_dest = pos[destino_idx]
                    return not self._destino_bloqueado(val_dest, jugador)
            except:
                return False
            return False
        
        # Revisar movimientos posibles
        for origen_idx in range(CASILLEROS):
            if pos[origen_idx] * jugador <= 0:
                continue
                
            destino_idx = origen_idx + jugador * valor_dado
            
            # Movimiento dentro del tablero
            if 0 <= destino_idx < CASILLEROS:
                val_dest = pos[destino_idx]
                if not self._destino_bloqueado(val_dest, jugador):
                    return True
            
            # Bear-off
            elif self.__todas_en_home__(jugador):
                if self._puede_hacer_bear_off(origen_idx, valor_dado):
                    return True
        
        return False

    def _puede_usar_dado_tras_simular(self, primer_dado: int, segundo_dado: int) -> bool:
        # Simula usar el primer dado y verifica si después se puede usar el segundo
        # Guardar estado
        pos_backup = self.__tablero__.__posiciones__.copy()
        barra_backup = self.__tablero__.__barra__.copy()
        
        try:
            # Intentar el mejor movimiento con primer_dado
            if self._simular_mejor_movimiento(primer_dado):
                # Verificar si se puede usar el segundo
                return self._puede_usar_dado(segundo_dado)
            return False
        finally:
            # Restaurar estado
            self.__tablero__.__posiciones__ = pos_backup
            self.__tablero__.__barra__ = barra_backup

    def debe_usar_dado_mayor(self) -> bool:
        # Verifica si debe usar el dado mayor cuando solo se puede usar uno
        if len(self.__movimientos_pendientes__) != 2:
            return False
        
        dado1, dado2 = self.__movimientos_pendientes__

        if dado1 == dado2:
            return False  # Son dobles
        
        puede_dado1 = self._puede_usar_dado(dado1)
        puede_dado2 = self._puede_usar_dado(dado2)
        puede_ambos = self.puede_usar_ambos_dados()
        
        # Si puede usar ambos, no hay restricción
        if puede_ambos:
            return False
        
        # Si solo puede usar uno de los dos, debe ser el mayor
        if puede_dado1 and puede_dado2:
            return True  # Debe elegir el mayor
        
        return False
    
    #---------------Lógica movimiento----------------------
    def finalizar_tirada(self):
        # Limpiar movimientos pendientes y cambiar turno
        self.__movimientos_pendientes__.clear()
        self.cambiar_turno()
    
    def mover(self, origen: int, valor_dado: int) -> str:
        jugador = self.__turno__ 
        posiciones = self.__tablero__.__posiciones__  
               
        if self.debe_usar_dado_mayor():
            dado_mayor = max(self.__movimientos_pendientes__)
            if valor_dado != dado_mayor:
                raise DadoNoDisponibleError(f"debe usar el dado mayor ({dado_mayor})")

        # Validación prioridad fichas en barra
        if self.__hay_en_barra__(jugador):
            mensaje = self.entrar_desde_barra(valor_dado)
            self.consumir_movimiento(valor_dado)
            return mensaje
            
        origen_idx = origen - 1
        destino_idx = origen_idx + jugador * valor_dado

        # Validación origen válido
        if not self._origen_valido(posiciones, origen_idx, jugador): 
            raise OrigenInvalidoError("origen inválido o sin fichas propias")    

        # INTENTAR BEAR OFF (sacar ficha)
        if destino_idx < 0 or destino_idx >= CASILLEROS:
            mensaje = self.__intentar_bear_off__(origen_idx, valor_dado)
            return mensaje

        valor_destino = posiciones[destino_idx]

        # Validación destino bloqueado (2+ fichas rivales)
        if self._destino_bloqueado(valor_destino, jugador): 
            raise DestinoBloquedoError("posición de destino bloqueada")
        
        # Validación que el dado esté disponible en esta tirada
        if self.__movimientos_pendientes__ and (valor_dado not in self.__movimientos_pendientes__):
            raise DadoNoDisponibleError("dado no disponible para este movimiento")
        
        # COMER: exactamente 1 ficha rival en destino 
        if self._destino_es_blot_rival(valor_destino, jugador): 
            posiciones[origen_idx] -= jugador
            posiciones[destino_idx] = jugador
            barra = self.__tablero__.__barra__          
            if jugador == 1:
                barra['negras'] += 1
            else:
                barra['blancas'] += 1

            self.consumir_movimiento(valor_dado)
            return "movió y comió"

        # MOVER NORMAL: destino vacío (0) o con fichas propias (mismo signo)
        posiciones[origen_idx] -= jugador
        posiciones[destino_idx] += jugador
        self.consumir_movimiento(valor_dado)
        return "movió"

    def entrar_desde_barra(self, valor_dado: int) -> str:
        #Lógica para entrar desde la barra
        jugador = self.__turno__
        posiciones = self.__tablero__.__posiciones__
        destino_idx = self.__indice_entrada__(jugador, valor_dado)

        # (Asume que ya existen fichas en la barra por la validación previa)
        # Validación: destino dentro del tablero
        if self._es_fuera(destino_idx): 
            raise MovimientoInvalidoError("movimiento fuera del tablero")

        valor_destino = posiciones[destino_idx]

        # Validación destino bloqueado (2+ fichas rivales)
        if self._destino_bloqueado(valor_destino, jugador): 
            raise DestinoBloquedoError("posición de destino bloqueada")

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

        return "entró"
    
    def __intentar_bear_off__(self, origen_idx: int, valor_dado: int) -> str:
        # Lógica para sacar ficha (bear off)
        jugador = self.__turno__
        pos = self.__tablero__.__posiciones__

        if not self.__todas_en_home__(jugador):
            raise BearOffInvalidoError("no todas las fichas están en home")
        
        needed = (24 - origen_idx) if jugador == 1 else (origen_idx + 1)

        #lógica overshoot
        if valor_dado < needed:
            raise BearOffInvalidoError("valor insuficiente para sacar la ficha")
        
        if valor_dado > needed:
            # Solo permitir overshoot si no hay fichas más adelantadas
            if jugador == 1:  # blancas
                if any(pos[i] > 0 for i in range(origen_idx + 1, 24)):
                    raise BearOffInvalidoError("debe mover ficha más adelantada")
            else:  # negras
                if any(pos[i] < 0 for i in range(0, origen_idx)):
                    raise BearOffInvalidoError("debe mover ficha más adelantada")

        # Ejecutar sacar ficha
        pos[origen_idx] -= jugador
        color = "blancas" if jugador == 1 else "negras"
        self.__tablero__.__fichas_fuera__[color] += 1

        self.consumir_movimiento(valor_dado)

        if self.__tablero__.__fichas_fuera__[color] == 15:
            return f"juego terminado! {color.capitalize()} ganaron"

        return "sacó ficha"
    
    def hay_movimiento_posible(self) -> bool:
        if not self.__movimientos_pendientes__:
            return False
        
        # Verificar cada valor único en los dados pendientes
        for valor in set(self.__movimientos_pendientes__):
            if self._puede_usar_dado(valor):
                return True
        
        return False

    
    
    

    


    









    