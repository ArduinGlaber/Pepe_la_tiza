# Pepe_la_tiza — Arquitectura Completa

## Diagrama de Componentes

```mermaid
graph TB
    subgraph User["👤 Usuario"]
        U[("/agent pepe_la_tiza")]
    end

    subgraph Core["📦 Core"]
        PT[("pepe_la_tiza.md<br/>mode: primary<br/>tools: delegate")]
    end

    subgraph Team["👥 Equipo Interno (.opencode/agents/)"]
        subgraph Planners["Planificación"]
            PL[("planner.md<br/>mode: subagent<br/>tools: delegate, read, todowrite")]
        end
        
        subgraph Executors["Ejecución"]
            BU[("builder.md<br/>mode: subagent<br/>tools: delegate, write, edit, bash")]
            BF[("bug-fixer.md<br/>mode: subagent<br/>tools: write, edit, bash")]
        end
        
        subgraph Quality["Calidad"]
            VE[("verifier.md<br/>mode: subagent<br/>tools: read, bash")]
            JE[("jester.md<br/>mode: subagent<br/>tools: read")]
        end
        
        subgraph Memory["🧠 Memoria"]
            MK[("memory-keeper.md<br/>mode: subagent<br/>tools: read, todowrite")]
        end
    end

    subgraph Tools["🛠️ Tools"]
        DE["delegate()<br/>Invoca sub-agentes"]
        DL["delegation_list<br/>Lista tareas"]
        DR["delegation_read<br/>Lee resultados"]
        TW["todowrite<br/>Escribe tasks/todo.md"]
        TR["todoread<br/>Lee tasks/todo.md"]
        W["write<br/>Escribe archivos"]
        E["edit<br/>Edita archivos"]
        B["bash<br/>Ejecuta comandos"]
        R["read<br/>Lee archivos"]
    end

    subgraph Storage["💾 Almacenamiento"]
        TD["tasks/todo.md<br/>Plan activo"]
        LM["tasks/lessons.md<br/>Lecciones"]
        EN["Engram<br/>Memoria persistente"]
    end

    subgraph Utilities["📊 Utilidades"]
        WS["workflow-status.py<br/>Dashboard CLI"]
        INST["install.py<br/>Installer"]
        TESTS["test_pepe.py<br/>Test Suite"]
    end

    U --> PT
    
    PT --> DE
    PT --> DL
    PT --> DR
    PT --> TW
    PT --> TR
    
    DE --> PL
    DE --> BU
    DE --> VE
    DE --> JE
    DE --> BF
    DE --> MK
    
    PL --> TW
    PL --> TR
    PL --> DE
    PL --> R
    
    BU --> W
    BU --> E
    BU --> B
    BU --> DE
    
    VE --> R
    VE --> B
    VE --> DE
    
    JE --> R
    
    BF --> W
    BF --> E
    BF --> B
    BF --> DE
    
    MK --> EN
    
    PL -.-> TD
    BU -.-> TD
    VE -.-> TD
    MK -.-> LM
    MK -.-> EN
```

---

## Diagrama de Flujo de Delegación

```mermaid
sequenceDiagram
    participant U as 👤 Usuario
    participant PT as Pepe_la_tiza
    participant PL as Planner
    participant BU as Builder
    participant VE as Verifier
    participant JE as Jester
    participant MK as Memory-Keeper
    participant EN as Engram

    U->>PT: "hola"
    PT->>MK: mem_search(workflow)
    MK->>EN: Busca lecciones
    EN-->>MK: Lecciones previas
    MK-->>PT: Muestra contexto
    PT-->>U: Saludo + status

    U->>PT: "plan hacer X"
    PT->>PT: Analiza tarea
    PT->>EN: mem_search(tags)
    PT->>PT: Genera plan
    PT->>TW: Escribe tasks/todo.md
    PT->>U: Presenta plan

    U->>PT: "hazlo"
    PT->>DE: delegate(planner)
    PL->>PL: Lee tasks/todo.md
    PL->>TW: Actualiza plan
    
    PT->>DE: delegate(builder)
    BU->>BU: Toma primer item
    BU->>W: Escribe código
    BU->>B: Ejecuta tests
    
    alt Tests fallan
        BU->>PT: Reporta error
        PT->>DE: delegate(bug-fixer)
        BF->>BF: Diagnostica bug
        BF->>E: Aplica fix
        BF->>B: Re-ejecuta
    end

    PT->>DE: delegate(verifier)
    VE->>VE: Revisa código
    VE->>B: Ejecuta tests
    VE->>PT: Resultado

    alt No trivial
        PT->>DE: delegate(jester)
        JE->>JE: Cuestiona suposiciones
        JE->>PT: Flags y veredicto
    end

    alt Todo OK
        VE->>TW: Marca items como [x]
        PT->>MK: Guardar lección
        MK->>EN: mem_save
        MK->>LM: Actualiza lessons.md
    end

    PT-->>U: "Listo! ✓"
```

