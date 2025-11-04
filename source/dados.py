import random

class Dados:
    """
    Responsabilidad: Gestionar la aleatoriedad y el estado de los dos dados.
    SRP: Encapsula la lógica de generación de números aleatorios (1 a 6) para los dados.
    Justificación: Al aislar la aleatoriedad en una sola clase, se facilita la
    testabilidad del sistema (DIP), permitiendo inyectar una clase 'Dados' simulada
    (Mock) en los tests, haciendo que la lógica del juego sea determinística.
    """

    def __init__(self):
        """
        Inicializa los dos dados con un valor aleatorio inicial.

        Funcionamiento: Llama a random.randint(1, 6) para establecer un estado inicial
        en ambos dados, asegurando que los atributos internos existan desde el principio.
        
        Atributos privados:
            __dado1__: int - Almacena el valor del primer dado (1-6). Se accede
                       solo a través de la propiedad dado1.
            __dado2__: int - Almacena el valor del segundo dado (1-6). Se accede
                       solo a través de la propiedad dado2.
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)

    @property 
    def dado1(self):
        """
        Retorna el valor actual del primer dado.

        Funcionamiento: Proporciona acceso de solo lectura al atributo privado __dado1__.
        Justificación: Mantiene el Encapsulamiento, impidiendo que el estado del dado
        sea modificado directamente desde fuera de la clase.
        
        Returns:
            int: El valor del primer dado.
        """
        return self.__dado1__

    @property
    def dado2(self):
        """
        Retorna el valor actual del segundo dado.

        Funcionamiento: Proporciona acceso de solo lectura al atributo privado __dado2__.
        Justificación: Mantiene el Encapsulamiento.
        
        Returns:
            int: El valor del segundo dado.
        """
        return self.__dado2__

    def tirar(self):
        """
        Simula la tirada de los dados, actualizando sus valores internos.

        Funcionamiento: Genera dos nuevos números aleatorios entre 1 y 6 y los
        asigna a los atributos internos __dado1__ y __dado2__.
        Justificación: Es el método de acción de la clase y cumple con la
        única responsabilidad de generar aleatoriedad (SRP).
        
        Returns:
            tuple[int, int]: Una tupla con los nuevos valores de (dado1, dado2).
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)
        return (self.__dado1__, self.__dado2__)

