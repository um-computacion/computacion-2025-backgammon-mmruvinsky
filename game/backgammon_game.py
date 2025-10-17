import pygame
import sys
from source.backgammon import Backgammon
from source.excepciones import *

# Inicializar Pygame
pygame.init()

# Constantes de colores
MARRON_OSCURO = (101, 67, 33)
MARRON_CLARO = (205, 170, 125)
BEIGE = (245, 222, 179)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (200, 50, 50)
VERDE = (50, 150, 50)
AZUL = (50, 100, 200)
AMARILLO = (255, 215, 0)
GRIS = (128, 128, 128)

# Dimensiones
ANCHO = 1200
ALTO = 800
ANCHO_TABLERO = 1000
MARGEN = 50
ANCHO_PUNTO = 60
ALTO_PUNTO = 200
RADIO_FICHA = 25
ESPACIO_BARRA = 60

class BackgammonGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Backgammon")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.juego = Backgammon()
        self.dados_tirados = False
        self.dados_valores = (0, 0)
        self.ficha_seleccionada = None
        self.mensaje = "Presiona ESPACIO para tirar dados"
        
    def pos_a_coordenadas(self, pos):
        """Convierte posición del tablero (1-24) a coordenadas x,y del punto"""
        if 1 <= pos <= 12:
            # Mitad inferior
            if pos <= 6:
                x = MARGEN + (pos - 1) * ANCHO_PUNTO
            else:
                x = MARGEN + (pos - 1) * ANCHO_PUNTO + ESPACIO_BARRA
            y = ALTO - MARGEN - ALTO_PUNTO
            return x + ANCHO_PUNTO // 2, y + ALTO_PUNTO - 30
        else:
            # Mitad superior (13-24)
            pos_inversa = 25 - pos
            if pos_inversa <= 6:
                x = MARGEN + (pos_inversa - 1) * ANCHO_PUNTO
            else:
                x = MARGEN + (pos_inversa - 1) * ANCHO_PUNTO + ESPACIO_BARRA
            y = MARGEN
            return x + ANCHO_PUNTO // 2, y + 30
    
    def coordenadas_a_pos(self, x, y):
        """Convierte coordenadas del mouse a posición del tablero"""
        if y > ALTO // 2:
            # Mitad inferior (posiciones 1-12)
            if x < MARGEN or x > MARGEN + 6 * ANCHO_PUNTO + ESPACIO_BARRA + 6 * ANCHO_PUNTO:
                return None
            
            x_rel = x - MARGEN
            if x_rel < 6 * ANCHO_PUNTO:
                pos = x_rel // ANCHO_PUNTO + 1
            elif x_rel > 6 * ANCHO_PUNTO + ESPACIO_BARRA:
                pos = (x_rel - ESPACIO_BARRA) // ANCHO_PUNTO + 1
            else:
                return None
            return pos if 1 <= pos <= 12 else None
        else:
            # Mitad superior (posiciones 13-24)
            if x < MARGEN or x > MARGEN + 6 * ANCHO_PUNTO + ESPACIO_BARRA + 6 * ANCHO_PUNTO:
                return None
            
            x_rel = x - MARGEN
            if x_rel < 6 * ANCHO_PUNTO:
                pos = 24 - x_rel // ANCHO_PUNTO
            elif x_rel > 6 * ANCHO_PUNTO + ESPACIO_BARRA:
                pos = 24 - (x_rel - ESPACIO_BARRA) // ANCHO_PUNTO
            else:
                return None
            return pos if 13 <= pos <= 24 else None
    
    def dibujar_tablero(self):
        """Dibuja el tablero de backgammon"""
        self.screen.fill(MARRON_CLARO)
        
        # Borde del tablero
        pygame.draw.rect(self.screen, MARRON_OSCURO, 
                        (MARGEN - 10, MARGEN - 10, 
                         ANCHO_TABLERO + 20, ALTO - 2 * MARGEN + 20), 5)
        
        # Dibujar puntos (triángulos)
        for i in range(24):
            if i < 12:
                # Mitad inferior
                if i < 6:
                    x = MARGEN + i * ANCHO_PUNTO
                else:
                    x = MARGEN + i * ANCHO_PUNTO + ESPACIO_BARRA
                y_base = ALTO - MARGEN
                y_punta = y_base - ALTO_PUNTO
                color = MARRON_OSCURO if i % 2 == 0 else BEIGE
                puntos = [(x, y_base), 
                         (x + ANCHO_PUNTO, y_base),
                         (x + ANCHO_PUNTO // 2, y_punta)]
            else:
                # Mitad superior
                idx = 23 - i
                if idx < 6:
                    x = MARGEN + idx * ANCHO_PUNTO
                else:
                    x = MARGEN + idx * ANCHO_PUNTO + ESPACIO_BARRA
                y_base = MARGEN
                y_punta = y_base + ALTO_PUNTO
                color = MARRON_OSCURO if i % 2 == 0 else BEIGE
                puntos = [(x, y_base),
                         (x + ANCHO_PUNTO, y_base),
                         (x + ANCHO_PUNTO // 2, y_punta)]
            
            pygame.draw.polygon(self.screen, color, puntos)
            pygame.draw.polygon(self.screen, NEGRO, puntos, 2)
        
        # Barra central
        barra_x = MARGEN + 6 * ANCHO_PUNTO
        pygame.draw.rect(self.screen, MARRON_OSCURO,
                        (barra_x, MARGEN, ESPACIO_BARRA, ALTO - 2 * MARGEN))
    
    def dibujar_fichas(self):
        """Dibuja todas las fichas en el tablero"""
        posiciones = self.juego.obtener_posiciones()
        
        # Fichas en el tablero
        for pos_idx, valor in enumerate(posiciones):
            if valor != 0:
                pos = pos_idx + 1
                x, y = self.pos_a_coordenadas(pos)
                color = BLANCO if valor > 0 else NEGRO
                num_fichas = abs(valor)
                
                for i in range(num_fichas):
                    if pos <= 12:
                        y_ficha = y - i * (RADIO_FICHA + 2)
                    else:
                        y_ficha = y + i * (RADIO_FICHA + 2)
                    
                    # Resaltar si está seleccionada
                    if self.ficha_seleccionada == pos:
                        pygame.draw.circle(self.screen, AMARILLO, (x, y_ficha), RADIO_FICHA + 3)
                    
                    pygame.draw.circle(self.screen, color, (x, y_ficha), RADIO_FICHA)
                    pygame.draw.circle(self.screen, NEGRO, (x, y_ficha), RADIO_FICHA, 2)
        
        # Fichas en la barra
        barra = self.juego.obtener_barra()
        barra_x = MARGEN + 6 * ANCHO_PUNTO + ESPACIO_BARRA // 2
        
        if barra['blancas'] > 0:
            for i in range(barra['blancas']):
                y = ALTO // 2 + 50 + i * (RADIO_FICHA + 2)
                pygame.draw.circle(self.screen, BLANCO, (barra_x, y), RADIO_FICHA)
                pygame.draw.circle(self.screen, NEGRO, (barra_x, y), RADIO_FICHA, 2)
        
        if barra['negras'] > 0:
            for i in range(barra['negras']):
                y = ALTO // 2 - 50 - i * (RADIO_FICHA + 2)
                pygame.draw.circle(self.screen, NEGRO, (barra_x, y), RADIO_FICHA)
                pygame.draw.circle(self.screen, BLANCO, (barra_x, y), RADIO_FICHA, 2)
        
        # Fichas fuera
        fichas_fuera = self.juego.obtener_fichas_fuera()
        fuera_x = MARGEN + ANCHO_TABLERO + 30
        
        # Blancas fuera (derecha abajo)
        if fichas_fuera['blancas'] > 0:
            y_base = ALTO - MARGEN - 100
            for i in range(min(fichas_fuera['blancas'], 5)):
                pygame.draw.circle(self.screen, BLANCO, (fuera_x, y_base + i * 25), RADIO_FICHA - 5)
                pygame.draw.circle(self.screen, NEGRO, (fuera_x, y_base + i * 25), RADIO_FICHA - 5, 2)
            if fichas_fuera['blancas'] > 5:
                texto = self.font_small.render(f"{fichas_fuera['blancas']}", True, NEGRO)
                self.screen.blit(texto, (fuera_x - 10, y_base - 40))
        
        # Negras fuera (derecha arriba)
        if fichas_fuera['negras'] > 0:
            y_base = MARGEN + 100
            for i in range(min(fichas_fuera['negras'], 5)):
                pygame.draw.circle(self.screen, NEGRO, (fuera_x, y_base + i * 25), RADIO_FICHA - 5)
                pygame.draw.circle(self.screen, BLANCO, (fuera_x, y_base + i * 25), RADIO_FICHA - 5, 2)
            if fichas_fuera['negras'] > 5:
                texto = self.font_small.render(f"{fichas_fuera['negras']}", True, BLANCO)
                self.screen.blit(texto, (fuera_x - 10, y_base - 40))
    
    def dibujar_dados(self):
        """Dibuja los dados"""
        if self.dados_tirados:
            dado_x = ANCHO - 150
            dado_y = ALTO // 2 - 80
            
            for i, valor in enumerate(self.dados_valores):
                y = dado_y + i * 70
                # Fondo del dado
                pygame.draw.rect(self.screen, BLANCO, 
                               (dado_x, y, 50, 50), border_radius=5)
                pygame.draw.rect(self.screen, NEGRO,
                               (dado_x, y, 50, 50), 2, border_radius=5)
                
                # Número
                texto = self.font.render(str(valor), True, NEGRO)
                texto_rect = texto.get_rect(center=(dado_x + 25, y + 25))
                self.screen.blit(texto, texto_rect)
    
    def dibujar_info(self):
        """Dibuja información del juego"""
        # Turno actual
        turno = self.juego.obtener_turno()
        color_turno = BLANCO if turno == "blancas" else NEGRO
        color_fondo = NEGRO if turno == "blancas" else BLANCO
        
        pygame.draw.rect(self.screen, color_fondo, (ANCHO - 180, 50, 160, 50))
        texto_turno = self.font_small.render(f"Turno: {turno}", True, color_turno)
        self.screen.blit(texto_turno, (ANCHO - 170, 60))
        
        # Movimientos pendientes
        movs = self.juego.obtener_movimientos_pendientes()
        if movs:
            texto_movs = self.font_small.render(f"Dados: {movs}", True, NEGRO)
            self.screen.blit(texto_movs, (ANCHO - 170, 120))
        
        # Mensaje
        if self.mensaje:
            # Fondo del mensaje
            pygame.draw.rect(self.screen, BEIGE, (50, 10, ANCHO - 100, 30))
            pygame.draw.rect(self.screen, NEGRO, (50, 10, ANCHO - 100, 30), 2)
            texto_msg = self.font_small.render(self.mensaje, True, NEGRO)
            self.screen.blit(texto_msg, (60, 15))
        
        # Instrucciones
        inst_y = ALTO - 100
        instrucciones = [
            "ESPACIO: Tirar dados",
            "Click: Seleccionar/Mover ficha",
            "F: Finalizar turno",
            "R: Reiniciar juego"
        ]
        for i, inst in enumerate(instrucciones):
            texto = self.font_small.render(inst, True, NEGRO)
            self.screen.blit(texto, (ANCHO - 250, inst_y + i * 25))
    
    def intentar_movimiento(self, origen):
        """Intenta realizar un movimiento desde el origen seleccionado"""
        movs = self.juego.obtener_movimientos_pendientes()
        if not movs:
            self.mensaje = "No hay dados disponibles"
            return
        
        # Intentar con cada dado disponible
        for dado in movs:
            try:
                resultado = self.juego.mover(origen, dado)
                self.mensaje = f"¡{resultado}!"
                self.ficha_seleccionada = None
                
                # Verificar si el juego terminó
                if "ganaron" in resultado:
                    self.dados_tirados = False
                
                # Si no quedan movimientos, sugerir finalizar turno
                if not self.juego.movimientos_disponibles():
                    if not self.juego.hay_movimiento_posible():
                        self.mensaje += " - Presiona F para finalizar turno"
                return
            except (OrigenInvalidoError, DestinoBloquedoError, 
                    DadoNoDisponibleError, BearOffInvalidoError) as e:
                continue
        
        self.mensaje = "Movimiento inválido con dados disponibles"
    
    def manejar_evento_mouse(self, pos):
        """Maneja clicks del mouse"""
        if not self.dados_tirados:
            return
        
        # Verificar click en barra
        barra_x = MARGEN + 6 * ANCHO_PUNTO
        if barra_x < pos[0] < barra_x + ESPACIO_BARRA:
            turno = self.juego.obtener_turno()
            if self.juego.tiene_fichas_en_barra(turno):
                # Intentar entrar desde barra
                movs = self.juego.obtener_movimientos_pendientes()
                for dado in movs:
                    try:
                        # Usar una posición ficticia, el método mover detectará la barra
                        resultado = self.juego.mover(1, dado)
                        self.mensaje = f"¡{resultado}!"
                        return
                    except Exception:
                        continue
                self.mensaje = "No se puede entrar desde la barra"
                return
        
        posicion = self.coordenadas_a_pos(pos[0], pos[1])
        if posicion is None:
            return
        
        turno_actual = self.juego.obtener_turno()
        valor_pos = self.juego.obtener_ficha_en_posicion(posicion)
        
        # Verificar si hay ficha del jugador actual
        es_ficha_propia = (turno_actual == "blancas" and valor_pos > 0) or \
                         (turno_actual == "negras" and valor_pos < 0)
        
        if self.ficha_seleccionada is None:
            if es_ficha_propia:
                self.ficha_seleccionada = posicion
                self.mensaje = f"Ficha en posición {posicion} seleccionada"
        else:
            # Intentar mover
            self.intentar_movimiento(self.ficha_seleccionada)
    
    def ejecutar(self):
        """Loop principal del juego"""
        ejecutando = True
        
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and not self.dados_tirados:
                        # Tirar dados
                        self.dados_valores = self.juego.tirar_dados()
                        self.dados_tirados = True
                        turno = self.juego.obtener_turno()
                        self.mensaje = f"Dados: {self.dados_valores} - Turno de {turno}"
                        self.ficha_seleccionada = None
                    
                    elif evento.key == pygame.K_f and self.dados_tirados:
                        # Finalizar turno
                        self.juego.finalizar_tirada()
                        self.dados_tirados = False
                        self.ficha_seleccionada = None
                        self.mensaje = "Turno finalizado - Presiona ESPACIO para tirar dados"
                    
                    elif evento.key == pygame.K_r:
                        # Reiniciar juego
                        self.juego = Backgammon()
                        self.dados_tirados = False
                        self.dados_valores = (0, 0)
                        self.ficha_seleccionada = None
                        self.mensaje = "Juego reiniciado - Presiona ESPACIO para tirar dados"
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.manejar_evento_mouse(evento.pos)
            
            # Dibujar todo
            self.dibujar_tablero()
            self.dibujar_fichas()
            self.dibujar_dados()
            self.dibujar_info()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    gui = BackgammonGUI()
    gui.ejecutar()