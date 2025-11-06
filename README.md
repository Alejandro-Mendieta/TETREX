# 🎮 Tetris 

## 🌟 Descripción
**Tetris Espacial** es una versión mejorada del clásico juego Tetris con temática espacial y efectos visuales neon. Desarrollado en Python usando Pygame, incluye características modernas como sistema de hold, rotaciones SRS, efectos de partículas y estadísticas detalladas.

## 🚀 Características Principales

### 🎯 Jugabilidad
- **Sistema de Hold**: Guarda piezas para usar después (Tecla `C` o `Shift`)
- **Rotaciones SRS**: Sistema profesional de rotación con wall kicks
- **Pieza fantasma**: Muestra dónde caerá la pieza actual
- **Sistema de niveles**: Velocidad aumenta progresivamente
- **Combo system**: Bonus por eliminar múltiples líneas consecutivas

### 🎨 Visuales
- **Tema espacial neón**: Colores vibrantes inspirados en el cosmos
- **Efectos de partículas**: Explosiones, chispas y estrellas
- **Animaciones fluidas**: Textos flotantes y transiciones suaves
- **Interfaz moderna**: Paneles organizados y diseño limpio

### 📊 Estadísticas
- **Puntuación detallada**: Sistema complejo con bonus por combo y nivel
- **Estadísticas completas**: Seguimiento de Tetris, triples, dobles, etc.
- **Tabla de records**: Guarda las 10 mejores puntuaciones
- **Tiempo de juego**: Cronómetro integrado

## 🎮 Controles

### Movimiento Básico
- **← →** (Flechas) o **A D**: Mover pieza izquierda/derecha
- **↑** (Flecha) o **W**: Rotar pieza
- **↓** (Flecha) o **S**: Bajar rápido
- **ESPACIO**: Caída instantánea

### Funciones Avanzadas
- **C** o **Shift**: Guardar pieza (Hold)
- **ESC**: Pausa/Menú
- **ENTER**: Confirmar/Reiniciar

### En Game Over
- **Click**: Botones "Jugar de nuevo" y "Menú principal"
- **ENTER**: Jugar de nuevo
- **ESC**: Volver al menú

## 🛠️ Instalación y Ejecución

### Requisitos
- Python 3.7+
- Pygame 2.0+

### Instalación en Linux
```bash
# Instalar dependencias
sudo apt update
sudo apt install python3 python3-pip python3-pygame

# Ejecutar el juego
python3 tetris_espacial.py
```

### Instalación en Windows
```bash
# Instalar Pygame
pip install pygame

# Ejecutar el juego
python tetris_espacial.py
```

## 📁 Estructura del Proyecto

```
tetris_espacial/
├── tetris_espacial.py      # Código principal del juego
├── config.json            # Configuración del usuario (se crea automáticamente)
├── puntuaciones.txt       # Records del juego (se crea automáticamente)
└── README.md             # Este archivo
```

## ⚙️ Configuración

El juego guarda automáticamente:
- **Volumen** de música y efectos
- **Controles** personalizados
- **Preferencias** visuales (pieza fantasma, sombras)
- **Estilo de rotación** (SRS o clásico)

## 🎯 Sistema de Puntuación

### Puntos Base por Líneas
- **1 línea**: 100 × nivel
- **2 líneas**: 300 × nivel  
- **3 líneas**: 500 × nivel
- **4 líneas (Tetris)**: 800 × nivel

### Bonus Adicionales
- **Combo**: +50% por combo consecutivo
- **Nivel**: Multiplicador progresivo
- **Tetris**: Efectos visuales especiales

## 🌌 Temática Espacial

### Colores de Piezas
- **I - Cyan Nebulosa**: Energía pura
- **J - Púrpura Quásar**: Materia oscura  
- **L - Rosa Supernova**: Explosión estelar
- **O - Amarillo Solar**: Estrella central
- **S - Verde Extraterrestre**: Vida alien
- **T - Naranja Estelar**: Gigante roja
- **Z - Magenta Cósmico**: Agujero de gusano

### Efectos Visuales
- **Partículas de energía** al colocar piezas
- **Explosiones estelares** al completar líneas
- **Efecto Tetris** especial con 4 líneas
- **Humo cósmico** en game over

## 🔧 Características Técnicas

### Optimizaciones
- **Sistema de partículas** eficiente
- **Renderizado** optimizado
- **Gestión de memoria** automática
- **Compatibilidad** multiplataforma

### Arquitectura
- **Programación orientada a objetos**
- **Sistemas modulares** (audio, estadísticas, efectos)
- **Manejo de errores** robusto
- **Configuración persistente**

## 🐛 Solución de Problemas

### Error: "Pygame no está instalado"
```bash
# Linux
sudo apt install python3-pygame

# Windows/Mac
pip install pygame
```

### Error: "No se puede cargar audio"
- El juego funciona sin archivos de audio
- Los efectos son simulados virtualmente

### El juego va lento
- Cierra otras aplicaciones
- Reduce la resolución si es necesario
- Verifica que tengas los drivers gráficos actualizados

## 📄 Licencia

Este proyecto es de código abierto para fines educativos y de entretenimiento.

## 👨‍💻 Desarrollo
Por Alejandro Mendieta

creado con ❤️ usando Python y Pygame. Incluye las mejores prácticas modernas de desarrollo de juegos y una arquitectura escalable para futuras mejoras.

---

**¡Disfruta del Tetris Espacial! 🚀✨**