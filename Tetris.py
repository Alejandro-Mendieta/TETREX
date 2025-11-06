import random 
import pygame 
from pygame import mixer
import os 
import sys
import math
import json
from datetime import datetime

def resource_path(relative_path):
    """Función para rutas compatibles con Linux y Windows"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    path = os.path.join(base_path, relative_path)
    return os.path.normpath(path)

def verificar_dependencias():
    """Verificar que todas las dependencias estén disponibles"""
    try:
        pygame.init()
        mixer.init()
        return True
    except Exception as e:
        print(f"Error inicializando Pygame: {e}")
        return False

# Inicializar Pygame con verificación
if not verificar_dependencias():
    print("Error: Pygame no está instalado correctamente.")
    print("Instala con: sudo apt install python3-pygame")
    sys.exit(1)

# Constantes del juego
ANCHO, ALTO = 1500, 800  
TAMANIO_CELDA = 30
FILAS_TABLERO, COLUMNAS_TABLERO = 20, 10
ANCHO_TABLERO = COLUMNAS_TABLERO * TAMANIO_CELDA
ALTO_TABLERO = FILAS_TABLERO * TAMANIO_CELDA
MARGEN_X = (ANCHO - ANCHO_TABLERO) // 2 - 100
MARGEN_Y = (ALTO - ALTO_TABLERO) // 2 - 20

FPS = 60

# Colores   
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
COLOR_BOTON = (255, 0, 0)
COLOR_BOTON_HOVER = (200, 0, 0)
COLOR_FONDO = (5, 5, 15)           # Negro azulado espacial
COLOR_TABLERO = (15, 15, 35)       # Azul cosmos
COLOR_BORDE = (80, 80, 160)        # Azul nebulosa
COLOR_TEXTO = (220, 240, 255)      # Blanco estelar

# PIEZAS ESPACIALES NEÓN - Colores de galaxia y energía cósmica
COLORES_PIEZAS = [
    (0, 255, 255),      # I - CYAN NEBULOSA (Energía pura)
    (150, 50, 255),     # J - PÚRPURA QUÁSAR (Materia oscura)
    (255, 50, 150),     # L - ROSA SUPERNOVA (Explosión estelar)
    (255, 255, 0),      # O - AMARILLO SOLAR (Estrella central)
    (50, 255, 150),     # S - VERDE EXTRATERRESTRE (Vida alien)
    (255, 150, 0),      # T - NARANJA ESTELAR (Gigante roja)
    (255, 0, 255)       # Z - MAGENTA CÓSMICO (Agujero de gusano)
]

# Crear pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Tetris Game - Mejorado")

# Variables globales para fuentes
fuente = None
fuente_game_over = None
fuente_pista = None

# Configuración de audio
def cargar_audio():
    """Cargar recursos de audio"""
    try:
        mixer.music.set_volume(0.5)
        print("Sistema de audio inicializado")
        return True
    except Exception as e:
        print(f"Error inicializando audio: {e}")
        return False

cargar_audio()

# Cargar icono
def cargar_icono():
    """Cargar icono con formatos compatibles"""
    try:
        # Crear un icono simple programáticamente
        icono = pygame.Surface((32, 32))
        icono.fill((0, 0, 0))
        pygame.draw.rect(icono, (0, 240, 240), (8, 8, 16, 4))
        pygame.draw.rect(icono, (240, 240, 0), (8, 16, 8, 8))
        pygame.display.set_icon(icono)
        print("Icono cargado")
        return True
    except Exception as e:
        print(f"No se pudo cargar icono: {e}")
        return False

cargar_icono()

# Definición de las piezas de Tetris
PIEZAS = [
    # I
    [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]
    ],
    # J
    [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        
        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],
        
        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]],
        
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ],
    # L
    [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
        
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],
        
        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],
        
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]]
    ],
    # O
    [
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
         
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
         
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
         
        [[0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ],
    # S
    [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
        
        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],
        
        [[0, 0, 0],
         [0, 1, 1],
         [1, 1, 0]],
        
        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    # T
    [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
        
        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],
        
        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],
        
        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    # Z
    [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
        
        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],
        
        [[0, 0, 0],
         [1, 1, 0],
         [0, 1, 1]],
        
        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]
    ]
]

# Tablas de kicks para rotaciones (Sistema de Rotación SRS)
KICKS = {
    'I': [
        [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
        [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
        [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
        [(0,0), (1,0), (-2,0), (1,-2), (-2,1)]
    ],
    'default': [
        [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
        [(0,0), (1,0), (1,-1), (0,2), (1,2)],
        [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
        [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)]
    ]
}

# Sistema de partículas
particulas = []

class Particula:
    def __init__(self, x, y, tipo="brillo", color=None):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.life = random.uniform(60, 120)
        self.size = random.randint(2, 6)
        
        # Configurar propiedades según el tipo de efecto
        if tipo == "brillo":
            self.color = color or (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.gravity = 0.05
        elif tipo == "humo":
            self.color = (random.randint(100, 150), random.randint(100, 150), random.randint(100, 150))
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-2, -1)
            self.gravity = -0.02
            self.size = random.randint(3, 8)
        elif tipo == "chispas":
            self.color = color or (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100))
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-5, -2)
            self.gravity = 0.3
        elif tipo == "estrellas":
            self.color = color or (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            self.gravity = 0.1
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-5, 5)
        else:  # confeti por defecto
            self.color = color or random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)])
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-8, -2)
            self.gravity = 0.2
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
        if self.tipo == "estrellas":
            self.rotation += self.rotation_speed
            
        self.life -= 1
        return self.life > 0
        
    def draw(self, pantalla):
        if self.tipo == "estrellas":
            # Dibujar estrella giratoria
            points = []
            for i in range(5):
                angle = self.rotation + i * 72
                rad = math.radians(angle)
                x = self.x + math.cos(rad) * self.size
                y = self.y + math.sin(rad) * self.size
                points.append((x, y))
                
                inner_angle = angle + 36
                inner_rad = math.radians(inner_angle)
                inner_x = self.x + math.cos(inner_rad) * (self.size / 2)
                inner_y = self.y + math.sin(inner_rad) * (self.size / 2)
                points.append((inner_x, inner_y))
                
            pygame.draw.polygon(pantalla, self.color, points)
            
        elif self.tipo in ["brillo", "humo"]:
            # Efecto de desvanecimiento para brillos y humo
            alpha = min(255, int(self.life * 2))
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            if self.tipo == "brillo":
                pygame.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
            else:  # humo
                pygame.draw.circle(surf, (*self.color, alpha // 2), (self.size, self.size), self.size)
            pantalla.blit(surf, (self.x - self.size, self.y - self.size))
            
        elif self.tipo == "chispas":
            # Chispas con cola
            tail_length = 5
            for i in range(tail_length):
                alpha = 255 - (i * 50)
                if alpha > 0:
                    pos_x = self.x - (self.vx * i * 0.5)
                    pos_y = self.y - (self.vy * i * 0.5)
                    size = max(1, self.size - i)
                    pygame.draw.circle(pantalla, (*self.color, alpha), (int(pos_x), int(pos_y)), size)
        else:
            # Confeti normal
            pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.size, self.size))

def crear_particulas(x, y, cantidad=50, tipo="confeti", color=None):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo, color))

# Botones
boton_pausa_rect = pygame.Rect(ANCHO - 80, 10, 32, 32)
boton_reiniciar_rect = pygame.Rect(ANCHO - 120, 10, 32, 32)

class SistemaAudio:
    def __init__(self):
        self.sonidos = {}
        self.volumen_efectos = 0.3
        self.inicializar_sonidos_virtuales()
    
    def inicializar_sonidos_virtuales(self):
        """Crear sonidos básicos programáticamente"""
        print("Inicializando sistema de audio virtual...")
    
    def reproducir(self, nombre):
        """Reproducir efecto de sonido (implementación virtual)"""
        print(f"Sonido reproducido: {nombre}")

class Estadisticas:
    def __init__(self):
        self.piezas_colocadas = [0] * 7  # Contador por tipo de pieza
        self.lineas_por_tipo = {1: 0, 2: 0, 3: 0, 4: 0}
        self.max_combo = 0
        self.tiempo_juego = 0
        self.picos_altura = []
    
    def registrar_pieza(self, tipo):
        self.piezas_colocadas[tipo] += 1
    
    def registrar_lineas(self, cantidad):
        if cantidad in self.lineas_por_tipo:
            self.lineas_por_tipo[cantidad] += 1
    
    def actualizar_combo(self, combo):
        self.max_combo = max(self.max_combo, combo)
    
    def actualizar_altura_maxima(self, tablero):
        altura = 0
        for y in range(FILAS_TABLERO):
            if any(tablero.grid[y]):
                altura = FILAS_TABLERO - y
                break
        self.picos_altura.append(altura)
    
    def actualizar_tiempo(self, dt):
        self.tiempo_juego += dt
    
    def obtener_estadisticas(self):
        return {
            'Altura Máxima': max(self.picos_altura) if self.picos_altura else 0,
            'Piezas Totales': sum(self.piezas_colocadas),
            'Tetris': self.lineas_por_tipo[4],
            'Triples': self.lineas_por_tipo[3],
            'Dobles': self.lineas_por_tipo[2],
            'Simples': self.lineas_por_tipo[1],
            'Combo Máximo': self.max_combo,
            'Tiempo Jugado': f"{self.tiempo_juego // 1000 // 60}:{self.tiempo_juego // 1000 % 60:02d}"
        }

class SistemaPuntuaciones:
    def __init__(self):
        self.archivo_puntuaciones = "puntuaciones.txt"
        self.puntuaciones = self.cargar_puntuaciones()
    
    def cargar_puntuaciones(self):
        try:
            with open(self.archivo_puntuaciones, 'r') as f:
                return [int(line.strip()) for line in f.readlines() if line.strip()]
        except:
            return [10000, 8000, 6000, 4000, 2000]  # Puntuaciones por defecto
    
    def guardar_puntuacion(self, puntuacion):
        self.puntuaciones.append(puntuacion)
        self.puntuaciones.sort(reverse=True)
        self.puntuaciones = self.puntuaciones[:10]  # Top 10
        
        try:
            with open(self.archivo_puntuaciones, 'w') as f:
                for score in self.puntuaciones:
                    f.write(f"{score}\n")
        except Exception as e:
            print(f"Error guardando puntuación: {e}")
    
    def es_puntuacion_alta(self, puntuacion):
        return len(self.puntuaciones) < 10 or puntuacion > min(self.puntuaciones)
    
    def dibujar_tabla_puntuaciones(self, pantalla, fuente, x, y):
        panel_ancho = 250
        panel_alto = 300
        panel_rect = pygame.Rect(x, y, panel_ancho, panel_alto)
        
        # Fondo del panel
        pygame.draw.rect(pantalla, COLOR_TABLERO, panel_rect, border_radius=8)
        pygame.draw.rect(pantalla, COLOR_BORDE, panel_rect, 2, border_radius=8)
        
        # Título
        titulo = fuente.render("MEJORES PUNTUACIONES", True, BLANCO)
        pantalla.blit(titulo, (x + panel_ancho//2 - titulo.get_width()//2, y + 20))
        
        # Lista de puntuaciones
        for i, score in enumerate(self.puntuaciones[:5]):
            texto = fuente.render(f"{i+1}. {score:08d}", True, BLANCO)
            pantalla.blit(texto, (x + 20, y + 70 + i * 40))

class Configuracion:
    def __init__(self):
        self.volumen_musica = 0.5
        self.volumen_efectos = 0.3
        self.controles = {
            'izquierda': [pygame.K_LEFT, pygame.K_a],
            'derecha': [pygame.K_RIGHT, pygame.K_d],
            'rotar': [pygame.K_UP, pygame.K_w],
            'bajar': [pygame.K_DOWN, pygame.K_s],
            'caida_instantanea': [pygame.K_SPACE],
            'hold': [pygame.K_c, pygame.K_LSHIFT]
        }
        self.mostrar_pieza_fantasma = True
        self.mostrar_sombra = True
        self.estilo_rotacion = 'srs'
    
    def guardar_configuracion(self):
        config = {
            'volumen_musica': self.volumen_musica,
            'volumen_efectos': self.volumen_efectos,
            'mostrar_pieza_fantasma': self.mostrar_pieza_fantasma,
            'mostrar_sombra': self.mostrar_sombra,
            'estilo_rotacion': self.estilo_rotacion
        }
        
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f)
        except:
            print("Error guardando configuración")
    
    def cargar_configuracion(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.volumen_musica = config.get('volumen_musica', 0.5)
                self.volumen_efectos = config.get('volumen_efectos', 0.3)
                self.mostrar_pieza_fantasma = config.get('mostrar_pieza_fantasma', True)
                self.mostrar_sombra = config.get('mostrar_sombra', True)
                self.estilo_rotacion = config.get('estilo_rotacion', 'srs')
        except:
            print("Configuración no encontrada, usando valores por defecto")

class TextoFlotante:
    def __init__(self, texto, x, y, color=BLANCO, duracion=1500):
        self.texto = texto
        self.x = x
        self.y = y
        self.color = color
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = duracion
    
    def actualizar(self):
        return pygame.time.get_ticks() - self.tiempo_inicio < self.duracion
    
    def dibujar(self, pantalla, fuente):
        tiempo = pygame.time.get_ticks() - self.tiempo_inicio
        progreso = tiempo / self.duracion
        
        alpha = int(255 * (1 - progreso))
        y_offset = -50 * progreso
        
        texto_surf = fuente.render(self.texto, True, self.color)
        texto_surf.set_alpha(alpha)
        
        pantalla.blit(texto_surf, (self.x - texto_surf.get_width() // 2, 
                                 self.y + y_offset - texto_surf.get_height() // 2))

class EfectosEspeciales:
    def __init__(self):
        self.animaciones = []
    
    def agregar_explosion_linea(self, fila):
        for x in range(COLUMNAS_TABLERO):
            crear_particulas(
                MARGEN_X + x * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                MARGEN_Y + fila * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                10, "chispas", (255, 255, 100)
            )
    
    def agregar_texto_flotante(self, texto, x, y, color=BLANCO):
        self.animaciones.append(TextoFlotante(texto, x, y, color))
    
    def actualizar(self):
        self.animaciones = [anim for anim in self.animaciones if anim.actualizar()]
    
    def dibujar(self, pantalla, fuente):
        for anim in self.animaciones:
            anim.dibujar(pantalla, fuente)

class Pieza:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.color = COLORES_PIEZAS[tipo]
        self.rotacion = 0
        self.forma = PIEZAS[tipo][self.rotacion]
        
    def rotar(self, direccion=1):
        nueva_rotacion = (self.rotacion + direccion) % 4
        return PIEZAS[self.tipo][nueva_rotacion]
    
    def aplicar_rotacion(self, direccion=1):
        self.rotacion = (self.rotacion + direccion) % 4
        self.forma = PIEZAS[self.tipo][self.rotacion]
    
    def obtener_bloques(self):
        bloques = []
        for y, fila in enumerate(self.forma):
            for x, celda in enumerate(fila):
                if celda:
                    bloques.append((self.x + x, self.y + y))
        return bloques

class Tablero:
    def __init__(self):
        self.grid = [[None for _ in range(COLUMNAS_TABLERO)] for _ in range(FILAS_TABLERO)]
        self.puntuacion = 0
        self.nivel = 1
        self.lineas_completadas = 0
        self.combo = 0
        self.ultima_linea_tiempo = 0
        
    def es_posicion_valida(self, pieza):
        for x, y in pieza.obtener_bloques():
            if x < 0 or x >= COLUMNAS_TABLERO or y >= FILAS_TABLERO:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    
    def agregar_pieza(self, pieza):
        for x, y in pieza.obtener_bloques():
            if y >= 0:
                self.grid[y][x] = pieza.color
    
    def limpiar_lineas(self):
        lineas_completas = []
        for y in range(FILAS_TABLERO):
            if all(self.grid[y]):
                lineas_completas.append(y)
        
        if lineas_completas:
            self.ultima_linea_tiempo = pygame.time.get_ticks()
            
            # Calcular puntuación
            lineas = len(lineas_completas)
            multiplicador_nivel = self.nivel
            
            # Puntos base por líneas
            if lineas == 1:
                puntos = 100 * multiplicador_nivel
            elif lineas == 2:
                puntos = 300 * multiplicador_nivel
            elif lineas == 3:
                puntos = 500 * multiplicador_nivel
            elif lineas == 4:
                puntos = 800 * multiplicador_nivel
            
            # Bonus por combo
            if self.combo > 0:
                puntos += puntos * self.combo * 0.5
            
            self.puntuacion += int(puntos)
            self.lineas_completadas += lineas
            self.combo += 1
            
            # Actualizar nivel
            self.nivel = self.lineas_completadas // 10 + 1
            
            # Eliminar líneas completas
            for linea in sorted(lineas_completas, reverse=True):
                del self.grid[linea]
                self.grid.insert(0, [None for _ in range(COLUMNAS_TABLERO)])
            
            return lineas_completas
        else:
            self.combo = 0
            return []
    
    def dibujar(self, pantalla):
        # Dibujar fondo del tablero
        tablero_rect = pygame.Rect(MARGEN_X, MARGEN_Y, ANCHO_TABLERO, ALTO_TABLERO)
        pygame.draw.rect(pantalla, COLOR_TABLERO, tablero_rect)
        pygame.draw.rect(pantalla, COLOR_BORDE, tablero_rect, 3)
        
        # Dibujar celdas ocupadas
        for y in range(FILAS_TABLERO):
            for x in range(COLUMNAS_TABLERO):
                if self.grid[y][x] is not None:
                    celda_rect = pygame.Rect(
                        MARGEN_X + x * TAMANIO_CELDA,
                        MARGEN_Y + y * TAMANIO_CELDA,
                        TAMANIO_CELDA, TAMANIO_CELDA
                    )
                    pygame.draw.rect(pantalla, self.grid[y][x], celda_rect)
                    pygame.draw.rect(pantalla, COLOR_BORDE, celda_rect, 1)
        
        # Dibujar rejilla
        for x in range(COLUMNAS_TABLERO + 1):
            pygame.draw.line(
                pantalla, 
                COLOR_BORDE, 
                (MARGEN_X + x * TAMANIO_CELDA, MARGEN_Y),
                (MARGEN_X + x * TAMANIO_CELDA, MARGEN_Y + ALTO_TABLERO),
                1
            )
        
        for y in range(FILAS_TABLERO + 1):
            pygame.draw.line(
                pantalla, 
                COLOR_BORDE, 
                (MARGEN_X, MARGEN_Y + y * TAMANIO_CELDA),
                (MARGEN_X + ANCHO_TABLERO, MARGEN_Y + y * TAMANIO_CELDA),
                1
            )

def dibujar_boton_reiniciar():
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLOR_BOTON_HOVER if boton_reiniciar_rect.collidepoint(mouse_pos) else COLOR_BOTON
    color_icono = (255, 255, 255) if boton_reiniciar_rect.collidepoint(mouse_pos) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_reiniciar_rect, border_radius=6)
    pygame.draw.rect(pantalla, color_icono, boton_reiniciar_rect, 2, border_radius=6)
    
    centro_x = boton_reiniciar_rect.centerx
    centro_y = boton_reiniciar_rect.centery
    radio = 8
    
    pygame.draw.circle(pantalla, color_icono, (centro_x, centro_y), radio, 2)
    
    inicio_x = centro_x + 4
    inicio_y = centro_y - 4
    
    puntos_flecha = [
        (inicio_x, inicio_y),
        (inicio_x - 3, inicio_y - 3),
        (inicio_x - 6, inicio_y)
    ]
    pygame.draw.polygon(pantalla, color_icono, puntos_flecha)

def dibujar_boton_pausa():
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLOR_BOTON_HOVER if boton_pausa_rect.collidepoint(mouse_pos) else COLOR_BOTON
    color_icono = (255, 255, 255) if boton_pausa_rect.collidepoint(mouse_pos) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_pausa_rect, border_radius=6)
    pygame.draw.rect(pantalla, color_icono, boton_pausa_rect, 2, border_radius=6)
    
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 8, boton_pausa_rect.y + 6, 4, 20))
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 20, boton_pausa_rect.y + 6, 4, 20))

def dibujar_pieza_fantasma(pieza, tablero, pantalla):
    pieza_fantasma = Pieza(pieza.x, pieza.y, pieza.tipo)
    pieza_fantasma.rotacion = pieza.rotacion
    pieza_fantasma.forma = pieza.forma
    
    while tablero.es_posicion_valida(pieza_fantasma):
        pieza_fantasma.y += 1
    
    pieza_fantasma.y -= 1
    
    # Dibujar la pieza fantasma
    for x, y in pieza_fantasma.obtener_bloques():
        if y >= 0:
            celda_rect = pygame.Rect(
                MARGEN_X + x * TAMANIO_CELDA,
                MARGEN_Y + y * TAMANIO_CELDA,
                TAMANIO_CELDA, TAMANIO_CELDA
            )
            surf = pygame.Surface((TAMANIO_CELDA, TAMANIO_CELDA), pygame.SRCALPHA)
            pygame.draw.rect(surf, (*pieza.color, 80), (0, 0, TAMANIO_CELDA, TAMANIO_CELDA))
            pygame.draw.rect(surf, (*pieza.color, 150), (0, 0, TAMANIO_CELDA, TAMANIO_CELDA), 1)
            pantalla.blit(surf, celda_rect)

def dibujar_pieza(pieza, pantalla, offset_x=0, offset_y=0, alpha=255):
    for x, y in pieza.obtener_bloques():
        if y + offset_y >= 0:
            celda_rect = pygame.Rect(
                MARGEN_X + (x + offset_x) * TAMANIO_CELDA,
                MARGEN_Y + (y + offset_y) * TAMANIO_CELDA,
                TAMANIO_CELDA, TAMANIO_CELDA
            )
            
            if alpha < 255:
                surf = pygame.Surface((TAMANIO_CELDA, TAMANIO_CELDA), pygame.SRCALPHA)
                pygame.draw.rect(surf, (*pieza.color, alpha), (0, 0, TAMANIO_CELDA, TAMANIO_CELDA))
                pygame.draw.rect(surf, COLOR_BORDE, (0, 0, TAMANIO_CELDA, TAMANIO_CELDA), 1)
                pantalla.blit(surf, celda_rect)
            else:
                pygame.draw.rect(pantalla, pieza.color, celda_rect)
                pygame.draw.rect(pantalla, COLOR_BORDE, celda_rect, 1)

def dibujar_menu_principal(juego):
    pantalla.fill(COLOR_FONDO)
    
    # Título animado
    tiempo = pygame.time.get_ticks() / 1000
    titulo = juego.fuente_grande.render("TETRIS", True, BLANCO)
    titulo_rect = titulo.get_rect(center=(ANCHO//2, 100))
    
    surf_temp = pygame.Surface(titulo.get_size(), pygame.SRCALPHA)
    surf_temp.blit(titulo, (0, 0))
    surf_temp.set_alpha(200 + int(math.sin(tiempo * 3) * 55))
    pantalla.blit(surf_temp, titulo_rect)
    
    # Botón jugar
    boton_jugar = pygame.Rect(ANCHO//2 - 100, 300, 200, 60)
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLOR_BOTON_HOVER if boton_jugar.collidepoint(mouse_pos) else COLOR_BOTON
    
    pygame.draw.rect(pantalla, color_boton, boton_jugar, border_radius=12)
    pygame.draw.rect(pantalla, BLANCO, boton_jugar, 3, border_radius=12)
    
    texto_jugar = juego.fuente.render("JUGAR", True, BLANCO)
    texto_rect = texto_jugar.get_rect(center=boton_jugar.center)
    pantalla.blit(texto_jugar, texto_rect)
    
    # Instrucciones
    instrucciones = [
        "CONTROLES:",
        "← → : MOVER PIEZA",
        "↑ : ROTAR PIEZA", 
        "↓ : BAJAR RÁPIDO",
        "ESPACIO : CAÍDA INSTANTÁNEA",
        "C : GUARDAR PIEZA (HOLD)",
        "ESC : PAUSA"
    ]
    
    for i, linea in enumerate(instrucciones):
        texto = juego.fuente_pista.render(linea, True, BLANCO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 400 + i * 25))
    
    # Efecto de partículas ocasionales
    if random.random() < 0.02:
        crear_particulas(ANCHO//2, 150, 5, "confeti")
    
    return boton_jugar

def mostrar_pausa_mejorada(juego):
    # Fondo semitransparente
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    juego.pantalla.blit(s, (0, 0))
    
    # Panel de pausa
    panel_rect = pygame.Rect(ANCHO//2 - 200, ALTO//2 - 150, 400, 300)
    pygame.draw.rect(juego.pantalla, COLOR_TABLERO, panel_rect, border_radius=12)
    pygame.draw.rect(juego.pantalla, BLANCO, panel_rect, 3, border_radius=12)
    
    # Título
    texto_pausa = juego.fuente_grande.render("PAUSA", True, BLANCO)
    juego.pantalla.blit(texto_pausa, (ANCHO//2 - texto_pausa.get_width()//2, ALTO//2 - 120))
    
    # Estadísticas en pausa
    stats = [
        f"Puntuación: {juego.tablero.puntuacion}",
        f"Nivel: {juego.tablero.nivel}",
        f"Líneas: {juego.tablero.lineas_completadas}",
        f"Combo Actual: {juego.tablero.combo}"
    ]
    
    for i, stat in enumerate(stats):
        texto = juego.fuente.render(stat, True, BLANCO)
        juego.pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 60 + i * 40))
    
    # Instrucciones
    texto_continuar = juego.fuente_pista.render("Presiona ESC para continuar", True, BLANCO)
    juego.pantalla.blit(texto_continuar, (ANCHO//2 - texto_continuar.get_width()//2, ALTO//2 + 100))

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Tetris Game ")
        self.reloj = pygame.time.Clock()
        
        # Sistemas
        self.audio = SistemaAudio()
        self.estadisticas = Estadisticas()
        self.puntuaciones = SistemaPuntuaciones()
        self.config = Configuracion()
        self.efectos = EfectosEspeciales()
        
        # Fuentes
        self.fuente = self.obtener_fuente(25)
        self.fuente_grande = self.obtener_fuente(50)
        self.fuente_mediana = self.obtener_fuente(24)
        self.fuente_pista = self.obtener_fuente(20)
        
        # Cargar configuración
        self.config.cargar_configuracion()
        
        self.reiniciar_juego()
    
    def obtener_fuente(self, tamaño):
        """Obtener fuentes compatibles con Linux"""
        fuentes_linux = [
            'dejavusans',
            'liberationsans', 
            'freesans',
            None
        ]
        
        for fuente_nombre in fuentes_linux:
            try:
                fuente = pygame.font.SysFont(fuente_nombre, tamaño)
                texto_prueba = fuente.render('Test', True, BLANCO)
                if texto_prueba.get_width() > 0:
                    return fuente
            except:
                continue
        
        return pygame.font.Font(None, tamaño)
    
    def reiniciar_juego(self):
        self.tablero = Tablero()
        self.pieza_actual = self.generar_pieza()
        self.pieza_siguiente = self.generar_pieza()
        self.pieza_hold = None
        self.puede_cambiar_hold = True
        self.juego_activo = True
        self.pausa = False
        self.estado_juego = "menu"
        self.ultima_caida = pygame.time.get_ticks()
        self.ultima_actualizacion_tiempo = pygame.time.get_ticks()
        self.niveles_gravedad = [
            1000, 800, 600, 450, 350,  # Niveles 1-5
            250, 200, 150, 100, 80,     # Niveles 6-10
            60, 50, 40, 30, 20,         # Niveles 11-15
            15, 10, 8, 6, 4, 2, 1       # Niveles 16+
        ]
    
    def generar_pieza(self):
        tipo = random.randint(0, len(PIEZAS) - 1)
        return Pieza(COLUMNAS_TABLERO // 2 - 2, 0, tipo)
    
    def obtener_velocidad_caida(self):
        nivel = min(self.tablero.nivel, len(self.niveles_gravedad))
        return self.niveles_gravedad[nivel - 1]
    
    def rotar_con_kick(self, direccion=1):
        rotacion_original = self.pieza_actual.rotacion
        forma_original = self.pieza_actual.forma
        
        # Aplicar rotación
        self.pieza_actual.aplicar_rotacion(direccion)
        
        # Obtener tabla de kicks apropiada
        kicks = KICKS['I'] if self.pieza_actual.tipo == 0 else KICKS['default']
        kick_table = kicks[rotacion_original]
        
        # Probar kicks
        for kick in kick_table:
            self.pieza_actual.x += kick[0]
            self.pieza_actual.y += kick[1]
            
            if self.tablero.es_posicion_valida(self.pieza_actual):
                self.audio.reproducir('rotar')
                return True  # Rotación exitosa
            
            # Revertir kick
            self.pieza_actual.x -= kick[0]
            self.pieza_actual.y -= kick[1]
        
        # Si ningún kick funciona, revertir rotación
        self.pieza_actual.rotacion = rotacion_original
        self.pieza_actual.forma = forma_original
        return False
    
    def cambiar_hold(self):
        if self.puede_cambiar_hold:
            self.audio.reproducir('hold')
            
            if self.pieza_hold is None:
                self.pieza_hold = Pieza(0, 0, self.pieza_actual.tipo)
                self.pieza_actual = self.pieza_siguiente
                self.pieza_siguiente = self.generar_pieza()
            else:
                tipo_temp = self.pieza_actual.tipo
                self.pieza_actual = Pieza(COLUMNAS_TABLERO // 2 - 2, 0, self.pieza_hold.tipo)
                self.pieza_hold = Pieza(0, 0, tipo_temp)
            
            self.puede_cambiar_hold = False
    
    
    def manejar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.config.guardar_configuracion()
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado_juego == "menu":
                    boton_jugar = pygame.Rect(ANCHO//2 - 100, 300, 200, 60)
                    if boton_jugar.collidepoint(mouse_pos):
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        print("Iniciando juego...")
                
                elif self.estado_juego == "jugando":
                    if boton_pausa_rect.collidepoint(mouse_pos):
                        self.pausa = not self.pausa
                        print(f"Pausa: {self.pausa}")
                        if self.pausa:
                            mixer.music.pause()
                        else:
                            mixer.music.unpause()
                        continue
                    
                    elif boton_reiniciar_rect.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('reiniciar')
                        print("Juego reiniciado")
                    
                    elif self.pausa:
                        self.pausa = False
                        mixer.music.unpause()
                        print("Pausa desactivada")
                
                elif self.estado_juego == "game_over":
                    # DEFINIR LOS BOTONES EN LA MISMA POSICIÓN QUE EN dibujar_pantalla_game_over
                    boton_reiniciar = pygame.Rect(ANCHO//2 - 125, ALTO//2 + 20, 250, 60)
                    boton_menu = pygame.Rect(ANCHO//2 - 125, ALTO//2 + 100, 250, 60)
                    
                    if boton_reiniciar.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        print("Reiniciando desde game over")
                        return True  # Continuar el juego
                    
                    elif boton_menu.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "menu"
                        self.audio.reproducir('menu')
                        print("Volviendo al menú principal")
                        return True  # Continuar en el menú
            
            if evento.type == pygame.KEYDOWN:
                if self.estado_juego == "jugando":
                    if evento.key == pygame.K_ESCAPE:
                        self.pausa = not self.pausa
                        print(f"Pausa con ESC: {self.pausa}")
                        if self.pausa:
                            mixer.music.pause()
                        else:
                            mixer.music.unpause()
                    
                    elif not self.pausa:
                        # Movimiento izquierda
                        if evento.key in self.config.controles['izquierda']:
                            self.pieza_actual.x -= 1
                            if not self.tablero.es_posicion_valida(self.pieza_actual):
                                self.pieza_actual.x += 1
                            else:
                                self.audio.reproducir('mover')
                        
                        # Movimiento derecha
                        elif evento.key in self.config.controles['derecha']:
                            self.pieza_actual.x += 1
                            if not self.tablero.es_posicion_valida(self.pieza_actual):
                                self.pieza_actual.x -= 1
                            else:
                                self.audio.reproducir('mover')
                        
                        # Rotación
                        elif evento.key in self.config.controles['rotar']:
                            if self.config.estilo_rotacion == 'srs':
                                self.rotar_con_kick(1)
                            else:
                                forma_original = self.pieza_actual.forma
                                self.pieza_actual.aplicar_rotacion(1)
                                if not self.tablero.es_posicion_valida(self.pieza_actual):
                                    self.pieza_actual.forma = forma_original
                                    self.pieza_actual.rotacion = (self.pieza_actual.rotacion - 1) % 4
                                else:
                                    self.audio.reproducir('rotar')
                        
                        # Bajar rápido
                        elif evento.key in self.config.controles['bajar']:
                            self.pieza_actual.y += 1
                            if not self.tablero.es_posicion_valida(self.pieza_actual):
                                self.pieza_actual.y -= 1
                                self.bloquear_pieza()
                            else:
                                self.audio.reproducir('mover')
                        
                        # Caída instantánea
                        elif evento.key in self.config.controles['caida_instantanea']:
                            while self.tablero.es_posicion_valida(self.pieza_actual):
                                self.pieza_actual.y += 1
                            self.pieza_actual.y -= 1
                            self.bloquear_pieza()
                            self.audio.reproducir('caer')
                        
                        # Hold
                        elif evento.key in self.config.controles['hold']:
                            self.cambiar_hold()
                
                elif self.estado_juego == "game_over":
                    if evento.key == pygame.K_RETURN:
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        print("Reiniciando con ENTER desde Game Over")
                    elif evento.key == pygame.K_ESCAPE:
                        self.reiniciar_juego()
                        self.estado_juego = "menu"
                        self.audio.reproducir('menu')
                        print("Volviendo al menú con ESC")
        
        return True

    def bloquear_pieza(self):
        # Registrar estadísticas
        self.estadisticas.registrar_pieza(self.pieza_actual.tipo)
        
        # Agregar pieza al tablero
        self.tablero.agregar_pieza(self.pieza_actual)
        
        # Efecto visual al bloquear pieza
        crear_particulas(
            MARGEN_X + self.pieza_actual.x * TAMANIO_CELDA,
            MARGEN_Y + self.pieza_actual.y * TAMANIO_CELDA,
            20, "brillo", self.pieza_actual.color
        )
        
        # Verificar líneas completas
        lineas_completas = self.tablero.limpiar_lineas()
        
        if lineas_completas:
            self.audio.reproducir('linea')
            self.estadisticas.registrar_lineas(len(lineas_completas))
            self.estadisticas.actualizar_combo(self.tablero.combo)
            
            # Efectos especiales según cantidad de líneas
            if len(lineas_completas) == 4:
                self.audio.reproducir('tetris')
                self.efectos.agregar_texto_flotante("TETRIS!", ANCHO//2, ALTO//2, (255, 255, 0))
                crear_particulas(ANCHO//2, ALTO//2, 100, "estrellas")
            elif len(lineas_completas) >= 3:
                self.efectos.agregar_texto_flotante(f"{len(lineas_completas)} LÍNEAS!", ANCHO//2, ALTO//2, (255, 200, 0))
                crear_particulas(ANCHO//2, MARGEN_Y, 50, "chispas", (255, 255, 100))
            
            # Efectos de explosión en cada línea
            for fila in lineas_completas:
                self.efectos.agregar_explosion_linea(fila)
        
        # Cambiar a la siguiente pieza
        self.pieza_actual = self.pieza_siguiente
        self.pieza_siguiente = self.generar_pieza()
        self.puede_cambiar_hold = True
        
        # Verificar game over
        if not self.tablero.es_posicion_valida(self.pieza_actual):
            self.estado_juego = "game_over"
            self.audio.reproducir('gameover')
            crear_particulas(ANCHO//2, ALTO//2, 100, "humo")
            
            # Guardar puntuación si es alta
            if self.puntuaciones.es_puntuacion_alta(self.tablero.puntuacion):
                self.puntuaciones.guardar_puntuacion(self.tablero.puntuacion)
            
            print("Game Over!")
    
    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        dt = tiempo_actual - self.ultima_actualizacion_tiempo
        self.ultima_actualizacion_tiempo = tiempo_actual
        
        if self.estado_juego == "jugando" and not self.pausa:
            # Actualizar estadísticas
            self.estadisticas.actualizar_tiempo(dt)
            self.estadisticas.actualizar_altura_maxima(self.tablero)
            
            # Actualizar efectos
            self.efectos.actualizar()
            
            # Caída automática
            if tiempo_actual - self.ultima_caida > self.obtener_velocidad_caida():
                self.pieza_actual.y += 1
                if not self.tablero.es_posicion_valida(self.pieza_actual):
                    self.pieza_actual.y -= 1
                    self.bloquear_pieza()
                self.ultima_caida = tiempo_actual
    
    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        
        if self.estado_juego == "menu":
            dibujar_menu_principal(self)  # Pasar self como parámetro
            # Mostrar tabla de puntuaciones en el menú
            self.puntuaciones.dibujar_tabla_puntuaciones(self.pantalla, self.fuente, 50, 200)
            
        elif self.estado_juego == "jugando":
            # Dibujar tablero
            self.tablero.dibujar(self.pantalla)
            
            # Dibujar pieza fantasma si está habilitado
            if self.config.mostrar_pieza_fantasma:
                dibujar_pieza_fantasma(self.pieza_actual, self.tablero, self.pantalla)
            
            # Dibujar pieza actual
            dibujar_pieza(self.pieza_actual, self.pantalla)
            
            # Dibujar información del juego
            self.dibujar_informacion()
            
            # Dibujar botones
            dibujar_boton_reiniciar()
            dibujar_boton_pausa()
            
            # Dibujar efectos
            self.efectos.dibujar(self.pantalla, self.fuente_grande)
            
            if self.pausa:
                mostrar_pausa_mejorada(self)
                
        elif self.estado_juego == "game_over":
            self.dibujar_pantalla_game_over()
        
        # Dibujar partículas
        for particula in particulas:
            particula.draw(self.pantalla)
        
        pygame.display.flip()
    
    def dibujar_informacion(self):
        panel_x = MARGEN_X + ANCHO_TABLERO + 20
        panel_y = MARGEN_Y
        
        # Panel de información principal
        panel_principal = pygame.Rect(panel_x, panel_y, 250, 200)
        pygame.draw.rect(self.pantalla, COLOR_TABLERO, panel_principal, border_radius=8)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_principal, 2, border_radius=8)
        
        # Información del juego
        textos = [
            f"Puntuación: {self.tablero.puntuacion}",
            f"Nivel: {self.tablero.nivel}",
            f"Líneas: {self.tablero.lineas_completadas}",
            f"Combo: {self.tablero.combo}",
            f"Velocidad: {self.obtener_velocidad_caida()}ms"
        ]
        
        for i, texto in enumerate(textos):
            texto_surf = self.fuente_pista.render(texto, True, BLANCO)
            self.pantalla.blit(texto_surf, (panel_x + 10, panel_y + 20 + i * 30))
        
        # Panel de pieza siguiente
        panel_siguiente = pygame.Rect(panel_x, panel_y + 220, 250, 150)
        pygame.draw.rect(self.pantalla, COLOR_TABLERO, panel_siguiente, border_radius=8)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_siguiente, 2, border_radius=8)
        
        texto_siguiente = self.fuente_pista.render("Siguiente:", True, BLANCO)
        self.pantalla.blit(texto_siguiente, (panel_x + 10, panel_y + 240))
        
        # Dibujar pieza siguiente
        dibujar_pieza(self.pieza_siguiente, self.pantalla, offset_x=12, offset_y=9, alpha=200)
        
        # Panel de hold
        if self.pieza_hold:
            panel_hold = pygame.Rect(panel_x, panel_y + 390, 250, 150)
            pygame.draw.rect(self.pantalla, COLOR_TABLERO, panel_hold, border_radius=8)
            pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_hold, 2, border_radius=8)
            
            texto_hold = self.fuente_pista.render("Reserva:", True, BLANCO)
            self.pantalla.blit(texto_hold, (panel_x + 10, panel_y + 410))
            
            # Dibujar pieza en hold
            dibujar_pieza(self.pieza_hold, self.pantalla, offset_x=12, offset_y=14, alpha=200)
        
        # Panel de estadísticas
        panel_stats = pygame.Rect(MARGEN_X - 270, MARGEN_Y, 250, 300)
        pygame.draw.rect(self.pantalla, COLOR_TABLERO, panel_stats, border_radius=8)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_stats, 2, border_radius=8)
        
        texto_stats = self.fuente_pista.render("Estadísticas:", True, BLANCO)
        self.pantalla.blit(texto_stats, (MARGEN_X - 260, MARGEN_Y + 20))
        
        stats = self.estadisticas.obtener_estadisticas()
        for i, (key, value) in enumerate(stats.items()):
            texto = self.fuente_pista.render(f"{key}: {value}", True, BLANCO)
            self.pantalla.blit(texto, (MARGEN_X - 260, MARGEN_Y + 60 + i * 25))

    def dibujar_pantalla_game_over(self):
        # Fondo semitransparente
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.pantalla.blit(s, (0, 0))
        
        # Panel principal - más alto para evitar superposiciones
        panel_rect = pygame.Rect(ANCHO//2 - 300, ALTO//2 - 250, 600, 550)
        pygame.draw.rect(self.pantalla, COLOR_TABLERO, panel_rect, border_radius=15)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_rect, 4, border_radius=15)
        
        # Título GAME OVER - posición ajustada
        texto_game_over = self.fuente_grande.render("GAME OVER", True, (255, 50, 50))
        self.pantalla.blit(texto_game_over, (ANCHO//2 - texto_game_over.get_width()//2, ALTO//2 - 220))
        
        # Mostrar si es puntuación alta - posición antes del título principal
        if self.puntuaciones.es_puntuacion_alta(self.tablero.puntuacion):
            texto_alta = self.fuente_grande.render("¡NUEVO RÉCORD!", True, (255, 255, 0))
            self.pantalla.blit(texto_alta, (ANCHO//2 - texto_alta.get_width()//2, ALTO//2 - 280))
            crear_particulas(ANCHO//2, ALTO//2 - 240, 50, "estrellas", (255, 255, 0))
        
        # Estadísticas - posición reorganizada
        estadisticas_y = ALTO//2 - 150
        textos_estadisticas = [
            f'Puntuación final: {self.tablero.puntuacion}',
            f'Líneas completadas: {self.tablero.lineas_completadas}',
            f'Nivel alcanzado: {self.tablero.nivel}',
            f'Piezas colocadas: {sum(self.estadisticas.piezas_colocadas)}'
        ]
        
        for i, texto in enumerate(textos_estadisticas):
            texto_surf = self.fuente.render(texto, True, BLANCO)
            self.pantalla.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, estadisticas_y + i * 40))
        
        # Botón reiniciar - posición ajustada
        boton_reiniciar = pygame.Rect(ANCHO//2 - 125, ALTO//2 + 20, 250, 60)
        mouse_pos = pygame.mouse.get_pos()
        color_reiniciar = COLOR_BOTON_HOVER if boton_reiniciar.collidepoint(mouse_pos) else COLOR_BOTON
        
        pygame.draw.rect(self.pantalla, color_reiniciar, boton_reiniciar, border_radius=12)
        pygame.draw.rect(self.pantalla, BLANCO, boton_reiniciar, 3, border_radius=12)
        
        texto_reiniciar = self.fuente.render("JUGAR DE NUEVO", True, BLANCO)
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=boton_reiniciar.center)
        self.pantalla.blit(texto_reiniciar, texto_reiniciar_rect)
        
        # Botón menú principal - posición ajustada
        boton_menu = pygame.Rect(ANCHO//2 - 125, ALTO//2 + 100, 250, 60)
        color_menu = (100, 100, 200) if boton_menu.collidepoint(mouse_pos) else (70, 70, 150)
        
        pygame.draw.rect(self.pantalla, color_menu, boton_menu, border_radius=12)
        pygame.draw.rect(self.pantalla, BLANCO, boton_menu, 3, border_radius=12)
        
        texto_menu = self.fuente.render("MENÚ PRINCIPAL", True, BLANCO)
        texto_menu_rect = texto_menu.get_rect(center=boton_menu.center)
        self.pantalla.blit(texto_menu, texto_menu_rect)
        
        # Instrucciones - posición ajustada
        texto_instrucciones = self.fuente_pista.render("", True, BLANCO)
        self.pantalla.blit(texto_instrucciones, (ANCHO//2 - texto_instrucciones.get_width()//2, ALTO//2 + 180))
        
        # Mostrar tabla de puntuaciones en un panel separado a la derecha
        tabla_x = ANCHO//2 + 320  # Mover más a la derecha
        tabla_y = ALTO//2 - 250
        self.puntuaciones.dibujar_tabla_puntuaciones(self.pantalla, self.fuente, tabla_x, tabla_y)
        
        # Panel adicional para estadísticas detalladas a la izquierda
        panel_stats = pygame.Rect(ANCHO//2 - 620, ALTO//2 - 250, 250, 400)
        pygame.draw.rect(self.pantalla, COLOR_TABLERO, panel_stats, border_radius=8)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, panel_stats, 2, border_radius=8)
        
        # Título estadísticas
        titulo_stats = self.fuente.render("ESTADÍSTICAS", True, BLANCO)
        self.pantalla.blit(titulo_stats, (panel_stats.centerx - titulo_stats.get_width()//2, panel_stats.y + 20))
        
        # Estadísticas detalladas
        stats_detalladas = self.estadisticas.obtener_estadisticas()
        stats_textos = [
            f"Tetris: {stats_detalladas['Tetris']}",
            f"Triples: {stats_detalladas['Triples']}",
            f"Dobles: {stats_detalladas['Dobles']}",
            f"Simples: {stats_detalladas['Simples']}",
            f"Combo Máx: {stats_detalladas['Combo Máximo']}",
            f"Altura Máx: {stats_detalladas['Altura Máxima']}",
            f"Tiempo: {stats_detalladas['Tiempo Jugado']}"
        ]
        
        for i, stat_text in enumerate(stats_textos):
            texto_stat = self.fuente_pista.render(stat_text, True, BLANCO)
            self.pantalla.blit(texto_stat, (panel_stats.x + 20, panel_stats.y + 70 + i * 35))

    def correr(self):
        global particulas
        
        corriendo = True
        while corriendo:
            # Actualizar partículas
            particulas = [p for p in particulas if p.update()]
            
            corriendo = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

def main():
    """Función principal con manejo de errores"""
    try:
        print("Iniciando Tetris Game - Versión Mejorada")
        print("Características implementadas:")
        print("- Sistema de Hold (Reserva de piezas)")
        print("- Rotación con Pared Kicks (SRS)")
        print("- Sistema de estadísticas detalladas")
        print("- Guardado de puntuaciones")
        print("- Efectos visuales mejorados")
        print("- Sistema de configuración")
        print("- Múltiples paneles de información")
        print("- Menú de Game Over mejorado")
        
        juego = Juego()
        
        # Hacer las fuentes globales disponibles
        global fuente, fuente_game_over, fuente_pista
        fuente = juego.fuente
        fuente_game_over = juego.fuente_grande
        fuente_pista = juego.fuente_pista
        
        juego.correr()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("Juego terminado correctamente")

if __name__ == "__main__":
    main()