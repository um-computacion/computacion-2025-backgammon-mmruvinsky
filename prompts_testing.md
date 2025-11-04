# PROMPTS DE TESTING - BACKGAMMON PY

Documento de consultas realizadas durante el desarrollo del proyecto sobre testing y validación.

---

## 1. CONFIGURACIÓN INICIAL DE PYTEST

### Prompt
```
Estoy desarrollando un juego de Backgammon en Python con arquitectura modular (Tablero, ValidadorMovimientos, EjecutorMovimientos, etc.). 

Necesito configurar pytest desde cero para el proyecto. ¿Cómo lo configuro correctamente? ¿Qué estructura de carpetas debo usar? ¿Necesito archivos de configuración especiales?

Estructura actual:
project/
├── source/
│   ├── backgammon.py
│   ├── tablero.py
│   ├── validador_movimientos.py
│   └── ...
├── cli/
│   └── cli.py
└── game/
    └── backgammon_game.py
```

### Modelo IA
**Claude Sonnet 4.5**

### Respuesta (Resumida)
```python
# Estructura recomendada:
project/
├── source/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_tablero.py
│   ├── test_validador.py
│   ├── test_ejecutor.py
│   ├── test_backgammon.py
│   └── test_integration.py
├── pytest.ini
└── requirements-dev.txt

# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers

# conftest.py - Fixtures compartidas
import pytest
from source.backgammon import Backgammon
from source.tablero import Tablero

@pytest.fixture
def juego_limpio():
    """Retorna instancia nueva de Backgammon"""
    return Backgammon()

@pytest.fixture
def tablero_vacio():
    """Tablero sin fichas para tests específicos"""
    tablero = Tablero()
    tablero._Tablero__posiciones = [0] * 24
    return tablero
```

**Comando instalación:**
```bash
pip install pytest pytest-cov pytest-mock
```

**Comando ejecución:**
```bash
pytest                    # Todos los tests
pytest -v                 # Verbose
pytest --cov=source      # Con coverage
pytest tests/test_tablero.py  # Test específico
```

---

## 2. TESTING DE VALIDACIONES SIN EJECUTAR MOVIMIENTOS

### Prompt
```
Tengo una clase ValidadorMovimientos que valida movimientos sin ejecutarlos (retorna tuple[bool, str]). 

¿Cómo escribo tests efectivos para validar TODAS las reglas del backgammon sin ejecutar movimientos reales? 

Reglas a testear:
- Origen debe tener fichas propias
- Destino no puede tener 2+ fichas rivales
- Bear-off solo si todas en home
- Entrada desde barra tiene prioridad
- Dado mayor obligatorio si solo se puede usar uno
```

### Modelo IA
**Claude Sonnet 4.5**

### Respuesta (Resumida)
```python
# tests/test_validador.py
import pytest
from source.validador_movimientos import ValidadorMovimientos
from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos

class TestValidadorMovimientos:
    """Suite de tests para validación pura (sin side effects)"""
    
    @pytest.fixture
    def setup(self):
        """Setup común para todos los tests"""
        tablero = Tablero()
        gestor = GestorTurnos()
        validador = ValidadorMovimientos(tablero, gestor)
        return tablero, gestor, validador
    
    def test_origen_sin_fichas_propias(self, setup):
        """Validar que falla si origen no tiene fichas propias"""
        tablero, gestor, validador = setup
        
        # Punto 5 tiene fichas negras, turno blancas
        tablero._Tablero__posiciones[4] = -2
        
        valido, msg = validador.validar_movimiento(4, 3)
        
        assert not valido
        assert "origen" in msg.lower()
    
    def test_destino_bloqueado(self, setup):
        """Validar que falla si destino tiene 2+ fichas rivales"""
        tablero, gestor, validador = setup
        
        # Blancas en punto 1, negras bloquean punto 4
        tablero._Tablero__posiciones[0] = 2   # origen (blancas)
        tablero._Tablero__posiciones[3] = -2  # destino bloqueado
        
        valido, msg = validador.validar_movimiento(0, 3)
        
        assert not valido
        assert "bloqueada" in msg.lower()
    
    def test_bear_off_sin_home_completo(self, setup):
        """No puede sacar fichas si no están todas en home"""
        tablero, gestor, validador = setup
        
        # Blanca en punto 20, otra en punto 10 (fuera de home)
        tablero._Tablero__posiciones = [0] * 24
        tablero._Tablero__posiciones[19] = 1  # home
        tablero._Tablero__posiciones[9] = 1   # NO home
        
        valido, msg = validador.validar_movimiento(19, 5)
        
        assert not valido
        assert "home" in msg.lower()
    
    def test_movimiento_valido_basico(self, setup):
        """Caso positivo: movimiento simple válido"""
        tablero, gestor, validador = setup
        
        tablero._Tablero__posiciones[0] = 2  # blancas en punto 1
        
        valido, msg = validador.validar_movimiento(0, 3)
        
        assert valido
        assert msg == ""
    
    @pytest.mark.parametrize("origen,dado,esperado", [
        (0, 3, True),   # Movimiento normal
        (0, 25, False), # Fuera de rango
        (23, 1, True),  # Extremo superior
    ])
    def test_movimientos_parametrizados(self, setup, origen, dado, esperado):
        """Tests parametrizados para múltiples casos"""
        tablero, gestor, validador = setup
        tablero._Tablero__posiciones[origen] = 1
        
        valido, _ = validador.validar_movimiento(origen, dado)
        
        assert valido == esperado
```