---

## Mapa de Archivos

```mermaid
graph LR
    subgraph Repo["Pepe_la_tiza_repo/"]
        subgraph Opencode[".opencode/"]
            A["agents/"]
            A1["pepe_la_tiza.md"]
            A2["planner.md"]
            A3["builder.md"]
            A4["verifier.md"]
            A5["jester.md"]
            A6["bug-fixer.md"]
            A7["memory-keeper.md"]
            A8["agents.json"]
            A9["README.md"]
        end
        
        subgraph Bin["bin/"]
            B1["workflow-status.py"]
            B2["install.py"]
        end
        
        subgraph Scripts["scripts/"]
            S1["test_pepe.py"]
            S2["install.sh"]
        end
        
        subgraph Templates["templates/"]
            T1["todo-template.md"]
            T2["lessons-template.md"]
        end
        
        subgraph Skills["skills/python/"]
            SK1["senior/SKILL.md"]
            SK2["pyqt6/SKILL.md"]
            SK3["pygame/SKILL.md"]
        end
        
        subgraph Tasks["tasks/"]
            TD["todo.md"]
            LM["lessons.md"]
        end
    end

    A1 -.->|"mode: primary"| PT
    A2 -.->|"mode: subagent"| PL
    A3 -.->|"mode: subagent"| BU
    A4 -.->|"mode: subagent"| VE
    A5 -.->|"mode: subagent"| JE
    A6 -.->|"mode: subagent"| BF
    A7 -.->|"mode: subagent"| MK
    
    B1 -->|Dashboard| TD
    B2 -->|Install| A & Bin & Templates
    S1 -->|Tests| A
    SK1 -->|~400 lines| PYTHON
    SK2 -->|~217 lines| PYTHON
    SK3 -->|~287 lines| PYTHON
```

---

## Tabla de Herramientas por Agente

| Agente | delegate | todowrite | todoread | read | write | edit | bash | mem_* |
|--------|----------|-----------|----------|------|-------|------|------|-------|
| **pepe_la_tiza** | ✅ | ✅ | ✅ | - | - | - | - | - |
| **planner** | ✅ | ✅ | ✅ | ✅ | - | - | - | ✅ |
| **builder** | ✅ | - | - | ✅ | ✅ | ✅ | ✅ | - |
| **verifier** | - | - | - | ✅ | - | - | ✅ | - |
| **jester** | - | - | - | ✅ | - | - | - | - |
| **bug-fixer** | ✅ | - | - | ✅ | ✅ | ✅ | ✅ | ✅ |
| **memory-keeper** | - | ✅ | - | ✅ | - | - | - | ✅ |

---

## Flujo de Datos

```mermaid
flowchart LR
    subgraph Input["Entrada"]
        CMD["Comando del usuario"]
        CTX["Contexto del proyecto"]
    end

    subgraph Process["Procesamiento"]
        PT["pepe_la_tiza<br/>Orquesta"]
        PL["Planner<br/>Planifica"]
        BU["Builder<br/>Ejecuta"]
        VE["Verifier<br/>Verifica"]
    end

    subgraph State["Estado"]
        TD["tasks/todo.md"]
        LM["tasks/lessons.md"]
        EN["Engram"]
    end

    subgraph Output["Salida"]
        FILES["Archivos<br/>creados"]
        CODE["Código<br/>implementado"]
        TESTS["Tests<br/>ejecutados"]
        DOCS["Documentación"]
    end

    CMD --> PT
    CTX --> PT
    
    PT --> |"delegate()"| PL
    PT --> |"delegate()"| BU
    PT --> |"delegate()"| VE
    
    PL --> |"write"| TD
    BU --> |"write"| FILES
    BU --> |"execute"| TESTS
    
    VE --> |"read"| TD
    VE --> |"verify"| TESTS
    
    TD -.-> |"Actualiza"| PL
    LM -.-> |"Guarda"| EN
    
    FILES --> |"Verificado"| VE
    TESTS --> |"Resultado"| VE
    
    VE --> |"Pass/Fail"| PT
    PT --> |"Resultado"| Output
```

---

*Generado: Release 1.0 - Arquitectura Pepe_la_tiza*