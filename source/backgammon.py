from source.tablero import Tablero
from source.dados import Dados
from source.gestor_turnos import GestorTurnos
from source.validador_movimientos import ValidadorMovimientos
from source.ejecutor_movimientos import EjecutorMovimientos
from source.analizador_posibilidades import AnalizadorPosibilidades
from source.excepciones import *
from source.constantes import CASILLEROS


class Backgammon:
    """
    Coordinador principal del juego de Backgammon.
    
    Responsabilidad (SRP): Orquestar el flujo del juego delegando 
    responsabilidades específicas a componentes especializados.
    
    Principios SOLID aplicados:
    - SRP: Cada componente tiene una sola responsabilidad
    - OCP: Extensible sin modificar (agregar validadores, etc.)
    - DIP: Depende de clases concretas pero bien separadas
    """

    def __init__(self):
        """
        Inicializa una instancia del juego Backgammon.

        Se crean y configuran los componentes necesarios:
        - Tablero con posiciones iniciales
        - Gestor de turnos
        - Dados
        - Validador de movimientos
        - Ejecutor de movimientos
        - Analizador de posibilidades
        - Lista de movimientos pendientes

        No recibe parámetros y no retorna valor.
        """
        # Componentes básicos
        self.__tablero__ = Tablero()
        self.__dados__ = Dados()
        self.__gestor_turnos__ = GestorTurnos()
        
        # Componentes especializados (inyección de dependencias)
        self.__validador__ = ValidadorMovimientos(self.__tablero__, self.__gestor_turnos__)
        self.__ejecutor__ = EjecutorMovimientos(self.__tablero__, self.__gestor_turnos__)
        self.__analizador__ = AnalizadorPosibilidades(self.__tablero__, self.__gestor_turnos__)
        
        # Estado del juego
        self.__movimientos_pendientes__ = []

    # ========== API PÚBLICA - CONSULTAS DE ESTADO ==========

    def obtener_turno(self) -> str:
        """
        Devuelve el color del jugador cuyo turno es actualmente.

        Returns:
            str: "blancas" o "negras"
        """
        return self.__gestor_turnos__.obtener_turno()

    def obtener_posiciones(self) -> list[int]:
        """
        API pública que retorna una copia del arreglo de posiciones del tablero.

        Returns:
            list[int]: Lista de 24 enteros que representan las fichas en cada punto
                    (valores positivos = blancas, negativos = negras).
        """
        return self.__tablero__.obtener_posiciones()

    def obtener_barra(self) -> dict[str, int]:
        """
        API pública que retorna el estado de la barra.

        Returns:
            dict[str,int]: Diccionario con claves 'blancas' y 'negras' indicando
                        cuántas fichas están en la barra para cada color.
        """
        return self.__tablero__.obtener_barra()

    def obtener_fichas_fuera(self) -> dict[str, int]:
        """
        API pública que retorna las fichas que ya se sacaron del tablero (bear-off).

        Returns:
            dict[str,int]: Diccionario con claves 'blancas' y 'negras' indicando
                        cuántas fichas han salido del tablero por color.
        """
        return self.__tablero__.obtener_fichas_fuera()

    def obtener_ficha_en_posicion(self, posicion: int) -> int:
        """
        Retorna la cantidad (con signo) de fichas en una posición específica.

        Args:
            posicion (int): Posición 1..24 (interfaz pública).

        Returns:
            int: Valor entero en la posición (positivo = blancas, negativo = negras).

        Raises:
            ValueError: Si la posición no está entre 1 y 24.
        """
        if not 1 <= posicion <= 24:
            raise ValueError(f"Posición debe estar entre 1 y 24")
        return self.__tablero__.obtener_ficha_en_posicion(posicion - 1)

    def tiene_fichas_en_barra(self, color: str = None) -> bool:
        """
        Indica si el jugador actual o un color especificado tiene fichas en la barra.

        Args:
            color (str, optional): "blancas" o "negras". Si es None, se asume el jugador actual.

        Returns:
            bool: True si el color indicado tiene >0 fichas en la barra, False en caso contrario.
        """
        if color is None:
            color = self.obtener_turno()
        return self.__tablero__.hay_fichas_en_barra(color)

    def obtener_movimientos_pendientes(self) -> list[int]:
        """
        Retorna una copia de los movimientos pendientes de la tirada actual.

        Returns:
            list[int]: Lista con valores de dados pendientes de usar
        """
        return list(self.__movimientos_pendientes__)

    def movimientos_disponibles(self) -> bool:
        """
        Indica si quedan movimientos pendientes en la tirada actual.

        Returns:
            bool: True si existen movimientos pendientes, False si la lista está vacía.
        """
        return bool(self.__movimientos_pendientes__)

    def hay_movimiento_posible(self) -> bool:
        """
        Verifica si existe al menos un movimiento válido con los movimientos pendientes actuales.

        Delega al AnalizadorPosibilidades para determinar si hay jugadas disponibles.

        Returns:
            bool: True si hay al menos un movimiento válido con los dados pendientes, False si no.
        """
        return self.__analizador__.hay_movimiento_posible(self.__movimientos_pendientes__)
    
    def obtener_movimientos_posibles(self) -> dict:
        """
        Obtiene todos los movimientos posibles con los dados actuales.
        
        Returns:
            dict: Diccionario con estructura:
                - Si hay fichas en barra: {'barra': [(destino, dado), ...]}
                - Si no: {origen: [(destino, dado), ...], ...}
                donde destino=-1 indica bear-off
        """
        movimientos = {}
        pendientes = self.__movimientos_pendientes__
        
        if not pendientes:
            return movimientos
        
        color = self.obtener_turno()
        jugador = 1 if color == "blancas" else -1
        
        # Caso especial: fichas en barra (prioridad)
        if self.tiene_fichas_en_barra():
            movimientos['barra'] = []
            for dado in set(pendientes):
                destino_idx = self.__validador__.indice_entrada(jugador, dado)
                # Verificar si es válido
                es_valido, _ = self.__validador__.validar_entrada_barra(dado)
                if es_valido:
                    destino = destino_idx + 1  # Convertir a 1-based
                    movimientos['barra'].append((destino, dado))
            return movimientos
        
        # Movimientos normales desde cada posición
        posiciones = self.obtener_posiciones()
        
        for origen_idx in range(24):
            # Solo posiciones con fichas propias
            if posiciones[origen_idx] * jugador <= 0:
                continue
            
            origen = origen_idx + 1  # Convertir a 1-based
            movimientos_origen = []
            
            for dado in set(pendientes):
                # Validar movimiento
                es_valido, _ = self.__validador__.validar_movimiento(origen_idx, dado)
                
                if es_valido:
                    destino_idx = origen_idx + jugador * dado
                    
                    # Bear-off
                    if destino_idx < 0 or destino_idx >= 24:
                        movimientos_origen.append((-1, dado))  # -1 = bear-off
                    # Movimiento normal
                    else:
                        destino = destino_idx + 1  # Convertir a 1-based
                        movimientos_origen.append((destino, dado))
            
            if movimientos_origen:
                movimientos[origen] = movimientos_origen
        
        return movimientos

    # ========== API PÚBLICA - ACCIONES DEL JUEGO ==========

    def tirar_dados(self) -> tuple[int, int]:
        """
        Realiza la tirada de dados y prepara la lista de movimientos pendientes para la jugada.

        Maneja dobles (4 movimientos iguales) y tiradas normales (2 movimientos).

        Returns:
            tuple[int,int]: Valores de los dos dados tirados (d1, d2).
        """
        d1, d2 = self.__dados__.tirar()

        # Preparar movimientos pendientes
        if d1 == d2:
            self.__movimientos_pendientes__ = [d1] * 4
        else:
            self.__movimientos_pendientes__ = [d1, d2]

        return d1, d2

    def cambiar_turno(self):
        """
        Cambia el turno del juego.

        Delega al GestorTurnos para alternar entre blancas y negras.
        No recibe parámetros y no devuelve valor.
        """
        self.__gestor_turnos__.cambiar_turno()

    def finalizar_tirada(self):
        """
        Finaliza la tirada actual: limpia los movimientos pendientes y cambia el turno al oponente.

        No recibe parámetros y no retorna valor.
        """
        self.__movimientos_pendientes__.clear()
        self.cambiar_turno()

    def consumir_movimiento(self, valor: int) -> bool:
        """
        Consume (quita) un valor de dado de la lista de movimientos pendientes si está disponible.

        Args:
            valor (int): Valor del dado a consumir.

        Returns:
            bool: True si el valor fue removido (estaba disponible), False si no estaba.
        """
        if valor in self.__movimientos_pendientes__:
            self.__movimientos_pendientes__.remove(valor)
            return True
        return False

    def mover(self, origen: int, valor_dado: int) -> str:
        """
        Ejecuta un movimiento de ficha desde una posición usando un valor de dado.

        Maneja automáticamente todos los casos especiales:
        - Validación de regla "usar dado mayor"
        - Entrada obligatoria desde la barra si hay fichas capturadas
        - Validación completa del movimiento
        - Captura de fichas rivales (blots)
        - Bear-off cuando todas las fichas están en home
        - Actualización de movimientos pendientes

        Args:
            origen (int): Posición de origen (1-24)
            valor_dado (int): Valor del dado a usar (1-6)

        Returns:
            str: Descripción del resultado del movimiento:
                - "entró": Entrada exitosa desde la barra
                - "movió": Movimiento normal
                - "movió y comió": Capturó una ficha rival
                - "sacó ficha": Bear-off exitoso
                - "juego terminado! {color} ganaron": Victoria

        Raises:
            DadoNoDisponibleError: Si el dado no está disponible o debe usar el mayor
            OrigenInvalidoError: Si no hay fichas propias en el origen
            DestinoBloquedoError: Si el destino tiene 2+ fichas rivales
            BearOffInvalidoError: Si intenta bear-off sin cumplir condiciones
            MovimientoInvalidoError: Si el movimiento es inválido por otras razones
        """
        origen_idx = origen - 1  # Convertir a 0-based

        # 1. Validar regla de dado mayor
        self._validar_dado_mayor(valor_dado)

        # 2. Caso especial: entrada desde barra (prioridad)
        if self.tiene_fichas_en_barra():
            return self._mover_desde_barra(valor_dado)

        # 3. Validar que el dado esté disponible
        if valor_dado not in self.__movimientos_pendientes__:
            raise DadoNoDisponibleError("dado no disponible para este movimiento")

        # 4. VALIDAR movimiento (delega a ValidadorMovimientos)
        es_valido, mensaje_error = self.__validador__.validar_movimiento(origen_idx, valor_dado)

        if not es_valido:
            self._lanzar_excepcion_apropiada(mensaje_error)

        # 5. EJECUTAR movimiento (delega a EjecutorMovimientos)
        resultado = self.__ejecutor__.ejecutar_movimiento(origen_idx, valor_dado)

        # 6. Consumir dado
        self.consumir_movimiento(valor_dado)

        return resultado

    # ========== MÉTODOS PRIVADOS (HELPERS) ==========

    def _validar_dado_mayor(self, valor_dado: int):
        """
        Valida la regla de dado mayor si corresponde.

        Si solo se puede usar uno de los dos dados, debe ser el mayor.
        Delega al AnalizadorPosibilidades para determinar esto.

        Args:
            valor_dado (int): Valor del dado que se intenta usar

        Raises:
            DadoNoDisponibleError: Si debe usar el dado mayor y no lo está usando
        """
        if self.__analizador__.debe_usar_dado_mayor(self.__movimientos_pendientes__):
            dado_mayor = max(self.__movimientos_pendientes__)
            if valor_dado != dado_mayor:
                raise DadoNoDisponibleError(f"debe usar el dado mayor ({dado_mayor})")

    def _mover_desde_barra(self, valor_dado: int) -> str:
        """
        Maneja el movimiento especial de entrada desde la barra.

        Args:
            valor_dado (int): Valor del dado a usar

        Returns:
            str: "entró" si la entrada fue exitosa

        Raises:
            MovimientoInvalidoError: Si el movimiento está fuera del tablero
            DestinoBloquedoError: Si la posición de entrada está bloqueada
        """
        # Validar entrada desde barra
        es_valido, mensaje_error = self.__validador__.validar_entrada_barra(valor_dado)

        if not es_valido:
            self._lanzar_excepcion_apropiada(mensaje_error)

        # Ejecutar entrada desde barra
        resultado = self.__ejecutor__.ejecutar_entrada_barra(valor_dado)

        # Consumir dado
        self.consumir_movimiento(valor_dado)

        return resultado

    def _lanzar_excepcion_apropiada(self, mensaje_error: str):
        """
        Mapea un mensaje de error a la excepción apropiada.

        Args:
            mensaje_error (str): Mensaje descriptivo del error

        Raises:
            OrigenInvalidoError: Si el error está relacionado con el origen
            DestinoBloquedoError: Si el error está relacionado con destino bloqueado
            BearOffInvalidoError: Si el error está relacionado con bear-off
            MovimientoInvalidoError: Para otros errores genéricos
        """
        # Mapeo de palabras clave a excepciones
        if "origen" in mensaje_error.lower():
            raise OrigenInvalidoError(mensaje_error)
        elif "bloqueada" in mensaje_error.lower() or "bloqueado" in mensaje_error.lower():
            raise DestinoBloquedoError(mensaje_error)
        elif any(palabra in mensaje_error.lower() for palabra in ["home", "insuficiente", "adelantada"]):
            raise BearOffInvalidoError(mensaje_error)
        elif "tablero" in mensaje_error.lower():
            raise MovimientoInvalidoError(mensaje_error)
        else:
            raise MovimientoInvalidoError(mensaje_error)