**Principio clave:** Los tests de validación NO deben modificar estado. Verificamos solo el retorno `(bool, str)`.

---

## 3. TESTING DE EJECUCIÓN CON VERIFICACIÓN DE ESTADO

### Prompt
```
Ahora necesito testear la clase EjecutorMovimientos que SÍ modifica el estado del tablero. 

¿Cómo verifico que:
1. Las fichas se mueven correctamente
2. Se capturan blots rivales
3. Se actualiza la barra
4. Bear-off incrementa fichas_fuera
5. Se detecta victoria (15 fichas fuera)

¿Debo restaurar estado entre tests? ¿Usar fixtures?
```

### Modelo IA
**Claude Sonnet 4.5**

### Respuesta (Resumida)
```python
# tests/test_ejecutor.py
import pytest
from source.ejecutor_movimientos import EjecutorMovimientos
from source.tablero import Tablero
from source.gestor_turnos import GestorTurnos

class TestEjecutorMovimientos:
    """Tests para ejecución de movimientos (con side effects)"""
    
    @pytest.fixture
    def ejecutor_setup(self):
        """Setup NUEVO para cada test (aislamiento)"""
        tablero = Tablero()
        gestor = GestorTurnos()
        ejecutor = EjecutorMovimientos(tablero, gestor)
        return tablero, gestor, ejecutor
    
    def test_movimiento_simple(self, ejecutor_setup):
        """Verificar que ficha se mueve correctamente"""
        tablero, gestor, ejecutor = ejecutor_setup
        
        # Setup: 2 blancas en punto 1
        pos = tablero._obtener_posiciones_ref()
        pos[0] = 2
        pos[3] = 0  # destino vacío
        
        # Ejecutar: mover de punto 1 con dado 3
        resultado = ejecutor.ejecutar_movimiento(0, 3)
        
        # Verificar estado final
        assert pos[0] == 1   # origen: quedó 1 ficha
        assert pos[3] == 1   # destino: llegó 1 ficha
        assert resultado == "movió"
    
    def test_captura_blot_rival(self, ejecutor_setup):
        """Verificar captura de ficha rival y envío a barra"""
        tablero, gestor, ejecutor = ejecutor_setup
        
        pos = tablero._obtener_posiciones_ref()
        barra = tablero._obtener_barra_ref()
        
        # Setup: blanca en 1, negra sola (blot) en 4
        pos[0] = 1   # blanca
        pos[3] = -1  # blot negro
        
        # Ejecutar
        resultado = ejecutor.ejecutar_movimiento(0, 3)
        
        # Verificar
        assert pos[0] == 0           # origen vacío
        assert pos[3] == 1           # destino con blanca
        assert barra["negras"] == 1  # negro capturado
        assert resultado == "movió y comió"
    
    def test_bear_off(self, ejecutor_setup):
        """Verificar sacar ficha del tablero"""
        tablero, gestor, ejecutor = ejecutor_setup
        
        pos = tablero._obtener_posiciones_ref()
        fuera = tablero._obtener_fichas_fuera_ref()
        
        # Setup: blanca en punto 20 (home)
        pos[:] = [0] * 24
        pos[19] = 1
        
        # Ejecutar: sacar con dado 5 (overshoot)
        resultado = ejecutor.ejecutar_movimiento(19, 5)
        
        # Verificar
        assert pos[19] == 0
        assert fuera["blancas"] == 1
        assert resultado == "sacó ficha"
    
    def test_victoria_15_fichas_fuera(self, ejecutor_setup):
        """Verificar detección de victoria"""
        tablero, gestor, ejecutor = ejecutor_setup
        
        pos = tablero._obtener_posiciones_ref()
        fuera = tablero._obtener_fichas_fuera_ref()
        
        # Setup: 14 fichas ya fuera, 1 última en punto 24
        pos[:] = [0] * 24
        pos[23] = 1
        fuera["blancas"] = 14
        
        # Ejecutar: sacar última ficha
        resultado = ejecutor.ejecutar_movimiento(23, 1)
        
        # Verificar
        assert fuera["blancas"] == 15
        assert "ganaron" in resultado.lower()
        assert "blancas" in resultado.lower()
    
    def test_entrada_desde_barra(self, ejecutor_setup):
        """Verificar entrada correcta desde barra"""
        tablero, gestor, ejecutor = ejecutor_setup
        
        pos = tablero._obtener_posiciones_ref()
        barra = tablero._obtener_barra_ref()
        
        # Setup: blanca en barra
        barra["blancas"] = 1
        pos[2] = 0  # punto 3 vacío
        
        # Ejecutar: entrar con dado 3
        resultado = ejecutor.ejecutar_entrada_barra(3)
        
        # Verificar
        assert barra["blancas"] == 0
        assert pos[2] == 1
        assert resultado == "entró"
```

