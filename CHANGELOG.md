# Changelog
Todas las modificaciones notables de este proyecto se documentarán en este archivo.  
Formato basado en [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

---

### Commits (completo, orden cronológico inverso)

#### 6fd25f6 — Merge pull request #14 from um-computacion/validadores_movimientos_complejos
**Autor / Fecha:** (agrupado en commits del 22 Sep 2025).  
**Mensaje:** Merge pull request #14.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:0]{index=0}

#### c0a10ea — agregamos tests  
**Autor / Fecha:** mmruvinsky — 22 Sep 2025.  
**Mensaje:** agregamos tests.  
**Files changed / diffstat (resumen):** `9 files changed`, **+619 / -73** líneas (tests añadidos y ajustes en `source/backgammon.py`). Ver archivos y diff en el commit. :contentReference[oaicite:1]{index=1}

#### 1068c12 — Refactorización de tests debido a implementación de helpers internos en clase Backgammon  
**Autor / Fecha:** mmruvinsky — 11 Sep 2025.  
**Mensaje:** Refactorización de tests por helpers internos.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:2]{index=2}

#### 086e5ae — Agrego funciones simular_mejor  
**Autor / Fecha:** mmruvinsky — 09 Sep 2025.  
**Mensaje / Cambios principales:** Añade funciones relacionadas a simulación y validación de movimientos (por ejemplo: `simular_mejor_mov`, `_mov`, `ejecutar_entrada_simulada`, `ejecutar_mov_simulado`, `puede_usar_ambos_dados`, `puede_usar_dado`, `puede_usar_dado_tras_simular`, `debe_usar_dado_mayor`, `hay_mov_posible`).  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:3]{index=3}

#### 817430d — pruebas CI  
**Autor / Fecha:** mmruvinsky — 06 Sep 2025.  
**Mensaje:** pruebas CI (ajustes en pipelines).  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:4]{index=4}

#### e7f1a4e — Merge pull request #8 (automated-reports-update)  
**Autor / Fecha:** (agrupado 06 Sep 2025).  
**Mensaje:** Merge PR: automated reports update.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:5]{index=5}

#### 960a898 — Merge pull request #11 (función_hay_movimiento_posible)
**Autor / Fecha:** (06 Sep 2025).  
**Mensaje:** Merge PR que integra la rama `función_hay_movimiento_posible`.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:6]{index=6}

#### 3a58907 — Agrego función que verifica si hay movimientos disponibles  
**Autor / Fecha:** mmruvinsky — 06 Sep 2025.  
**Mensaje:** Implementa la función que verifica si existen movimientos posibles en el tablero.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:7]{index=7}

#### f8d7686 — docs: Update automated reports [skip ci]  
**Autor / Fecha:** (06 Sep 2025).  
**Mensaje:** Actualización de documentación de los reports automáticos.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:8]{index=8}

#### f554a3c — Merge pull request #10 (agrego_excepciones_personalizadas)  
**Autor / Fecha:** (06 Sep 2025).  
**Mensaje:** Merge PR que introduce excepciones personalizadas.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:9]{index=9}

#### 68997d0 — Agrego excepciones personalizadas, reformateo clase backgammon y tests  
**Autor / Fecha:** mmruvinsky — 05 Sep 2025.  
**Mensaje / Cambios principales:** Añade excepciones personalizadas y refactoriza `Backgammon` para usar esas excepciones; actualiza tests.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:10]{index=10}

#### 68e636d — Merge pull request #9 (imp_logica_basica)  
**Autor / Fecha:** (05 Sep 2025).  
**Mensaje:** Merge PR con lógica básica mejorada.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:11]{index=11}

#### f365474 — agregamos 95% de coverage, función bear off, unificamos variables y helpers  
**Autor / Fecha:** mmruvinsky — 05 Sep 2025.  
**Mensaje / Cambios principales:** Implementación `bear off`, unificación de variables de barra, helpers para reducir duplicación, ajustes en `coverage.rc`.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:12]{index=12}

#### 4086dd5 — Merge pull request #7 (imp_logica_basica)
**Autor / Fecha:** (04 Sep 2025).  
**Mensaje:** Merge PR.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:13]{index=13}

