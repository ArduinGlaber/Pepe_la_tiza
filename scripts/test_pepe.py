#!/usr/bin/env python3
"""
Tests básicos para Pepe_la_tiza
Valida estructura de agentes, templates y flujo
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


def is_windows_legacy_terminal() -> bool:
    if os.name != "nt":
        return False
    encoding = sys.stdout.encoding or ""
    return "cp1252" in encoding.lower() or "latin" in encoding.lower()


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    
    @classmethod
    def disable(cls):
        for attr in ["RED", "GREEN", "YELLOW", "BLUE", "RESET"]:
            setattr(cls, attr, "")


def get_box_chars() -> tuple:
    if is_windows_legacy_terminal():
        return "+", "-", "|"
    return "╔", "═", "║"


def get_check_marks() -> tuple:
    if is_windows_legacy_terminal():
        return "[+]", "[x]"
    return "✓", "✗"


def print_banner():
    tl, h, _ = get_box_chars()
    width = 39
    print(f"{Colors.BLUE}{tl}{h * width}{Colors.RESET}")
    print(f"{Colors.BLUE}{tl.replace(chr(0x2554), chr(0x2550))}{h * width}{Colors.RESET}")


def run_test(name: str, test_fn) -> Tuple[bool, str]:
    """Ejecuta un test y retorna (passed, message)"""
    ok_mark, fail_mark = get_check_marks()
    try:
        test_fn()
        return True, f"{Colors.GREEN}{ok_mark}{Colors.RESET} {name}"
    except AssertionError as e:
        return False, f"{Colors.RED}{fail_mark}{Colors.RESET} {name}: {e}"
    except Exception as e:
        return False, f"{Colors.RED}{fail_mark}{Colors.RESET} {name}: Unexpected error: {e}"


def read_file_safe(path: Path) -> str:
    """Lee archivo manejando encoding UTF-8"""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def test_agents_exist(root: Path):
    """Verifica que todos los agentes internos existan"""
    agents = ["planner", "builder", "verifier", "jester", "bug-fixer", "memory-keeper"]
    for agent in agents:
        # Los agents están en agents/.team/
        agent_file = root / "agents" / ".team" / f"{agent}.md"
        assert agent_file.exists(), f"Agent {agent}.md not found at {agent_file}"


def test_agents_have_self_checks(root: Path):
    """Verifica que cada agente tenga sección Self-Check"""
    agents = ["planner", "builder", "verifier", "jester", "bug-fixer", "memory-keeper"]
    
    for agent in agents:
        content = read_file_safe(root / "agents" / ".team" / f"{agent}.md")
        assert re.search(r"## Self-Check", content, re.IGNORECASE), \
            f"{agent}.md missing Self-Check section"


def test_main_agent_exists(root: Path):
    """Verifica que pepe_la_tiza.md exista"""
    main_agent = root / "agents" / "pepe_la_tiza.md"
    assert main_agent.exists(), "pepe_la_tiza.md not found"


def test_main_agent_has_team_section(root: Path):
    """Verifica que el agente principal documente su equipo"""
    content = read_file_safe(root / "agents" / "pepe_la_tiza.md")
    
    assert re.search(r"planner", content, re.IGNORECASE), "Missing planner reference"
    assert re.search(r"builder", content, re.IGNORECASE), "Missing builder reference"
    assert re.search(r"verifier", content, re.IGNORECASE), "Missing verifier reference"
    assert re.search(r"jester", content, re.IGNORECASE), "Missing jester reference"


def test_templates_exist(root: Path):
    """Verifica que los templates existan"""
    templates = ["todo-template.md", "lessons-template.md"]
    for template in templates:
        template_file = root / "templates" / template
        assert template_file.exists(), f"Template {template} not found"


def test_todo_template_structure(root: Path):
    """Verifica que todo-template.md tenga la estructura correcta"""
    content = read_file_safe(root / "templates" / "todo-template.md")
    
    assert re.search(r"#\s*Plan:", content), "Missing Plan header"
    assert re.search(r"\*\*Fecha:\*\*", content), "Missing Fecha field"
    assert re.search(r"\*\*Estado:\*\*", content), "Missing Estado field"
    assert re.search(r"##\s*Items", content), "Missing Items section"
    assert re.search(r"-\s*\[\s*\]", content), "Missing checkbox format"


def test_lessons_template_structure(root: Path):
    """Verifica que lessons-template.md tenga la estructura correcta"""
    content = read_file_safe(root / "templates" / "lessons-template.md")
    
    assert re.search(r"#\s*Lecciones", content), "Missing Lecciones header"
    assert re.search(r"\*\*Error:\*\*", content), "Missing Error field"
    assert re.search(r"\*\*Corrección:\*\*", content), "Missing Corrección field"
    assert re.search(r"\*\*Patrón", content), "Missing Patrón field"


def test_workflow_status_script(root: Path):
    """Verifica que workflow-status.py exista y sea ejecutable"""
    script = root / "bin" / "workflow-status.py"
    assert script.exists(), "workflow-status.py not found"
    
    content = read_file_safe(script)
    assert "def main" in content, "Missing main function"
    assert "def find_file" in content, "Missing find_file function"


def test_install_script_exists(root: Path):
    """Verifica que install.sh exista"""
    install = root / "scripts" / "install.sh"
    assert install.exists(), "install.sh not found"


def test_planner_has_correct_flow(root: Path):
    """Verifica que el planner tenga el flujo correcto"""
    content = read_file_safe(root / "agents" / ".team" / "planner.md")
    
    assert re.search(r"## Rol", content), "Missing Rol section"
    assert re.search(r"## Herramientas", content), "Missing Herramientas section"
    assert re.search(r"mem_search", content), "Missing mem_search reference"
    assert re.search(r"verifier", content, re.IGNORECASE), "Missing verifier delegation"


def test_builder_has_correct_flow(root: Path):
    """Verifica que el builder tenga el flujo correcto"""
    content = read_file_safe(root / "agents" / ".team" / "builder.md")
    
    assert re.search(r"## Rol", content), "Missing Rol section"
    assert re.search(r"UNA tarea a la vez", content, re.IGNORECASE), \
        "Missing 'one task at a time' constraint"
    assert re.search(r"test", content, re.IGNORECASE), "Missing test reference"
    assert re.search(r"planner", content, re.IGNORECASE), "Missing planner reference"


def test_verifier_has_correct_flow(root: Path):
    """Verifica que el verifier tenga el flujo correcto"""
    content = read_file_safe(root / "agents" / ".team" / "verifier.md")
    
    assert re.search(r"## Rol", content), "Missing Rol section"
    assert re.search(r"## Herramientas", content), "Missing Herramientas section"
    assert re.search(r"git diff", content, re.IGNORECASE), "Missing git diff reference"
    assert re.search(r"## Checklist", content), "Missing Checklist section"


def test_jester_has_correct_flow(root: Path):
    """Verifica que el jester tenga el flujo correcto"""
    content = read_file_safe(root / "agents" / ".team" / "jester.md")
    
    assert re.search(r"## Rol", content), "Missing Rol section"
    assert re.search(r"## Comportamiento", content), "Missing Comportamiento section"
    assert re.search(r"Escenario", content, re.IGNORECASE), "Missing scenario format"
    assert re.search(r"## Flags", content, re.IGNORECASE), "Missing flags section"


def test_bug_fixer_has_correct_flow(root: Path):
    """Verifica que el bug-fixer tenga el flujo correcto"""
    content = read_file_safe(root / "agents" / ".team" / "bug-fixer.md")
    
    assert re.search(r"## Rol", content), "Missing Rol section"
    assert re.search(r"mem_save", content), "Missing mem_save reference"
    assert re.search(r"conventional commit", content, re.IGNORECASE), \
        "Missing conventional commit reference"


def test_memory_keeper_has_correct_flow(root: Path):
    """Verifica que el memory-keeper tenga el flujo correcto"""
    content = read_file_safe(root / "agents" / ".team" / "memory-keeper.md")
    
    assert re.search(r"## Rol", content), "Missing Rol section"
    assert re.search(r"mem_search", content), "Missing mem_search reference"
    assert re.search(r"mem_save", content), "Missing mem_save reference"
    assert re.search(r"## Comportamiento", content), "Missing Comportamiento section"


def test_readme_exists_and_complete(root: Path):
    """Verifica que README.md exista y tenga secciones clave"""
    readme = root / "README.md"
    assert readme.exists(), "README.md not found"
    
    content = read_file_safe(readme)
    assert re.search(r"#\s*Pepe_la_tiza", content), "Missing main header"
    assert re.search(r"##\s*Instalación", content), "Missing Installation section"
    assert re.search(r"##\s*Uso", content), "Missing Usage section"
    assert re.search(r"##\s*Comandos", content), "Missing Commands section"


def run_all_tests(root: Path) -> Tuple[int, int, List[str]]:
    """Ejecuta todos los tests y retorna (passed, failed, messages)"""
    tests = [
        ("Estructura: Agentes existen", lambda: test_agents_exist(root)),
        ("Estructura: Agentes tienen Self-Check", lambda: test_agents_have_self_checks(root)),
        ("Estructura: Agente principal existe", lambda: test_main_agent_exists(root)),
        ("Estructura: Agente principal documenta equipo", lambda: test_main_agent_has_team_section(root)),
        ("Estructura: Templates existen", lambda: test_templates_exist(root)),
        ("Estructura: todo-template.md correcto", lambda: test_todo_template_structure(root)),
        ("Estructura: lessons-template.md correcto", lambda: test_lessons_template_structure(root)),
        ("Estructura: workflow-status.py existe", lambda: test_workflow_status_script(root)),
        ("Estructura: install.sh existe", lambda: test_install_script_exists(root)),
        ("Flujo: planner correcto", lambda: test_planner_has_correct_flow(root)),
        ("Flujo: builder correcto", lambda: test_builder_has_correct_flow(root)),
        ("Flujo: verifier correcto", lambda: test_verifier_has_correct_flow(root)),
        ("Flujo: jester correcto", lambda: test_jester_has_correct_flow(root)),
        ("Flujo: bug-fixer correcto", lambda: test_bug_fixer_has_correct_flow(root)),
        ("Flujo: memory-keeper correcto", lambda: test_memory_keeper_has_correct_flow(root)),
        ("Documentación: README completo", lambda: test_readme_exists_and_complete(root)),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        ok, msg = run_test(name, test_fn)
        results.append(msg)
        if ok:
            passed += 1
        else:
            failed += 1
    
    return passed, failed, results


def main():
    # Detectar si colores/Unicode están soportados
    if not sys.stdout.isatty() or is_windows_legacy_terminal():
        Colors.disable()
    
    root = Path(__file__).parent.parent
    
    tl, h, v = get_box_chars()
    print(f"\n{Colors.BLUE}{tl}{h * 39}{Colors.RESET}")
    print(f"{Colors.BLUE}{v}  Pepe_la_tiza — Test Suite              {v}{Colors.RESET}")
    print(f"{Colors.BLUE}{tl.replace(chr(0x2554), chr(0x255A))}{h * 39}{Colors.RESET}")
    
    passed, failed, results = run_all_tests(root)
    total = passed + failed
    
    print(f"{Colors.BLUE}Ejecutando {total} tests...{Colors.RESET}")
    print()
    
    for result in results:
        print(f"  {result}")
    
    tl, h, _ = get_box_chars()
    print(f"\n{Colors.BLUE}{tl}{h * 39}{Colors.RESET}")
    print(f"{Colors.BLUE}{tl.replace(chr(0x2554), chr(0x2550))}{h * 39}{Colors.RESET}")
    print(f"  Resultados: {Colors.GREEN}{passed} passed{Colors.RESET}, {Colors.RED}{failed} failed{Colors.RESET}")
    print(f"{Colors.BLUE}{tl.replace(chr(0x2554), chr(0x2514))}{h * 39}{Colors.RESET}")
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()