# Justificación de Diseño - Backgammon

## 1. Resumen General

Este proyecto implementa un juego de Backgammon completo en Python, siguiendo los principios de diseño orientado a objetos y cumpliendo con los estándares SOLID. La arquitectura se diseñó para maximizar la separación de responsabilidades, facilitar el testing y permitir la extensibilidad del sistema.

### Objetivos principales:
- **Separación clara** entre lógica de negocio y presentación
- **Testabilidad**: Facilitar la creación de tests unitarios con alta cobertura
- **Extensibilidad**: Permitir múltiples interfaces (CLI, Pygame) sin modificar el core
- **Mantenibilidad**: Código limpio, documentado y fácil de entender
- **Robustez**: Manejo exhaustivo de errores mediante excepciones personalizadas

---

## 2. Arquitectura del Sistema

### 2.1. Estructura de Capas

```
┌─────────────────────────────────────┐
│   PRESENTACIÓN                      │
│  - cli/cli.py                       │
│  - pygame_ui/ (futuro)              │
└─────────────┬───────────────────────┘
              │ depende de
              ↓
┌─────────────────────────────────────┐
│   LÓGICA DE NEGOCIO                 │
│  - source/backgammon.py             │
│  - source/tablero.py                │
│  - source/dados.py                  │
│  - source/excepciones.py            │
└─────────────────────────────────────┘
```

**Decisión:** Arquitectura en capas con dependencias unidireccionales (UI → Core)

**Razón:** 
- El core **nunca** conoce la existencia de la UI
- Permite agregar nuevas interfaces sin modificar la lógica
- Facilita el testing (no necesita instanciar UI para probar lógica)

**Principio SOLID aplicado:** 
- **Dependency Inversion Principle (DIP)**: Las capas superiores dependen de abstracciones del core
- **Open/Closed Principle (OCP)**: Abierto para extensión (nuevas UIs) pero cerrado para modificación (core estable)

---

## 3. Decisiones de Diseño por Clase

### 3.1. Clase `Backgammon` (Coordinador/Fachada)

#### Responsabilidad
Orquestar el flujo completo del juego, coordinando los componentes (Tablero, Dados) y aplicando las reglas del Backgammon.

#### Atributos principales

__tablero__ (Tablero)

Composición: Backgammon "tiene un" Tablero
No usa herencia porque Backgammon NO ES un tipo de Tablero
Permite encapsular toda la lógica del estado del tablero

__turno__ (int)

Valores: 1 para blancas, -1 para negras
Ventaja: Permite cálculos directos como destino = origen + jugador * dado
Alternativa descartada: usar strings (menos eficiente, más comparaciones)

__dados__ (Dados)

Composición: encapsula la generación aleatoria
Facilita testing: se puede reemplazar con dados determinísticos (mock)
Separa responsabilidades (SRP)

__movimientos_pendientes__ (list[int])

Almacena los valores de dados disponibles en la tirada actual
Permite consumo selectivo (usar un dado específico)
Necesario para validar regla "debe usar dado mayor"
Ejemplo: [3, 5] para tirada normal, [6, 6, 6, 6] para dobles

#### Métodos clave y justificación

**Métodos públicos (API):**
```python
def mover(self, origen: int, valor_dado: int) -> str
```
- **Interfaz simple**: El usuario solo necesita proporcionar origen y dado
- **Retorna descripción textual**: Útil para feedback en cualquier UI
- **Maneja TODOS los casos**: entrada desde barra, capturas, bear-off, victoria
- **Razón**: Método fachada que simplifica la complejidad interna

**Métodos protegidos (helpers internos):**
```python
def _puede_usar_dado(self, valor_dado: int) -> bool
def _simular_mejor_movimiento(self, valor_dado: int) -> bool
def _puede_hacer_bear_off(self, origen_idx: int, valor_dado: int) -> bool
```
- **Prefijo `_`**: Convención Python para métodos internos (no son parte de la API pública)
- **Razón de existencia**: Implementan la regla compleja "debe usar dado mayor si solo uno es posible"
- **Simulación**: Necesario para evaluar si después de usar un dado, el otro es usable

