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
    

