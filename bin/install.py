#!/usr/bin/env python3
"""
install.py — Pepe_la_tiza Cross-Platform Installer
Instala el meta-agente en ~/.opencode/
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Optional


def is_windows() -> bool:
    return os.name == "nt"


def get_opencode_dir() -> Path:
    """Obtiene ~/.opencode/"""
    return Path.home() / ".opencode"


def get_config_dir() -> Path:
    """Obtiene el directorio de configuración según el SO"""
    if is_windows():
        # Windows: %APPDATA%/opencode
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "opencode"
    # Unix: ~/.opencode
    return Path.home() / ".opencode"


def get_opencode_bin_dir() -> Path:
    """Obtiene el directorio de binarios"""
    config = get_config_dir()
    if is_windows():
        return config / "Scripts"  # Windows usa Scripts para executables
    return config / "bin"


def colors():
    class C:
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"
        BOLD = "\033[1m"
        RESET = "\033[0m"
        
        @classmethod
        def disable(cls):
            if not sys.stdout.isatty() or is_windows():
                for attr in ["RED", "GREEN", "YELLOW", "BLUE", "CYAN", "BOLD", "RESET"]:
                    setattr(cls, attr, "")
    return C


C = colors()


def step(msg: str) -> None:
    print(f"{C.CYAN}→{C.RESET} {msg}")


def success(msg: str) -> None:
    print(f"{C.GREEN}✓{C.RESET} {msg}")


def error(msg: str) -> None:
    print(f"{C.RED}✗{C.RESET} {msg}")


def warn(msg: str) -> None:
    print(f"{C.YELLOW}⚠{C.RESET} {msg}")


def install(skip_backup: bool = False) -> int:
    """Instala Pepe_la_tiza"""
    install_dir = Path(__file__).parent.parent.resolve()
    config_dir = get_config_dir()
    opencode_dir = get_opencode_dir()
    
    # Banner
    tl, h = ("+", "-") if is_windows() else ("╔", "═")
    print(f"\n{C.BLUE}{tl}{h * 43}{C.RESET}")
    print(f"{C.BLUE}{tl.replace('╔', '║')}  Pepe_la_tiza — Install Wizard        {tl.replace('╔', '║')}{C.RESET}")
    br = "+" if is_windows() else "╚"
    print(f"{C.BLUE}{br}{h * 43}{C.RESET}\n")
    
    # Backup si existe
    if opencode_dir.exists() and not skip_backup:
        backup_dir = Path.home() / f".opencode.backup"
        step(f"Backing up existing installation...")
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(opencode_dir, backup_dir)
        success(f"Backup saved to {backup_dir}")
    elif opencode_dir.exists():
        step(f"Updating existing installation...")
    
    # Crear directorios
    step(f"Creating directories in {config_dir}...")
    dirs = [
        config_dir,
        config_dir / ".team",
        get_opencode_bin_dir(),
        config_dir / "templates",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    success(f"Created {len(dirs)} directories")
    
    # Copiar archivos
    step(f"Copying files...")
    
    # Agent principal
    src_agent = install_dir / "agents" / "pepe_la_tiza.md"
    dst_agent = config_dir / "agents" / "pepe_la_tiza.md"
    if src_agent.exists():
        shutil.copy2(src_agent, dst_agent)
        success(f"Agent principal: {dst_agent.name}")
    
    # Sub-agentes
    src_team = install_dir / "agents" / ".team"
    dst_team = config_dir / ".team"
    copied = 0
    if src_team.exists():
        for agent in src_team.glob("*.md"):
            shutil.copy2(agent, dst_team / agent.name)
            copied += 1
    success(f"Sub-agentes: {copied}")
    
    # Binaries
    src_bin = install_dir / "bin"
    dst_bin = get_opencode_bin_dir()
    copied_bin = 0
    if src_bin.exists():
        for script in src_bin.glob("*"):
            if script.is_file():
                dst_script = dst_bin / script.name
                shutil.copy2(script, dst_script)
                # Solo chmod en Unix
                if not is_windows():
                    os.chmod(dst_script, 0o755)
                copied_bin += 1
    success(f"Binaries: {copied_bin}")
    
    # Templates
    src_templates = install_dir / "templates"
    dst_templates = config_dir / "templates"
    copied_templates = 0
    if src_templates.exists():
        for template in src_templates.glob("*.md"):
            shutil.copy2(template, dst_templates / template.name)
            copied_templates += 1
    success(f"Templates: {copied_templates}")
    
    # Configuración de OpenCode (opcional)
    src_config = install_dir / ".opencode" / "agents.json"
    dst_config = config_dir / "agents.json"
    if src_config.exists():
        step(f"Copying OpenCode config...")
        shutil.copy2(src_config, dst_config)
        success(f"OpenCode config")
    
    # Docs
    src_docs = install_dir / ".opencode" / "README.md"
    dst_docs = config_dir / "README.md"
    if src_docs.exists():
        shutil.copy2(src_docs, dst_docs)
        success(f"Documentation")
    
    # Resumen
    print(f"\n{C.BLUE}{tl}{h * 43}{C.RESET}")
    print(f"{C.GREEN}Pepe_la_tiza installed successfully!{C.RESET}")
    print(f"{C.BLUE}{br}{h * 43}{C.RESET}\n")
    
    print("Files installed:")
    print(f"  - Agent principal: {config_dir}/agents/pepe_la_tiza.md")
    print(f"  - Sub-agentes:   {config_dir}/.team/")
    print(f"  - Dashboard:   {dst_bin}/workflow-status.py")
    print(f"  - Templates:   {config_dir}/templates/")
    
    print("\nTo use in OpenCode:")
    print(f"  {C.CYAN}1.{C.RESET} Run {C.BOLD}/agent pepe_la_tiza{C.RESET}")
    print(f"  {C.CYAN}2.{C.RESET} Say {C.BOLD}hola{C.RESET} to start")
    
    return 0


def main() -> int:
    import argparse
    
    parser = argparse.ArgumentParser(description="Install Pepe_la_tiza")
    parser.add_argument("--skip-backup", action="store_true", help="Skip backup")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall")
    args = parser.parse_args()
    
    if args.uninstall:
        config_dir = get_config_dir()
        if config_dir.exists():
            import shutil
            shutil.rmtree(config_dir)
            print(f"{C.GREEN}Uninstalled from {config_dir}{C.RESET}")
            return 0
        else:
            print(f"{C.YELLOW}Not installed{C.RESET}")
            return 1
    
    return install(skip_backup=args.skip_backup)


if __name__ == "__main__":
    sys.exit(main())