#### Decisión: ¿Por qué no usar herencia?

**Alternativa descartada:** 
```python
class Backgammon(Tablero):  # ❌ NO
```

**Razón del descarte:**
- Backgammon NO ES un tipo de Tablero (violación de "is-a")
- Backgammon USA un Tablero ("has-a" → composición)
- La herencia expondría métodos internos del Tablero innecesariamente

**Principio SOLID:** 
- **Liskov Substitution Principle (LSP)**: Si usáramos herencia incorrectamente, no podríamos sustituir Tablero por Backgammon sin romper el código
- **Composition over Inheritance**: Preferimos composición cuando la relación es "tiene un" en lugar de "es un"

---

### 3.2. Clase `Tablero`

#### Responsabilidad
Gestionar el estado del tablero: posiciones de fichas, barra y fichas fuera (bear-off).

#### Atributos

```python
__posiciones__: list[int]      # 24 posiciones
__barra__: dict[str, int]      # {'blancas': n, 'negras': n}
__fichas_fuera__: dict[str, int]
```

**Decisión: Representación con enteros con signo**

**Alternativa considerada:**
```python
# Opción A (descartada): Listas separadas
__fichas_blancas__: list[int]
__fichas_negras__: list[int]
```

**Razón del descarte:**
- Duplicación de lógica (dos listas a mantener sincronizadas)
- Más complejo verificar colisiones

**Opción elegida:**
```python
# Opción B (elegida): Lista única con signo
__posiciones__: list[int]  # positivo=blancas, negativo=negras
```

**Ventajas:**
- **Operaciones matemáticas directas**: `posiciones[idx] += jugador`
- **Detección de colisiones simple**: `if posiciones[idx] * jugador < 0`
- **Menos código**: Una sola estructura de datos
- **Eficiencia**: Menos espacio en memoria

#### Métodos públicos vs protegidos

**Métodos públicos (copia defensiva):**
```python
def obtener_posiciones(self) -> list[int]:
    return list(self.__posiciones__)  # Copia
```

**Razón**: Evita que código externo modifique directamente el estado interno (encapsulación).

**Métodos protegidos (referencias directas):**
```python
def _obtener_posiciones_ref(self) -> list[int]:
    return self.__posiciones__  # Referencia directa
```

**Razón**: 
- Solo para uso interno de `Backgammon`
- Necesario para simulaciones (evitar copias costosas)
- Prefijo `_` documenta que es interno

**Principio SOLID:**
- **Encapsulation**: El estado interno está protegido
- **Information Hiding**: Solo se expone lo necesario

---

### 3.3. Clase `Dados`

#### Responsabilidad
Generar valores aleatorios para las tiradas de dados.

#### Diseño minimalista

```python
class Dados:
    def __init__(self):
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)

    def tirar(self) -> tuple[int, int]:
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)
        return (self.__dado1__, self.__dado2__)
```

#### Decisión: Clase separada vs función

**Alternativa descartada:**
```python
# En backgammon.py
def tirar_dados():
    return (random.randint(1, 6), random.randint(1, 6))
```

**Razón del descarte:**
- Dificulta el testing (no se puede mockear fácilmente)
- Viola Single Responsibility (Backgammon tendría más responsabilidades)

**Opción elegida:** Clase independiente

**Ventajas:**
- **Testeable**: Se puede crear una clase `DadosDeterministicos` para tests
- **Extensible**: Podría agregarse historial de tiradas, semillas para reproducibilidad
- **Single Responsibility**: Una clase, una responsabilidad

**Principio SOLID:**
- **Single Responsibility Principle (SRP)**: Solo se encarga de generar valores aleatorios
- **Dependency Injection**: Backgammon recibe Dados como dependencia (facilita testing)

