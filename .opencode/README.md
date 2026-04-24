# Pepe_la_tiza — Arquitectura de Sub-Agentes

## Cómo funciona la delegación en OpenCode

Basado en el sistema de OpenCode (ver [issues #7756](https://github.com/anomalyco/opencode/issues/7756) y [#7296](https://github.com/anomalyco/opencode/issues/7296)).

### El problema

Por defecto, **los sub-agentes NO pueden delegar a otros sub-agentes**. Necesitás configurar `task_budget` y `permission.task` para activar la cadena de delegación.

### Configuración requerida

```json
// .opencode/agents.json (ejemplo)
{
  "agents": {
    "pepe_la_tiza": {
      "file": ".team/pepe_la_tiza.md",
      "tools": { "task": true },
      "task_budget": 20,
      "subagents": ["planner", "builder", "verifier", "jester", "bug-fixer", "memory-keeper"]
    },
    "planner": {
      "file": ".team/planner.md",
      "mode": "subagent",
      "tools": { "task": true },
      "task_budget": 5,
      "permission": { "task": { "*": "deny", "jester": "allow", "builder": "allow" } }
    }
  }
}
```

### Conceptos clave

| Campo | Qué hace | Ejemplo |
|-------|----------|---------|
| `task_budget` | Cantidad máxima de delegations permitidas | `5` = puede delegar hasta 5 veces |
| `permission.task` | Quién puede ser delegado | `{ "*": "deny", "jester": "allow" }` = solo al jester |
| `subagents` | Qué sub-agentes aparecen disponibles | `["planner", "builder"]` = solo estos |
| `mode: "subagent"` | Marca que es un sub-agente | Necesario para que funcione |

### El flujo de Pepe_la_tiza

```
USER ──► pepe_la_tiza (task_budget: 20)
              │
              ├─► planner (task_budget: 5)
              │        │
              │        ├─► jester (task_budget: 0, NO puede delegar más)
              │        └─► builder (task_budget: 5)
              │                 │
              │                 ├─► verifier (task_budget: 3)
              │                 │         │
              │                 │         └─► builder (para re-trabajo)
              │                 └─► bug-fixer (task_budget: 10)
              │                          │
              │                          └─► planner (si necesita replanificar)
              │
              └─► memory-keeper (task_budget: 0, solo lectura)
```

### Por qué cada agent tiene diferente task_budget

| Agent | task_budget | Por qué |
|-------|-------------|---------|
| pepe_la_tiza | 20 | Orchestrator, necesita muchas delegaciones |
| planner | 5 | Planifica → delega a builder/jester |
| builder | 5 | Implementa → puede invocar verifier/bug-fixer |
| verifier | 3 | Verifica → rara vez necesita delegar más |
| jester | 0 | Solo cuestiona, no delega |
| bug-fixer | 10 | Arregla bugs → puede replanificar si es complejo |
| memory-keeper | 0 | Solo guarda/recupera, no delega |

### Instalación de la configuración

```bash
# En tu proyecto OpenCode, crea la config:
mkdir -p .opencode
cp /path/a/pepe-la-tiza/.opencode/agents.json .opencode/

# O usa el install script que ya lo hace
./scripts/install.sh
```

### Testing manual del flujo

```bash
# Test 1: Verificar que los agents se cargan
opencode --agent pepe_la_tiza

# Test 2: Verificar delegation (en la conversación)
> hola
> plan implementame un hello world en Python
> hazlo

# Test 3: Verificar que el jester cuestiona antes de cerrar
> revisá
```

### Debugging de delegation

Si la delegación no funciona:

1. Verificá que `task_budget > 0` para el agent que intenta delegar
2. Verificá que `permission.task` permite el target
3. Ejecutá con `--verbose` para ver los logs de OpenCode
4. Verificá que los archivos `.team/*.md` están en la ubicación correcta

### Alternativa: Sin config (comportamiento legacy)

Si no querés configurar `agents.json`, podés usar el comando `/task` manualmente en la conversación principal:

```
> Ejecutá el planner para crear un plan
→ Usa la tool task con agent="planner"

> Ejecutá el builder con el plan
→ Usa la tool task con agent="builder"
```

Esto es más manual pero no requiere configuración de OpenCode.