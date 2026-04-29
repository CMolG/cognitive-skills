# Ejemplo realista — Alert Tuner Skill — {engineer_name}

## Escenario

Un equipo usa el skill `alert-tuner` durante una tarea operativa real del rol `ceet-devops-sre`. El objetivo es producir una respuesta utilizable inmediatamente, no un ejemplo vacío.

## Entrada de trabajo

- Contexto: sprint activo con fecha de entrega comprometida.
- Restricciones: no romper estándares del rol ni reglas globales del pack.
- Entregable solicitado: recomendación priorizada + pasos de ejecución.

## Qué debe hacer el skill

- Aplica las reglas del rol antes de responder.
- Explica decisiones con criterios observables.
- Entrega salida accionable y verificable.

## Salida esperada (ejemplo)

1. **Diagnóstico:** resume el problema en 3–5 líneas con riesgos explícitos.
2. **Plan priorizado:** lista de acciones por impacto/riesgo con orden de ejecución.
3. **Criterios de aceptación:** checks verificables para dar la tarea por correcta.
4. **Riesgos y mitigaciones:** tradeoffs, señales de alerta y plan de rollback/escalación.

## Evidencia de calidad

- La salida referencia estándares del rol y evita recomendaciones genéricas.
- Incluye decisiones concretas (qué hacer primero, qué no hacer y por qué).
- Puede ejecutarse sin interpretación adicional por parte del equipo.
