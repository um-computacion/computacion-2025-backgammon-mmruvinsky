# game/backgammon_game.py
import os
import pygame
from source.backgammon import Backgammon


class GameUI:
    """UI de Backgammon con Pygame - Drag & Drop funcional"""

    def __init__(self, game: Backgammon, width=1440, height=900):
        self.game = game

        # --- Pygame ---
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass

        # --- Ventana ---
        self.w, self.h = width, height
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Backgammon - Computación 2025")

        # --- Paleta ---
        self.C_BG = (9, 14, 28)
        self.C_N1 = (234, 0, 217)
        self.C_N2 = (10, 189, 198)
        self.C_N3 = (113, 28, 145)

        # --- Fuentes ---
        self.font_title = pygame.font.SysFont("freesansbold", 72, bold=True)
        self.font_hud   = pygame.font.SysFont("consolas", 24)

        # --- Rutas de assets ---
        ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        IMG  = os.path.join(ROOT, "assets", "images")
        SND  = os.path.join(ROOT, "assets", "sound")

        # --- Texturas del tablero ---
        self.img_wood         = self._load_img(os.path.join(IMG, "wood.png"))
        self.img_line         = self._load_img(os.path.join(IMG, "v-line.gif"))
        self.img_tri_top_dark = self._load_img(os.path.join(IMG, "row1-triangle-dark.gif"))
        self.img_tri_top_light= self._load_img(os.path.join(IMG, "row1-triangle-light.gif"))
        self.img_tri_bot_dark = self._load_img(os.path.join(IMG, "row2-triangle-dark.gif"))
        self.img_tri_bot_light= self._load_img(os.path.join(IMG, "row2-triangle-light.gif"))

        # --- Piezas (con fallback si no están los PNG) ---
        self.piece_white = (
            self._load_img(os.path.join(IMG, "piece-white-2.png")) or
            self._load_img(os.path.join(IMG, "piece-white.png")) or
            self._create_fallback_piece((255, 255, 255))
        )
        self.piece_black = (
            self._load_img(os.path.join(IMG, "piece-black-2.png")) or
            self._load_img(os.path.join(IMG, "piece-black.png")) or
            self._create_fallback_piece((50, 50, 50))
        )

        # --- Sonidos ---
        self.snd_button = self._load_snd(os.path.join(SND, "button.wav"))
        self.snd_cheer  = self._load_snd(os.path.join(SND, "cheer.wav"))
        self.snd_dice   = self._load_snd(os.path.join(SND, "dice.wav"))
        self.snd_impact = self._load_snd(os.path.join(SND, "impact.wav"))
        self.snd_home   = self._load_snd(os.path.join(SND, "todashome.mp3"))
        self.snd_win    = self._load_snd(os.path.join(SND, "win.mp3"))

        # --- Geometría del tablero ---
        self.board_rect = pygame.Rect(0, 0, int(self.w * 0.92), int(self.h * 0.78))
        self.board_rect.center = (self.w // 2, self.h // 2 + 20)
        self.col_w   = self.board_rect.width / 12.0
        self.mid_gap = max(30, int(self.board_rect.height * 0.08))

        # Escalado de imágenes según geometría
        self._scale_board_assets()

        # --- Apilado de fichas ---
        ph = self.piece_white.get_height()
        self.stack_gap = ph * 0.8  # superposición para que entren más

        # --- Drag & Drop ---
        self.dragging     = False
        self.drag_from_idx= None      # int 0..23 o "barra"
        self.drag_img     = None      # Surface de la ficha arrastrada
        self.drag_offset  = (0, 0)
        self.drag_pos     = (0, 0)

        # --- Hints y selección ---
        self.hints           = {}     # origen(1-based| "barra") -> [(dest, dado), ...]
        self.selected_origin = None   # 1-based o "barra"
        self.allowed_dests   = set()  # {destinos válidos}

        # --- Estado general UI ---
        self.last_roll      = None
        self.show_help      = False
        self.dice_anim_until= 0

        # --- Alertas HOME y victoria ---
        self._last_turn                = None              # para detectar cambio de turno
        self._home_alert_color         = None              # "blancas" | "negras"
        self._home_alert_latched       = {}                # {"blancas": bool, "negras": bool}
        self._home_alert_active_until  = 0                 # ms (pygame.time.get_ticks()) fin de cartel HOME

        self.victory_info   = None                         # {"color": "...", "since": ticks} o None
        self._home_sound_played = False                    # flags para no repetir sonidos
        self._win_sound_played  = False
        self._win_who          = None

        # --- Dígitos de dados (para mostrar pendientes / animación) ---
        self.dice_digits = {}
        for i in range(1, 7):
            img = self._load_img(os.path.join(IMG, f"digit-{i}-white.png"))
            if img:
                self.dice_digits[i] = img

    def _create_fallback_piece(self, color):
        """Crea una pieza simple si no hay imagen"""
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (20, 20), 18)
        pygame.draw.circle(surf, (0, 0, 0), (20, 20), 18, 2)
        return surf

    def _load_img(self, path):
        if os.path.exists(path):
            try:
                return pygame.image.load(path).convert_alpha()
            except Exception:
                pass
        return None

    def _load_snd(self, path):
        if os.path.exists(path):
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                pass
        return None

    def _scale_board_assets(self):
        if self.img_wood:
            self.img_wood = pygame.transform.smoothscale(
                self.img_wood, (self.board_rect.width, self.board_rect.height)
            )

        half_h = (self.board_rect.height - self.mid_gap) // 2

        def scale_tri(img, target_h):
            if not img:
                return None
            w = int(self.col_w * 0.8)
            h = int(target_h * 0.95)
            return pygame.transform.smoothscale(img, (w, h))

        self.img_tri_top_dark = scale_tri(self.img_tri_top_dark, half_h)
        self.img_tri_top_light = scale_tri(self.img_tri_top_light, half_h)
        self.img_tri_bot_dark = scale_tri(self.img_tri_bot_dark, half_h)
        self.img_tri_bot_light = scale_tri(self.img_tri_bot_light, half_h)

        if self.img_line:
            self.img_line = pygame.transform.smoothscale(self.img_line, (2, self.board_rect.height))

        def scale_piece(img):
            if not img:
                return None
            target_h = max(40, int(self.board_rect.height / 16))
            r = target_h / img.get_height()
            target_w = int(img.get_width() * r)
            return pygame.transform.smoothscale(img, (target_w, target_h))

        self.piece_white = scale_piece(self.piece_white)
        self.piece_black = scale_piece(self.piece_black)

    def _idx_to_col_row(self, idx):
        """Convierte índice 0-23 (interno) a (col, row) visual
        
        Mapeo del core de Backgammon:
        - Punto 1 (idx 0): Abajo-derecha → col=11, row=1
        - Punto 12 (idx 11): Abajo-izquierda → col=0, row=1
        - Punto 13 (idx 12): Arriba-izquierda → col=0, row=0
        - Punto 24 (idx 23): Arriba-derecha → col=11, row=0
        
        Fila 1 (abajo): puntos 1-12 (idx 0-11), de DERECHA a IZQUIERDA
        Fila 0 (arriba): puntos 13-24 (idx 12-23), de IZQUIERDA a DERECHA
        """
        if 0 <= idx <= 11:
            # Puntos 1-12: fila inferior, de derecha a izquierda
            return (11 - idx, 1)
        else:
            # Puntos 13-24: fila superior, de izquierda a derecha
            return (idx - 12, 0)

    def _point_rect(self, idx):
        """Retorna el rect completo de un punto (para detección de click)"""
        col, row = self._idx_to_col_row(idx)
        x = self.board_rect.left + col * self.col_w
        w = self.col_w
        half_h = (self.board_rect.height - self.mid_gap) // 2
        
        if row == 0:  # Arriba
            y = self.board_rect.top
            h = half_h
        else:  # Abajo
            y = self.board_rect.centery + self.mid_gap // 2
            h = half_h
        
        return pygame.Rect(x, y, w, h)
    
    def _target_rect(self, idx: int) -> pygame.Rect:
        """
        Rect grande del punto (ocupa toda la mitad superior/inferior de esa columna).
        Lo usamos sólo para pintar las zonas destino; evita que se vean corridas abajo.
        idx: 0..23 (0-based)
        """
        col, row = self._idx_to_col_row(idx)
        x = int(self.board_rect.left + col * self.col_w)
        w = int(self.col_w)
        half_h = (self.board_rect.height - self.mid_gap) // 2
        if row == 0:  # arriba
            y = int(self.board_rect.top)
        else:         # abajo (debajo del gap)
            y = int(self.board_rect.centery + self.mid_gap // 2)
        return pygame.Rect(x, y, w, half_h)


    def _bar_rect(self):
        w = int(self.col_w * 1.1)
        x = int(self.board_rect.centerx - w // 2)
        return pygame.Rect(x, self.board_rect.top, w, self.board_rect.height)

    def _mouse_to_point(self, mx, my):
        """Convierte coordenadas mouse a índice 0-23 o 'barra' o 'bearoff' o None"""
        # Primero verificar zona de bear-off (a la derecha)
        if -1 in self.allowed_dests:  # Solo si bear-off es válido
            zona_x = self.board_rect.right + 30
            zona_w = 80
            zona_h = self.board_rect.height // 2 - 40
            
            turno = self.game.obtener_turno()
            # BLANCAS sacan ARRIBA (donde se apilan las blancas fuera)
            # NEGRAS sacan ABAJO (donde se apilan las negras fuera)
            if turno == "blancas":
                zona_y = self.board_rect.top
            else:
                zona_y = self.board_rect.centery + self.mid_gap // 2
            
            bearoff_rect = pygame.Rect(zona_x, zona_y, zona_w, zona_h)
            if bearoff_rect.collidepoint(mx, my):
                return "bearoff"
        
        # Verificar barra
        bar = self._bar_rect()
        if bar.collidepoint(mx, my):
            turno = self.game.obtener_turno()
            if self.game.tiene_fichas_en_barra(turno):
                return "barra"
        
        # Verificar cada punto del tablero
        for idx in range(24):
            rect = self._point_rect(idx)
            if rect.collidepoint(mx, my):
                return idx
        
        return None

    def _get_bar_counts(self):
        try:
            b = self.game.obtener_barra()
            if isinstance(b, dict):
                return int(b.get("blancas", 0)), int(b.get("negras", 0))
        except Exception:
            pass
        return 0, 0

    def _update_hints(self):
        """Actualiza hints desde el core"""
        try:
            self.hints = self.game.obtener_movimientos_posibles() or {}
        except Exception as e:
            print(f"Error obteniendo hints: {e}")
            self.hints = {}

        # Si hay movimientos desde barra, priorizarlos
        barra_moves = self.hints.get("barra", [])
        if barra_moves:
            self.allowed_dests = {dest for (dest, _) in barra_moves}
            return

        # Movimientos normales
        if isinstance(self.selected_origin, int):
            movs = self.hints.get(self.selected_origin, [])
            self.allowed_dests = {dest for (dest, _) in movs}
        else:
            self.allowed_dests = set()

    def _draw_board(self):
        self.screen.fill(self.C_BG)
        
        if self.img_wood:
            self.screen.blit(self.img_wood, self.board_rect.topleft)
        else:
            pygame.draw.rect(self.screen, (40, 40, 60), self.board_rect)

        # Barra central
        bar = self._bar_rect()
        panel = pygame.Surface((bar.width, bar.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 90), panel.get_rect(), border_radius=8)
        self.screen.blit(panel, bar.topleft)

        # Gap central
        gap_rect = pygame.Rect(
            self.board_rect.left,
            self.board_rect.centery - self.mid_gap // 2,
            self.board_rect.width,
            self.mid_gap
        )
        gap = pygame.Surface(gap_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(gap, (0, 0, 0, 110), gap.get_rect())
        pygame.draw.line(gap, self.C_N3, (0, 0), (gap_rect.width, 0), 2)
        pygame.draw.line(gap, self.C_N3, (0, gap_rect.height-1), (gap_rect.width, gap_rect.height-1), 2)
        self.screen.blit(gap, gap_rect.topleft)

        half_h = (self.board_rect.height - self.mid_gap) // 2

        # Triángulos superiores
        for c in range(12):
            img = self.img_tri_top_light if c % 2 == 0 else self.img_tri_top_dark
            if img:
                x = self.board_rect.left + c * self.col_w + (self.col_w - img.get_width()) / 2
                y = self.board_rect.top
                self.screen.blit(img, (x, y))

        # Triángulos inferiores
        for c in range(12):
            img = self.img_tri_bot_dark if c % 2 == 0 else self.img_tri_bot_light
            if img:
                x = self.board_rect.left + c * self.col_w + (self.col_w - img.get_width()) / 2
                y = self.board_rect.centery + self.mid_gap // 2 + (half_h - img.get_height())
                self.screen.blit(img, (x, y))

        # Línea vertical central
        if self.img_line:
            cx = self.board_rect.centerx - self.img_line.get_width() // 2
            self.screen.blit(self.img_line, (cx, self.board_rect.top))

    def _draw_pieces(self):
        pos = self.game.obtener_posiciones()
        pw, ph = self.piece_white.get_size()
        
        for idx, val in enumerate(pos):
            if val == 0:
                continue
            
            col, row = self._idx_to_col_row(idx)
            base_x = self.board_rect.left + col * self.col_w
            piece_x = base_x + (self.col_w - pw) / 2
            
            count = abs(val)
            color_img = self.piece_white if val > 0 else self.piece_black
            
            # Calcular Y base según fila
            if row == 0:  # Arriba - crecen hacia abajo
                base_y = self.board_rect.top + 5
                for n in range(count):
                    if self.dragging and self.drag_from_idx == idx and n == count - 1:
                        continue
                    piece_y = base_y + n * self.stack_gap
                    self.screen.blit(color_img, (piece_x, piece_y))
            else:  # Abajo - crecen hacia arriba
                base_y = self.board_rect.bottom - ph - 5
                for n in range(count):
                    if self.dragging and self.drag_from_idx == idx and n == count - 1:
                        continue
                    piece_y = base_y - n * self.stack_gap
                    self.screen.blit(color_img, (piece_x, piece_y))
        
        # Pieza arrastrada
        if self.dragging and self.drag_img:
            self.screen.blit(self.drag_img, self.drag_pos)

    def _draw_bar(self):
        w_bar, n_bar = self._get_bar_counts()
        if not w_bar and not n_bar:
            return

        bar = self._bar_rect()
        half_h = (self.board_rect.height - self.mid_gap) // 2
        top_rect = pygame.Rect(bar.x, bar.y, bar.width, half_h)
        bot_rect = pygame.Rect(bar.x, self.board_rect.centery + self.mid_gap // 2, bar.width, half_h)

        pw, ph = self.piece_white.get_size()
        cx = bar.x + (bar.width - pw) // 2
        overlap = ph * 0.7

        # BLANCAS ABAJO (crecen hacia arriba desde bottom)
        for i in range(w_bar):
            x = cx
            y = bot_rect.bottom - ph - 8 - i * overlap
            if y < bot_rect.top + 4:
                break
            self.screen.blit(self.piece_white, (x, y))

        # NEGRAS ARRIBA (crecen hacia abajo desde top)
        for i in range(n_bar):
            x = cx
            y = top_rect.top + 8 + i * overlap
            if y + ph > top_rect.bottom - 4:
                break
            self.screen.blit(self.piece_black, (x, y))

    def _draw_hints(self):
        """Resalta SOLO los destinos válidos (sin marcar el origen)."""
        if not self.allowed_dests:
            return

        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        for dest in self.allowed_dests:
            # Bear-off (-1): dibujar zona de salida a la derecha según el turno
            if dest == -1:
                zona_x = self.board_rect.right + 30
                zona_w = 80
                zona_h = self.board_rect.height // 2 - 40
                turno = self.game.obtener_turno()
                # BLANCAS sacan ARRIBA (donde se apilan las blancas fuera)
                # NEGRAS sacan ABAJO (donde se apilan las negras fuera)
                if turno == "blancas":
                    zona_y = self.board_rect.top
                else:
                    zona_y = self.board_rect.centery + self.mid_gap // 2
                rect = pygame.Rect(zona_x, zona_y, zona_w, zona_h)
            else:
                # Puntos 1..24 → a 0..23 para calcular el rect
                idx0 = dest - 1
                if not (0 <= idx0 < 24):
                    continue
                rect = self._target_rect(idx0)

            # Glow + borde neón
            glow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*self.C_N2, 70), glow.get_rect(), border_radius=10)
            overlay.blit(glow, rect.topleft)
            pygame.draw.rect(overlay, (*self.C_N2, 200), rect, width=3, border_radius=10)

        self.screen.blit(overlay, (0, 0))

    def _draw_bear_off_zone(self):
        """Zona de fichas ya sacadas (bear-off) a la derecha del tablero, siempre visible."""
        try:
            fichas_fuera = self.game.obtener_fichas_fuera() or {}
            w_fuera = int(fichas_fuera.get("blancas", 0))
            n_fuera = int(fichas_fuera.get("negras", 0))
        except Exception:
            return

        if not w_fuera and not n_fuera:
            return

        pw, ph = self.piece_white.get_size()
        overlap = int(ph * 0.6)

        # Posicionar la "columna" a la derecha del tablero, pero SIN salirse de la ventana
        pad_x = 16
        zona_x = max(self.board_rect.right + 12, self.board_rect.right + 12)
        zona_x = min(zona_x, self.w - pw - pad_x)   # <- clamp dentro de la pantalla

        # Alto disponible de cada mitad
        half_h = (self.board_rect.height - self.mid_gap) // 2

        # Pequeños paneles para que se vean nítidas
        col_w = pw + 10
        panel_top = pygame.Surface((col_w, half_h), pygame.SRCALPHA)
        panel_bot = pygame.Surface((col_w, half_h), pygame.SRCALPHA)
        pygame.draw.rect(panel_top, (0, 0, 0, 100), panel_top.get_rect(), border_radius=8)
        pygame.draw.rect(panel_bot, (0, 0, 0, 100), panel_bot.get_rect(), border_radius=8)

        # TOP: BLANCAS (apilan hacia ABAJO desde el borde superior de la mitad superior)
        top_x = zona_x - 5
        top_y = self.board_rect.top
        self.screen.blit(panel_top, (top_x, top_y))
        for i in range(min(w_fuera, 15)):
            y = top_y + 8 + i * overlap
            self.screen.blit(self.piece_white, (zona_x, y))

        # BOTTOM: NEGRAS (apilan hacia ARRIBA desde el borde inferior de la mitad inferior)
        bot_x = zona_x - 5
        bot_y = self.board_rect.centery + self.mid_gap // 2
        self.screen.blit(panel_bot, (bot_x, bot_y))
        for i in range(min(n_fuera, 15)):
            y = bot_y + half_h - ph - 8 - i * overlap
            self.screen.blit(self.piece_black, (zona_x, y))

    def _who_can_bearoff(self):
        """
        Devuelve "blancas", "negras" o None según quién tenga TODAS sus fichas en su home
        y sin fichas en barra. No depende del turno.
        Retorna None si ese color ya ganó (15 fichas fuera).
        """
        try:
            posiciones = self.game.obtener_posiciones()
            barra = self.game.obtener_barra() or {"blancas": 0, "negras": 0}
            fichas_fuera = self.game.obtener_fichas_fuera() or {"blancas": 0, "negras": 0}

            # Si ya ganó, no mostrar cartel HOME
            if fichas_fuera.get("blancas", 0) >= 15 or fichas_fuera.get("negras", 0) >= 15:
                return None

            # Si hay fichas en barra, ese color NO puede sacar
            if int(barra.get("blancas", 0)) > 0:
                blancas_ok = False
            else:
                # Blancas: home = idx 18..23 (puntos 19..24)
                # No debe haber fichas blancas en idx 0..17
                blancas_fuera_home = any(posiciones[i] > 0 for i in range(18))  # 0..17
                blancas_tienen_en_home = any(posiciones[i] > 0 for i in range(18, 24))
                blancas_ok = (not blancas_fuera_home) and blancas_tienen_en_home

            if int(barra.get("negras", 0)) > 0:
                negras_ok = False
            else:
                # Negras: home = idx 0..5 (puntos 1..6)
                # No debe haber fichas negras en idx 6..23
                negras_fuera_home = any(posiciones[i] < 0 for i in range(6, 24))
                negras_tienen_en_home = any(posiciones[i] < 0 for i in range(0, 6))
                negras_ok = (not negras_fuera_home) and negras_tienen_en_home

            if blancas_ok and not negras_ok:
                return "blancas"
            if negras_ok and not blancas_ok:
                return "negras"
            # Si ambos o ninguno, no mostramos cartel (caso raro "ambos")
            return None
        except Exception:
            return None

    def _update_win_state(self):
        """Detecta si ya ganó alguien (15 fichas fuera)."""
        try:
            fichas_fuera = self.game.obtener_fichas_fuera()
            w = fichas_fuera.get("blancas", 0)
            n = fichas_fuera.get("negras", 0)
            if w >= 15:
                self._win_who = "blancas"
            elif n >= 15:
                self._win_who = "negras"
            else:
                self._win_who = None
                self._win_sound_played = False
        except Exception:
            pass

    def _draw_win_banner(self):
        """Banner gigante de victoria + sonido + confetti animado."""
        if not self._win_who:
            return

        # Reproducir sonido una sola vez
        if not self._win_sound_played and self.snd_win:
            try:
                self.snd_win.play()
            except Exception:
                pass
            self._win_sound_played = True

        # Oscurecer el fondo
        dim = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        self.screen.blit(dim, (0, 0))

        # Texto principal enorme con colores vibrantes
        title = f"¡FICHAS {self._win_who.upper()} GANARON!"
        font_big  = pygame.font.SysFont("freesansbold", 72, bold=True)
        font_glow = pygame.font.SysFont("freesansbold", 72, bold=True)

        # Colores más vibrantes y llamativos
        t_main  = font_big.render(title,  True, (50, 255, 100))  # Verde brillante
        t_glow1 = font_glow.render(title, True, (255, 220, 50))  # Amarillo dorado
        t_glow2 = font_glow.render(title, True, (20, 210, 255))  # Cyan brillante

        cx, cy = self.w // 2, self.h // 2

        # "Glow" más pronunciado
        self.screen.blit(t_glow2, t_glow2.get_rect(center=(cx+6, cy-85+6)))
        self.screen.blit(t_glow1, t_glow1.get_rect(center=(cx+3, cy-85+3)))
        self.screen.blit(t_main,  t_main.get_rect(center=(cx,   cy-85)))

        # Subtítulo
        font_sub = pygame.font.SysFont("consolas", 28, bold=True)
        sub = font_sub.render("Pulsa ESC para salir o R para seguir viendo", True, (255, 255, 100))
        self.screen.blit(sub, sub.get_rect(center=(cx, cy-26)))

        # Confetti animado más denso y colorido
        now = pygame.time.get_ticks()
        rng = (now // 30) % 1000
        for i in range(200):  # Más confetti
            x = (i * 37 + rng * 19) % self.w
            y = (i * 53 + rng * 23) % self.h
            r = 3 + ((i + rng) % 5)
            col = [(255, 70, 220), (70, 255, 100), (255, 220, 70), (70, 220, 255)][i % 4]
            pygame.draw.circle(self.screen, col, (x, y), r)

    def _draw_bearoff_alert(self):
        """
        Cartel '¡TODAS EN HOME!' centrado y temporizado.
        Se muestra solo si el temporizador sigue activo y hay color válido.
        """
        # Salidas rápidas
        if not getattr(self, "_home_alert_active_until", 0):
            return

        now = pygame.time.get_ticks()
        if now > self._home_alert_active_until:
            return

        turno = getattr(self, "_home_alert_color", None)
        if turno not in ("blancas", "negras"):
            return

        # Panel centrado en el tablero
        panel_w = int(self.board_rect.width * 0.55)
        panel_h = 110
        panel_x = self.board_rect.centerx - panel_w // 2
        panel_y = self.board_rect.centery - panel_h // 2

        # Animación de borde pulsante
        pulse = abs(((now // 180) % 100) - 50) / 50.0   # 0..1
        alpha = int(160 + pulse * 80)                   # 160..240

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 200), panel.get_rect(), border_radius=16)
        pygame.draw.rect(panel, (255, 80, 80, alpha), panel.get_rect(), width=4, border_radius=16)
        pygame.draw.rect(panel, (255, 160, 160, alpha // 2), panel.get_rect(), width=2, border_radius=16)
        self.screen.blit(panel, (panel_x, panel_y))

        # Títulos
        font_big  = pygame.font.SysFont("freesansbold", 46, bold=True)
        font_sub  = pygame.font.SysFont("consolas", 26, bold=True)

        title = "¡TODAS EN HOME!"
        sub   = f"{turno.upper()} pueden sacar fichas"

        # Efecto glow
        t_main = font_big.render(title, True, (255, 80, 80))
        t_g1   = font_big.render(title, True, (255, 140, 140))
        t_g2   = font_big.render(title, True, (255, 200, 200))

        cx = self.board_rect.centerx
        ty = panel_y + 12

        self.screen.blit(t_g2, t_g2.get_rect(center=(cx+4, ty+4)))
        self.screen.blit(t_g1, t_g1.get_rect(center=(cx+2, ty+2)))
        self.screen.blit(t_main, t_main.get_rect(center=(cx, ty)))

        s_surf = font_sub.render(sub, True, (240, 240, 240))
        self.screen.blit(s_surf, s_surf.get_rect(center=(cx, ty + t_main.get_height() + 10)))

    def _draw_title(self):
        text = "BACKGAMMON PY"
        base = self.font_title.render(text, True, self.C_N1)
        glow1 = self.font_title.render(text, True, self.C_N2)
        glow2 = self.font_title.render(text, True, self.C_N3)
        cx = self.w // 2
        y = 48
        self.screen.blit(glow2, glow2.get_rect(center=(cx+3, y+3)))
        self.screen.blit(glow1, glow1.get_rect(center=(cx-2, y-2)))
        self.screen.blit(base, base.get_rect(center=(cx, y)))

    def _draw_hud(self):
        turno = self.game.obtener_turno()
        pendientes = self.game.obtener_movimientos_pendientes()
        
        # Texto principal
        hud_txt = f"Turno: {turno}"
        if pendientes:
            hud_txt += f" | Movimientos: {len(pendientes)}"
        
        self.screen.blit(self.font_hud.render(hud_txt, True, self.C_N2), (20, self.h - 40))

    def _draw_dice(self):
        """Muestra los dados pendientes en tiempo real"""
        cell = 64
        pad = 10
        spacing = 10
        
        now = pygame.time.get_ticks()
        
        # Durante animación: mostrar dados originales
        if now < self.dice_anim_until:
            if not self.last_roll:
                return
            import random
            # Animación con números aleatorios
            dados_a_mostrar = [random.randint(1, 6), random.randint(1, 6)]
        else:
            # Después de animación: mostrar movimientos PENDIENTES
            pendientes = self.game.obtener_movimientos_pendientes()
            if not pendientes:
                return
            dados_a_mostrar = pendientes
        
        # Calcular posiciones de derecha a izquierda
        total_dados = len(dados_a_mostrar)
        x_start = self.w - (cell + pad)
        y = self.h - (cell + pad)
        
        for i, dado in enumerate(dados_a_mostrar):
            x = x_start - i * (cell + spacing)
            surf = self.dice_digits.get(dado)
            
            if surf:
                s = pygame.transform.smoothscale(surf, (cell, cell))
                # Fondo y borde
                pygame.draw.rect(self.screen, self.C_BG, (x-4, y-4, cell+8, cell+8), border_radius=10)
                
                # Borde con diferentes colores según estado
                if now < self.dice_anim_until:
                    border_color = self.C_N1  # Fucsia durante animación
                else:
                    border_color = self.C_N3  # Púrpura para pendientes
                
                pygame.draw.rect(self.screen, border_color, (x-4, y-4, cell+8, cell+8), width=2, border_radius=10)
                self.screen.blit(s, (x, y))

    def _draw_help(self):
        if not self.show_help:
            return

        font_t = pygame.font.SysFont("monospace", 18, bold=True)
        font = pygame.font.SysFont("monospace", 16)

        lines = [
            ("COMANDOS", font_t, (255, 120, 255)),
            ("ESPACIO o R: tirar dados", font, (190, 255, 255)),
            ("F: finalizar tirada", font, (190, 255, 255)),
            ("H: ayuda", font, (190, 255, 255)),
            ("ESC: salir", font, (190, 255, 255)),
            ("", font, (190, 255, 255)),
            ("Click y arrastrar para mover", font, (190, 255, 255)),
        ]

        pad_x, pad_y, gap = 14, 12, 6
        max_w = max(f.render(text, True, (0,0,0)).get_width() for text, f, _ in lines)
        total_h = pad_y + sum(f.render(text, True, (0,0,0)).get_height() + gap for text, f, _ in lines)
        panel_w, panel_h = max_w + pad_x * 2, total_h

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 180), panel.get_rect(), border_radius=12)
        pygame.draw.rect(panel, (140, 255, 255, 180), panel.get_rect(), width=2, border_radius=12)

        y = pad_y
        for text, f, color in lines:
            surf = f.render(text, True, color)
            panel.blit(surf, (pad_x, y))
            y += surf.get_height() + gap

        self.screen.blit(panel, (28, 92))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self._update_hints()

        print("Juego iniciado. Presiona ESPACIO para tirar dados.")

        while running:
            # -------------------- Eventos --------------------
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                elif e.type == pygame.KEYDOWN:
                    # Tirar dados (si no hay movimientos pendientes)
                    if e.key in (pygame.K_SPACE, pygame.K_r):
                        if not self.game.movimientos_disponibles():
                            try:
                                self.last_roll = self.game.tirar_dados()
                                pendientes = self.game.obtener_movimientos_pendientes()
                                print(f"\n=== NUEVA TIRADA ===")
                                print(f"Dados: {self.last_roll}")
                                print(f"Pendientes: {pendientes}")
                                print(f"Turno: {self.game.obtener_turno()}")
                                if self.snd_dice:
                                    self.snd_dice.play()
                                self.dice_anim_until = pygame.time.get_ticks() + 600
                                # limpiar selección/hints
                                self.selected_origin = None
                                self.allowed_dests = set()
                                self._update_hints()
                                print("Movimientos posibles:")
                                for origen, movs in self.hints.items():
                                    print(f"  Desde {origen}: {movs}")
                            except Exception as ex:
                                print(f"Error tirar dados: {ex}")

                    # Finalizar tirada
                    elif e.key == pygame.K_f:
                        try:
                            self.game.finalizar_tirada()
                            print("Tirada finalizada")
                            if self.snd_button:
                                self.snd_button.play()
                            self.selected_origin = None
                            self.allowed_dests = set()
                            self._update_hints()
                        except Exception as ex:
                            print(f"Error finalizar: {ex}")

                    # Ayuda
                    elif e.key == pygame.K_h:
                        self.show_help = not self.show_help

                    # Salir
                    elif e.key == pygame.K_ESCAPE:
                        running = False

                # ----- Drag & Drop -----
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    idx = self._mouse_to_point(mx, my)

                    self._update_hints()

                    # Priorizar barra si hay fichas en barra
                    barra_moves = self.hints.get("barra", [])
                    if barra_moves and idx != "barra":
                        print("⚠️  Debes mover desde la barra primero")
                        continue

                    # Click en barra
                    if idx == "barra":
                        self.selected_origin = "barra"
                        self.allowed_dests = {dest for (dest, _) in barra_moves}
                        print(f"Barra seleccionada, destinos: {self.allowed_dests}")
                        if not self.allowed_dests:
                            continue
                        turno = self.game.obtener_turno()
                        self.drag_img = self.piece_white if turno == "blancas" else self.piece_black
                        iw, ih = self.drag_img.get_size()
                        self.drag_offset = (iw // 2, ih // 2)
                        self.dragging = True
                        self.drag_from_idx = "barra"
                        self.drag_pos = (mx - self.drag_offset[0], my - self.drag_offset[1])
                        continue

                    # Click en un punto del tablero
                    if isinstance(idx, int) and 0 <= idx < 24:
                        posiciones = self.game.obtener_posiciones()
                        val = posiciones[idx]
                        if val == 0:
                            continue
                        turno = self.game.obtener_turno()
                        if not ((val > 0 and turno == "blancas") or (val < 0 and turno == "negras")):
                            continue

                        self.selected_origin = idx + 1  # 1-based para el core
                        movs = self.hints.get(self.selected_origin, [])
                        self.allowed_dests = {dest for (dest, _) in movs}
                        if not self.allowed_dests:
                            continue

                        self.drag_img = self.piece_white if turno == "blancas" else self.piece_black
                        iw, ih = self.drag_img.get_size()
                        self.drag_offset = (iw // 2, ih // 2)
                        self.dragging = True
                        self.drag_from_idx = idx
                        self.drag_pos = (mx - self.drag_offset[0], my - self.drag_offset[1])

                elif e.type == pygame.MOUSEMOTION and self.dragging:
                    mx, my = e.pos
                    self.drag_pos = (mx - self.drag_offset[0], my - self.drag_offset[1])

                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.dragging:
                    mx, my = e.pos
                    drop_idx = self._mouse_to_point(mx, my)

                    # Mapear a destino del core
                    if drop_idx == "bearoff":
                        destino = -1
                    elif isinstance(drop_idx, int):
                        destino = drop_idx + 1
                    else:
                        destino = None

                    try:
                        if self.selected_origin and destino is not None and destino in self.allowed_dests:
                            key_hints = "barra" if self.selected_origin == "barra" else self.selected_origin
                            dado = None
                            for (dest, d) in self.hints.get(key_hints, []):
                                if dest == destino:
                                    dado = d
                                    break

                            if dado:
                                origen_core = 1 if self.selected_origin == "barra" else self.selected_origin
                                res = self.game.mover(origen_core, dado)

                                # Sonidos
                                if isinstance(res, str) and ("ganaron" in res):
                                    if self.snd_cheer:
                                        self.snd_cheer.play()
                                elif self.snd_impact:
                                    self.snd_impact.play()

                                # ¿Se acabó la tirada?
                                if not self.game.movimientos_disponibles():
                                    self.game.finalizar_tirada()
                                    if self.snd_button:
                                        self.snd_button.play()

                                # Limpiar UI y refrescar hints
                                self.selected_origin = None
                                self.allowed_dests = set()
                                self._update_hints()
                            else:
                                print("❌ No se encontró dado válido para este destino")
                        else:
                            print("❌ Movimiento inválido (destino no permitido)")
                    except Exception as ex:
                        print(f"💥 Error al mover: {ex}")
                        import traceback
                        traceback.print_exc()
                    finally:
                        self.dragging = False
                        self.drag_from_idx = None
                        self.drag_img = None

            # -------------------- Lógica cartel "todas en home" (3.5 s, por color) --------------------
            who = self._who_can_bearoff()          # "blancas" | "negras" | None
            now = pygame.time.get_ticks()

            if who:
                # Se puede sacar -> verificar si ya mostramos cartel para este color
                if not self._home_alert_latched.get(who, False):
                    # Primera vez que este color puede sacar -> disparar cartel
                    self._home_alert_latched[who] = True
                    self._home_alert_color = who
                    self._home_alert_active_until = now + 3500  # 3.5 s
                    if self.snd_home:
                        try: self.snd_home.play()
                        except Exception: pass
            else:
                # Nadie puede sacar -> no hacer nada (mantener estados)
                pass

            # -------------------- Actualizar estado de victoria --------------------
            self._update_win_state()

            # -------------------- Render --------------------
            self._draw_board()
            self._draw_pieces()
            self._draw_bar()
            self._draw_bear_off_zone()   # blancas arriba, negras abajo
            self._draw_hints()
            
            # Solo mostrar cartel HOME si NO hay victoria
            if not self._win_who:
                self._draw_bearoff_alert()   # cartel centrado y temporizado
            
            self._draw_title()
            self._draw_hud()
            self._draw_dice()
            self._draw_help()
            
            # Victoria siempre encima de todo
            self._draw_win_banner()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    from source.backgammon import Backgammon

    game = Backgammon()          # ← crear instancia del core
    ui = GameUI(game)            # ← pasarla al UI
    ui.run()