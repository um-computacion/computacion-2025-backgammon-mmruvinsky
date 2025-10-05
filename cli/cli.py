import sys
import os

# Configurar path para importaciones
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
source_dir = os.path.join(project_root, "source")

if source_dir not in sys.path:
    sys.path.insert(0, source_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from source.backgammon import Backgammon
from source.excepciones import *


class BackgammonCLI:
    """
    Interfaz de línea de comandos para Backgammon.
    
    Responsabilidad (SRP): Solo maneja la interacción con el usuario,
    delega toda la lógica del juego a la clase Backgammon.
    """
    
    def __init__(self):
        """
        Inicializa la interfaz CLI con una instancia del juego.
        """
        self.__juego__ = Backgammon()
        self.__comandos__ = {
            'help': self.mostrar_ayuda,
            'h': self.mostrar_ayuda,
            'dados': self.tirar_dados,
            'd': self.tirar_dados,
            'mover': self.mover_ficha_interactivo,
            'm': self.mover_ficha_interactivo,
            'tablero': self.mostrar_tablero,
            't': self.mostrar_tablero,
            'estado': self.mostrar_estado,
            'e': self.mostrar_estado,
            'salir': self.salir,
            'q': self.salir,
            'finalizar': self.finalizar_tirada,
            'f': self.finalizar_tirada
        }
    
    # ========== WRAPPERS DE ACCESO A DATOS ==========
    
    def _obtener_posiciones_tablero(self) -> list[int]:
        """
        Obtiene las posiciones del tablero.
        
        Returns:
            list[int]: Array de 24 posiciones
        """
        return self.__juego__.obtener_posiciones()

    def _obtener_barra(self) -> dict[str, int]:
        """
        Obtiene el estado de la barra.
        
        Returns:
            dict[str, int]: Fichas en barra por color
        """
        return self.__juego__.obtener_barra()

    def _obtener_fichas_fuera(self) -> dict[str, int]:
        """
        Obtiene las fichas fuera del tablero.
        
        Returns:
            dict[str, int]: Fichas fuera por color
        """
        return self.__juego__.obtener_fichas_fuera()
    
    # ========== VISUALIZACIÓN DEL TABLERO ==========
    
    def mostrar_tablero(self, *args):
        """
        Muestra el tablero visual en ASCII.
        
        Args:
            *args: Argumentos ignorados (compatibilidad con comandos)
        """
        try:
            posiciones = self._obtener_posiciones_tablero()
            barra = self._obtener_barra()
            fichas_fuera = self._obtener_fichas_fuera()
            
            if not posiciones or len(posiciones) != 24:
                print("Error: Estado del tablero inválido")
                return
                
            print("\n" + "="*80)
            print("                              TABLERO DE BACKGAMMON")
            print("="*80)
            
            # Mostrar fichas fuera (bear off)
            print(f"Fichas fuera - Blancas: {fichas_fuera.get('blancas', 0)} | Negras: {fichas_fuera.get('negras', 0)}")
            print()
            
            # Parte superior del tablero (posiciones 13-24)
            self._mostrar_fila_superior(posiciones)
            
            # Barra central
            self._mostrar_barra(barra)
            
            # Parte inferior del tablero (posiciones 12-1)
            self._mostrar_fila_inferior(posiciones)
            
            print("="*80)
            print()
            
        except Exception as e:
            print(f"Error mostrando tablero: {e}")
            print("Estado del juego puede estar corrupto")
    
    def _mostrar_fila_superior(self, posiciones: list[int]):
        """
        Muestra la fila superior del tablero (13-24).
        
        Args:
            posiciones (list[int]): Array de posiciones del tablero
        """
        print("┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Números de posición (13-24)
        numeros = "│"
        for i in range(13, 19):
            numeros += f" {i:2d}  │"
        numeros += "   │"
        for i in range(19, 25):
            numeros += f" {i:2d}  │"
        print(numeros)
        
        print("├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Fichas (máximo 5 filas visibles)
        for fila in range(5):
            linea = "│"
            
            # Posiciones 13-18
            for posicion in range(13, 19):
                idx = posicion - 1
                fichas = posiciones[idx] if idx < len(posiciones) else 0
                
                if abs(fichas) > fila:
                    linea += "  B  │" if fichas > 0 else "  N  │"
                else:
                    linea += "     │"
            
            linea += "   │"
            
            # Posiciones 19-24
            for posicion in range(19, 25):
                idx = posicion - 1
                fichas = posiciones[idx] if idx < len(posiciones) else 0
                
                if abs(fichas) > fila:
                    linea += "  B  │" if fichas > 0 else "  N  │"
                else:
                    linea += "     │"
            
            print(linea)
        
        print("└─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")
    
    def _mostrar_barra(self, barra: dict[str, int]):
        """
        Muestra la barra central.
        
        Args:
            barra (dict[str, int]): Estado de la barra
        """
        try:
            blancas_barra = barra.get('blancas', 0)
            negras_barra = barra.get('negras', 0)
            print(f"                                 BARRA")
            print(f"                        Blancas: {blancas_barra} | Negras: {negras_barra}")
            print()
        except Exception as e:
            print(f"                        Error mostrando barra: {e}")
            print()
    
    def _mostrar_fila_inferior(self, posiciones: list[int]):
        """
        Muestra la fila inferior del tablero (12-1).
        
        Args:
            posiciones (list[int]): Array de posiciones del tablero
        """
        print("┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Fichas (máximo 5 filas visibles, de arriba hacia abajo)
        for fila in range(4, -1, -1):
            linea = "│"
            
            # Posiciones 12-7
            for posicion in range(12, 6, -1):
                idx = posicion - 1
                fichas = posiciones[idx] if 0 <= idx < len(posiciones) else 0
                
                if abs(fichas) > fila:
                    linea += "  B  │" if fichas > 0 else "  N  │"
                else:
                    linea += "     │"
            
            linea += "   │"
            
            # Posiciones 6-1
            for posicion in range(6, 0, -1):
                idx = posicion - 1
                fichas = posiciones[idx] if 0 <= idx < len(posiciones) else 0
                
                if abs(fichas) > fila:
                    linea += "  B  │" if fichas > 0 else "  N  │"
                else:
                    linea += "     │"
            
            print(linea)
        
        print("├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Números de posición (12-1)
        numeros = "│"
        for i in range(12, 6, -1):
            numeros += f" {i:2d}  │"
        numeros += "   │"
        for i in range(6, 0, -1):
            numeros += f" {i:2d}  │"
        print(numeros)
        
        print("└─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")

    # ========== COMANDOS DEL JUEGO ==========

    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida."""
        print("=" * 80)
        print("                    BACKGAMMON - CLI")
        print("=" * 80)
        print("Escribe 'help' para ver los comandos disponibles")
        print("Turno actual:", self.__juego__.obtener_turno().capitalize())
        self.mostrar_tablero()
    
    def mostrar_ayuda(self, *args):
        """
        Muestra la lista de comandos disponibles.
        
        Args:
            *args: Argumentos ignorados
        """
        print("\n--- COMANDOS DISPONIBLES ---")
        print("help, h          - Mostrar esta ayuda")
        print("dados, d         - Tirar dados")
        print("mover, m         - Mover ficha (modo interactivo)")
        print("tablero, t       - Mostrar tablero")
        print("estado, e        - Mostrar estado resumido")
        print("finalizar, f     - Finalizar tirada actual")
        print("salir, q         - Salir del juego")
        print()
        print("LEYENDA DEL TABLERO:")
        print("B = Fichas Blancas | N = Fichas Negras")
        print("Las posiciones van del 1 al 24")
        print("Blancas se mueven hacia números más altos (1->24)")
        print("Negras se mueven hacia números más bajos (24->1)")
        print()
    
    def tirar_dados(self, *args):
        """
        Tira los dados y muestra el resultado.
        
        Args:
            *args: Argumentos ignorados
        """
        try:
            d1, d2 = self.__juego__.tirar_dados()
            print(f"\nDados: {d1}, {d2}")
            
            if d1 == d2:
                print(f"Dobles! Tienes 4 movimientos de {d1}")
            
            pendientes = self.__juego__.obtener_movimientos_pendientes()
            print(f"Movimientos disponibles: {pendientes}")
            
            # Mostrar tablero después de tirar
            self.mostrar_tablero()
            
            # Verificar si hay movimientos posibles
            if not self.__juego__.hay_movimiento_posible():
                print("No hay movimientos posibles con estos dados")
                input("Presiona Enter para finalizar tirada...")
                self.__juego__.finalizar_tirada()
                print(f"Turno cambiado a: {self.__juego__.obtener_turno().capitalize()}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def mover_ficha_interactivo(self, *args):
        """
        Modo interactivo para mover fichas.
        
        Args:
            *args: Argumentos ignorados
        """
        # Verificar dados disponibles
        pendientes = self.__juego__.obtener_movimientos_pendientes()
        if not pendientes:
            print("No hay dados disponibles. Tira los dados primero.")
            return
        
        # Mostrar tablero actual
        self.mostrar_tablero()
        
        # Verificar fichas en barra primero
        color_turno = self.__juego__.obtener_turno()
        
        if self.__juego__.tiene_fichas_en_barra(color_turno):
            barra = self._obtener_barra()
            fichas_en_barra = barra.get(color_turno, 0)
            print(f"Tienes {fichas_en_barra} ficha(s) en la BARRA.")
            print("Debes entrar primero antes de mover otras fichas.")
            return self._mover_desde_barra(pendientes)
        
        # Selección de origen
        print(f"Dados disponibles: {pendientes}")
        print(f"Turno de: {color_turno.capitalize()}")
        
        try:
            # Pedir posición origen
            origen_str = input("Desde que posición quieres mover? (1-24): ").strip()
            if not origen_str:
                print("Movimiento cancelado")
                return
            
            origen = int(origen_str)
            if not (1 <= origen <= 24):
                print("La posición debe estar entre 1 y 24")
                return
            
            # Verificar que hay fichas propias en el origen
            try:
                valor_origen = self.__juego__.obtener_ficha_en_posicion(origen)
                jugador = 1 if color_turno == "blancas" else -1
                
                if valor_origen * jugador <= 0:
                    print("No tienes fichas en esa posición")
                    return
            except ValueError as e:
                print(f"Error: {e}")
                return
            
            # Mostrar opciones de dados
            return self._seleccionar_dado_y_mover(origen, pendientes)
            
        except ValueError:
            print("Debes introducir un número válido")
        except Exception as e:
            print(f"Error: {e}")
    
    def _mover_desde_barra(self, pendientes: list[int]):
        """
        Maneja el movimiento desde la barra.
        
        Args:
            pendientes (list[int]): Dados pendientes
        """
        print("\nSelecciona que dado usar para entrar desde la barra:")
        dados_unicos = list(set(pendientes))
        
        if len(dados_unicos) == 1:
            dado = dados_unicos[0]
            print(f"Usando dado: {dado}")
        else:
            for i, dado in enumerate(dados_unicos, 1):
                print(f"{i}. Dado {dado}")
            
            try:
                opcion = int(input("Elige una opción: ")) - 1
                if not (0 <= opcion < len(dados_unicos)):
                    print("Opción inválida")
                    return
                dado = dados_unicos[opcion]
            except ValueError:
                print("Debes introducir un número")
                return
        
        try:
            # Usar posición 1 (cualquier posición, el juego maneja la barra)
            resultado = self.__juego__.mover(1, dado)
            print(f"Resultado: {resultado.capitalize()}")
            self._finalizar_movimiento(resultado)
        except BackgammonError as e:
            print(f"Error: {e}")
    
    def _seleccionar_dado_y_mover(self, origen: int, pendientes: list[int]):
        """
        Permite seleccionar el dado y ejecutar el movimiento.
        
        Args:
            origen (int): Posición de origen (1-24)
            pendientes (list[int]): Dados pendientes
        """
        dados_unicos = list(set(pendientes))
        color_turno = self.__juego__.obtener_turno()
        jugador = 1 if color_turno == "blancas" else -1
        
        print(f"\nMoviendo desde posición {origen}")
        print("Opciones disponibles:")
        
        # Mostrar destinos posibles
        opciones_validas = []
        for i, dado in enumerate(dados_unicos, 1):
            destino = origen + (jugador * dado)
            
            if 1 <= destino <= 24:
                print(f"{i}. Usar dado {dado} -> ir a posición {destino}")
                opciones_validas.append((dado, destino, "normal"))
            elif destino > 24 or destino < 1:
                print(f"{i}. Usar dado {dado} -> SACAR FICHA (bear off)")
                opciones_validas.append((dado, destino, "bear_off"))
        
        if not opciones_validas:
            print("No hay movimientos válidos desde esa posición")
            return
        
        try:
            opcion = int(input("Elige una opción: ")) - 1
            if not (0 <= opcion < len(opciones_validas)):
                print("Opción inválida")
                return
            
            dado_elegido, destino, tipo = opciones_validas[opcion]
            
            # Confirmar movimiento
            if tipo == "bear_off":
                confirmar = input(f"Confirmar sacar ficha desde posición {origen}? (s/n): ")
            else:
                confirmar = input(f"Confirmar mover de {origen} a {destino}? (s/n): ")
            
            if confirmar.lower() not in ['s', 'si', 'y', 'yes']:
                print("Movimiento cancelado")
                return
            
            # Ejecutar movimiento
            resultado = self.__juego__.mover(origen, dado_elegido)
            print(f"Resultado: {resultado.capitalize()}")
            self._finalizar_movimiento(resultado)
            
        except ValueError:
            print("Debes introducir un número")
        except BackgammonError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def _finalizar_movimiento(self, resultado: str):
        """
        Finaliza el movimiento y actualiza el estado.
        
        Args:
            resultado (str): Mensaje del resultado del movimiento
        """
        # Mostrar tablero actualizado
        self.mostrar_tablero()
        
        # Mostrar movimientos restantes
        restantes = self.__juego__.obtener_movimientos_pendientes()
        if restantes:
            print(f"Movimientos restantes: {restantes}")
        else:
            print("Todos los dados utilizados")
            self.__juego__.finalizar_tirada()
            print(f"Turno cambiado a: {self.__juego__.obtener_turno().capitalize()}")
        
        # Verificar si el juego terminó
        if "ganaron" in resultado:
            print("\nJUEGO TERMINADO!")
            return True
        
        return False
    
    def mostrar_estado(self, *args):
        """
        Muestra el estado resumido del juego.
        
        Args:
            *args: Argumentos ignorados
        """
        print("\n--- ESTADO RESUMIDO ---")
        print(f"Turno: {self.__juego__.obtener_turno().capitalize()}")
        
        pendientes = self.__juego__.obtener_movimientos_pendientes()
        if pendientes:
            print(f"Dados pendientes: {pendientes}")
        else:
            print("Sin dados pendientes")
        
        barra = self._obtener_barra()
        if barra['blancas'] > 0 or barra['negras'] > 0:
            print(f"Fichas en barra - Blancas: {barra['blancas']}, Negras: {barra['negras']}")
        
        fichas_fuera = self._obtener_fichas_fuera()
        print(f"Fichas fuera - Blancas: {fichas_fuera.get('blancas', 0)}, Negras: {fichas_fuera.get('negras', 0)}")
        print()
    
    def finalizar_tirada(self, *args):
        """
        Finaliza la tirada actual manualmente.
        
        Args:
            *args: Argumentos ignorados
        """
        pendientes = self.__juego__.obtener_movimientos_pendientes()
        if pendientes:
            print(f"Tienes dados sin usar: {pendientes}")
            respuesta = input("Estas seguro de finalizar la tirada? (s/n): ")
            if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
                print("Tirada no finalizada")
                return
        
        self.__juego__.finalizar_tirada()
        print(f"Tirada finalizada. Turno: {self.__juego__.obtener_turno().capitalize()}")
        self.mostrar_tablero()
    
    def salir(self, *args):
        """
        Sale del juego.
        
        Args:
            *args: Argumentos ignorados
            
        Returns:
            bool: True para indicar salida
        """
        print("\nGracias por jugar!")
        return True
    
    # ========== PROCESAMIENTO DE COMANDOS ==========
    
    def procesar_comando(self, entrada: str) -> bool:
        """
        Procesa un comando del usuario.
        
        Args:
            entrada (str): Comando ingresado por el usuario
            
        Returns:
            bool: True si debe salir, False para continuar
        """
        partes = entrada.strip().lower().split()
        if not partes:
            return False
        
        comando = partes[0]
        argumentos = partes[1:]
        
        if comando in self.__comandos__:
            return self.__comandos__[comando](*argumentos)
        else:
            print(f"Comando desconocido: '{comando}'")
            print("Escribe 'help' para ver los comandos disponibles")
            return False
    
    def ejecutar(self):
        """
        Bucle principal del CLI.
        
        Maneja la entrada del usuario y ejecuta comandos hasta salir.
        """
        self.mostrar_bienvenida()
        
        try:
            while True:
                try:
                    entrada = input(f"\n{self.__juego__.obtener_turno()}> ")
                    
                    if not entrada.strip():
                        continue
                    
                    if self.procesar_comando(entrada):
                        break
                        
                except KeyboardInterrupt:
                    print("\n\nSalida con Ctrl+C")
                    break
                except EOFError:
                    print("\n\nSalida con Ctrl+D")
                    break
                    
        except Exception as e:
            print(f"\nError fatal: {e}")
            sys.exit(1)


def main():
    """Función principal para ejecutar el CLI."""
    cli = BackgammonCLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()