**Principio clave:** Cada test tiene su propio fixture (aislamiento). Verificamos estado ANTES y DESPUÉS.

---

## 4. TESTING DE INTEGRACIÓN (FLUJO COMPLETO)

### Prompt
```
Necesito tests de integración que verifiquen el flujo completo:
1. Tirar dados
2. Validar movimiento
3. Ejecutar movimiento
4. Actualizar estado
5. Cambiar turno

¿Cómo estructuro estos tests? ¿Debo mockear los dados para reproducibilidad?
```

### Modelo IA
**Claude Sonnet 4.5**

### Respuesta (Resumida)
```python
# tests/test_integration.py
import pytest
from source.backgammon import Backgammon
from source.excepciones import *

class TestIntegracionBackgammon:
    """Tests de flujo completo end-to-end"""
    
    @pytest.fixture
    def juego(self):
        """Juego nuevo para cada test"""
        return Backgammon()
    
    def test_flujo_completo_tirar_y_mover(self, juego):
        """Test del flujo: tirar → mover → cambiar turno"""
        
        # 1. Tirar dados
        d1, d2 = juego.tirar_dados()
        
        assert d1 in range(1, 7)
        assert d2 in range(1, 7)
        assert len(juego.obtener_movimientos_pendientes()) in [2, 4]
        
        # 2. Verificar turno inicial
        assert juego.obtener_turno() == "blancas"
        
        # 3. Intentar movimiento válido (punto 1 siempre tiene fichas)
        try:
            resultado = juego.mover(1, d1)
            assert resultado in ["movió", "movió y comió", "sacó ficha"]
        except Exception as e:
            # Puede fallar si no hay movimiento posible (aceptable)
            assert isinstance(e, MovimientoInvalidoError)
        
        # 4. Finalizar tirada
        juego.finalizar_tirada()
        
        # 5. Verificar cambio de turno
        assert juego.obtener_turno() == "negras"
    
    def test_dados_dobles_cuatro_movimientos(self, juego):
        """Verificar que dobles generan 4 movimientos"""
        
        # Mock de dados (retornar dobles)
        juego._Backgammon__dados.tirar = lambda: (3, 3)
        
        d1, d2 = juego.tirar_dados()
        
        assert d1 == 3
        assert d2 == 3
        assert juego.obtener_movimientos_pendientes() == [3, 3, 3, 3]
    
    def test_regla_dado_mayor(self, juego):
        """Verificar que fuerza usar dado mayor si solo puede usar uno"""
        
        # Setup complicado: posición donde solo dado 5 es válido
        pos = juego._Backgammon__tablero__._obtener_posiciones_ref()
        pos[:] = [0] * 24
        pos[0] = 1    # blanca en punto 1
        pos[1:6] = [-2] * 5  # negras bloquean puntos 2-6
        pos[5] = 0    # punto 6 libre
        
        # Mock: dados 2 y 5
        juego._Backgammon__movimientos_pendientes__ = [2, 5]
        
        # Debe FORZAR uso del 5
        with pytest.raises(DadoNoDisponibleError):
            juego.mover(1, 2)  # Intenta usar el menor
        
        # El 5 sí debe funcionar
        juego.mover(1, 5)  # ✅
    
    def test_entrada_obligatoria_desde_barra(self, juego):
        """Si hay fichas en barra, debe entrar primero"""
        
        barra = juego._Backgammon__tablero__._obtener_barra_ref()
        barra["blancas"] = 1
        
        juego._Backgammon__movimientos_pendientes__ = [3]
        
        # Intentar mover desde tablero (debe fallar)
        # La lógica del core debe detectar fichas en barra
        
        # Mover desde barra (entrada = origen 1)
        resultado = juego.mover(1, 3)
        assert resultado == "entró"
        assert barra["blancas"] == 0
    
    @pytest.mark.slow
    def test_partida_completa_simulada(self, juego):
        """Simular partida completa hasta victoria"""
        
        # Mock: dados favorables para blancas
        juego._Backgammon__dados.tirar = lambda: (6, 6)
        
        turnos = 0
        max_turnos = 100  # Límite de seguridad
        
        while turnos < max_turnos:
            juego.tirar_dados()
            
            # Intentar mover todas las fichas posibles
            while juego.movimientos_disponibles():
                movimientos = juego.obtener_movimientos_posibles()
                
                if not movimientos:
                    break
                
                # Tomar primer movimiento disponible
                origen = list(movimientos.keys())[0]
                destino, dado = movimientos[origen][0]
                
                try:
                    resultado = juego.mover(origen, dado)
                    
                    if "ganaron" in resultado:
                        print(f"Victoria en turno {turnos}")
                        return  # ✅ Test exitoso
                        
                except Exception:
                    break
            
            juego.finalizar_tirada()
            turnos += 1
        
        pytest.fail("No hubo victoria en 100 turnos")
```