---

### 3.4. Sistema de Excepciones

#### Jerarquía diseñada

```python
BackgammonError (base)
    ├── MovimientoInvalidoError
    │   ├── OrigenInvalidoError
    │   ├── DestinoBloquedoError
    │   ├── DadoNoDisponibleError
    │   └── BearOffInvalidoError
    └── FichasEnBarraError
```

#### Justificación de cada excepción

| Excepción | Cuándo se lanza | Por qué existe |
|-----------|-----------------|----------------|
| `BackgammonError` | Nunca (clase base) | Permite `except BackgammonError` para capturar cualquier error del juego |
| `MovimientoInvalidoError` | Raramente directa | Agrupa todos los errores de movimiento |
| `OrigenInvalidoError` | Origen sin fichas propias | Feedback específico: "No tienes fichas ahí" |
| `DestinoBloquedoError` | Destino con 2+ fichas rivales | Feedback: "Esa posición está bloqueada" |
| `DadoNoDisponibleError` | Dado ya usado o debe usar mayor | Feedback: "Ese dado no está disponible" |
| `BearOffInvalidoError` | Bear-off sin fichas en home | Feedback: "No puedes sacar fichas aún" |

#### Decisión: Granularidad de excepciones

**Alternativa descartada:**
```python
# Una sola excepción genérica
raise BackgammonError("Movimiento inválido")
```

**Razón del descarte:**
- No permite manejo diferenciado por tipo de error
- Feedback genérico al usuario (mala UX)
- Dificulta el testing (no se puede verificar tipo específico)

**Opción elegida:** Excepciones granulares

**Ventajas:**
- **Feedback preciso**: Cada excepción tiene mensaje específico
- **Testing robusto**: Se puede verificar el tipo exacto de error esperado
- **Manejo diferenciado**: La UI puede reaccionar distinto según el error

**Ejemplo en CLI:**
```python
try:
    self.juego.mover(origen, dado)
except OrigenInvalidoError:
    print("❌ No tienes fichas en esa posición")
except DestinoBloquedoError:
    print("❌ El destino está bloqueado")
except DadoNoDisponibleError as e:
    print(f"❌ {e}")  # Puede ser "debe usar dado mayor"
```

**Principio SOLID:**
- **Open/Closed**: Nuevas excepciones pueden agregarse sin modificar las existentes
- **Liskov Substitution**: Cualquier `MovimientoInvalidoError` puede tratarse como tal

---

## 4. Decisiones de Implementación Específicas

### 4.1. Representación del Turno (int vs str)

**Opción A (descartada):** `self.__turno__ = "blancas"`

**Opción B (elegida):** `self.__turno__ = 1  # o -1`

**Justificación:**
```python
# Con int (elegido):
destino_idx = origen_idx + jugador * valor_dado  # ✅ Directo

# Con string (descartado):
if jugador == "blancas":
    destino_idx = origen_idx + valor_dado
else:
    destino_idx = origen_idx - valor_dado  # ❌ Duplicación
```

**Ventajas del int:**
- Operaciones matemáticas directas
- Menos comparaciones condicionales
- Más eficiente (comparar ints vs strings)

**Trade-off aceptado:** Necesita conversión para mostrar al usuario
```python
def obtener_turno(self) -> str:
    return "blancas" if self.__turno__ == 1 else "negras"
```

---

### 4.2. Convención de Nombres de Atributos

**Requisito del proyecto:** Todos los atributos deben usar `__nombre__`

**Justificación:**
- Cumplimiento de requisitos del proyecto
- Indica claramente que son atributos internos
- Python no tiene "private" real, esto es una convención fuerte

---

### 4.4. Simulación de Movimientos para Validación

**Problema:** Regla "debe usar dado mayor si solo uno es usable"

**Requiere:** Simular un movimiento para ver si después es posible usar el otro dado

