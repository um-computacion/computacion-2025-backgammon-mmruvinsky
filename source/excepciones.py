class BackgammonError(Exception):
    """Clase base para todas las excepciones del backgammon"""
    pass

class MovimientoInvalidoError(BackgammonError):
    """Se lanza cuando se intenta hacer un movimiento inválido"""
    pass

class OrigenInvalidoError(MovimientoInvalidoError):
    """Se lanza cuando el origen no tiene fichas del jugador actual"""
    pass

class DestinoBloquedoError(MovimientoInvalidoError):
    """Se lanza cuando el destino está bloqueado por fichas rivales"""
    pass

class DadoNoDisponibleError(MovimientoInvalidoError):
    """Se lanza cuando se intenta usar un dado que no está disponible"""
    pass

class BearOffInvalidoError(MovimientoInvalidoError):
    """Se lanza cuando se intenta hacer bear off sin tener todas las fichas en home"""
    pass

class FichasEnBarraError(BackgammonError):
    """Se lanza cuando hay fichas en la barra y se debe entrar primero"""
    pass



