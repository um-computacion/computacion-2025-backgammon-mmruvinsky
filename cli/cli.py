#!/usr/bin/env python3
"""
CLI mejorado para probar el juego de Backgammon con tablero visual
"""

import sys
import os

# Configurar path para importaciones
script_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(script_dir, "source")
sys.path.insert(0, source_dir)

from source.backgammon import Backgammon
from source.excepciones import *


class BackgammonCLI:
    """Interfaz de línea de comandos mejorada para Backgammon"""
    
    def __init__(self):
        self.juego = Backgammon()
        self.comandos = {
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
    
    def obtener_posiciones_tablero(self):
        """Obtiene las posiciones del tablero desde el juego"""
        # Acceder a las posiciones del tablero (necesitarás exponer esto públicamente)
        return self.juego.__tablero__.__posiciones__
    
    def obtener_barra(self):
        """Obtiene el estado de la barra"""
        return self.juego.__tablero__.__barra__
    
    def obtener_fichas_fuera(self):
        """Obtiene las fichas que están fuera del tablero"""
        return self.juego.__tablero__.__fichas_fuera__
    
    def mostrar_tablero(self, *args):
        """Muestra el tablero visual en ASCII"""
        posiciones = self.obtener_posiciones_tablero()
        barra = self.obtener_barra()
        fichas_fuera = self.obtener_fichas_fuera()
        
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
    
    def _mostrar_fila_superior(self, posiciones):
        """Muestra la fila superior del tablero (13-24)"""
        print("┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Números de posición
        numeros = "│"
        for i in range(13, 25):
            numeros += f" {i:2d}  │"
        print(numeros)
        
        print("├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Fichas (máximo 5 filas visibles)
        for fila in range(5):
            linea = "│"
            for pos in range(12, 24):  # Posiciones 13-24 (índices 12-23)
                fichas = posiciones[pos]
                if abs(fichas) > fila:
                    if fichas > 0:
                        linea += "  B  │"  # Blanca
                    else:
                        linea += "  N  │"  # Negra
                else:
                    linea += "     │"
                
                # Separador en el medio (después de posición 18)
                if pos == 17:  # índice 17 = posición 18
                    linea += "   │"
            
            print(linea)
        
        print("└─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")
    
    def _mostrar_barra(self, barra):
        """Muestra la barra central"""
        print(f"                                 BARRA")
        print(f"                        Blancas: {barra.get('blancas', 0)} | Negras: {barra.get('negras', 0)}")
        print()
    
    def _mostrar_fila_inferior(self, posiciones):
        """Muestra la fila inferior del tablero (12-1)"""
        print("┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Fichas (máximo 5 filas visibles)
        for fila in range(4, -1, -1):  # De arriba hacia abajo
            linea = "│"
            for pos in range(11, -1, -1):  # Posiciones 12-1 (índices 11-0)
                fichas = posiciones[pos]
                if abs(fichas) > fila:
                    if fichas > 0:
                        linea += "  B  │"  # Blanca
                    else:
                        linea += "  N  │"  # Negra
                else:
                    linea += "     │"
                
                # Separador en el medio (después de posición 7)
                if pos == 6:  # índice 6 = posición 7
                    linea += "   │"
            
            print(linea)
        
        print("├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Números de posición
        numeros = "│"
        for i in range(12, 0, -1):
            numeros += f" {i:2d}  │"
        print(numeros)
        
        print("└─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")
    
    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida"""
        print("=" * 80)
        print("                    BACKGAMMON - CLI MEJORADO")
        print("=" * 80)
        print("Escribe 'help' para ver los comandos disponibles")
        print("Turno actual:", self.juego.obtener_turno().capitalize())
        self.mostrar_tablero()
    
    def mostrar_ayuda(self, *args):
        """Muestra la lista de comandos disponibles"""
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
        print("Blancas se mueven hacia números más altos (1→24)")
        print("Negras se mueven hacia números más bajos (24→1)")
        print()
    
    def tirar_dados(self, *args):
        """Tira los dados y muestra el resultado"""
        try:
            d1, d2 = self.juego.tirar_dados()
            print(f"\n🎲 Dados: {d1}, {d2}")
            
            if d1 == d2:
                print(f"¡Dobles! Tienes 4 movimientos de {d1}")
            
            pendientes = self.juego.obtener_movimientos_pendientes()
            print(f"Movimientos disponibles: {pendientes}")
            
            # Mostrar tablero después de tirar
            self.mostrar_tablero()
            
            # Verificar si hay movimientos posibles
            if not self.juego.hay_movimiento_posible():
                print("⚠️  No hay movimientos posibles con estos dados")
                input("Presiona Enter para finalizar tirada...")
                self.juego.finalizar_tirada()
                print(f"Turno cambiado a: {self.juego.obtener_turno().capitalize()}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def mover_ficha_interactivo(self, *args):
        """Modo interactivo para mover fichas"""
        # Verificar dados disponibles
        pendientes = self.juego.obtener_movimientos_pendientes()
        if not pendientes:
            print("❌ No hay dados disponibles. Tira los dados primero.")
            return
        
        # Mostrar tablero actual
        self.mostrar_tablero()
        
        # Verificar fichas en barra primero
        jugador = 1 if self.juego.obtener_turno() == "blancas" else -1
        barra = self.obtener_barra()
        fichas_en_barra = barra.get('blancas', 0) if jugador == 1 else barra.get('negras', 0)
        
        if fichas_en_barra > 0:
            print(f"⚠️  Tienes {fichas_en_barra} ficha(s) en la BARRA.")
            print("Debes entrar primero antes de mover otras fichas.")
            return self._mover_desde_barra(pendientes)
        
        # Selección de origen
        print(f"Dados disponibles: {pendientes}")
        print(f"Turno de: {self.juego.obtener_turno().capitalize()}")
        
        try:
            # Pedir posición origen
            origen_str = input("¿Desde qué posición quieres mover? (1-24): ").strip()
            if not origen_str:
                print("❌ Movimiento cancelado")
                return
            
            origen = int(origen_str)
            if not (1 <= origen <= 24):
                print("❌ La posición debe estar entre 1 y 24")
                return
            
            # Verificar que hay fichas propias en el origen
            posiciones = self.obtener_posiciones_tablero()
            valor_origen = posiciones[origen - 1]
            if valor_origen * jugador <= 0:
                print("❌ No tienes fichas en esa posición")
                return
            
            # Mostrar opciones de dados
            return self._seleccionar_dado_y_mover(origen, pendientes)
            
        except ValueError:
            print("❌ Debes introducir un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _mover_desde_barra(self, pendientes):
        """Maneja el movimiento desde la barra"""
        print("\nSelecciona qué dado usar para entrar desde la barra:")
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
                    print("❌ Opción inválida")
                    return
                dado = dados_unicos[opcion]
            except ValueError:
                print("❌ Debes introducir un número")
                return
        
        try:
            resultado = self.juego.mover(1, dado)  # Usar cualquier posición para barra
            print(f"✅ {resultado.capitalize()}")
            self._finalizar_movimiento(resultado)
        except BackgammonError as e:
            print(f"❌ {e}")
    
    def _seleccionar_dado_y_mover(self, origen, pendientes):
        """Permite seleccionar el dado y ejecutar el movimiento"""
        dados_unicos = list(set(pendientes))
        jugador = 1 if self.juego.obtener_turno() == "blancas" else -1
        
        print(f"\nMoviendo desde posición {origen}")
        print("Opciones disponibles:")
        
        # Mostrar destinos posibles
        opciones_validas = []
        for i, dado in enumerate(dados_unicos, 1):
            destino = origen + (jugador * dado)
            
            if 1 <= destino <= 24:
                print(f"{i}. Usar dado {dado} → ir a posición {destino}")
                opciones_validas.append((dado, destino, "normal"))
            elif destino > 24 or destino < 1:
                # Posible bear off
                print(f"{i}. Usar dado {dado} → SACAR FICHA (bear off)")
                opciones_validas.append((dado, destino, "bear_off"))
        
        if not opciones_validas:
            print("❌ No hay movimientos válidos desde esa posición")
            return
        
        try:
            opcion = int(input("Elige una opción: ")) - 1
            if not (0 <= opcion < len(opciones_validas)):
                print("❌ Opción inválida")
                return
            
            dado_elegido, destino, tipo = opciones_validas[opcion]
            
            # Confirmar movimiento
            if tipo == "bear_off":
                confirmar = input(f"¿Confirmar sacar ficha desde posición {origen}? (s/n): ")
            else:
                confirmar = input(f"¿Confirmar mover de {origen} a {destino}? (s/n): ")
            
            if confirmar.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                print("Movimiento cancelado")
                return
            
            # Ejecutar movimiento
            resultado = self.juego.mover(origen, dado_elegido)
            print(f"✅ {resultado.capitalize()}")
            self._finalizar_movimiento(resultado)
            
        except ValueError:
            print("❌ Debes introducir un número")
        except BackgammonError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def _finalizar_movimiento(self, resultado):
        """Finaliza el movimiento y actualiza el estado"""
        # Mostrar tablero actualizado
        self.mostrar_tablero()
        
        # Mostrar movimientos restantes
        restantes = self.juego.obtener_movimientos_pendientes()
        if restantes:
            print(f"Movimientos restantes: {restantes}")
        else:
            print("🎯 Todos los dados utilizados")
            self.juego.finalizar_tirada()
            print(f"Turno cambiado a: {self.juego.obtener_turno().capitalize()}")
        
        # Verificar si el juego terminó
        if "ganaron" in resultado:
            print("\n🎉 ¡JUEGO TERMINADO! 🎉")
            return True
        
        return False
    
    def mostrar_estado(self, *args):
        """Muestra el estado resumido del juego"""
        print("\n--- ESTADO RESUMIDO ---")
        print(f"Turno: {self.juego.obtener_turno().capitalize()}")
        
        pendientes = self.juego.obtener_movimientos_pendientes()
        if pendientes:
            print(f"Dados pendientes: {pendientes}")
        else:
            print("Sin dados pendientes")
        
        barra = self.obtener_barra()
        if barra['blancas'] > 0 or barra['negras'] > 0:
            print(f"Fichas en barra - Blancas: {barra['blancas']}, Negras: {barra['negras']}")
        
        fichas_fuera = self.obtener_fichas_fuera()
        print(f"Fichas fuera - Blancas: {fichas_fuera.get('blancas', 0)}, Negras: {fichas_fuera.get('negras', 0)}")
        print()
    
    def finalizar_tirada(self, *args):
        """Finaliza la tirada actual manualmente"""
        pendientes = self.juego.obtener_movimientos_pendientes()
        if pendientes:
            print(f"⚠️  Tienes dados sin usar: {pendientes}")
            respuesta = input("¿Estás seguro de finalizar la tirada? (s/n): ")
            if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                print("Tirada no finalizada")
                return
        
        self.juego.finalizar_tirada()
        print(f"✅ Tirada finalizada. Turno: {self.juego.obtener_turno().capitalize()}")
        self.mostrar_tablero()
    
    def salir(self, *args):
        """Sale del juego"""
        print("\n👋 ¡Gracias por jugar!")
        return True
    
    def procesar_comando(self, entrada):
        """Procesa un comando del usuario"""
        partes = entrada.strip().lower().split()
        if not partes:
            return False
        
        comando = partes[0]
        argumentos = partes[1:]
        
        if comando in self.comandos:
            return self.comandos[comando](*argumentos)
        else:
            print(f"❌ Comando desconocido: '{comando}'")
            print("Escribe 'help' para ver los comandos disponibles")
            return False
    
    def ejecutar(self):
        """Bucle principal del CLI"""
        self.mostrar_bienvenida()
        
        try:
            while True:
                try:
                    entrada = input(f"\n{self.juego.obtener_turno()}> ")
                    
                    if not entrada.strip():
                        continue
                    
                    if self.procesar_comando(entrada):
                        break
                        
                except KeyboardInterrupt:
                    print("\n\n👋 Salida con Ctrl+C")
                    break
                except EOFError:
                    print("\n\n👋 Salida con Ctrl+D")
                    break
                    
        except Exception as e:
            print(f"\n❌ Error fatal: {e}")
            sys.exit(1)


def main():
    """Función principal"""
    cli = BackgammonCLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()