**Implementación:**
```python
def _simular_mejor_movimiento(self, valor_dado: int) -> bool:
    pos = self.__tablero__._obtener_posiciones_ref()  # Referencia directa
    # ... modifica pos ...
    return True/False

def _puede_usar_dado_tras_simular(self, primer_dado, segundo_dado):
    pos_backup = self.__tablero__.obtener_posiciones()  # Copia
    barra_backup = self.__tablero__.obtener_barra()
    
    try:
        if self._simular_mejor_movimiento(primer_dado):
            return self._puede_usar_dado(segundo_dado)
    finally:
        # Restaurar estado original
        pos_ref = self.__tablero__._obtener_posiciones_ref()
        pos_ref[:] = pos_backup
        # ...
```

**Decisión clave:** Simular modificando el estado real y luego restaurar

**Alternativas consideradas:**

**Opción A (descartada):** Deep copy completo
```python
tablero_temp = copy.deepcopy(self.__tablero__)  # ❌ Costoso
```
**Razón del descarte:** Overhead significativo para cada validación

**Opción B (elegida):** Backup ligero + modificación in-place + restauración

**Ventajas:**
- Reutiliza la lógica existente de movimiento
- No duplica código de validación
- Relativamente eficiente

**Trade-off aceptado:** Complejidad temporal (modifica y restaura)

