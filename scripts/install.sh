#!/bin/bash
#
# Pepe_la_tiza Installer
# Meta-agente de IA bajo el sello Gentleman
#
set -e

AGENTS_DIR="${HOME}/.opencode/agents"
TEAM_DIR="${HOME}/.opencode/.team"

echo "🎭 Instalando Pepe_la_tiza..."

# Crear directorios si no existen
mkdir -p "${AGENTS_DIR}"
mkdir -p "${TEAM_DIR}"

# Detectar si es una instalación nueva o actualización
if [ -d "${TEAM_DIR}" ] && [ "$(ls -A ${TEAM_DIR} 2>/dev/null)" ]; then
    echo "📦 Detectada instalación existente. Actualizando..."
    # Backup de la versión anterior
    BACKUP_DIR="${HOME}/.opencode.backup.$(date +%Y%m%d_%H%M%S)"
    mv "${HOME}/.opencode" "${BACKUP_DIR}"
    mkdir -p "${AGENTS_DIR}"
    mkdir -p "${TEAM_DIR}"
    echo "   Backup en: ${BACKUP_DIR}"
else
    echo "🆕 Instalación nueva"
fi

# Obtener la ruta del script para copiar desde ahí o del repo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Si hay archivos locales, usarlos; si no, descargar del repo
if [ -d "${SCRIPT_DIR}/../agents" ]; then
    echo "📁 Usando archivos locales..."
    cp "${SCRIPT_DIR}/../agents/pepe_la_tiza.md" "${AGENTS_DIR}/"
    cp -r "${SCRIPT_DIR}/../.team/"* "${TEAM_DIR}/"
else
    echo "🌐 Descargando del repositorio..."
    TEMP_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/ArduinGlaber/Pepe_la_tiza.git "${TEMP_DIR}"
    cp "${TEMP_DIR}/agents/pepe_la_tiza.md" "${AGENTS_DIR}/"
    cp -r "${TEMP_DIR}/.team/"* "${TEAM_DIR}/"
    rm -rf "${TEMP_DIR}"
fi

echo ""
echo "✅ Pepe_la_tiza instalado exitosamente!"
echo ""
echo "Para usar Pepe_la_tiza en OpenCode:"
echo "  1. Ejecuta /agent pepe_la_tiza"
echo "  2. O simplemente empieza a chatear"
echo ""
echo "Ubicación: ${AGENTS_DIR}/pepe_la_tiza.md"
echo "Agentes internos: ${TEAM_DIR}/"
