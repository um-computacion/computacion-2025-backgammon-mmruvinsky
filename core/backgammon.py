from core.tablero import Tablero

class Backgammon:

    def __init__(self):
        self.__tablero__ = Tablero
        self.__turno__ = 1  
      
    def cambiar_turno(self):
        self.__turno__ = 2 if self.__turno__ == 1 else 1

    def obtener_turno(self):
        return self.__turno__
    


    