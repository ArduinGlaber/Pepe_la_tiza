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
│   └── pepe_la_tiza.md      # Meta-agente principal (visible en opencode)
├── .team/                    # Agentes internos (ocultos)
│   ├── planner.md
│   ├── builder.md
│   ├── verifier.md
│   ├── jester.md
│   ├── bug-fixer.md
│   └── memory-keeper.md
├── bin/
│   └── workflow-status       # CLI dashboard de estado
├── templates/
│   ├── todo-template.md      # Template para tasks/todo.md
│   └── lessons-template.md   # Template para tasks/lessons.md
├── scripts/
│   └── install.sh            # Script de instalación
└── README.md
```

## Estructura instalada

```
~/.opencode/
├── agents/
│   └── pepe_la_tiza.md      # Meta-agente principal
├── .team/                    # Agentes internos (ocultos de opencode)
├── bin/
│   └── workflow-status       # CLI dashboard
└── templates/               # Templates para proyectos
    ├── todo-template.md
    └── lessons-template.md
```

## Créditos

- **Sello Gentleman**: [Alan Buscaglia](https://github.com/alanf)
- Inspirado en el [Gentle AI Stack](https://github.com/alanf/gentle-ai-stack)

## Licencia

MIT — Ver archivo [LICENSE](LICENSE)

---

*Cuando me necesitás, solo decime qué necesitás. Yo me encargo del resto.*
