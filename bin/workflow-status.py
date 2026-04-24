#!/usr/bin/env python3
"""
workflow-status — Pepe_la_tiza Workflow Dashboard
Uso: workflow-status [proyecto] [--engram] [--verbose]
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional


# Colores cross-platform
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @classmethod
    def is_supported(cls) -> bool:
        """Detecta si el terminal soporta colores ANSI"""
        return sys.stdout.isatty() or os.name != "nt"

    @classmethod
    def disable(cls):
        cls.RED = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.BLUE = ""
        cls.CYAN = ""
        cls.BOLD = ""
        cls.RESET = ""


def is_windows_legacy_terminal() -> bool:
    """Detecta terminal Windows sin soporte Unicode"""
    if os.name != "nt":
        return False
    encoding = sys.stdout.encoding or ""
    return "cp1252" in encoding.lower() or "latin" in encoding.lower()


def get_box_chars() -> tuple:
    """Retorna chars de box según capacidad del terminal"""
    if is_windows_legacy_terminal():
        return "+", "-", "|"
    return "╔", "═", "║"


def find_file(directory: Path, pattern: str) -> Optional[Path]:
    """Busca un archivo recursivamente, ignorando node_modules y dependencias"""
    exclude_dirs = {"node_modules", ".git", "__pycache__", "venv", ".venv", "env"}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if pattern in file:
                return Path(root) / file
    return None


def read_todo_content(todo_path: Path) -> dict:
    """Extrae metadata del plan"""
    try:
        content = todo_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = todo_path.read_text(encoding="utf-8-sig", errors="replace")

    plan_name = re.search(r"^#\s*Plan:\s*(.+)$", content, re.MULTILINE)
    plan_date = re.search(r"^\*\*Fecha:\*\*\s*(.+)$", content, re.MULTILINE)
    plan_status = re.search(r"^\*\*Estado:\*\*\s*(.+)$", content, re.MULTILINE)

    total = len(re.findall(r"^-\s*\[\s*\]", content, re.MULTILINE))
    done = len(re.findall(r"^-\s*\[x\]", content, re.MULTILINE))
    in_progress = len(re.findall(r"^-\s*\[~\]", content, re.MULTILINE))

    pending_items = [(i, line) for i, line in enumerate(content.split("\n"), 1)
                     if re.match(r"^-\s*\[\s*\]", line)]
    in_progress_items = [(i, line) for i, line in enumerate(content.split("\n"), 1)
                          if re.match(r"^-\s*\[~\]", line)]
    done_items = [(i, line) for i, line in enumerate(content.split("\n"), 1)
                  if re.match(r"^-\s*\[x\]", line)]

    return {
        "name": plan_name.group(1) if plan_name else "Plan sin nombre",
        "date": plan_date.group(1) if plan_date else "Sin fecha",
        "status": plan_status.group(1) if plan_status else "En progreso",
        "total": total,
        "done": done,
        "in_progress": in_progress,
        "pending_items": pending_items,
        "in_progress_items": in_progress_items,
        "done_items": done_items,
        "content": content,
    }


def get_lessons_count(lessons_path: Optional[Path]) -> int:
    """Cuenta lecciones en lessons.md"""
    if not lessons_path or not lessons_path.exists():
        return 0
    content = lessons_path.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(r"^###\s+\d{4}-\d{2}", content, re.MULTILINE))


def status_color(status: str) -> str:
    """Colorea el estado"""
    status_lower = status.lower()
    if "completado" in status_lower:
        if is_windows_legacy_terminal():
            return f"{Colors.GREEN}[OK] Completado{Colors.RESET}"
        return f"{Colors.GREEN}OK Completado{Colors.RESET}"
    elif "bloqueado" in status_lower:
        if is_windows_legacy_terminal():
            return f"{Colors.RED}[X] Bloqueado{Colors.RESET}"
        return f"{Colors.RED}X Bloqueado{Colors.RESET}"
    if is_windows_legacy_terminal():
        return f"{Colors.YELLOW}[~] En progreso{Colors.RESET}"
    return f"{Colors.YELLOW}~ En progreso{Colors.RESET}"


def progress_bar(done: int, total: int) -> str:
    """Genera barra de progreso"""
    if total == 0 and done == 0:
        pct = 0
    elif total == 0:
        pct = 100
    else:
        pct = min(100, (done * 100) // (done + total))

    filled = min(10, (pct * 10) // 100)
    empty = 10 - filled

    if is_windows_legacy_terminal():
        bar = f"{Colors.GREEN}{'#' * filled}{Colors.RESET}{'-' * empty}"
    else:
        bar = f"{Colors.GREEN}{'█' * filled}{Colors.RESET}{'░' * empty}"
    return f"{bar} {pct}%"


def print_banner() -> None:
    """Imprime el banner con chars apropiados para el terminal"""
    tl, h, v = get_box_chars()
    width = 39
    print(f"{Colors.BOLD}{Colors.BLUE}{tl}{h * width}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{v}  Pepe_la_tiza — Workflow Status        {v}{Colors.RESET}")
    br = chr(0x255A) if not is_windows_legacy_terminal() else "+"
    print(f"{Colors.BOLD}{Colors.BLUE}{br}{h * width}{Colors.RESET}")


def print_box_line(label: str) -> None:
    """Imprime una línea con formato de box"""
    tl, h, v = get_box_chars()
    br = chr(0x2514) if not is_windows_legacy_terminal() else "+"
    mid = chr(0x16) if not is_windows_legacy_terminal() else "-"
    content = f"{label}"
    if is_windows_legacy_terminal():
        print(f"{Colors.BOLD}{tl}{mid * 37}{Colors.RESET}")
        print(f"{Colors.BOLD}{v}{Colors.RESET} {content}")
        print(f"{Colors.BOLD}{br}{mid * 37}{Colors.RESET}")
    else:
        print(f"{Colors.BOLD}{tl}{h * 37}{Colors.RESET}")
        print(f"{Colors.BOLD}{v}{Colors.RESET} {content}")
        print(f"{Colors.BOLD}{br}{h * 37}{Colors.RESET}")


def show_help() -> str:
    return f"""{Colors.BOLD}workflow-status — Pepe_la_tiza Workflow Dashboard{Colors.RESET}

