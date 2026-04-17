# Pepe_la_tiza 🤹

> El meta-agente que orquesta un equipo completo de agentes especializados.

**Sello Gentleman** — Desarrollado con la filosofía de [Alan Buscaglia](https://github.com/alanf)

---

## ¿Qué es Pepe_la_tiza?

Pepe_la_tiza es un **meta-agente de IA** que actúa como tu único punto de contacto con un equipo completo de agentes especializados. Vos solo conversás con Pepe_la_tiza — él se encarga de coordinar todo lo demás.

### El equipo interno

| Agente | Rol |
|--------|-----|
| `planner` | Analiza y genera planes de trabajo |
| `builder` | Implementa código, uno a la vez |
| `verifier` | Verifica que cada paso esté completo |
| `jester` | Cuestiona suposiciones, busca puntos ciegos |
| `bug-fixer` | Arregla bugs de forma autónoma |
| `memory-keeper` | Guarda y recupera lecciones del proyecto |

## Instalación

### Opción 1: Script rápido (recomendado)

```bash
curl -sL https://raw.githubusercontent.com/ArduinGlaber/Pepe_la_tiza/main/scripts/install.sh | bash
```

### Opción 2: Manual

```bash
# Clonar el repo
git clone https://github.com/ArduinGlaber/Pepe_la_tiza.git

# Copiar el agente principal a tu directorio de agentes
cp agents/pepe_la_tiza.md ~/.opencode/agents/

# Copiar los agentes internos (fuera de agents/ para que estén ocultos)
mkdir -p ~/.opencode/.team
cp agents/.team/* ~/.opencode/.team/
```

## Uso

1. En tu terminal con OpenCode, activa el agente:
   ```
   /agent pepe_la_tiza
   ```

2. O simplemente empieza a conversar — Pepe_la_tiza detectará cuando necesite delegar.

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│                        USER                             │
│                    (vos, solo vos)                      │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    Pepe_la_tiza        │
              │  (meta-agente)        │
              └───────────┬───────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   ┌─────────┐      ┌─────────┐      ┌─────────┐
   │ planner │ ──►  │ builder │ ──►  │verifier │
   └─────────┘      └─────────┘      └─────────┘
        │                 │                 │
        ▼                 ▼                 │
   ┌─────────┐      ┌─────────┐            │
   │ jester  │      │bug-fixer│ ◄──────────┘
   └─────────┘      └─────────┘
        │
        ▼
   ┌─────────────┐
   │memory-keeper│
   └─────────────┘
```

## Comandos

| Comando | Qué hace Pepe_la_tiza |
|---------|----------------------|
| `hola`, `hi` | Se presenta y carga contexto |
| `plan <tarea>` | Genera un plan detallado |
| `hazlo` | Ejecuta el plan paso a paso |
| `status` | Muestra estado del proyecto |
| `revisá` | Invoca al jester para cuestionar |
| `memo` | Busca lecciones guardadas |
| `arrepentite` | Cancela el trabajo en curso |

## Para desarrolladores

### Estructura del proyecto

```
Pepe_la_tiza/
├── agents/
│   └── pepe_la_tiza.md      # Meta-agente principal (visible en opencode)
├── .team/                    # Agentes internos (fuera de agents/, ocultos)
│   ├── planner.md
│   ├── builder.md
│   ├── verifier.md
│   ├── jester.md
│   ├── bug-fixer.md
│   └── memory-keeper.md
├── scripts/
│   └── install.sh            # Script de instalación
└── README.md
```

**Nota**: Los agentes en `.team/` están fuera del directorio `agents/` de opencode, por lo que no aparecen en la lista de agentes. Solo `pepe_la_tiza` es visible, pero puede invocar los internos transparentemente.

### Agregar nuevos agentes internos

1. Crear el agente en `.team/nuevo-agente.md`
2. Definir su rol y comportamiento
3. Actualizar `pepe_la_tiza.md` para que lo invoque
4. Pull request bienvenido

## Créditos

- **Sello Gentleman**: [Alan Buscaglia](https://github.com/alanf)
- Inspirado en el [Gentle AI Stack](https://github.com/alanf/gentle-ai-stack)

## Licencia

MIT — Ver archivo [LICENSE](LICENSE)

---

*Cuando me necesitás, solo decime qué necesitás. Yo me encargo del resto.*
