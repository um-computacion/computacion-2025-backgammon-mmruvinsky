import sys
import os
from pathlib import Path
from source.backgammon import Backgammon
from source.excepciones import *


class BackgammonCLI:
    """Interfaz de línea de comandos para el juego de Backgammon"""
    
    def __init__(self):
        self.juego = Backgammon()
        self.comandos = {
            'help': self.mostrar_ayuda,
            'h': self.mostrar_ayuda,
            'dados': self.tirar_dados,
            'd': self.tirar_dados,
            'mover': self.mover_ficha,
            'm': self.mover_ficha,
            'estado': self.mostrar_estado,
            'e': self.mostrar_estado,
            'salir': self.salir,
            'q': self.salir,
            'finalizar': self.finalizar_tirada,
            'f': self.finalizar_tirada
        }
    
    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida"""
        print("=" * 50)
        print("    BACKGAMMON - CLI BÁSICO")
        print("=" * 50)
        print("Escribe 'help' para ver los comandos disponibles")
        print("Turno actual:", self.juego.obtener_turno().capitalize())
        print()
    
    def mostrar_ayuda(self, *args):
        """Muestra la lista de comandos disponibles"""
        print("\n--- COMANDOS DISPONIBLES ---")
        print("help, h          - Mostrar esta ayuda")
        print("dados, d         - Tirar dados")
        print("mover, m <pos>   - Mover ficha desde posición (1-24)")
        print("                   Ejemplo: mover 8")
        print("estado, e        - Mostrar estado del tablero")
        print("finalizar, f     - Finalizar tirada actual")
        print("salir, q         - Salir del juego")
        print()
        print("NOTA: Las fichas en la barra se mueven automáticamente")
        print("      al usar el comando 'mover' con cualquier posición.")
        print()
    
    def tirar_dados(self, *args):
        """Tira los dados y muestra el resultado"""
        try:
            d1, d2 = self.juego.tirar_dados()
            print(f"🎲 Dados: {d1}, {d2}")
            
            if d1 == d2:
                print(f"¡Dobles! Tienes 4 movimientos de {d1}")
            
            pendientes = self.juego.obtener_movimientos_pendientes()
            print(f"Movimientos disponibles: {pendientes}")
            
            # Verificar si hay movimientos posibles
            if not self.juego.hay_movimiento_posible():
                print("⚠️  No hay movimientos posibles con estos dados")
                print("Presiona enter para finalizar tirada...")
                input()
                self.juego.finalizar_tirada()
                print(f"Turno cambiado a: {self.juego.obtener_turno().capitalize()}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def mover_ficha(self, *args):
        """Mueve una ficha desde la posición especificada"""
        if not args:
            print("❌ Debes especificar una posición (1-24)")
            print("Ejemplo: mover 8")
            return
        
        try:
            posicion = int(args[0])
            if not (1 <= posicion <= 24):
                print("❌ La posición debe estar entre 1 y 24")
                return
            
        except ValueError:
            print("❌ La posición debe ser un número")
            return
        
        # Mostrar dados disponibles
        pendientes = self.juego.obtener_movimientos_pendientes()
        if not pendientes:
            print("❌ No hay dados disponibles. Tira los dados primero.")
            return
        
        print(f"Dados disponibles: {pendientes}")
        
        # Si hay múltiples opciones, pedir al usuario que elija
        if len(set(pendientes)) > 1:
            try:
                dado_str = input("¿Qué dado quieres usar? ")
                dado = int(dado_str)
                if dado not in pendientes:
                    print(f"❌ El dado {dado} no está disponible")
                    return
            except ValueError:
                print("❌ Debes introducir un número válido")
                return
        else:
            dado = pendientes[0]
            print(f"Usando dado: {dado}")
        
        # Intentar el movimiento
        try:
            resultado = self.juego.mover(posicion, dado)
            print(f"✅ {resultado.capitalize()}")
            
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
                return True  # Señal para terminar el juego
                
        except BackgammonError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        return False
    
    def mostrar_estado(self, *args):
        """Muestra el estado actual del tablero"""
        print("\n--- ESTADO DEL JUEGO ---")
        print(f"Turno: {self.juego.obtener_turno().capitalize()}")
        
        # Mostrar dados pendientes
        pendientes = self.juego.obtener_movimientos_pendientes()
        if pendientes:
            print(f"Dados pendientes: {pendientes}")
        else:
            print("Sin dados pendientes")
        
        # Acceder al tablero (asumiendo que tiene métodos públicos o getters)
        try:
            # Nota: Necesitarías agregar un método público en Tablero para esto
            # Por ahora, mostraremos información básica
            print("\n(Para ver el estado completo del tablero, necesitas implementar")
            print("métodos de visualización en la clase Tablero)")
            
        except Exception as e:
            print(f"No se puede mostrar el tablero: {e}")
        
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
                    entrada = input(f"{self.juego.obtener_turno()}> ")
                    
                    # Permitir salida rápida con Ctrl+C o comandos vacíos
                    if not entrada.strip():
                        continue
                    
                    # Procesar el comando
                    if self.procesar_comando(entrada):
                        break  # Salir del bucle principal
                        
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