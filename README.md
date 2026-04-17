# Pepe_la_tiza 🤹

> El meta-agente que orquesta un equipo completo de agentes especializados.

**Sello Gentleman** — Inspirado en la filosofía de [Alan Buscaglia](https://github.com/alanf)

---

## ¿Qué es Pepe_la_tiza?

Pepe_la_tiza es un **meta-agente de IA** que actúa como tu único punto de contacto con un equipo completo de agentes especializados. Vos solo conversás con Pepe_la_tiza — él se encarga de coordinar todo lo demás.

### Dependencias

- **OpenCode** — Base del runtime
- **Engram** — Memoria persistente (mem_save, mem_search, mem_context)

> ⚠️ **No necesita** el Gentle AI Stack completo. Solo Engram como sistema de memoria.

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
cd Pepe_la_tiza

# Instalar todo
cp agents/pepe_la_tiza.md ~/.opencode/agents/
mkdir -p ~/.opencode/.team ~/.opencode/bin ~/.opencode/templates
cp .team/* ~/.opencode/.team/
cp bin/workflow-status ~/.opencode/bin/
chmod +x ~/.opencode/bin/workflow-status
cp templates/* ~/.opencode/templates/
```

## Uso

1. En tu terminal con OpenCode, activa el agente:
   ```
   /agent pepe_la_tiza
   ```

2. O simplemente empieza a conversar — Pepe_la_tiza detectará cuando necesite delegar.

3. Al iniciar, Pepe_la_tiza ejecuta `workflow-status` automáticamente para mostrar el estado del proyecto.

## Comandos

| Comando | Qué hace Pepe_la_tiza |
|---------|----------------------|
| `hola`, `hi` | Se presenta, ejecuta workflow-status y carga contexto |
| `plan <tarea>` | Genera un plan detallado |
| `hazlo` | Ejecuta el plan paso a paso |
| `status` | Ejecuta workflow-status para mostrar estado actual |
| `revisá` | Invoca al jester para cuestionar |
| `memo` | Busca lecciones guardadas del proyecto |
| `arrepentite` | Cancela el trabajo en curso |

## Skills técnicos

Pepe_la_tiza carga skills automáticamente según el contexto del proyecto.

### Skills propios (incluidos)

| Skill | Cuándo lo cargo |
|-------|-----------------|
| `python-senior` | Código Python avanzado, async, type hints, patrones senior |
| `python-pyqt6` | Apps de escritorio con interfaz gráfica |
| `python-pygame` | Juegos 2D, desarrollo de games |

### Gentle AI Stack (opcional)

Si está instalado en `~/.opencode/skills/gentleman/`, Pepe_la_tiza puede usar sus skills:

| Skill | Para qué |
|-------|----------|
| `angular-core` | Componentes Angular, signals, zoneless |
| `angular-architecture` | Estructura de proyectos Angular |
| `react-19` | Componentes React 19 |
| `tailwind-4` | Estilos con Tailwind CSS |
| `typescript` | TypeScript strict patterns |
| `django-drf` | APIs REST con Django |
| `playwright` | Tests E2E |
| `pytest` | Tests Python |

Para instalar Gentle AI Stack:
```bash
git clone https://github.com/alanf/gentle-ai-stack.git ~/.opencode/skills/gentleman
```

## Herramientas

### workflow-status

Dashboard CLI para ver el estado del proyecto.

```bash
workflow-status                    # Estado del proyecto actual
workflow-status ./mi-proyecto      # Proyecto específico
workflow-status --engram           # Incluye stats de Engram
workflow-status --verbose          # Muestra tareas completadas
```

## Estructura del proyecto

```
Pepe_la_tiza/
├── agents/
│   └── pepe_la_tiza.md      # Meta-agente principal
├── .team/                    # Agentes internos (ocultos)
│   ├── planner.md
│   ├── builder.md
│   ├── verifier.md
│   ├── jester.md
│   ├── bug-fixer.md
│   └── memory-keeper.md
├── skills/
│   └── python/              # Skills propios de Pepe_la_tiza
│       ├── pyqt6/
│       └── pygame/
├── bin/
│   └── workflow-status       # CLI dashboard de estado
├── templates/
│   ├── todo-template.md
│   └── lessons-template.md
├── scripts/
│   └── install.sh
└── README.md
```

## Estructura instalada

```
~/.opencode/
├── agents/
│   └── pepe_la_tiza.md      # Meta-agente principal
├── .team/                    # Agentes internos (ocultos)
├── bin/
│   └── workflow-status       # CLI dashboard
├── templates/
│   ├── todo-template.md
│   └── lessons-template.md
└── skills/                   # (opcional) Gentle AI Stack
    └── gentleman/
```

## Créditos

- **Filosofía**: [Alan Buscaglia](https://github.com/alanf) — Sello Gentleman
- Pepe_la_tiza usa la filosofía de Alan pero es **standalone**: solo necesita OpenCode + Engram

## Licencia

MIT — Ver archivo [LICENSE](LICENSE)

---

*Cuando me necesitás, solo decime qué necesitás. Yo me encargo del resto.*
