import random

class Dados:
    def __init__(self):
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)

    @property # Agregado para acceder a los valores de los dados como atributos
    def dado1(self):
        return self.__dado1__

    @property
    def dado2(self):
        return self.__dado2__

    def tirar(self): # Método para tirar los dados
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)
        return (self.__dado1__, self.__dado2__)
    
    def __str__(self):
        return f"Dados: [{self.__dado1__}, {self.__dado2__}]"

