import pygame
import sys
from source.backgammon import Backgammon
from source.excepciones import *


class InterfazPygame:
    """
    Responsabilidad: Gestionar la ventana principal y el loop del juego.
    SRP: Coordina renderizado y eventos, delegando detalles al Renderizador y GestorEventos.
    """
    
    def __init__(self):
        """
        Inicializa Pygame y crea la ventana principal.
        """
        pygame.init()
        
        # Configuración de ventana
        self.__ancho__ = 1200
        self.__alto__ = 700
        self.__ventana__ = pygame.display.set_mode((self.__ancho__, self.__alto__))
        pygame.display.set_caption("Backgammon")
        
        # Reloj para controlar FPS
        self.__reloj__ = pygame.time.Clock()
        self.__fps__ = 60
        
        # Juego
        self.__juego__ = Backgammon()
        
        # Renderizador
        self.__renderizador__ = Renderizador(self.__ventana__, self.__ancho__, self.__alto__)
        
        # Gestor de eventos
        self.__gestor_eventos__ = GestorEventos(
            self.__juego__, 
            self.__renderizador__,
            self.__ancho__,
            self.__alto__
        )
        
        # Estado de UI
        self.__mensaje__ = "Blancas: haz clic en 'Tirar Dados'"
        self.__dados_tirados__ = False
        
    def ejecutar(self):
        """
        Loop principal del juego.
        """
        ejecutando = True
        
        while ejecutando:
            # Manejar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                else:
                    # Delegar al gestor de eventos
                    resultado = self.__gestor_eventos__.manejar_evento(
                        evento, 
                        self.__dados_tirados__
                    )
                    
                    if resultado:
                        if resultado['tipo'] == 'dados_tirados':
                            self.__dados_tirados__ = True
                            d1, d2 = resultado['dados']
                            turno = self.__juego__.obtener_turno()
                            self.__mensaje__ = f"{turno.capitalize()}: {d1}, {d2} - Mueve tus fichas"
                        
                        elif resultado['tipo'] == 'movimiento':
                            self.__mensaje__ = resultado['mensaje']
                            
                            # Verificar victoria
                            if "ganaron" in resultado['mensaje'].lower():
                                self.__dados_tirados__ = False
                            # Verificar si hay movimientos pendientes
                            elif not self.__juego__.movimientos_disponibles():
                                self.__juego__.finalizar_tirada()
                                nuevo_turno = self.__juego__.obtener_turno()
                                self.__mensaje__ = f"{nuevo_turno.capitalize()}: haz clic en 'Tirar Dados'"
                                self.__dados_tirados__ = False
                            elif not self.__juego__.hay_movimiento_posible():
                                self.__juego__.finalizar_tirada()
                                nuevo_turno = self.__juego__.obtener_turno()
                                self.__mensaje__ = f"Sin movimientos. {nuevo_turno.capitalize()}: Tira dados"
                                self.__dados_tirados__ = False
                        
                        elif resultado['tipo'] == 'error':
                            self.__mensaje__ = f"Error: {resultado['mensaje']}"
            
            # Renderizar
            self.__ventana__.fill((139, 90, 43))  # Color madera
            
            self.__renderizador__.dibujar_tablero()
            self.__renderizador__.dibujar_fichas(
                self.__juego__.obtener_posiciones(),
                self.__juego__.obtener_barra(),
                self.__juego__.obtener_fichas_fuera()
            )
            self.__renderizador__.dibujar_ui(
                self.__mensaje__,
                self.__juego__.obtener_turno(),
                self.__juego__.obtener_movimientos_pendientes(),
                self.__dados_tirados__
            )
            
            # Resaltar movimientos posibles
            if self.__dados_tirados__ and self.__gestor_eventos__.obtener_origen_seleccionado() is not None:
                origen = self.__gestor_eventos__.obtener_origen_seleccionado()
                movimientos = self.__juego__.obtener_movimientos_posibles()
                
                if origen == 'barra' and 'barra' in movimientos:
                    destinos_validos = [dest for dest, _ in movimientos['barra']]
                    self.__renderizador__.resaltar_destinos(destinos_validos)
                elif origen in movimientos:
                    destinos_validos = [dest for dest, _ in movimientos[origen]]
                    self.__renderizador__.resaltar_destinos(destinos_validos)
            
            pygame.display.flip()
            self.__reloj__.tick(self.__fps__)
        
        pygame.quit()
        sys.exit()