**Principio clave:** Tests de integración verifican el **contrato** entre componentes, no detalles internos.

---

## 5. MOCKING Y FIXTURES AVANZADAS

### Prompt
```
¿Cómo creo fixtures más avanzadas para tests complejos?

Por ejemplo:
- Tablero en situación específica (casi victoria)
- Dados determinísticos para reproducibilidad
- Estados intermedios del juego
```

### Modelo IA
**Claude Sonnet 4.5**

### Respuesta (Resumida)
```python
# tests/conftest.py
import pytest
from source.backgammon import Backgammon
from source.tablero import Tablero

@pytest.fixture
def juego_limpio():
    """Juego nuevo con estado inicial estándar"""
    return Backgammon()

@pytest.fixture
def juego_casi_victoria_blancas():
    """14 fichas blancas fuera, 1 restante en punto 24"""
    juego = Backgammon()
    
    pos = juego._Backgammon__tablero__._obtener_posiciones_ref()
    fuera = juego._Backgammon__tablero__._obtener_fichas_fuera_ref()
    
    pos[:] = [0] * 24
    pos[23] = 1  # Última ficha blanca
    fuera["blancas"] = 14
    
    return juego

@pytest.fixture
def juego_con_barra():
    """Blancas con 2 fichas en barra"""
    juego = Backgammon()
    barra = juego._Backgammon__tablero__._obtener_barra_ref()
    barra["blancas"] = 2
    return juego

@pytest.fixture
def dados_mock():
    """Clase mock para dados determinísticos"""
    class DadosMock:
        def __init__(self, secuencia):
            self.secuencia = secuencia
            self.index = 0
        
        def tirar(self):
            resultado = self.secuencia[self.index % len(self.secuencia)]
            self.index += 1
            return resultado
    
    return DadosMock

# Uso de fixtures
def test_con_fixture_compleja(juego_casi_victoria_blancas, dados_mock):
    """Test usando fixture de estado avanzado"""
    juego = juego_casi_victoria_blancas
    
    # Inyectar dados determinísticos
    juego._Backgammon__dados = dados_mock([(1, 1)])
    
    d1, d2 = juego.tirar_dados()
    resultado = juego.mover(24, 1)
    
    assert "ganaron" in resultado
    assert "blancas" in resultado.lower()
```

