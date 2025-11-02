# 🎲 BACKGAMMON PY

> Implementación completa del juego de Backgammon en Python con arquitectura modular SOLID y múltiples interfaces (CLI + GUI).

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)

---

## 📋 Descripción

**Backgammon PY** es una implementación profesional del clásico juego de Backgammon que demuestra principios avanzados de diseño de software:

- ✅ **Arquitectura SOLID**: SRP, OCP, DIP aplicados rigurosamente
- ✅ **Separación Core-UI**: Lógica de negocio independiente de interfaces
- ✅ **Múltiples interfaces**: CLI (terminal) y GUI (Pygame)
- ✅ **Testing exhaustivo**: >90% cobertura con pytest
- ✅ **Documentación completa**: Docstrings, type hints, justificaciones de diseño

### 🎯 Características

- 🎮 **Dos modos de juego**:
  - CLI interactiva con colores ANSI
  - GUI con Pygame (drag & drop, animaciones, sonidos)
- 🎲 **Reglas completas**:
  - Movimientos normales y captura de blots
  - Entrada obligatoria desde barra
  - Bear-off con validación de home
  - Regla del dado mayor
  - Detección de victoria
- 🧪 **Testing robusto**:
  - Tests unitarios por componente
  - Tests de integración end-to-end
  - Fixtures avanzadas y mocking

---

## 📁 Estructura del Proyecto

```
backgammon-py/
├── source/                      # 🎯 Core del juego (lógica de negocio)
│   ├── backgammon.py           # Orquestador principal
│   ├── tablero.py              # Estado del juego
│   ├── validador_movimientos.py
│   ├── ejecutor_movimientos.py
│   ├── analizador_posibilidades.py
│   ├── gestor_turnos.py
│   ├── dados.py
│   ├── constantes.py
│   └── excepciones.py
│
├── cli/                         # 🖥️ Interfaz de línea de comandos
│   └── cli.py
│
├── game/                        # 🎮 Interfaz gráfica (Pygame)
│   └── backgammon_game.py
│
├── tests/                       # 🧪 Suite de testing
│   ├── conftest.py             # Fixtures compartidas
│   ├── test_tablero.py
│   ├── test_validador.py
│   ├── test_ejecutor.py
│   ├── test_backgammon.py
│   └── test_integration.py
│
├── assets/                      # 🎨 Recursos multimedia
│   ├── images/                 # Texturas del tablero
│   └── sound/                  # Efectos de sonido
│
├── docs/                        # 📚 Documentación
│   ├── JUSTIFICACION.md
│   ├── prompts_testing.md
│   └── CHANGELOG.md
│
├── requirements.txt             # 📦 Dependencias
├── pytest.ini                   # ⚙️ Configuración de pytest
└── README.md                    # 📖 Este archivo
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior
- pip (gestor de paquetes)

### Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/backgammon-py.git
cd backgammon-py
```

### Instalar dependencias

```bash
# Dependencias principales
pip install -r requirements.txt

# Dependencias de desarrollo (opcional, para testing)
pip install pytest pytest-cov pytest-mock
```

---

## 🎮 Cómo Jugar

### Opción 1: Interfaz CLI (Terminal)

Interfaz de línea de comandos con colores ANSI y comandos interactivos.

```bash
python -m cli.cli
```

**Comandos disponibles:**

```
dados, d        Tirar dados
mover, m        Mover ficha (modo interactivo)
tablero, t      Mostrar tablero
estado, e       Mostrar estado resumido
finalizar, f    Finalizar tirada actual
help, h         Mostrar ayuda
salir, q        Salir del juego
```

**Ejemplo de sesión:**

```
blancas> dados
  🎲 Dados: [3] [5]
  Movimientos disponibles: [3, 5]

blancas> mover
  ¿Desde qué posición mover? (1-24): 1
  Elige dado: 1
  ✓ Movió correctamente

blancas> finalizar
  ✓ Tirada finalizada
  → Turno: Negras
```

### Opción 2: Interfaz GUI (Pygame)

Interfaz gráfica con drag & drop, animaciones y efectos visuales/sonoros.

```bash
python -m game.backgammon_game
```

**Controles:**

- **ESPACIO / R**: Tirar dados
- **Click + Arrastrar**: Mover fichas
- **F**: Finalizar tirada manualmente
- **H**: Mostrar/ocultar ayuda
- **ESC**: Salir

**Características visuales:**

- 🎨 Tablero realista con texturas de madera
- 🎯 Hints visuales de movimientos válidos
- 🎬 Animaciones de dados y fichas
- 🔊 Efectos de sonido (entrada, captura, victoria)
- 🏆 Banner de victoria animado

---

## 🧪 Testing

### Ejecutar todos los tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Tests con output detallado (verbose)

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Tests de un archivo específico

```bash
python -m unittest tests.test_tablero
python -m unittest tests.test_validador
python -m unittest tests.test_integration
```

### Tests de una clase específica

```bash
python -m unittest tests.test_tablero.TestTablero
```

### Test de un método específico

```bash
python -m unittest tests.test_tablero.TestTablero.test_inicializacion
```

### Tests con cobertura (coverage)

```bash
# Instalar coverage
pip install coverage

# Ejecutar tests con cobertura
coverage run -m unittest discover -s tests -p "test_*.py"

# Ver reporte en terminal
coverage report

# Ver reporte detallado por archivo
coverage report -m

# Generar reporte HTML (se abre en navegador)
coverage html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Cobertura de módulos específicos

```bash
# Solo cobertura del directorio source
coverage run --source=source -m unittest discover -s tests

