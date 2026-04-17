#!/bin/bash
#
# Pepe_la_tiza Installer
# Meta-agente de IA bajo el sello Gentleman
#
set -e

AGENTS_DIR="${HOME}/.opencode/agents"
TEAM_DIR="${HOME}/.opencode/.team"
BIN_DIR="${HOME}/.opencode/bin"
TEMPLATES_DIR="${HOME}/.opencode/templates"

echo "🎭 Instalando Pepe_la_tiza..."

# Crear directorios si no existen
mkdir -p "${AGENTS_DIR}"
mkdir -p "${TEAM_DIR}"
mkdir -p "${BIN_DIR}"
mkdir -p "${TEMPLATES_DIR}"

# Detectar si es una instalación nueva o actualización
if [ -d "${TEAM_DIR}" ] && [ "$(ls -A ${TEAM_DIR} 2>/dev/null)" ]; then
    echo "📦 Detectada instalación existente. Actualizando..."
    # Backup de la versión anterior
    BACKUP_DIR="${HOME}/.opencode.backup.$(date +%Y%m%d_%H%M%S)"
    mv "${HOME}/.opencode" "${BACKUP_DIR}"
    mkdir -p "${AGENTS_DIR}"
    mkdir -p "${TEAM_DIR}"
    mkdir -p "${BIN_DIR}"
    mkdir -p "${TEMPLATES_DIR}"
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
    cp "${SCRIPT_DIR}/../bin/workflow-status" "${BIN_DIR}/"
    chmod +x "${BIN_DIR}/workflow-status"
    cp "${SCRIPT_DIR}/../templates/"* "${TEMPLATES_DIR}/"
else
    echo "🌐 Descargando del repositorio..."
    TEMP_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/ArduinGlaber/Pepe_la_tiza.git "${TEMP_DIR}"
    cp "${TEMP_DIR}/agents/pepe_la_tiza.md" "${AGENTS_DIR}/"
    cp -r "${TEMP_DIR}/.team/"* "${TEAM_DIR}/"
    cp "${TEMP_DIR}/bin/workflow-status" "${BIN_DIR}/"
    chmod +x "${BIN_DIR}/workflow-status"
    cp "${TEMP_DIR}/templates/"* "${TEMPLATES_DIR}/"
    rm -rf "${TEMP_DIR}"
fi

echo ""
echo "✅ Pepe_la_tiza instalado exitosamente!"
echo ""
echo "Para usar Pepe_la_tiza en OpenCode:"
echo "  1. Ejecuta /agent pepe_la_tiza"
echo "  2. O simplemente empieza a chatear"
echo ""
echo "Archivos instalados:"
echo "  - Agente principal: ${AGENTS_DIR}/pepe_la_tiza.md"
echo "  - Agentes internos: ${TEAM_DIR}/"
echo "  - CLI workflow-status: ${BIN_DIR}/workflow-status"
echo "  - Templates: ${TEMPLATES_DIR}/"
