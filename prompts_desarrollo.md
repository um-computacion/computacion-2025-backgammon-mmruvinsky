prompt Chatgpt 5: no me convendria hacer funciones def destino bloqueado por ejemplo para que las funciones mover entrar desde barra los usen como helpers

ChatGPT dijo:
    Pensado durante 8s

    Sí, 100%. Extraer helpers te da:

    menos duplicación entre mover y entrar_desde_barra

    tests más chicos y precisos (testeás reglas aisladas)

    código más legible

    Te propongo estos helpers “puros” (sin efectos secundarios) y un par con efecto controlado: ...

sería buena practica?

ChatGPT dijo:

Sí 💯, sería una buena práctica extraer helpers como __es_destino_bloqueado__, __es_blots_rival__, etc., por varias razones:

Evita duplicación de código
Ahora mismo tenés la misma lógica repetida en mover y en entrar_desde_barra. Si un día cambiás esa regla (ej. “bloqueo son 3 fichas y no 2”), tendrías que tocar varias funciones → más chance de errores.

Alinea con los principios SOLID
El enunciado pide aplicar estos principios.

S (Single Responsibility): cada función hace una sola cosa → helpers claros para validar reglas.

O (Open/Closed): si cambiás reglas, agregás o modificás helpers sin romper el resto.

Mejora la legibilidad