#### 201b929 — Modificamos archivo ci.yml  
**Autor / Fecha:** mmruvinsky — 04 Sep 2025.  
**Mensaje:** Cambios en `ci.yml` (workflows).  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:14]{index=14}

#### 5f8755a — Merge pull request #6 (imp_logica_basica)
**Autor / Fecha:** (03 Sep 2025).  
**Mensaje:** Merge PR.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:15]{index=15}

#### 5efad4c — Corregimos validaciones mover  
**Autor / Fecha:** mmruvinsky — 03 Sep 2025.  
**Mensaje:** Correcciones en las validaciones de la función `mover`.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:16]{index=16}

#### 26cb21e — Migrando a GitHub Actions y Sonar Cloud  
**Autor / Fecha:** mmruvinsky — 03 Sep 2025.  
**Mensaje:** Integración CI/CD y Sonar Cloud.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:17]{index=17}

#### 50773f3 — Agrego lógica de dados y movimientos; refactor de `mover`  
**Autor / Fecha:** mmruvinsky — 03 Sep 2025.  
**Mensaje / Cambios principales:** Implementa la lógica de dados y movimientos, refactoriza `mover`.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:18]{index=18}

#### 4df8ea7 — Agregación función `entrar_desde_barra`  
**Autor / Fecha:** mmruvinsky — 02 Sep 2025.  
**Mensaje:** Añade la función para ingresar fichas desde la barra.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:19]{index=19}

#### 24b9757 — mejora tests y bugs  
**Autor / Fecha:** mmruvinsky — 01 Sep 2025.  
**Mensaje:** Mejoras y corrección de bugs en tests.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:20]{index=20}

#### b6dee14 — Refactorización función de movimiento y tests  
**Autor / Fecha:** mmruvinsky — 30 Aug 2025.  
**Mensaje:** Refactor de movimiento y tests.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:21]{index=21}

#### 73ad4fc — Continuammos lógica movimiento  
**Autor / Fecha:** mmruvinsky — 28 Aug 2025.  
**Mensaje:** Avances en la lógica de movimiento.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:22]{index=22}

#### a3e28f3 — Agrego funciones entrar desde la barra  
**Autor / Fecha:** mmruvinsky — 26 Aug 2025.  
**Mensaje:** Funciones auxiliares para entrada desde barra.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:23]{index=23}

#### af130a2 — lógica movimientos legales  
**Autor / Fecha:** mmruvinsky — 25 Aug 2025.  
**Mensaje:** Implementa validaciones de movimientos legales.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:24]{index=24}

#### a5661b1 — Agrego lógica básica dado, tablero, backgammon  
**Autor / Fecha:** mmruvinsky — 25 Aug 2025.  
**Mensaje:** Implementación base (dado, tablero, clase Backgammon).  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:25]{index=25}

#### cfaa4fa — Merge pull request #3 (creacion_de_clases)  
**Autor / Fecha:** 24 Aug 2025.  
**Mensaje:** Merge PR (creación de clases).  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:26]{index=26}

#### fcf22e3 — Creación clases principales  
**Autor / Fecha:** mmruvinsky — 24 Aug 2025.  
**Mensaje:** Creación de las clases principales del proyecto.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:27]{index=27}

#### 755eeda — Merge pull request #2 (creación_de_archivos)  
**Autor / Fecha:** 22 Aug 2025.  
**Mensaje:** Merge PR que integra archivos iniciales.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:28]{index=28}

#### 3129736 — Creación de archivos  
**Autor / Fecha:** mmruvinsky — 22 Aug 2025.  
**Mensaje:** Archivos iniciales creados.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:29]{index=29}

#### d1d8dc6 — Setting up GitHub Classroom Feedback (bot)  
**Autor / Fecha:** github-classroom[bot] — 21 Aug 2025.  
**Mensaje:** Setup de feedback classroom.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:30]{index=30}

#### 3595946 — GitHub Classroom Feedback (bot)  
**Autor / Fecha:** github-classroom[bot] — 21 Aug 2025.  
**Mensaje:** Feedback de GitHub Classroom.  
**Detalle / diff:** ver la página del commit. :contentReference[oaicite:31]{index=31}

---