---

## 6. COVERAGE Y REPORTE DE CALIDAD

### Prompt
```
¿Cómo mido la cobertura de mis tests? ¿Qué porcentaje es aceptable? ¿Cómo genero reportes?
```

### Modelo IA
**Claude Sonnet 4.5**

### Respuesta (Resumida)
```bash
# Instalar herramientas
pip install pytest-cov coverage

# Ejecutar tests con coverage
pytest --cov=source --cov-report=html --cov-report=term

# Genera reporte en htmlcov/index.html

# Output esperado:
# Name                              Stmts   Miss  Cover
# -----------------------------------------------------
# source/tablero.py                   120      5    96%
# source/validador_movimientos.py     180     12    93%
# source/ejecutor_movimientos.py      150      8    95%
# source/backgammon.py                250     20    92%
# -----------------------------------------------------
# TOTAL                               700     45    94%
```

**Estándares recomendados:**
- **>90%**: Excelente (core de negocio)
- **>80%**: Aceptable (código general)
- **>70%**: Mínimo aceptable (UI/CLI)

**Áreas que NO necesitan 100% coverage:**
- Código de UI/rendering
- Manejo de excepciones raras
- Código de debugging

---

## 7. TESTS PARAMETRIZADOS PARA REGLAS COMPLEJAS

### Prompt
```
Tengo que testear la regla de bear-off que tiene múltiples casos:
1. Distancia exacta → válido
2. Overshoot SIN fichas más adelantadas → válido
3. Overshoot CON fichas más adelantadas → inválido
4. No todas en home → inválido

¿Cómo evito duplicar código de test para cada caso?
```

### Modelo IA
**Claude Sonnet 4.5**

### Respuesta (Resumida)
```python
# tests/test_bear_off.py
import pytest
from source.backgammon import Backgammon

class TestBearOffReglas:
    """Tests parametrizados para regla compleja de bear-off"""
    
    @pytest.mark.parametrize("posicion,dado,otras_fichas,esperado", [
        # (punto_origen, dado, [puntos_con_fichas], debe_ser_valido)
        (24, 1, [], True),           # Distancia exacta
        (23, 3, [], True),           # Overshoot sin otras
        (22, 6, [23, 24], False),    # Overshoot con más adelantadas
        (20, 5, [15], False),        # Fichas fuera de home
        (24, 1, [10], False),        # Ficha fuera de home
    ])
    def test_bear_off_casos(self, posicion, dado, otras_fichas, esperado):
        """Test parametrizado de todos los casos de bear-off"""
        juego = Backgammon()
        
        # Setup: solo fichas en home
        pos = juego._Backgammon__tablero__._obtener_posiciones_ref()
        pos[:] = [0] * 24
        pos[posicion - 1] = 1  # Ficha a testear
        
        for otra in otras_fichas:
            pos[otra - 1] = 1
        
        # Mock dados
        juego._Backgammon__movimientos_pendientes__ = [dado]
        
        # Ejecutar y verificar
        if esperado:
            resultado = juego.mover(posicion, dado)
            assert "sacó" in resultado or "ganaron" in resultado
        else:
            with pytest.raises(Exception):  # Alguna excepción
                juego.mover(posicion, dado)
```

**Beneficio:** 5 casos testeados con 1 función (5 líneas en lugar de 50+).

