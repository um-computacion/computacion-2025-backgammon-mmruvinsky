from source.excepciones import *

class GestorTurnos:
    """
    Responsabilidad: Controlar el flujo de la partida, alternando el turno entre jugadores
    y proporcionando la dirección de movimiento para los cálculos de reglas.
    SRP: Se encarga exclusivamente del estado del turno y la dirección asociada,
         sin lógica de movimiento o validación.
    Justificación: Al centralizar la gestión del turno, clases como ValidadorMovimientos
    y EjecutorMovimientos pueden depender de esta para saber quién está moviendo
    y en qué dirección, facilitando la implementación de la lógica con números
    con signo (1 para blancas, -1 para negras).
    """
    
    def __init__(self):
        """
        Inicializa el gestor de turnos.
        El juego comienza con las blancas (turno = 1).
        
        Funcionamiento: Inicializa el atributo interno que rastrea el turno.
        
        No recibe parámetros.

        Atributos privados:
            __turno__: int - Rastrea el jugador actual. 1 para Blancas, -1 para Negras.
                       Se utiliza el valor numérico (con signo) para calcular
                       el destino de los movimientos: destino = origen + __turno__ * dado.
        """
        self.__turno__ = 1  # 1 = blancas, -1 = negras

    def cambiar_turno(self):
        """
        Cambia el turno al jugador contrario.
        
        Funcionamiento: Alterna el valor de __turno__ entre 1 y -1.
        Justificación: Es el método de acción para el flujo principal del juego.
        
        No recibe parámetros y no retorna valor.
        """
        self.__turno__ = -1 if self.__turno__ == 1 else 1

    def obtener_turno(self) -> str:
        """
        Obtiene el color del jugador actual en formato de texto.
        
        Funcionamiento: Mapea el valor numérico de __turno__ a una cadena de texto.
        Justificación: Proporciona una interfaz amigable (ej. para la UI o logs)
        para el jugador actual.
        
        Returns:
            str: "blancas" si turno=1, "negras" si turno=-1
        """
        return "blancas" if self.__turno__ == 1 else "negras"
    
    def obtener_direccion(self) -> int:
        """
        Obtiene la dirección de movimiento del jugador actual.
        
        Funcionamiento: Retorna directamente el valor numérico del atributo __turno__.
        Justificación: Este método es crucial para cálculos de movimiento en ValidadorMovimientos,
        EjecutorMovimientos y AnalizadorPosibilidades, ya que simplifica la lógica
        matemática del movimiento (ej. origen + direccion * dado).
        
        Returns:
            int: 1 para blancas (avanzan hacia arriba), 
                 -1 para negras (avanzan hacia abajo).
        """
        return self.__turno__
    
    def es_turno_de(self, color: str) -> bool:
        """
        Verifica si es el turno de un color específico.
        
        Funcionamiento: Compara el color proporcionado con el resultado de obtener_turno().
        
        Args:
            color (str): "blancas" o "negras".
        
        Returns:
            bool: True si es el turno del color indicado.
        
        Raises:
            ValueError: Si el color proporcionado no es "blancas" ni "negras".
        """
        if color not in ["blancas", "negras"]:
            raise ValueError(f"Color inválido: {color}. Debe ser 'blancas' o 'negras'")
        
        turno_actual = self.obtener_turno()
        return turno_actual == color