{Colors.BOLD}USO:{Colors.RESET}
    workflow-status [opciones] [proyecto]

{Colors.BOLD}ARGUMENTOS:{Colors.RESET}
    proyecto    Directorio del proyecto (default: directorio actual)

{Colors.BOLD}OPCIONES:{Colors.RESET}
    -h, --help          Muestra esta ayuda
    -e, --engram        Muestra stats de Engram
    -v, --verbose       Muestra tareas completadas
    -nc, --no-colors    Desactiva colores

{Colors.BOLD}EJEMPLOS:{Colors.RESET}
    workflow-status                    # Usa directorio actual
    workflow-status ./mi-proyecto     # Proyecto especifico
    workflow-status --engram           # Incluye stats de Engram
    workflow-status -e ~/projects/app # Combinar opciones

{Colors.BOLD}ARCHIVOS BUSCADOS:{Colors.RESET}
    tasks/todo.md       Plan activo
    tasks/lessons.md    Lecciones aprendidas

{Colors.BOLD}INFO:{Colors.RESET}
    https://github.com/ArduinGlaber/Pepe_la_tiza
"""


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-e", "--engram", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-nc", "--no-colors", action="store_true")
    args = parser.parse_args()

    if args.no_colors or not Colors.is_supported():
        Colors.disable()

    if args.help:
        print(show_help())
        sys.exit(0)

    print_banner()
    print()

    project = Path(args.project).resolve()

    todo_file = find_file(project, "todo.md")
    lessons_file = find_file(project, "lessons.md")

    if not todo_file:
        print(f"{Colors.YELLOW}! No se encontro tasks/todo.md{Colors.RESET}")
        print()
        print("   Para crear uno:")
        install_dir = Path(__file__).parent.parent
        template = install_dir / "templates" / "todo-template.md"
        if template.exists():
            print(f"   {Colors.CYAN}copy {template} tu-proyecto\\tasks\\todo.md{Colors.RESET}")
        else:
            print(f"   {Colors.CYAN}mkdir tasks && crear tasks/todo.md{Colors.RESET}")
        sys.exit(0)

    todo = read_todo_content(todo_file)
    lessons_count = get_lessons_count(lessons_file)

    print(f"{Colors.BOLD}@ Plan:{Colors.RESET} {todo_file}")
    print(f"   {Colors.CYAN}{todo['name']}{Colors.RESET}")
    print(f"   Fecha: {todo['date']} | Estado: {status_color(todo['status'])}")
    print()

    print_box_line(f"Completados: {Colors.GREEN}{todo['done']}{Colors.RESET}  "
                  f"En progreso: {Colors.YELLOW}{todo['in_progress']}{Colors.RESET}  "
                  f"Pendientes: {todo['total']}")
    print(f"{Colors.BOLD}  {progress_bar(todo['done'], todo['total'])}{Colors.RESET}")
    print()

    if todo["in_progress_items"]:
        print(f"   {Colors.YELLOW}~ En progreso:{Colors.RESET}")
        for line_num, line in todo["in_progress_items"]:
            task = re.sub(r"^-\s*\[~\]\s*", "", line).strip()
            print(f"     L{line_num}: {task}")
        print()

    if todo["pending_items"]:
        print(f"   {Colors.YELLOW}o Pendientes:{Colors.RESET}")
        for line_num, line in todo["pending_items"]:
            task = re.sub(r"^-\s*\[\s*\]\s*", "", line).strip()
            print(f"     L{line_num}: {task}")
        print()

    if args.verbose and todo["done_items"]:
        print(f"   {Colors.GREEN}+ Completados:{Colors.RESET}")
        for line_num, line in todo["done_items"]:
            task = re.sub(r"^-\s*\[x\]\s*", "", line).strip()
            print(f"     L{line_num}: {task}")
        print()

    if lessons_file:
        print(f"{Colors.BOLD}@ Lecciones:{Colors.RESET}")
        print(f"   {lessons_count} lecciones en {lessons_file}")

        if lessons_count > 0:
            content = todo.get("content", "")
            last_date = re.search(r"(###\s+\d{4}-\d{2}-\d{2})", content)
            if last_date:
                print(f"   Ultima: {Colors.CYAN}{last_date.group(1)}{Colors.RESET}")
        print()

    if args.engram:
        print(f"{Colors.BOLD}* Engram Memory:{Colors.RESET}")
        engram_dir = Path.home() / ".engram"
        if engram_dir.exists():
            db_files = list(engram_dir.rglob("*.db")) + list(engram_dir.rglob("*.json"))
            print(f"   Observations disponibles: {Colors.CYAN}{len(db_files)}{Colors.RESET}")
            print(f"   Comando: {Colors.CYAN}mem_search(query: \"workflow\"){Colors.RESET} para buscar")
        else:
            print(f"   {Colors.YELLOW}Engram no configurado{Colors.RESET}")
        print()

    tl, h, _ = get_box_chars()
    print(f"{Colors.BLUE}{tl}{h * 39}{Colors.RESET}")
    print(f"   {Colors.CYAN}workflow-status{Colors.RESET} — {Colors.BOLD}Use -h para mas opciones{Colors.RESET}")


if __name__ == "__main__":
    main()