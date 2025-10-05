from source.excepciones import *

class GestorTurnos:
    """
    Gestionar el turno actual del juego.
    """
    
    def __init__(self):
        """
        Inicializa el gestor de turnos.
        El juego comienza con las blancas (turno = 1).
        
        No recibe parámetros.
        """
        self.__turno__ = 1  # 1 = blancas, -1 = negras

    def cambiar_turno(self):
        """
        Cambia el turno al jugador contrario.
        
        Alterna entre 1 (blancas) y -1 (negras).
        No recibe parámetros y no retorna valor.
        """
        self.__turno__ = -1 if self.__turno__ == 1 else 1

    def obtener_turno(self) -> str:
        """
        Obtiene el color del jugador actual.
        
        Returns:
            str: "blancas" si turno=1, "negras" si turno=-1
        """
        return "blancas" if self.__turno__ == 1 else "negras"
    
    def obtener_direccion(self) -> int:
        """
        Obtiene la dirección de movimiento del jugador actual.
        
        Este método es crucial para cálculos de movimiento en ValidadorMovimientos,
        EjecutorMovimientos y AnalizadorPosibilidades.
        
        Returns:
            int: 1 para blancas (avanzan hacia arriba), 
                 -1 para negras (avanzan hacia abajo)
        """
        return self.__turno__
    
    def es_turno_de(self, color: str) -> bool:
        """
        Verifica si es el turno de un color específico.
        
        Args:
            color (str): "blancas" o "negras"
        
        Returns:
            bool: True si es el turno del color indicado
        
        Raises:
            ValueError: Si el color no es válido
        """
        if color not in ["blancas", "negras"]:
            raise ValueError(f"Color inválido: {color}. Debe ser 'blancas' o 'negras'")
        
        turno_actual = self.obtener_turno()
        return turno_actual == color
    