class Renderizador:
    """
    Responsabilidad: Dibujar todos los elementos visuales del juego.
    SRP: Solo renderiza, no maneja lógica de juego ni eventos.
    """
    
    def __init__(self, ventana, ancho, alto):
        """
        Inicializa el renderizador.
        
        Args:
            ventana: Surface de pygame
            ancho (int): Ancho de la ventana
            alto (int): Alto de la ventana
        """
        self.__ventana__ = ventana
        self.__ancho__ = ancho
        self.__alto__ = alto
        
        # Dimensiones del tablero
        self.__tablero_x__ = 50
        self.__tablero_y__ = 100
        self.__tablero_ancho__ = 900
        self.__tablero_alto__ = 500
        
        # Dimensiones de puntos (triángulos)
        self.__punto_ancho__ = self.__tablero_ancho__ // 13  # 12 puntos + barra
        self.__punto_alto__ = (self.__tablero_alto__ - 20) // 2
        
        # Dimensiones de fichas
        self.__ficha_radio__ = min(self.__punto_ancho__ // 2 - 5, 25)
        
        # Fuentes
        self.__fuente_titulo__ = pygame.font.Font(None, 48)
        self.__fuente_normal__ = pygame.font.Font(None, 32)
        self.__fuente_pequena__ = pygame.font.Font(None, 24)
        
        # Colores
        self.__color_punto_claro__ = (222, 184, 135)
        self.__color_punto_oscuro__ = (139, 90, 43)
        self.__color_barra__ = (100, 60, 30)
        self.__color_blancas__ = (255, 255, 255)
        self.__color_negras__ = (30, 30, 30)
        self.__color_borde__ = (0, 0, 0)
        self.__color_resaltado__ = (255, 255, 0)
    
    def dibujar_tablero(self):
        """
        Dibuja el tablero base (triángulos y barra).
        """
        # Fondo del tablero
        pygame.draw.rect(
            self.__ventana__,
            (160, 120, 80),
            (self.__tablero_x__, self.__tablero_y__, 
             self.__tablero_ancho__, self.__tablero_alto__)
        )
        
        # Borde
        pygame.draw.rect(
            self.__ventana__,
            self.__color_borde__,
            (self.__tablero_x__, self.__tablero_y__, 
             self.__tablero_ancho__, self.__tablero_alto__),
            3
        )
        
        # Barra central
        barra_x = self.__tablero_x__ + 6 * self.__punto_ancho__
        pygame.draw.rect(
            self.__ventana__,
            self.__color_barra__,
            (barra_x, self.__tablero_y__, 
             self.__punto_ancho__, self.__tablero_alto__)
        )
        
        # Dibujar puntos (triángulos)
        for i in range(24):
            self._dibujar_punto(i)
    
    def _dibujar_punto(self, posicion):
        """
        Dibuja un triángulo (punto) en la posición dada.
        
        Args:
            posicion (int): Posición 0-23
        """
        # Calcular coordenadas
        if posicion < 12:
            # Parte superior
            columna = 11 - posicion
            if columna >= 6:
                columna += 1  # Saltar barra
            
            x = self.__tablero_x__ + columna * self.__punto_ancho__
            y_base = self.__tablero_y__
            direccion = 1  # Hacia abajo
        else:
            # Parte inferior
            columna = posicion - 12
            if columna >= 6:
                columna += 1  # Saltar barra
            
            x = self.__tablero_x__ + columna * self.__punto_ancho__
            y_base = self.__tablero_y__ + self.__tablero_alto__
            direccion = -1  # Hacia arriba
        
        # Color alternado
        color = self.__color_punto_claro__ if posicion % 2 == 0 else self.__color_punto_oscuro__
        
        # Puntos del triángulo
        punta_x = x + self.__punto_ancho__ // 2
        punta_y = y_base + direccion * self.__punto_alto__
        
        puntos = [
            (x, y_base),
            (x + self.__punto_ancho__, y_base),
            (punta_x, punta_y)
        ]
        
        pygame.draw.polygon(self.__ventana__, color, puntos)
        pygame.draw.polygon(self.__ventana__, self.__color_borde__, puntos, 1)
    
    def dibujar_fichas(self, posiciones, barra, fichas_fuera):
        """
        Dibuja todas las fichas en el tablero.
        
        Args:
            posiciones (list[int]): Array de posiciones
            barra (dict): Fichas en la barra
            fichas_fuera (dict): Fichas fuera del tablero
        """
        # Fichas en posiciones
        for i, cantidad in enumerate(posiciones):
            if cantidad != 0:
                self._dibujar_fichas_en_posicion(i, cantidad)
        
        # Fichas en barra
        if barra['blancas'] > 0:
            self._dibujar_fichas_barra('blancas', barra['blancas'])
        if barra['negras'] > 0:
            self._dibujar_fichas_barra('negras', barra['negras'])
        
        # Fichas fuera
        self._dibujar_fichas_fuera('blancas', fichas_fuera['blancas'])
        self._dibujar_fichas_fuera('negras', fichas_fuera['negras'])
    
    def _dibujar_fichas_en_posicion(self, posicion, cantidad):
        """
        Dibuja fichas en una posición del tablero.
        
        Args:
            posicion (int): Posición 0-23
            cantidad (int): Cantidad (con signo)
        """
        color = self.__color_blancas__ if cantidad > 0 else self.__color_negras__
        num_fichas = abs(cantidad)
        
        # Calcular posición x, y
        if posicion < 12:
            columna = 11 - posicion
            if columna >= 6:
                columna += 1
            x = self.__tablero_x__ + columna * self.__punto_ancho__ + self.__punto_ancho__ // 2
            y_inicial = self.__tablero_y__ + 10
            direccion = 1
        else:
            columna = posicion - 12
            if columna >= 6:
                columna += 1
            x = self.__tablero_x__ + columna * self.__punto_ancho__ + self.__punto_ancho__ // 2
            y_inicial = self.__tablero_y__ + self.__tablero_alto__ - 10
            direccion = -1
        
        # Dibujar fichas (máximo 5 visibles, luego mostrar número)
        max_visible = 5
        for i in range(min(num_fichas, max_visible)):
            y = y_inicial + direccion * i * (self.__ficha_radio__ * 2 + 2)
            self._dibujar_ficha(x, y, color)
        
        # Si hay más de 5, mostrar número
        if num_fichas > max_visible:
            y = y_inicial + direccion * max_visible * (self.__ficha_radio__ * 2 + 2)
            texto = self.__fuente_pequena__.render(str(num_fichas), True, (255, 0, 0))
            rect = texto.get_rect(center=(x, y))
            self.__ventana__.blit(texto, rect)
    
    def _dibujar_ficha(self, x, y, color):
        """
        Dibuja una ficha individual.
        
        Args:
            x, y (int): Coordenadas del centro
            color: Color de la ficha
        """
        pygame.draw.circle(self.__ventana__, color, (x, y), self.__ficha_radio__)
        pygame.draw.circle(self.__ventana__, self.__color_borde__, (x, y), self.__ficha_radio__, 2)
    
    def _dibujar_fichas_barra(self, color_str, cantidad):
        """
        Dibuja fichas en la barra.
        
        Args:
            color_str (str): 'blancas' o 'negras'
            cantidad (int): Cantidad de fichas
        """
        color = self.__color_blancas__ if color_str == 'blancas' else self.__color_negras__
        
        barra_x = self.__tablero_x__ + 6 * self.__punto_ancho__ + self.__punto_ancho__ // 2
        
        if color_str == 'blancas':
            y_inicial = self.__tablero_y__ + self.__tablero_alto__ // 4
        else:
            y_inicial = self.__tablero_y__ + 3 * self.__tablero_alto__ // 4
        
        for i in range(min(cantidad, 5)):
            y = y_inicial + i * (self.__ficha_radio__ * 2 + 2)
            self._dibujar_ficha(barra_x, y, color)
        
        if cantidad > 5:
            y = y_inicial + 5 * (self.__ficha_radio__ * 2 + 2)
            texto = self.__fuente_pequena__.render(str(cantidad), True, (255, 0, 0))
            rect = texto.get_rect(center=(barra_x, y))
            self.__ventana__.blit(texto, rect)
    
    def _dibujar_fichas_fuera(self, color_str, cantidad):
        """
        Dibuja fichas que salieron del tablero.
        
        Args:
            color_str (str): 'blancas' o 'negras'
            cantidad (int): Cantidad de fichas
        """
        color = self.__color_blancas__ if color_str == 'blancas' else self.__color_negras__
        
        x = self.__tablero_x__ + self.__tablero_ancho__ + 30
        
        if color_str == 'blancas':
            y = self.__tablero_y__ + self.__tablero_alto__ - 50
        else:
            y = self.__tablero_y__ + 50
        
        # Dibujar un stack representativo
        for i in range(min(cantidad, 3)):
            self._dibujar_ficha(x, y + i * 5, color)
        
        # Mostrar número
        texto = self.__fuente_normal__.render(f"{color_str.capitalize()}: {cantidad}/15", 
                                              True, color)
        self.__ventana__.blit(texto, (x + 30, y - 10))
    
    def dibujar_ui(self, mensaje, turno, movimientos_pendientes, dados_tirados):
        """
        Dibuja la interfaz de usuario (título, mensaje, botones).
        
        Args:
            mensaje (str): Mensaje a mostrar
            turno (str): Turno actual
            movimientos_pendientes (list): Dados pendientes
            dados_tirados (bool): Si ya se tiraron los dados
        """
        # Título
        titulo = self.__fuente_titulo__.render("BACKGAMMON", True, (255, 255, 255))
        self.__ventana__.blit(titulo, (self.__ancho__ // 2 - titulo.get_width() // 2, 20))
        
        # Mensaje
        texto_mensaje = self.__fuente_pequena__.render(mensaje, True, (255, 255, 255))
        self.__ventana__.blit(texto_mensaje, (50, self.__tablero_y__ + self.__tablero_alto__ + 20))
        
        # Botón tirar dados
        boton_rect = pygame.Rect(self.__ancho__ - 250, 150, 200, 50)
        color_boton = (100, 100, 100) if dados_tirados else (0, 150, 0)
        pygame.draw.rect(self.__ventana__, color_boton, boton_rect)
        pygame.draw.rect(self.__ventana__, (0, 0, 0), boton_rect, 2)
        
        texto_boton = self.__fuente_normal__.render("Tirar Dados", True, (255, 255, 255))
        texto_rect = texto_boton.get_rect(center=boton_rect.center)
        self.__ventana__.blit(texto_boton, texto_rect)
        
        # Movimientos pendientes
        if movimientos_pendientes:
            y = 250
            texto = self.__fuente_normal__.render("Dados disponibles:", True, (255, 255, 255))
            self.__ventana__.blit(texto, (self.__ancho__ - 250, y))
            
            for i, dado in enumerate(movimientos_pendientes):
                self._dibujar_dado(self.__ancho__ - 200 + i * 50, y + 40, dado)
        
        # Botón finalizar turno
        boton_fin_rect = pygame.Rect(self.__ancho__ - 250, 400, 200, 50)
        pygame.draw.rect(self.__ventana__, (150, 0, 0), boton_fin_rect)
        pygame.draw.rect(self.__ventana__, (0, 0, 0), boton_fin_rect, 2)
        
        texto_fin = self.__fuente_normal__.render("Finalizar Turno", True, (255, 255, 255))
        texto_fin_rect = texto_fin.get_rect(center=boton_fin_rect.center)
        self.__ventana__.blit(texto_fin, texto_fin_rect)
    
    def _dibujar_dado(self, x, y, valor):
        """
        Dibuja un dado con su valor.
        
        Args:
            x, y (int): Posición
            valor (int): Valor del dado (1-6)
        """
        pygame.draw.rect(self.__ventana__, (255, 255, 255), (x, y, 35, 35))
        pygame.draw.rect(self.__ventana__, (0, 0, 0), (x, y, 35, 35), 2)
        
        texto = self.__fuente_normal__.render(str(valor), True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(x + 17, y + 17))
        self.__ventana__.blit(texto, texto_rect)
    
    def obtener_posicion_click(self, pos_mouse):
        """
        Convierte coordenadas de mouse a posición del tablero.
        
        Args:
            pos_mouse (tuple): (x, y) del mouse
        
        Returns:
            int o str: Posición 1-24, 'barra', 'boton_dados', 'boton_fin' o None
        """
        x, y = pos_mouse
        
        # Verificar botón dados
        if (self.__ancho__ - 250 <= x <= self.__ancho__ - 50 and 
            150 <= y <= 200):
            return 'boton_dados'
        
        # Verificar botón finalizar
        if (self.__ancho__ - 250 <= x <= self.__ancho__ - 50 and 
            400 <= y <= 450):
            return 'boton_fin'
        
        # Verificar si está en el tablero
        if not (self.__tablero_x__ <= x <= self.__tablero_x__ + self.__tablero_ancho__ and
                self.__tablero_y__ <= y <= self.__tablero_y__ + self.__tablero_alto__):
            return None
        
        # Calcular columna
        x_rel = x - self.__tablero_x__
        columna = x_rel // self.__punto_ancho__
        
        # Verificar barra
        if columna == 6:
            return 'barra'
        
        # Ajustar por barra
        if columna > 6:
            columna -= 1
        
        # Determinar si es parte superior o inferior
        y_rel = y - self.__tablero_y__
        
        if y_rel < self.__tablero_alto__ // 2:
            # Parte superior (posiciones 12-23)
            posicion = 23 - columna
        else:
            # Parte inferior (posiciones 0-11)
            posicion = columna
        
        return posicion + 1  # Convertir a 1-based
    
    def resaltar_destinos(self, destinos):
        """
        Resalta las posiciones de destino válidas.
        
        Args:
            destinos (list[int]): Lista de posiciones válidas (1-24 o -1 para bear-off)
        """
        for destino in destinos:
            if destino == -1:
                # Bear-off: resaltar área de fichas fuera
                continue
            
            # Calcular coordenadas de la posición
            pos = destino - 1  # Convertir a 0-based
            
            if pos < 12:
                columna = 11 - pos
                if columna >= 6:
                    columna += 1
                x = self.__tablero_x__ + columna * self.__punto_ancho__ + self.__punto_ancho__ // 2
                y = self.__tablero_y__ + 50
            else:
                columna = pos - 12
                if columna >= 6:
                    columna += 1
                x = self.__tablero_x__ + columna * self.__punto_ancho__ + self.__punto_ancho__ // 2
                y = self.__tablero_y__ + self.__tablero_alto__ - 50
            
            # Dibujar círculo resaltado
            pygame.draw.circle(self.__ventana__, self.__color_resaltado__, (x, y), 
                             self.__ficha_radio__ + 5, 3)


class GestorEventos:
    """
    Responsabilidad: Procesar eventos del usuario (clicks, teclado).
    SRP: Solo maneja eventos, delega lógica al juego y renderizado al Renderizador.
    """
    
    def __init__(self, juego, renderizador, ancho, alto):
        """
        Inicializa el gestor de eventos.
        
        Args:
            juego (Backgammon): Instancia del juego
            renderizador (Renderizador): Instancia del renderizador
            ancho, alto (int): Dimensiones de la ventana
        """
        self.__juego__ = juego
        self.__renderizador__ = renderizador
        self.__ancho__ = ancho
        self.__alto__ = alto
        
        # Estado de selección
        self.__origen_seleccionado__ = None
    
    def obtener_origen_seleccionado(self):
        """Retorna el origen actualmente seleccionado."""
        return self.__origen_seleccionado__
    
    def manejar_evento(self, evento, dados_tirados):
        """
        Maneja un evento de pygame.
        
        Args:
            evento: Evento de pygame
            dados_tirados (bool): Si ya se tiraron los dados
        
        Returns:
            dict o None: Resultado del evento
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            return self._manejar_click(evento.pos, dados_tirados)
        
        return None
    
    def _manejar_click(self, pos_mouse, dados_tirados):
        """
        Maneja un click del mouse.
        
        Args:
            pos_mouse (tuple): Posición del mouse
            dados_tirados (bool): Si ya se tiraron los dados
        
        Returns:
            dict o None: Resultado del click
        """
        posicion = self.__renderizador__.obtener_posicion_click(pos_mouse)
        
        if posicion is None:
            return None
        
        # Botón tirar dados
        if posicion == 'boton_dados':
            if not dados_tirados:
                d1, d2 = self.__juego__.tirar_dados()
                self.__origen_seleccionado__ = None
                return {
                    'tipo': 'dados_tirados',
                    'dados': (d1, d2)
                }
            return None
        
        # Botón finalizar turno
        if posicion == 'boton_fin':
            if dados_tirados:
                self.__juego__.finalizar_tirada()
                self.__origen_seleccionado__ = None
                return {
                    'tipo': 'movimiento',
                    'mensaje': f"{self.__juego__.obtener_turno().capitalize()}: Tira dados"
                }
            return None
        
        # Click en el tablero
        if dados_tirados:
            return self._manejar_click_tablero(posicion)
        
        return None
    
    def _manejar_click_tablero(self, posicion):
        """
        Maneja un click en el tablero.
        
        Args:
            posicion (int o str): Posición clickeada
        
        Returns:
            dict o None: Resultado del movimiento
        """
        # Si hay fichas en barra, solo permitir clicks en barra
        if self.__juego__.tiene_fichas_en_barra():
            if posicion == 'barra':
                if self.__origen_seleccionado__ == 'barra':
                    self.__origen_seleccionado__ = None
                else:
                    self.__origen_seleccionado__ = 'barra'
                return None
            elif self.__origen_seleccionado__ == 'barra':
                # Intentar mover desde barra al destino
                return self._intentar_movimiento_barra(posicion)
            return None
        
        # Primer click: seleccionar origen
        if self.__origen_seleccionado__ is None:
            # Verificar que haya fichas propias en el origen
            if isinstance(posicion, int):
                valor = self.__juego__.obtener_ficha_en_posicion(posicion)
                turno = self.__juego__.obtener_turno()
                if (turno == 'blancas' and valor > 0) or (turno == 'negras' and valor < 0):
                    self.__origen_seleccionado__ = posicion
            return None
        
        # Segundo click: intentar mover al destino
        else:
            return self._intentar_movimiento(posicion)
    
    def _intentar_movimiento(self, destino):
        """
        Intenta realizar un movimiento desde el origen seleccionado.
        
        Args:
            destino (int): Posición de destino
        
        Returns:
            dict: Resultado del movimiento
        """
        origen = self.__origen_seleccionado__
        
        # Obtener movimientos posibles
        movimientos = self.__juego__.obtener_movimientos_posibles()
        
        if origen not in movimientos:
            self.__origen_seleccionado__ = None
            return {'tipo': 'error', 'mensaje': 'No hay movimientos posibles desde ese origen'}
        
        # Buscar el dado correcto
        for dest, dado in movimientos[origen]:
            if dest == destino or (dest == -1 and destino == origen):
                try:
                    resultado = self.__juego__.mover(origen, dado)
                    self.__origen_seleccionado__ = None
                    
                    # Verificar victoria
                    if "ganaron" in resultado:
                        return {
                            'tipo': 'movimiento',
                            'mensaje': resultado
                        }
                    
                    return {
                        'tipo': 'movimiento',
                        'mensaje': f"{resultado.capitalize()}"
                    }
                except BackgammonError as e:
                    self.__origen_seleccionado__ = None
                    return {'tipo': 'error', 'mensaje': str(e)}
        
        self.__origen_seleccionado__ = None
        return {'tipo': 'error', 'mensaje': 'Movimiento inválido'}
    
