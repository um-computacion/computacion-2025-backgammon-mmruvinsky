from source.constantes import CASILLEROS

class Tablero:
    """
    Responsabilidad: Encapsular y gestionar el estado del juego (posiciones, barra y fichas fuera).
    SRP: Actúa como el único punto de verdad para los datos del juego. No contiene lógica de
         movimiento, validación o reglas.
    Justificación: Separar el estado (Tablero) de la lógica (Validador, Ejecutor) es clave para el
                   diseño SOLID, permitiendo que la lógica sea fácilmente testeable y
                   agnóstica a la representación del tablero (DIP).
    """
    def __init__(self):
        """
        Inicializa el tablero con la configuración estándar del Backgammon.
        
        Funcionamiento: Llama a `inicializar_posiciones` para establecer el estado inicial
        de las 24 posiciones y configura los contadores de barra y fichas fuera a cero.

        Atributos privados:
            __posiciones__: list[int] - El array principal de 24 casilleros (0 a 23).
                            Los valores son enteros con signo: positivo (+) para blancas,
                            negativo (-) para negras. Esto simplifica la lógica de movimiento
                            y colisiones.
            __barra__: dict - Contadores de fichas capturadas: {'blancas': int, 'negras': int}.
            __fichas_fuera__: dict - Contadores de fichas que han salido (*bear-off*):
                              {'blancas': int, 'negras': int}.
        """
        self.__posiciones__ = self.inicializar_posiciones()
        self.__barra__ = { 'blancas': 0, 'negras': 0 }
        self.__fichas_fuera__ = { 'blancas': 0, 'negras': 0 }

    def inicializar_posiciones(self):
        """
        Establece la configuración de inicio estándar del Backgammon.
        
        Funcionamiento: Inicializa un array de 24 ceros y luego asigna los valores
        con signo según la posición inicial (Blancas con signo positivo, Negras negativo).
        
        Returns:
            list[int]: El array de 24 posiciones inicializado.
        """
        posiciones = [0] * CASILLEROS
        posiciones[0] = 2   # blancas
        posiciones[11] = 5
        posiciones[16] = 3
        posiciones[18] = 5

        posiciones[23] = -2   # negras
        posiciones[12] = -5
        posiciones[7]  = -3
        posiciones[5]  = -5
        return posiciones
    
    def obtener_posiciones(self) -> list[int]:
        """
        API Pública. Obtiene el estado de las 24 posiciones.

        Funcionamiento: Retorna una **copia defensiva** de la lista interna.
        Justificación: Protege el estado del tablero (`__posiciones__`) de ser modificado
                       accidentalmente por clases externas (Encapsulamiento).
                       Solo el EjecutorMovimientos puede modificar la referencia interna.
        
        Returns:
            list[int]: Una copia de la lista de posiciones.
        """
        return list(self.__posiciones__)
    
    def obtener_barra(self) -> dict:
        """
        API Pública. Obtiene el estado de las fichas en la barra.

        Funcionamiento: Retorna una **copia defensiva** del diccionario interno.
        Justificación: Evita la modificación directa del estado de la barra.
        
        Returns:
            dict: Una copia del diccionario de la barra.
        """
        return dict(self.__barra__)
    
    def obtener_fichas_fuera(self) -> dict:
        """
        API Pública. Obtiene el contador de fichas que han salido (*bear-off*).

        Funcionamiento: Retorna una **copia defensiva** del diccionario interno.
        Justificación: Evita la modificación directa del estado de `fichas_fuera`.
        
        Returns:
            dict: Una copia del diccionario de fichas fuera.
        """
        return dict(self.__fichas_fuera__)
    
    def hay_fichas_en_barra(self, color: str) -> bool:
        """
        Verifica si hay fichas del color especificado en la barra.

        Funcionamiento: Consulta directamente el atributo privado `__barra__` para el color dado.

        Args:
            color (str): El color de las fichas a verificar. Debe ser 'blancas' o 'negras'.

        Returns:
            bool: True si hay al menos una ficha del color dado en la barra.

        Raises:
            ValueError: Si el color proporcionado no es 'blancas' ni 'negras'.
        """
        if color not in ['blancas', 'negras']:
            raise ValueError(f"Color inválido: {color}")
        return self.__barra__[color] > 0
    
    def obtener_ficha_en_posicion(self, posicion: int) -> int:
        """
        Devuelve el número de fichas en la posición especificada del tablero.

        Funcionamiento: Accede al valor en el índice del array de posiciones,
        previamente validando que la posición esté dentro del rango [0, 23].

        Args:
            posicion (int): Índice de la posición en el tablero (de 0 a CASILLEROS-1).

        Returns:
            int: Número de fichas en la posición indicada (con signo).

        Raises:
            IndexError: Si la posición está fuera del rango permitido.
        """
        if not 0 <= posicion < CASILLEROS:
            raise IndexError(f"Posición {posicion} fuera de rango [0, 23]")
        return self.__posiciones__[posicion]
    
    def _obtener_posiciones_ref(self) -> list[int]:
        """
        MÉTODO PROTEGIDO: Retorna la REFERENCIA directa a `__posiciones__`.
        
        Funcionamiento: Retorna la referencia mutable (no una copia).
        Justificación: Permite a los servicios de lógica (EjecutorMovimientos,
                       AnalizadorPosibilidades) realizar modificaciones de estado
                       de alto rendimiento sin la sobrecarga de copiar el array de 24 posiciones.
        ⚠️ SOLO para uso interno del CORE del juego. NO usar desde código externo.
        """
        return self.__posiciones__

    def _obtener_barra_ref(self) -> dict:
        """
        MÉTODO PROTEGIDO: Retorna la REFERENCIA directa a `__barra__`.

        Funcionamiento: Retorna la referencia mutable.
        Justificación: Permite la modificación eficiente por parte de EjecutorMovimientos
                       y AnalizadorPosibilidades.
        ⚠️ SOLO para uso interno del CORE del juego.
        """
        return self.__barra__

    def _obtener_fichas_fuera_ref(self) -> dict:
        """
        MÉTODO PROTEGIDO: Retorna la REFERENCIA directa a `__fichas_fuera__`.

        Funcionamiento: Retorna la referencia mutable.
        Justificación: Permite la actualización de contadores de Bear-off por
                       EjecutorMovimientos.
        ⚠️ SOLO para uso interno del CORE del juego.
        """
        return self.__fichas_fuera__