**Principio aplicado:** DRY (Don't Repeat Yourself) - no duplicamos la lógica de movimiento

---

## 5. Cumplimiento de Principios SOLID

### 5.1. Single Responsibility Principle (SRP)

**Cada clase tiene UNA responsabilidad:**

| Clase | Responsabilidad única |
|-------|----------------------|
| `Backgammon` | Coordinar flujo del juego y aplicar reglas |
| `Tablero` | Gestionar estado de posiciones |
| `Dados` | Generar valores aleatorios |
| `BackgammonCLI` | Interacción con usuario por consola |

---

### 5.2. Open/Closed Principle (OCP)

**Abierto para extensión, cerrado para modificación:**

**Ejemplo 1:** Nuevas interfaces
```python
# Sin modificar Backgammon:
class BackgammonCLI:
    def __init__(self):
        self.juego = Backgammon()  # Usa el core sin modificarlo

class BackgammonPygame:  
    def __init__(self):
        self.juego = Backgammon()  # Mismo core, distinta UI
```

**Ejemplo 2:** Nuevas excepciones
```python
# Agregar nueva excepción sin modificar jerarquía existente:
class TiempoExcedidoError(BackgammonError):  # Futura (para modo reloj)
    pass
```

---

### 5.3. Liskov Substitution Principle (LSP)

**Subtipos deben ser sustituibles por sus tipos base:**

```python
# Todas las excepciones pueden tratarse como BackgammonError:
try:
    juego.mover(origen, dado)
except BackgammonError as e:  # Captura cualquier subclase
    print(f"Error: {e}")
```

**No se viola LSP** porque no usamos herencia donde no corresponde (Backgammon no hereda de Tablero).

---

### 5.4. Interface Segregation Principle (ISP)

**Los clientes no deben depender de interfaces que no usan:**

**Aplicación:** Métodos públicos vs protegidos en `Tablero`

```python
# CLI solo usa métodos públicos (API limpia):
posiciones = self.juego.obtener_posiciones()  # ✅ Copia segura

# Backgammon interno usa métodos protegidos (eficiencia):
pos_ref = self.__tablero__._obtener_posiciones_ref()  # ⚠️ Solo interno
```

**Beneficio:** La UI no puede corromper el estado interno accidentalmente.

---

### 5.5. Dependency Inversion Principle (DIP)

**Depender de abstracciones, no de concreciones:**

**Aplicación:** Composición en Backgammon

```python
class Backgammon:
    def __init__(self):
        self.__tablero__ = Tablero()  # Dependencia de clase concreta
        self.__dados__ = Dados()
```

**Nota:** En este proyecto no usamos interfaces explícitas (Python no las tiene nativamente), pero la estructura permite extensión:

```python
# Futuro: Inyección de dependencias para testing
class Backgammon:
    def __init__(self, tablero=None, dados=None):
        self.__tablero__ = tablero or Tablero()
        self.__dados__ = dados or Dados()

# Testing:
dados_mock = DadosDeterministicos([6, 6])  # Siempre tira 6-6
juego = Backgammon(dados=dados_mock)
```

---

## 6. Estrategia de Testing

### 6.1. Cobertura Actual: 98%

**Distribución:**
- `backgammon.py`: 98%
- `tablero.py`: 100%
- `dados.py`: 100%
- `excepciones.py`: 100%

**Líneas no cubiertas en backgammon.py:**
- Principalmente casos edge en helpers de simulación
- No afectan funcionalidad crítica

### 6.2. Categorías de Tests

#### Tests de Estado Inicial
```python
def test_inicializacion_tablero()
def test_posiciones_iniciales_correctas()
def test_turno_inicial_blancas()
```

#### Tests de Movimientos Básicos
```python
def test_movimiento_simple_valido()
def test_movimiento_invalido_sin_fichas()
def test_movimiento_destino_bloqueado()
```

#### Tests de Reglas Especiales
```python
def test_entrada_desde_barra_obligatoria()
def test_captura_ficha_rival()
def test_bear_off_valido()
def test_bear_off_sin_home_completo()
def test_overshoot_bear_off()
```

#### Tests de Regla del Dado Mayor
```python
def test_debe_usar_dado_mayor()
def test_puede_usar_ambos_dados()
```

#### Tests de Excepciones
```python
def test_origen_invalido_lanza_excepcion()
def test_destino_bloquedo_lanza_excepcion()
# ... para cada excepción
```

#### Tests de Victoria
```python
def test_victoria_blancas()
def test_victoria_negras()
```

### 6.3. Estrategia de Testing: AAA Pattern

**Arrange-Act-Assert:**

```python
def test_movimiento_simple():
    # Arrange: Preparar estado
    juego = Backgammon()
    juego._Backgammon__turno__ = 1
    juego._Backgammon__movimientos_pendientes__ = [3]
    
    # Act: Ejecutar acción
    resultado = juego.mover(1, 3)
    
    # Assert: Verificar resultado
    self.assertEqual(resultado, "movió")
    posiciones = juego.obtener_posiciones()
    self.assertEqual(posiciones[0], 1)  # Queda 1 ficha
    self.assertEqual(posiciones[3], 3)  # Llegan 1 ficha
```
---

## 8. Decisiones de Rendimiento

### 8.1. Referencias vs Copias

**Trade-off:** Seguridad vs Eficiencia

**API Pública (seguridad prioritaria):**
```python
def obtener_posiciones(self) -> list[int]:
    return list(self.__posiciones__)  # Copia O(n)
```

**API Interna (eficiencia prioritaria):**
```python
def _obtener_posiciones_ref(self) -> list[int]:
    return self.__posiciones__  # Referencia O(1)
```

**Justificación:**
- La UI puede llamar `obtener_posiciones()` muchas veces (redibuja)
- Pero **nunca debe modificar** el estado
- El core interno necesita eficiencia en simulaciones

---

### 8.2. Validaciones Tempranas

**Principio:** Fallar rápido evita trabajo innecesario

```python
def mover(self, origen: int, valor_dado: int):
    # ✅ Validaciones baratas primero:
    if valor_dado not in self.__movimientos_pendientes__:
        raise DadoNoDisponibleError(...)  # O(n) pequeño
    
    if not self._origen_valido(...):
        raise OrigenInvalidoError(...)    # O(1)
    
    # ✅ Validaciones costosas al final:
    if self.debe_usar_dado_mayor():       # O(n²) en peor caso
        # ...
```

**Razón:** 99% de errores se detectan con validaciones baratas

---




