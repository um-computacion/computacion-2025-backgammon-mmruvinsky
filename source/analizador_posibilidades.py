from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos
from source.constantes import CASILLEROS


class AnalizadorPosibilidades:
    """
    Responsabilidad: Analizar qué movimientos son posibles sin ejecutarlos.
    SRP: Solo analiza y simula, no valida ni ejecuta movimientos reales.
    """
    
    def __init__(self, tablero: Tablero, gestor_turnos: GestorTurnos):
        """
        Inicializa el analizador con sus dependencias.
        
        Args:
            tablero (Tablero): Referencia al tablero del juego
            gestor_turnos (GestorTurnos): Referencia al gestor de turnos
        """
        self.__tablero__ = tablero
        self.__gestor_turnos__ = gestor_turnos

    def puede_usar_dado(self, valor_dado: int) -> bool:
        """
        Evalúa si existe al menos un movimiento válido con el dado dado.
        
        Args:
            valor_dado (int): Valor del dado a evaluar (1-6)
        
        Returns:
            bool: True si existe al menos un movimiento válido
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        pos = self.__tablero__.obtener_posiciones()
        
        # Prioridad: fichas en barra
        if self._hay_en_barra(jugador):
            return self._puede_entrar_desde_barra(valor_dado, jugador)
        
        # Revisar movimientos posibles desde cada posición
        for origen_idx in range(CASILLEROS):
            # Saltar si no hay fichas propias
            if pos[origen_idx] * jugador <= 0:
                continue
            
            destino_idx = origen_idx + jugador * valor_dado
            
            # Movimiento dentro del tablero
            if 0 <= destino_idx < CASILLEROS:
                if not self._destino_bloqueado(pos[destino_idx], jugador):
                    return True
            
            # Bear-off
            elif self._todas_en_home(jugador):
                if self._puede_hacer_bear_off(origen_idx, valor_dado, jugador, pos):
                    return True
        
        return False

    def puede_usar_ambos_dados(self, dado1: int, dado2: int) -> bool:
        """
        Verifica si es posible usar ambos dados en algún orden válido.
        
        Args:
            dado1 (int): Primer dado
            dado2 (int): Segundo dado
        
        Returns:
            bool: True si existe un orden que permita usar ambos dados
        """
        # Si son iguales (dobles), no aplica esta validación
        if dado1 == dado2:
            return True
        
        # Intentar en ambos órdenes
        return (self._puede_usar_dado_tras_simular(dado1, dado2) or 
                self._puede_usar_dado_tras_simular(dado2, dado1))

    def debe_usar_dado_mayor(self, movimientos_pendientes: list[int]) -> bool:
        """
        Verifica si debe usarse obligatoriamente el dado mayor.
        
        Regla: Si solo se puede usar uno de los dos dados, debe ser el mayor.
        
        Args:
            movimientos_pendientes (list[int]): Lista de dados pendientes
        
        Returns:
            bool: True si existe la obligación de usar el dado mayor
        """
        if len(movimientos_pendientes) != 2:
            return False
        
        dado1, dado2 = movimientos_pendientes
        
        # Si son dobles, no aplica
        if dado1 == dado2:
            return False
        
        puede_dado1 = self.puede_usar_dado(dado1)
        puede_dado2 = self.puede_usar_dado(dado2)
        puede_ambos = self.puede_usar_ambos_dados(dado1, dado2)
        
        # Si puede usar ambos, no hay restricción
        if puede_ambos:
            return False
        
        # Si solo puede usar uno de los dos, debe ser el mayor
        if puede_dado1 and puede_dado2:
            return True
        
        return False

    def hay_movimiento_posible(self, movimientos_pendientes: list[int]) -> bool:
        """
        Verifica si existe al menos un movimiento válido con los dados pendientes.
        
        Args:
            movimientos_pendientes (list[int]): Lista de dados pendientes
        
        Returns:
            bool: True si hay al menos un movimiento válido
        """
        if not movimientos_pendientes:
            return False
        
        # Verificar cada valor único en los dados pendientes
        for valor in set(movimientos_pendientes):
            if self.puede_usar_dado(valor):
                return True
        
        return False

    # ========== MÉTODOS PRIVADOS ==========

    def _puede_usar_dado_tras_simular(self, primer_dado: int, segundo_dado: int) -> bool:
        """
        Simula usar primer_dado y verifica si luego se puede usar segundo_dado.
        
        Args:
            primer_dado (int): Dado a simular primero
            segundo_dado (int): Dado a verificar después
        
        Returns:
            bool: True si tras usar primer_dado se puede usar segundo_dado
        """
        # Guardar estado original (backup para restaurar)
        pos_backup = self.__tablero__.obtener_posiciones()
        barra_backup = self.__tablero__.obtener_barra()
        
        try:
            # Simular mejor movimiento con primer_dado
            if self._simular_mejor_movimiento(primer_dado):
                # Verificar si se puede usar segundo_dado
                return self.puede_usar_dado(segundo_dado)
            return False
        finally:
            # Restaurar estado original
            self._restaurar_estado(pos_backup, barra_backup)

    def _simular_mejor_movimiento(self, valor_dado: int) -> bool:
        """
        Simula y aplica el mejor movimiento posible con el dado dado.
        
        Modifica el estado del tablero temporalmente (debe restaurarse después).
        
        Args:
            valor_dado (int): Valor del dado a simular
        
        Returns:
            bool: True si encontró y aplicó un movimiento válido
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        pos = self.__tablero__._obtener_posiciones_ref()
        
        # Prioridad: entrada desde barra
        if self._hay_en_barra(jugador):
            destino_idx = self._calcular_indice_entrada(jugador, valor_dado)
            if 0 <= destino_idx < CASILLEROS:
                if not self._destino_bloqueado(pos[destino_idx], jugador):
                    self._ejecutar_entrada_simulada(destino_idx, jugador)
                    return True
            return False
        
        # Buscar primer movimiento válido
        for origen_idx in range(CASILLEROS):
            if pos[origen_idx] * jugador <= 0:
                continue
            
            destino_idx = origen_idx + jugador * valor_dado
            
            # Movimiento dentro del tablero
            if 0 <= destino_idx < CASILLEROS:
                if not self._destino_bloqueado(pos[destino_idx], jugador):
                    self._ejecutar_movimiento_simulado(origen_idx, destino_idx, jugador)
                    return True
            
            # Bear-off
            elif self._todas_en_home(jugador):
                if self._puede_hacer_bear_off(origen_idx, valor_dado, jugador, pos):
                    pos[origen_idx] -= jugador
                    return True
        
        return False

    def _ejecutar_entrada_simulada(self, destino_idx: int, jugador: int):
        """
        Simula entrada desde la barra (modifica estado temporalmente).
        
        Args:
            destino_idx (int): Índice de destino
            jugador (int): 1 para blancas, -1 para negras
        """
        pos = self.__tablero__._obtener_posiciones_ref()
        barra = self.__tablero__._obtener_barra_ref()
        
        # Capturar si hay blot rival
        if self._es_blot_rival(pos[destino_idx], jugador):
            color_rival = "negras" if jugador == 1 else "blancas"
            barra[color_rival] += 1
            pos[destino_idx] = jugador
        else:
            pos[destino_idx] += jugador
        
        # Decrementar barra
        color = "blancas" if jugador == 1 else "negras"
        barra[color] -= 1

    def _ejecutar_movimiento_simulado(self, origen_idx: int, destino_idx: int, jugador: int):
        """
        Simula movimiento normal (modifica estado temporalmente).
        
        Args:
            origen_idx (int): Índice de origen
            destino_idx (int): Índice de destino
            jugador (int): 1 para blancas, -1 para negras
        """
        pos = self.__tablero__._obtener_posiciones_ref()
        barra = self.__tablero__._obtener_barra_ref()
        
        # Capturar si hay blot rival
        if self._es_blot_rival(pos[destino_idx], jugador):
            color_rival = "negras" if jugador == 1 else "blancas"
            barra[color_rival] += 1
            pos[destino_idx] = jugador
        else:
            pos[destino_idx] += jugador
        
        pos[origen_idx] -= jugador

    def _restaurar_estado(self, pos_backup: list[int], barra_backup: dict):
        """
        Restaura el estado del tablero después de una simulación.
        
        Args:
            pos_backup (list[int]): Backup de posiciones
            barra_backup (dict): Backup de barra
        """
        pos_ref = self.__tablero__._obtener_posiciones_ref()
        barra_ref = self.__tablero__._obtener_barra_ref()
        
        # Restaurar valores originales
        pos_ref[:] = pos_backup
        barra_ref.update(barra_backup)

    def _puede_entrar_desde_barra(self, valor_dado: int, jugador: int) -> bool:
        """
        Verifica si puede entrar desde la barra con el dado dado.
        
        Args:
            valor_dado (int): Valor del dado
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si puede entrar
        """
        destino_idx = self._calcular_indice_entrada(jugador, valor_dado)
        
        if not (0 <= destino_idx < CASILLEROS):
            return False
        
        pos = self.__tablero__.obtener_posiciones()
        return not self._destino_bloqueado(pos[destino_idx], jugador)

    def _puede_hacer_bear_off(self, origen_idx: int, valor_dado: int, 
                              jugador: int, pos: list[int]) -> bool:
        """
        Verifica si puede hacer bear-off desde el origen con el dado dado.
        
        Args:
            origen_idx (int): Índice de origen
            valor_dado (int): Valor del dado
            jugador (int): 1 para blancas, -1 para negras
            pos (list[int]): Array de posiciones
        
        Returns:
            bool: True si puede hacer bear-off
        """
        needed = (CASILLEROS - origen_idx) if jugador == 1 else (origen_idx + 1)
        
        # Distancia exacta
        if valor_dado == needed:
            return True
        
        # Overshoot: solo si no hay fichas más adelantadas
        if valor_dado > needed:
            if jugador == 1:
                return all(pos[i] <= 0 for i in range(origen_idx + 1, CASILLEROS))
            else:
                return all(pos[i] >= 0 for i in range(0, origen_idx))
        
        return False

    def _todas_en_home(self, jugador: int) -> bool:
        """
        Verifica si todas las fichas del jugador están en home.
        
        Args:
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si todas están en home
        """
        pos = self.__tablero__.obtener_posiciones()
        if jugador == 1:  # blancas: home 18..23
            return all(x <= 0 for x in pos[:18])
        else:  # negras: home 0..5
            return all(x >= 0 for x in pos[6:])

    def _hay_en_barra(self, jugador: int) -> bool:
        """
        Verifica si el jugador tiene fichas en la barra.
        
        Args:
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si hay fichas en la barra
        """
        barra = self.__tablero__.obtener_barra()
        color = "blancas" if jugador == 1 else "negras"
        return barra[color] > 0

    def _destino_bloqueado(self, valor_destino: int, jugador: int) -> bool:
        """
        Verifica si el destino está bloqueado por 2+ fichas rivales.
        
        Args:
            valor_destino (int): Valor en la posición
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si está bloqueado
        """
        return (valor_destino * jugador < 0) and (abs(valor_destino) >= 2)

    def _es_blot_rival(self, valor_destino: int, jugador: int) -> bool:
        """
        Verifica si hay exactamente una ficha rival (blot).
        
        Args:
            valor_destino (int): Valor en la posición
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si hay un blot rival
        """
        return (valor_destino * jugador < 0) and (abs(valor_destino) == 1)

    def _calcular_indice_entrada(self, jugador: int, valor_dado: int) -> int:
        """
        Calcula el índice de entrada desde la barra.
        
        Args:
            jugador (int): 1 para blancas, -1 para negras
            valor_dado (int): Valor del dado (1-6)
        
        Returns:
            int: Índice 0-based de entrada
        """
        return valor_dado - 1 if jugador == 1 else CASILLEROS - valor_dado