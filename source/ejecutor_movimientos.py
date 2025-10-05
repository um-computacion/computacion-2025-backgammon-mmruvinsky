from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos  
from source.constantes import CASILLEROS


class EjecutorMovimientos:
    """
    Ejecutar movimientos en el tablero sin validar.
    """
    
    def __init__(self, tablero: Tablero, gestor_turnos: GestorTurnos):
        """
        Inicializa el ejecutor con sus dependencias.
        
        Args:
            tablero (Tablero): Referencia al tablero del juego
            gestor_turnos (GestorTurnos): Referencia al gestor de turnos
        """
        self.__tablero__ = tablero
        self.__gestor_turnos__ = gestor_turnos

    def ejecutar_movimiento(self, origen_idx: int, valor_dado: int) -> str:
        """
        Ejecuta un movimiento ya validado (normal o bear-off).
        
        Args:
            origen_idx (int): Índice 0-based de origen
            valor_dado (int): Valor del dado usado
        
        Returns:
            str: Mensaje describiendo el resultado:
                 "movió", "movió y comió", "sacó ficha", 
                 "juego terminado! Blancas ganaron", etc.
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        destino_idx = origen_idx + jugador * valor_dado
        
        # Si es bear-off (fuera del tablero)
        if not (0 <= destino_idx < CASILLEROS):
            return self._ejecutar_bear_off(origen_idx)
        
        # Si es movimiento normal
        return self._ejecutar_movimiento_normal(origen_idx, destino_idx)

    def ejecutar_entrada_barra(self, valor_dado: int) -> str:
        """
        Ejecuta la entrada desde la barra (ya validada).
        
        Args:
            valor_dado (int): Valor del dado usado para entrar
        
        Returns:
            str: "entró"
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        destino_idx = self._calcular_indice_entrada(jugador, valor_dado)
        
        pos = self.__tablero__._obtener_posiciones_ref()
        barra = self.__tablero__._obtener_barra_ref()
        
        # Si hay un blot rival, capturarlo
        if self._es_blot_rival(pos[destino_idx], jugador):
            self._capturar_ficha(destino_idx, jugador)
            pos[destino_idx] = jugador
        else:
            pos[destino_idx] += jugador
        
        # Decrementar barra del jugador actual
        color = self.__gestor_turnos__.obtener_turno()
        barra[color] -= 1
        
        return "entró"

    # ========== MÉTODOS PRIVADOS ==========

    def _ejecutar_movimiento_normal(self, origen_idx: int, destino_idx: int) -> str:
        """
        Ejecuta un movimiento normal dentro del tablero.
        
        Args:
            origen_idx (int): Índice 0-based de origen
            destino_idx (int): Índice 0-based de destino
        
        Returns:
            str: "movió" o "movió y comió"
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        pos = self.__tablero__._obtener_posiciones_ref()
        
        mensaje = "movió"
        
        # Si hay un blot rival en el destino, capturarlo
        if self._es_blot_rival(pos[destino_idx], jugador):
            self._capturar_ficha(destino_idx, jugador)
            pos[destino_idx] = jugador
            mensaje = "movió y comió"
        else:
            pos[destino_idx] += jugador
        
        # Mover ficha desde origen
        pos[origen_idx] -= jugador
        
        return mensaje

    def _ejecutar_bear_off(self, origen_idx: int) -> str:
        """
        Ejecuta un bear-off (sacar ficha del tablero).
        
        Args:
            origen_idx (int): Índice 0-based de origen
        
        Returns:
            str: "sacó ficha" o "juego terminado! {Color} ganaron"
        """
        jugador = self.__gestor_turnos__.obtener_direccion()
        color = self.__gestor_turnos__.obtener_turno()
        
        pos = self.__tablero__._obtener_posiciones_ref()
        fichas_fuera = self.__tablero__._obtener_fichas_fuera_ref()
        
        # Sacar ficha del origen
        pos[origen_idx] -= jugador
        
        # Incrementar fichas fuera
        fichas_fuera[color] += 1
        
        # Verificar victoria
        if fichas_fuera[color] == 15:
            return f"juego terminado! {color.capitalize()} ganaron"
        
        return "sacó ficha"

    def _capturar_ficha(self, destino_idx: int, jugador: int):
        """
        Captura una ficha rival y la envía a la barra.
        
        Args:
            destino_idx (int): Índice donde está el blot rival
            jugador (int): 1 para blancas, -1 para negras
        """
        barra = self.__tablero__._obtener_barra_ref()
        
        # Determinar color rival
        color_rival = "negras" if jugador == 1 else "blancas"
        
        # Incrementar barra del rival
        barra[color_rival] += 1

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