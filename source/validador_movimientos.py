from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos
from source.constantes import CASILLEROS

class ValidadorMovimientos:
    """
    Validar movimientos sin ejecutarlos.
    """
    
    def __init__(self, tablero: Tablero, gestor_turnos):
        """
        Inicializa el validador con sus dependencias.
        
        Args:
            tablero (Tablero): Referencia al tablero del juego
            gestor_turnos (GestorTurnos): Referencia al gestor de turnos
        """
        self.__tablero__ = Tablero()
        self.__gestor_turnos__ = gestor_turnos

    def validar_movimiento(self, origen: int, valor_dado: int) -> tuple[bool, str]:
        """
        Valida si un movimiento es legal según todas las reglas del backgammon.
        
        Args:
            origen (int): Índice 0-based de la posición de origen
            valor_dado (int): Valor del dado a usar (1-6)
        
        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
                            Si es_valido=True, mensaje_error=""
                            Si es_valido=False, mensaje_error contiene razón
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        posiciones = self.__tablero__.obtener_posiciones()
        
        # 1. Validar que el origen tenga fichas propias
        if not self._origen_valido(posiciones, origen, jugador):
            return False, "origen inválido o sin fichas propias"
        
        # 2. Calcular destino
        destino = origen + jugador * valor_dado
        
        # 3. Si es bear-off (fuera del tablero)
        if self._es_fuera(destino):
            return self._validar_bear_off(origen, valor_dado, jugador)
        
        # 4. Si es movimiento normal (dentro del tablero)
        valor_destino = posiciones[destino]
        
        if self._destino_bloqueado(valor_destino, jugador):
            return False, "posición de destino bloqueada"
        
        # Movimiento válido
        return True, ""

    def validar_entrada_barra(self, valor_dado: int) -> tuple[bool, str]:
        """
        Valida si es posible entrar desde la barra con el dado dado.
        
        Args:
            valor_dado (int): Valor del dado (1-6)
        
        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        
        try:
            destino_idx = self.indice_entrada(jugador, valor_dado)
        except ValueError as e:
            return False, str(e)
        
        # Validar que el destino esté dentro del tablero
        if self._es_fuera(destino_idx):
            return False, "movimiento fuera del tablero"
        
        posiciones = self.__tablero__.obtener_posiciones()
        valor_destino = posiciones[destino_idx]
        
        # Validar que no esté bloqueado
        if self._destino_bloqueado(valor_destino, jugador):
            return False, "posición de entrada bloqueada"
        
        return True, ""

    def indice_entrada(self, jugador: int, valor_dado: int) -> int:
        """
        Convierte el valor de un dado (1..6) en el índice de entrada (0..23) según el jugador.

        Args:
            jugador (int): 1 para blancas, -1 para negras.
            valor_dado (int): Valor del dado (1..6).

        Returns:
            int: Índice 0-based de la casilla de entrada correspondiente.

        Raises:
            ValueError: Si valor_dado no está en el rango 1..6.
        """
        if not 1 <= valor_dado <= 6:
            raise ValueError("dado inválido (1..6)")
        return valor_dado - 1 if jugador == 1 else CASILLEROS - valor_dado

    # ========== MÉTODOS PRIVADOS ==========

    def _validar_bear_off(self, origen: int, valor_dado: int, jugador: int) -> tuple[bool, str]:
        """
        Valida si un bear-off es legal.
        
        Args:
            origen (int): Índice 0-based del origen
            valor_dado (int): Valor del dado
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        # 1. Verificar que todas las fichas estén en home
        if not self._todas_en_home(jugador):
            return False, "no todas las fichas están en home"
        
        posiciones = self.__tablero__.obtener_posiciones()
        
        # 2. Calcular distancia necesaria
        needed = (CASILLEROS - origen) if jugador == 1 else (origen + 1)
        
        # 3. Valor insuficiente
        if valor_dado < needed:
            return False, "valor insuficiente para sacar la ficha"
        
        # 4. Overshoot: solo permitido si no hay fichas más adelantadas
        if valor_dado > needed:
            if jugador == 1:
                if any(posiciones[i] > 0 for i in range(origen + 1, CASILLEROS)):
                    return False, "debe mover ficha más adelantada"
            else:
                if any(posiciones[i] < 0 for i in range(0, origen)):
                    return False, "debe mover ficha más adelantada"
        
        return True, ""

    def _todas_en_home(self, jugador: int) -> bool:
        """
        Verifica si todas las fichas del jugador están en su home.
        
        Args:
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si todas las fichas están en home, False en caso contrario
        """
        pos = self.__tablero__.obtener_posiciones()
        if jugador == 1:  # blancas: home 18..23
            return all(x <= 0 for x in pos[:18])
        else:  # negras: home 0..5
            return all(x >= 0 for x in pos[6:])

    def _origen_valido(self, posiciones: list[int], origen_idx: int, jugador: int) -> bool:
        """
        Verifica que el origen contenga fichas del jugador.
        
        Args:
            posiciones (list[int]): Array de posiciones del tablero
            origen_idx (int): Índice del origen
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si hay fichas propias en el origen
        """
        return (0 <= origen_idx < CASILLEROS) and (posiciones[origen_idx] * jugador > 0)
    
    def _destino_bloqueado(self, valor_destino: int, jugador: int) -> bool:
        """
        Verifica si el destino está bloqueado por 2 o más fichas rivales.
        
        Args:
            valor_destino (int): Valor en la posición de destino
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si está bloqueado
        """
        return (valor_destino * jugador < 0) and (abs(valor_destino) >= 2)

    def _destino_es_blot_rival(self, valor_destino: int, jugador: int) -> bool:
        """
        Verifica si hay exactamente una ficha rival (blot) en el destino.
        
        Args:
            valor_destino (int): Valor en la posición de destino
            jugador (int): 1 para blancas, -1 para negras
        
        Returns:
            bool: True si hay un blot rival
        """
        return (valor_destino * jugador < 0) and (abs(valor_destino) == 1)
    
    def _es_fuera(self, idx: int) -> bool:
        """
        Verifica si un índice está fuera del tablero.
        
        Args:
            idx (int): Índice a verificar
        
        Returns:
            bool: True si está fuera del rango [0, 23]
        """
        return not (0 <= idx < CASILLEROS)