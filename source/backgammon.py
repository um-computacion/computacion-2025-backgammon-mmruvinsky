from source.tablero import Tablero
from source.dados import Dados
from source.excepciones import *
from source.constantes import CASILLEROS

class Backgammon:

    def __init__(self):
        """
        Inicializa una instancia del juego Backgammon.

        Se crean y configuran los objetos internos necesarios:
        - Tablero con posiciones iniciales
        - Turno inicial (1 = blancas, -1 = negras)
        - Dados
        - Lista de movimientos pendientes

        No recibe parámetros y no retorna valor.

        Raises:
            Ninguna excepción explícita.
        """
        self.__tablero__ = Tablero()
        self.__turno__ = 1  # 1 = blancas, -1 = negras
        self.__dados__ = Dados() 
        self.__movimientos_pendientes__ = []
        

    # ---------- Lógica turnos ---------- 
    def cambiar_turno(self):
        """
        Cambia el turno del juego.

        Alterna el atributo __turno__ entre 1 (blancas) y -1 (negras).
        No recibe parámetros y no devuelve valor.
        """
        self.__turno__ = -1 if self.__turno__ == 1 else 1

    def obtener_turno(self):
        """
        Devuelve el color del jugador cuyo turno es actualmente.

        Returns:
            str: "blancas" si el turno es 1, "negras" si el turno es -1.
        """
        if self.__turno__ == 1:
            return "blancas"
        else:   
            return "negras"
    
    # ---------- Helpers internos ----------
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

    def hay_en_barra(self, jugador: int) -> bool:
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
        barra = self.__tablero__.obtener_barra()
        return (barra['blancas'] > 0) if jugador == 1 else (barra['negras'] > 0)
    
    def todas_en_home(self, jugador: int) -> bool:
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
        pos = self.__tablero__.obtener_posiciones()
        if jugador == 1:  # blancas: home 18..23
            return all(x <= 0 for x in pos[:18])  # antes de 18 no hay blancas
        else:            # negras: home 0..5
            return all(x >= 0 for x in pos[6:])   # después de 5 no hay negras
        
    def obtener_movimientos_pendientes(self) -> list[int]:
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
        return list(self.__movimientos_pendientes__)
    
    def movimientos_disponibles(self) -> bool:
        """
        Indica si quedan movimientos pendientes en la tirada actual.

        Returns:
            bool: True si existen movimientos pendientes, False si la lista está vacía.
        """
        return bool(self.__movimientos_pendientes__)
    
    def _es_fuera(self, idx: int) -> bool:
        """
        Indica si quedan movimientos pendientes en la tirada actual.

        Returns:
            bool: True si existen movimientos pendientes, False si la lista está vacía.
        """
        return not (0 <= idx < CASILLEROS)

    def _destino_bloqueado(self, valor_destino: int, jugador: int) -> bool:
        """
        Indica si quedan movimientos pendientes en la tirada actual.

        Returns:
            bool: True si existen movimientos pendientes, False si la lista está vacía.
        """
        return (valor_destino * jugador < 0) and (abs(valor_destino) >= 2)

    def _destino_es_blot_rival(self, valor_destino: int, jugador: int) -> bool:
        """
        Indica si quedan movimientos pendientes en la tirada actual.

        Returns:
            bool: True si existen movimientos pendientes, False si la lista está vacía.
        """
        return (valor_destino * jugador < 0) and (abs(valor_destino) == 1)
    
    def _origen_valido(self, posiciones: list[int], origen_idx: int, jugador: int) -> bool:
        """
        Indica si quedan movimientos pendientes en la tirada actual.

        Returns:
            bool: True si existen movimientos pendientes, False si la lista está vacía.
        """
        return (0 <= origen_idx < CASILLEROS) and (posiciones[origen_idx] * jugador > 0)
    
    def _simular_mejor_movimiento(self, valor_dado: int) -> bool:
        """
        Simula y aplica el 'mejor' movimiento posible para el dado dado, sin confirmar el movimiento real.

        Este helper se usa para probar si después de usar un dado es posible usar otro (simulación).
        La función modifica referencias internas durante la simulación (usa métodos _obtener_*_ref).

        Args:
            valor_dado (int): Valor del dado a usar en la simulación.

        Returns:
            bool: True si encontró y aplicó una simulación válida, False si no encontró movimiento válido.
        """
        jugador = self.__turno__
        pos = self.__tablero__._obtener_posiciones_ref() 
        
        # Prioridad: barra
        if self.hay_en_barra(jugador):
            try:
                destino_idx = self.indice_entrada(jugador, valor_dado)
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
            
            elif self.todas_en_home(jugador) and self._puede_hacer_bear_off(origen_idx, valor_dado):
                pos[origen_idx] -= jugador
                return True
        
        return False

    def _puede_hacer_bear_off(self, origen_idx: int, valor_dado: int) -> bool:
        """
        Verifica si es válido realizar un bear-off desde un origen concreto con el valor de dado dado.

        Args:
            origen_idx (int): Índice 0-based del origen.
            valor_dado (int): Valor del dado a usar.

        Returns:
            bool: True si el bear-off está permitido según reglas (incluye overshoot rules), False si no.
        """
        jugador = self.__turno__
        pos = self.__tablero__.obtener_posiciones()
        
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
            """
            Ejecuta la entrada desde la barra en modo simulación.

            Modifica las referencias internas a posiciones y barra (simulación).
            No realiza comprobaciones exhaustivas; asume que la entrada es válida o ya fue verificada.

            Args:
                destino_idx (int): Índice 0-based de la casilla de entrada.
            """
            jugador = self.__turno__
            pos = self.__tablero__._obtener_posiciones_ref()
            barra = self.__tablero__._obtener_barra_ref() 
            
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
            """
            Ejecuta un movimiento normal en modo simulación sobre las referencias internas.

            Actualiza posiciones y barra según corresponda (incluye captura si existe blot rival).
            Args:
                origen_idx (int): Índice 0-based de origen.
                destino_idx (int): Índice 0-based de destino.
            """
            jugador = self.__turno__
            pos = self.__tablero__._obtener_posiciones_ref() 
            barra = self.__tablero__._obtener_barra_ref()  
            
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
        """
        Realiza la tirada de dados y prepara la lista de movimientos pendientes para la jugada.

        Maneja dobles (4 movimientos iguales) y tiradas normales (2 movimientos).

        Returns:
            tuple[int,int]: Valores de los dos dados tirados (d1, d2).
        """
        d1, d2 = self.__dados__.tirar()

        # Validación dobles
        if d1 == d2: 
            self.__movimientos_pendientes__ = [d1] * 4
        else:
            self.__movimientos_pendientes__ = [d1, d2]

        return d1, d2
    
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
    
    def puede_usar_ambos_dados(self) -> bool:
        """
        Verifica si es posible usar ambos dados de la tirada actual en algún orden válido.

        Considera casos de dobles, bloqueo por barra y simula el uso de un dado para ver si luego es posible usar el otro.

        Returns:
            bool: True si existe un orden que permita usar ambos dados, False en otro caso.
        """
        if len(self.__movimientos_pendientes__) != 2:
            return True  # Dobles o un solo dado - no aplica
        
        if self.__movimientos_pendientes__[0] == self.__movimientos_pendientes__[1]:
            return True  # Son dobles - no aplica
        
        # Verificar si puede usar ambos dados en cualquier orden
        dado1, dado2 = self.__movimientos_pendientes__
        
        return (self._puede_usar_dado(dado1) and self._puede_usar_dado_tras_simular(dado1, dado2)) or \
            (self._puede_usar_dado(dado2) and self._puede_usar_dado_tras_simular(dado2, dado1))

    def _puede_usar_dado(self, valor_dado: int) -> bool:
        """
        Evalúa si un dado específico (valor_dado) puede usarse para producir al menos un movimiento válido
        en el estado actual del tablero.

        Args:
            valor_dado (int): Valor del dado a evaluar.

        Returns:
            bool: True si existe al menos un movimiento válido con ese dado, False si no.
        """
        jugador = self.__turno__
        pos = self.__tablero__.obtener_posiciones()
        
        # Prioridad: fichas en barra
        if self.hay_en_barra(jugador):
            try:
                destino_idx = self.indice_entrada(jugador, valor_dado)
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
            elif destino_idx < 0 or destino_idx >= CASILLEROS:
                # DEBE verificar que todas estén en home ANTES de permitir bear-off
                if self.todas_en_home(jugador):
                    if self._puede_hacer_bear_off(origen_idx, valor_dado):
                        return True
        
        return False
    
    def _puede_usar_dado_tras_simular(self, primer_dado: int, segundo_dado: int) -> bool:
        """
        Simula usar un primer dado y verifica si, tras esa simulación, es posible usar el segundo dado.

        Guarda el estado antes de la simulación y lo restaura al final para no alterar el juego real.

        Args:
            primer_dado (int): Valor del primer dado a simular.
            segundo_dado (int): Valor del segundo dado a verificar tras la simulación.

        Returns:
            bool: True si tras usar primer_dado existe movimiento válido para segundo_dado, False en caso contrario.
        """
        # Guardar estado ANTES de modificar (copias para backup)
        pos_backup = self.__tablero__.obtener_posiciones()
        barra_backup = self.__tablero__.obtener_barra()
        
        try:
            # Intentar el mejor movimiento con primer_dado (esto MODIFICA el estado real)
            if self._simular_mejor_movimiento(primer_dado):
                # Verificar si se puede usar el segundo
                return self._puede_usar_dado(segundo_dado)
            return False
        finally:
            # Restaurar estado original (necesitamos referencias para escribir)
            pos_ref = self.__tablero__._obtener_posiciones_ref()
            barra_ref = self.__tablero__._obtener_barra_ref()
            
            # Restaurar valores originales
            pos_ref[:] = pos_backup           # Reemplaza el contenido de la lista
            barra_ref.update(barra_backup)    # Actualiza el diccionario

    def debe_usar_dado_mayor(self) -> bool:
        """
        Verifica si, en la situación actual, el reglamento obliga a usar el dado mayor cuando sólo uno de los dos es usable.

        Reglas consideradas:
        - Si ambos dados son usables no hay obligación.
        - Si sólo uno es usable, y los valores son distintos, debe usarse el mayor.

        Returns:
            bool: True si existe la obligación de usar el dado mayor, False en caso contrario.
        """
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
        """
        Finaliza la tirada actual: limpia los movimientos pendientes y cambia el turno al oponente.

        No recibe parámetros y no retorna valor.
        """
        self.__movimientos_pendientes__.clear()
        self.cambiar_turno()
    
    def mover(self, origen: int, valor_dado: int) -> str:
        """
        Ejecuta un movimiento de ficha desde una posición usando un valor de dado.

        Maneja automáticamente todos los casos especiales:
        - Entrada obligatoria desde la barra si hay fichas capturadas
        - Validación de regla "usar dado mayor"
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
        jugador = self.__turno__ 
        posiciones = self.__tablero__._obtener_posiciones_ref() 
               
        if self.debe_usar_dado_mayor():
            dado_mayor = max(self.__movimientos_pendientes__)
            if valor_dado != dado_mayor:
                raise DadoNoDisponibleError(f"debe usar el dado mayor ({dado_mayor})")

        # Validación prioridad fichas en barra
        if self.hay_en_barra(jugador):
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
            barra = self.__tablero__._obtener_barra_ref() 
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
        """
        Lógica para reingresar (entrar) una ficha desde la barra usando un valor de dado.

        Realiza las comprobaciones de destino dentro del tablero, bloqueo y captura de blots rivales,
        actualiza la barra y retorna el resultado.

        Args:
            valor_dado (int): Valor del dado usado para entrar (1..6).

        Returns:
            str: "entró" si la ficha pudo ingresar correctamente.

        Raises:
            MovimientoInvalidoError: Si el destino está fuera del tablero
            DestinoBloquedoError: Si la casilla de entrada está bloqueada por 2+ fichas rivales
        """
        jugador = self.__turno__
        posiciones = self.__tablero__._obtener_posiciones_ref()
        destino_idx = self.indice_entrada(jugador, valor_dado)

        # (Asume que ya existen fichas en la barra por la validación previa)
        # Validación: destino dentro del tablero
        if self._es_fuera(destino_idx): 
            raise MovimientoInvalidoError("movimiento fuera del tablero")

        valor_destino = posiciones[destino_idx]

        # Validación destino bloqueado (2+ fichas rivales)
        if self._destino_bloqueado(valor_destino, jugador): 
            raise DestinoBloquedoError("posición de destino bloqueada")

        barra = self.__tablero__._obtener_barra_ref() 
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
        """
        Intenta ejecutar un bear-off (sacar una ficha del tablero) desde un índice específico.

        Verifica:
        - Que todas las fichas del jugador estén en home
        - Que el valor del dado permita sacar la ficha (incluye reglas de overshoot)
        - Que no existan fichas más adelantadas que impidan el overshoot

        Si el bear-off es válido actualiza las fichas fuera y consume el movimiento.

        Args:
            origen_idx (int): Índice 0-based de la posición de origen.
            valor_dado (int): Valor del dado usado para intentar el bear-off.

        Returns:
            str: "sacó ficha" si se sacó una ficha, o "juego terminado! {Color} ganaron" si se completó la partida.

        Raises:
            BearOffInvalidoError: Si no se cumplen las condiciones para realizar bear-off.
        """
        jugador = self.__turno__
        pos = self.__tablero__._obtener_posiciones_ref()

        if not self.todas_en_home(jugador):
            raise BearOffInvalidoError("no todas las fichas están en home")
        
        needed = (24 - origen_idx) if jugador == 1 else (origen_idx + 1)

        if valor_dado < needed:
            raise BearOffInvalidoError("valor insuficiente para sacar la ficha")
        
        if valor_dado > needed:
            if jugador == 1:
                if any(pos[i] > 0 for i in range(origen_idx + 1, 24)):
                    raise BearOffInvalidoError("debe mover ficha más adelantada")
            else:
                if any(pos[i] < 0 for i in range(0, origen_idx)):
                    raise BearOffInvalidoError("debe mover ficha más adelantada")

        # Ejecutar sacar ficha
        pos[origen_idx] -= jugador
        color = "blancas" if jugador == 1 else "negras"
        
        fichas_fuera = self.__tablero__._obtener_fichas_fuera_ref()
        fichas_fuera[color] += 1

        self.consumir_movimiento(valor_dado)

        if fichas_fuera[color] == 15:
            return f"juego terminado! {color.capitalize()} ganaron"

        return "sacó ficha"
    
    def hay_movimiento_posible(self) -> bool:
        """
        Verifica si existe al menos un movimiento válido con los movimientos pendientes actuales.

        Recorre los valores únicos pendientes y utiliza la lógica de evaluación de movimientos
        para confirmar la existencia de al menos uno valido.

        Returns:
            bool: True si hay al menos un movimiento válido con los dados pendientes, False si no.
        """
        if not self.__movimientos_pendientes__:
            return False
        
        # Verificar cada valor único en los dados pendientes
        for valor in set(self.__movimientos_pendientes__):
            if self._puede_usar_dado(valor):
                return True
        
        return False


    
    

    


    









    