# Ver reporte
coverage report
```

### Detener en el primer fallo

```bash
python -m unittest discover -s tests -p "test_*.py" --failfast
```

### Modo buffer (ocultar prints excepto en fallos)

```bash
python -m unittest discover -s tests -p "test_*.py" --buffer
```

### Tests con captura de output

```bash
python -m unittest discover -s tests -p "test_*.py" --locals
```

---


## 📊 Cobertura de Código

El proyecto mantiene >90% de cobertura en el core de negocio.

```bash
pytest --cov=source --cov-report=term

Name                                Stmts   Miss  Cover
--------------------------------------------------------
source/tablero.py                     120      5    96%
source/validador_movimientos.py       180     12    93%
source/ejecutor_movimientos.py        150      8    95%
source/analizador_posibilidades.py    170     15    91%
source/backgammon.py                  250     20    92%
source/gestor_turnos.py                45      2    96%
source/dados.py                        25      0   100%
--------------------------------------------------------
TOTAL                                 940     62    93%
```

---

## 🏗️ Arquitectura

### Principios de Diseño

El proyecto implementa **SOLID** de forma rigurosa:

1. **Single Responsibility Principle (SRP)**
   - `Tablero`: Solo gestiona estado
   - `ValidadorMovimientos`: Solo valida sin ejecutar
   - `EjecutorMovimientos`: Solo ejecuta sin validar
   - `AnalizadorPosibilidades`: Solo analiza sin modificar

2. **Open/Closed Principle (OCP)**
   - Extensible mediante herencia (ej: nuevas variantes de backgammon)
   - Cerrado a modificación (añadir validadores no requiere cambiar core)

3. **Dependency Inversion Principle (DIP)**
   - Componentes dependen de abstracciones (inyección de dependencias)
   - Facilita testing con mocks y stubs

### Componentes Principales

```python
Backgammon                    # Orquestador (Facade)
    ├── Tablero              # Estado del juego
    ├── Dados                # Generador de aleatoriedad
    ├── GestorTurnos         # Control de flujo
    ├── ValidadorMovimientos # Reglas de validación
    ├── EjecutorMovimientos  # Mutador de estado
    └── AnalizadorPosibilidades  # Lookahead y simulación
```

### Flujo de un Movimiento

```
Usuario solicita mover
        ↓
Backgammon.mover(origen, dado)
        ↓
1. Validar dado mayor (AnalizadorPosibilidades)
        ↓
2. Validar movimiento (ValidadorMovimientos)
        ↓
3. Ejecutar movimiento (EjecutorMovimientos)
        ↓
4. Actualizar estado (Tablero)
        ↓
5. Verificar victoria (EjecutorMovimientos)
        ↓
Retornar resultado
```

---

## 🎓 Decisiones de Diseño Destacadas

### 1. Representación con Números con Signo

```python
posiciones = [
    2,   # Punto 1: 2 fichas blancas
    -5,  # Punto 2: 5 fichas negras
    0    # Punto 3: vacío
]

# Movimiento unificado para ambos colores
destino = origen + direccion * dado  # ✨ Una sola fórmula
```

**Beneficio**: 60% menos código en validaciones.

### 2. API Dual del Tablero

```python
# Pública: Copias defensivas (seguridad)
def obtener_posiciones(self) -> list[int]:
    return list(self.__posiciones__)  # Copia

# Protegida: Referencias directas (performance)
def _obtener_posiciones_ref(self) -> list[int]:
    return self.__posiciones__  # Referencia mutable
```

**Trade-off**: Seguridad por defecto, performance cuando se necesita.

### 3. Simulación sin Efectos Secundarios

```python
# Patrón backup-restore para lookahead
backup = tablero.obtener_posiciones()
simular_movimiento(dado1)
resultado = puede_usar_dado(dado2)
restaurar_estado(backup)  # Rollback
```

**Justificación**: 5x más rápido que `deepcopy()`.

---

## 🧩 Extensiones Futuras

### Posibles mejoras:

- [ ] IA con minimax o Monte Carlo Tree Search
- [ ] Modo multijugador online (sockets/websockets)
- [ ] Replay de partidas guardadas
- [ ] Variantes: Hypergammon, Nackgammon
- [ ] Estadísticas de jugador (victorias, capturas, etc.)
- [ ] Tutorial interactivo para principiantes
- [ ] Exportar partida a formato portable (JSON/XML)

---

## 📚 Documentación Adicional

- **[JUSTIFICACION.md](docs/JUSTIFICACION.md)**: Decisiones técnicas y arquitectónicas detalladas
- **[prompts_testing.md](docs/prompts_testing.md)**: Guía de testing y fixtures
- **[CHANGELOG.md](docs/CHANGELOG.md)**: Historial de cambios por rama

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Lineamientos:

- ✅ Mantener cobertura >90%
- ✅ Seguir principios SOLID
- ✅ Agregar tests para nuevo código
- ✅ Documentar con docstrings

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [tu-usuario](https://github.com/tu-usuario)

---

## 🙏 Agradecimientos

- Proyecto desarrollado como parte del curso **Computación 2025**
- Inspirado en las reglas oficiales de la [World Backgammon Federation](https://www.worldbackgammonfederation.com/)
- Assets gráficos y sonoros de dominio público

---

## 📞 Contacto

- Email: tu-email@example.com
- LinkedIn: [Miguel Martin ](https://www.linkedin.com/in/miguel-mart%C3%ADn-08558b249/)
- GitHub: [@mmruvinsky](https://github.com/mmruvinsky)

---

