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


# ========== COLORES ANSI ==========
class Color:
    """Códigos de color ANSI para terminal"""
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    AMARILLO = '\033[93m'
    VERDE = '\033[92m'
    ROJO = '\033[91m'
    BLANCO = '\033[97m'
    GRIS = '\033[90m'
    AZUL = '\033[94m'
    
    NEGRITA = '\033[1m'
    RESET = '\033[0m'
    
    @staticmethod
    def t(color, texto):
        """Retorna texto coloreado"""
        return f"{color}{texto}{Color.RESET}"


class BackgammonCLI:
    """
    Interfaz de línea de comandos para Backgammon.
    
    Responsabilidad (SRP): Solo maneja la interacción con el usuario,
    delega toda la lógica del juego a la clase Backgammon.
    """
    
    def __init__(self):
        """Inicializa la interfaz CLI con una instancia del juego."""
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
        return self.__juego__.obtener_posiciones()

    def _obtener_barra(self) -> dict[str, int]:
        return self.__juego__.obtener_barra()

    def _obtener_fichas_fuera(self) -> dict[str, int]:
        return self.__juego__.obtener_fichas_fuera()
    
    # ========== HELPERS DE VISUALIZACIÓN ==========
    
    def _ficha(self, valor: int) -> str:
        """Retorna representación coloreada de una ficha."""
        if valor > 0:  # Blancas
            return Color.t(Color.CYAN + Color.NEGRITA, "  ●  ")
        elif valor < 0:  # Negras
            return Color.t(Color.MAGENTA + Color.NEGRITA, "  ●  ")
        else:  # Vacío
            return "     "
    
    # ========== VISUALIZACIÓN DEL TABLERO ==========
    
    def mostrar_tablero(self, *args):
        """Muestra el tablero visual en ASCII con colores."""
        try:
            posiciones = self._obtener_posiciones_tablero()
            barra = self._obtener_barra()
            fichas_fuera = self._obtener_fichas_fuera()
            
            if not posiciones or len(posiciones) != 24:
                print(Color.t(Color.ROJO, "⚠ Error: Estado del tablero inválido"))
                return
            
            # Header
            print("\n" + Color.t(Color.CYAN + Color.NEGRITA, "═" * 80))
            print(Color.t(Color.AMARILLO + Color.NEGRITA, 
                         "                        🎲  BACKGAMMON - COMPUTACIÓN 2025 🎲"))
            print(Color.t(Color.CYAN + Color.NEGRITA, "═" * 80))
            
            # Fichas fuera
            self._mostrar_fichas_fuera(fichas_fuera)
            
            # Tablero
            self._mostrar_fila_superior(posiciones)
            self._mostrar_barra_central(barra)
            self._mostrar_fila_inferior(posiciones)
            
            print(Color.t(Color.CYAN + Color.NEGRITA, "═" * 80) + "\n")
            
        except Exception as e:
            print(Color.t(Color.ROJO, f"⚠ Error mostrando tablero: {e}"))
    
    def _mostrar_fichas_fuera(self, fichas_fuera: dict):
        """Muestra contador de fichas fuera."""
        blancas = fichas_fuera.get('blancas', 0)
        negras = fichas_fuera.get('negras', 0)
        
        print(f"  Fichas fuera │ "
              f"{Color.t(Color.CYAN + Color.NEGRITA, '●')} Blancas: {Color.t(Color.CYAN, f'{blancas:2d}')}  │  "
              f"{Color.t(Color.MAGENTA + Color.NEGRITA, '●')} Negras: {Color.t(Color.MAGENTA, f'{negras:2d}')}")
        print()
    
    def _mostrar_fila_superior(self, posiciones: list[int]):
        """Muestra fila superior (13-24)."""
        print("  ┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Números
        linea = "  │"
        for i in range(13, 19):
            linea += f" {i:2d}  │"
        linea += "   │"
        for i in range(19, 25):
            linea += f" {i:2d}  │"
        print(linea)
        
        print("  ├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Fichas (5 filas máximo)
        for fila in range(5):
            linea = "  │"
            
            for pos in range(13, 19):
                idx = pos - 1
                fichas = posiciones[idx]
                linea += self._ficha(fichas if abs(fichas) > fila else 0) + "│"
            
            linea += "   │"
            
            for pos in range(19, 25):
                idx = pos - 1
                fichas = posiciones[idx]
                linea += self._ficha(fichas if abs(fichas) > fila else 0) + "│"
            
            print(linea)
        
        print("  └─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")
    
    def _mostrar_barra_central(self, barra: dict):
        """Muestra barra central."""
        blancas = barra.get('blancas', 0)
        negras = barra.get('negras', 0)
        
        texto_barra = Color.t(Color.AMARILLO + Color.NEGRITA, "BARRA")
        
        print(f"                                      {texto_barra}")
        print(f"                                   {Color.t(Color.CYAN, '●')} {blancas}  │  "
            f"{Color.t(Color.MAGENTA, '●')} {negras}")
        print()
    
    def _mostrar_fila_inferior(self, posiciones: list[int]):
        """Muestra fila inferior (12-1)."""
        print("  ┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Fichas
        for fila in range(4, -1, -1):
            linea = "  │"
            
            for pos in range(12, 6, -1):
                idx = pos - 1
                fichas = posiciones[idx]
                linea += self._ficha(fichas if abs(fichas) > fila else 0) + "│"
            
            linea += "   │"
            
            for pos in range(6, 0, -1):
                idx = pos - 1
                fichas = posiciones[idx]
                linea += self._ficha(fichas if abs(fichas) > fila else 0) + "│"
            
            print(linea)
        
        print("  ├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Números
        linea = "  │"
        for i in range(12, 6, -1):
            linea += f" {i:2d}  │"
        linea += "   │"
        for i in range(6, 0, -1):
            linea += f" {i:2d}  │"
        print(linea)
        
        print("  └─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")
    
    # ========== COMANDOS ==========
    
    def mostrar_bienvenida(self):
        """Muestra mensaje de bienvenida."""
        print(Color.t(Color.CYAN + Color.NEGRITA, "═" * 80))
        print(Color.t(Color.AMARILLO + Color.NEGRITA, 
                     "                       🎲  BACKGAMMON - COMPUTACIÓN 2025  🎲"))
        print(Color.t(Color.CYAN + Color.NEGRITA, "═" * 80))
        print(f"\n  {Color.t(Color.VERDE + Color.NEGRITA, '→')} Escribe {Color.t(Color.AMARILLO, 'help')} para ver comandos")
        turno = self.__juego__.obtener_turno().capitalize()
        print(f"  {Color.t(Color.VERDE + Color.NEGRITA, '→')} Turno: {Color.t(Color.CYAN + Color.NEGRITA, turno)}")
        self.mostrar_tablero()
    
    def mostrar_ayuda(self, *args):
        """Muestra ayuda con colores."""
        print(f"\n{Color.t(Color.AMARILLO + Color.NEGRITA, '═══ COMANDOS DISPONIBLES ═══')}\n")
        
        comandos = [
            ("dados, d", "Tirar dados"),
            ("mover, m", "Mover ficha (modo interactivo)"),
            ("tablero, t", "Mostrar tablero"),
            ("estado, e", "Mostrar estado resumido"),
            ("finalizar, f", "Finalizar tirada actual"),
            ("help, h", "Mostrar esta ayuda"),
            ("salir, q", "Salir del juego")
        ]
        
        for cmd, desc in comandos:
            print(f"  {Color.t(Color.CYAN + Color.NEGRITA, cmd):20s} {desc}")
        
        print(f"\n{Color.t(Color.AMARILLO + Color.NEGRITA, '═══ LEYENDA ═══')}\n")
        print(f"  {Color.t(Color.CYAN + Color.NEGRITA, '●')} Blancas (avanzan 1→24)")
        print(f"  {Color.t(Color.MAGENTA + Color.NEGRITA, '●')} Negras (avanzan 24→1)\n")
    
    def tirar_dados(self, *args):
        """Tira dados y muestra resultado."""
        try:
            d1, d2 = self.__juego__.tirar_dados()
            
            print(f"\n  🎲 {Color.t(Color.AMARILLO + Color.NEGRITA, 'Dados:')} "
                  f"{Color.t(Color.VERDE + Color.NEGRITA, f'[{d1}]')} "
                  f"{Color.t(Color.VERDE + Color.NEGRITA, f'[{d2}]')}")
            
            if d1 == d2:
                print(Color.t(Color.MAGENTA + Color.NEGRITA, 
                            f"  ✨ ¡Dobles! Tienes 4 movimientos de {d1}"))
            
            pendientes = self.__juego__.obtener_movimientos_pendientes()
            print(f"  Movimientos disponibles: {pendientes}\n")
            
            self.mostrar_tablero()
            
            if not self.__juego__.hay_movimiento_posible():
                print(Color.t(Color.ROJO + Color.NEGRITA, 
                            "  ❌ No hay movimientos posibles con estos dados"))
                input(f"\n  {Color.t(Color.GRIS, 'Presiona Enter para continuar...')}")
                self.__juego__.finalizar_tirada()
                turno = self.__juego__.obtener_turno().capitalize()
                print(f"\n  {Color.t(Color.VERDE, '→')} Turno: {Color.t(Color.CYAN + Color.NEGRITA, turno)}")
            
        except Exception as e:
            print(Color.t(Color.ROJO, f"  ⚠ Error: {e}"))
    
    def mover_ficha_interactivo(self, *args):
        """Modo interactivo para mover fichas."""
        pendientes = self.__juego__.obtener_movimientos_pendientes()
        if not pendientes:
            print(Color.t(Color.ROJO, "  ⚠ No hay dados disponibles. Tira primero (comando: dados)"))
            return
        
        self.mostrar_tablero()
        
        color_turno = self.__juego__.obtener_turno()
        
        # Caso especial: fichas en barra
        if self.__juego__.tiene_fichas_en_barra(color_turno):
            barra = self._obtener_barra()
            fichas = barra.get(color_turno, 0)
            print(Color.t(Color.AMARILLO + Color.NEGRITA, 
                         f"  ⚠ Tienes {fichas} ficha(s) en la BARRA"))
            print("  Debes entrar primero antes de mover otras fichas\n")
            return self._mover_desde_barra(pendientes)
        
        # Movimiento normal
        print(f"  🎲 Dados: {Color.t(Color.VERDE + Color.NEGRITA, str(pendientes))}")
        print(f"  🎯 Turno: {Color.t(Color.CYAN + Color.NEGRITA, color_turno.capitalize())}\n")
        
        try:
            # Pedir posición origen
            origen_str = input(f"  {Color.t(Color.AMARILLO, '¿Desde qué posición mover? (1-24):')} ").strip()
            if not origen_str:
                print(Color.t(Color.GRIS, "  Movimiento cancelado"))
                return
            
            origen = int(origen_str)
            if not (1 <= origen <= 24):
                print(Color.t(Color.ROJO, "  ⚠ Posición debe estar entre 1 y 24"))
                return
            
            # Verificar que hay fichas propias
            valor_origen = self.__juego__.obtener_ficha_en_posicion(origen)
            jugador = 1 if color_turno == "blancas" else -1
            
            if valor_origen * jugador <= 0:
                print(Color.t(Color.ROJO, f"  ⚠ No tienes fichas en posición {origen}"))
                return
            
            # Mostrar opciones de dados
            self._seleccionar_dado_y_mover(origen, pendientes)
            
        except ValueError:
            print(Color.t(Color.ROJO, "  ⚠ Debes introducir un número válido"))
        except Exception as e:
            print(Color.t(Color.ROJO, f"  ⚠ Error: {e}"))
    
    def _mover_desde_barra(self, pendientes: list[int]):
        """Maneja el movimiento desde la barra."""
        dados_unicos = sorted(set(pendientes), reverse=True)
        
        print(f"  {Color.t(Color.AMARILLO, 'Selecciona dado para entrar:')}\n")
        
        for i, dado in enumerate(dados_unicos, 1):
            print(f"    {Color.t(Color.VERDE + Color.NEGRITA, f'{i}.')} Dado {dado}")
        
        try:
            opcion = int(input(f"\n  {Color.t(Color.AMARILLO, 'Elige opción:')} ")) - 1
            if not (0 <= opcion < len(dados_unicos)):
                print(Color.t(Color.ROJO, "  ⚠ Opción inválida"))
                return
            
            dado = dados_unicos[opcion]
            resultado = self.__juego__.mover(1, dado)
            
            print(Color.t(Color.VERDE + Color.NEGRITA, f"\n  ✓ {resultado.capitalize()}"))
            self._finalizar_movimiento(resultado)
            
        except (ValueError, BackgammonError) as e:
            print(Color.t(Color.ROJO, f"  ⚠ Error: {e}"))
    
    def _seleccionar_dado_y_mover(self, origen: int, pendientes: list[int]):
        """Permite seleccionar el dado y ejecutar el movimiento."""
        dados_unicos = sorted(set(pendientes), reverse=True)
        color_turno = self.__juego__.obtener_turno()
        jugador = 1 if color_turno == "blancas" else -1
        
        print(f"\n  {Color.t(Color.AMARILLO, f'Moviendo desde posición {origen}:')}\n")
        
        # Mostrar opciones
        opciones_validas = []
        for dado in dados_unicos:
            destino = origen + (jugador * dado)
            
            if 1 <= destino <= 24:
                opciones_validas.append((dado, destino, "normal"))
                print(f"    {Color.t(Color.VERDE + Color.NEGRITA, f'{len(opciones_validas)}.')} "
                      f"Dado {dado} → Posición {destino}")
            elif destino > 24 or destino < 1:
                opciones_validas.append((dado, destino, "bear_off"))
                print(f"    {Color.t(Color.VERDE + Color.NEGRITA, f'{len(opciones_validas)}.')} "
                      f"Dado {dado} → {Color.t(Color.MAGENTA, '⬆ SACAR FICHA')}")
        
        if not opciones_validas:
            print(Color.t(Color.ROJO, "  ⚠ No hay movimientos válidos desde esa posición"))
            return
        
        try:
            opcion = int(input(f"\n  {Color.t(Color.AMARILLO, 'Elige opción:')} ")) - 1
            if not (0 <= opcion < len(opciones_validas)):
                print(Color.t(Color.ROJO, "  ⚠ Opción inválida"))
                return
            
            dado_elegido, destino, tipo = opciones_validas[opcion]
            
            # Confirmación
            if tipo == "bear_off":
                msg = f"sacar ficha desde posición {origen}"
            else:
                msg = f"mover de {origen} a {destino}"
            
            confirmar = input(f"  {Color.t(Color.GRIS, f'¿Confirmar {msg}? (s/n):')} ")
            if confirmar.lower() not in ['s', 'si', 'y', 'yes']:
                print(Color.t(Color.GRIS, "  Movimiento cancelado"))
                return
            
            # Ejecutar
            resultado = self.__juego__.mover(origen, dado_elegido)
            print(Color.t(Color.VERDE + Color.NEGRITA, f"\n  ✓ {resultado.capitalize()}"))
            self._finalizar_movimiento(resultado)
            
        except ValueError:
            print(Color.t(Color.ROJO, "  ⚠ Debes introducir un número"))
        except BackgammonError as e:
            print(Color.t(Color.ROJO, f"  ⚠ {e}"))
        except Exception as e:
            print(Color.t(Color.ROJO, f"  ⚠ Error inesperado: {e}"))
    
    def _finalizar_movimiento(self, resultado: str):
        """Finaliza el movimiento y actualiza el estado."""
        self.mostrar_tablero()
        
        restantes = self.__juego__.obtener_movimientos_pendientes()
        if restantes:
            print(f"  🎲 Dados restantes: {Color.t(Color.VERDE, str(restantes))}")
        else:
            print(Color.t(Color.GRIS, "  ✓ Todos los dados utilizados"))
            self.__juego__.finalizar_tirada()
            turno = self.__juego__.obtener_turno().capitalize()
            print(f"\n  {Color.t(Color.VERDE, '→')} Turno: {Color.t(Color.CYAN + Color.NEGRITA, turno)}")
        
        if "ganaron" in resultado:
            print(Color.t(Color.VERDE + Color.NEGRITA, "\n  🏆 ¡JUEGO TERMINADO! 🏆"))
            return True
        
        return False
    
    def mostrar_estado(self, *args):
        """Muestra estado resumido."""
        print(f"\n{Color.t(Color.AMARILLO + Color.NEGRITA, '═══ ESTADO DEL JUEGO ═══')}\n")
        
        turno = self.__juego__.obtener_turno().capitalize()
        print(f"  Turno: {Color.t(Color.CYAN + Color.NEGRITA, turno)}")
        
        pendientes = self.__juego__.obtener_movimientos_pendientes()
        if pendientes:
            print(f"  Dados: {Color.t(Color.VERDE, str(pendientes))}")
        else:
            print(f"  Dados: {Color.t(Color.GRIS, 'ninguno')}")
        
        barra = self._obtener_barra()
        if barra['blancas'] > 0 or barra['negras'] > 0:
            print(f"  Barra: {Color.t(Color.CYAN, '●')} {barra['blancas']}  │  "
                  f"{Color.t(Color.MAGENTA, '●')} {barra['negras']}")
        
        fichas_fuera = self._obtener_fichas_fuera()
        print(f"  Fuera: {Color.t(Color.CYAN, '●')} {fichas_fuera.get('blancas', 0)}  │  "
              f"{Color.t(Color.MAGENTA, '●')} {fichas_fuera.get('negras', 0)}\n")
    
    def finalizar_tirada(self, *args):
        """Finaliza la tirada actual manualmente."""
        pendientes = self.__juego__.obtener_movimientos_pendientes()
        if pendientes:
            print(f"  ⚠ Tienes dados sin usar: {pendientes}")
            respuesta = input(f"  {Color.t(Color.AMARILLO, '¿Seguro finalizar? (s/n):')} ")
            if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
                print(Color.t(Color.GRIS, "  Cancelado"))
                return
        
        self.__juego__.finalizar_tirada()
        turno = self.__juego__.obtener_turno().capitalize()
        print(f"  ✓ Tirada finalizada")
        print(f"  {Color.t(Color.VERDE, '→')} Turno: {Color.t(Color.CYAN + Color.NEGRITA, turno)}")
        self.mostrar_tablero()
    
    def salir(self, *args):
        """Sale del juego."""
        print(f"\n{Color.t(Color.CYAN + Color.NEGRITA, '  👋 ¡Gracias por jugar!')}\n")
        return True
    
    # ========== PROCESAMIENTO DE COMANDOS ==========
    
    def procesar_comando(self, entrada: str) -> bool:
        """Procesa un comando del usuario."""
        partes = entrada.strip().lower().split()
        if not partes:
            return False
        
        comando = partes[0]
        argumentos = partes[1:]
        
        if comando in self.__comandos__:
            return self.__comandos__[comando](*argumentos)
        else:
            print(Color.t(Color.ROJO, f"  ⚠ Comando desconocido: '{comando}'"))
            print(f"  {Color.t(Color.GRIS, 'Escribe')} {Color.t(Color.AMARILLO, 'help')} "
                  f"{Color.t(Color.GRIS, 'para ver comandos')}")
            return False
    
    def ejecutar(self):
        """Bucle principal del CLI."""
        self.mostrar_bienvenida()
        
        try:
            while True:
                try:
                    turno = self.__juego__.obtener_turno()
                    prompt = Color.t(Color.CYAN + Color.NEGRITA, f"{turno}> ")
                    entrada = input(f"\n{prompt}")
                    
                    if not entrada.strip():
                        continue
                    
                    if self.procesar_comando(entrada):
                        break
                        
                except KeyboardInterrupt:
                    print(f"\n\n{Color.t(Color.CYAN, '  👋 Salida con Ctrl+C')}")
                    break
                except EOFError:
                    print(f"\n\n{Color.t(Color.CYAN, '  👋 Salida con Ctrl+D')}")
                    break
                    
        except Exception as e:
            print(Color.t(Color.ROJO, f"\n  ⚠ Error fatal: {e}"))
            sys.exit(1)


def main():
    """Función principal para ejecutar el CLI."""
    cli = BackgammonCLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()