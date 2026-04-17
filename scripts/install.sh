#!/bin/bash
#
# Pepe_la_tiza Installer
# Meta-agente de IA bajo el sello Gentleman
#
set -e

INSTALL_DIR="${HOME}/.opencode/agents"
INTERNAL_DIR="${INSTALL_DIR}/internal"

echo "🎭 Instalando Pepe_la_tiza..."

# Crear directorios si no existen
mkdir -p "${INSTALL_DIR}"
mkdir -p "${INTERNAL_DIR}"

# Detectar si es una instalación nueva o actualización
if [ -d "${INTERNAL_DIR}" ] && [ "$(ls -A ${INTERNAL_DIR} 2>/dev/null)" ]; then
    echo "📦 Detectada instalación existente. Actualizando..."
    # Backup de la versión anterior
    BACKUP_DIR="${HOME}/.opencode/agents.backup.$(date +%Y%m%d_%H%M%S)"
    mv "${INSTALL_DIR}" "${BACKUP_DIR}"
    mkdir -p "${INSTALL_DIR}"
    mkdir -p "${INTERNAL_DIR}"
    echo "   Backup en: ${BACKUP_DIR}"
else
    echo "🆕 Instalación nueva"
fi

# Obtener la ruta del script para copiar desde ahí o del repo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Si hay archivos locales, usarlos; si no, descargar del repo
if [ -d "${SCRIPT_DIR}/../agents" ]; then
    echo "📁 Usando archivos locales..."
    cp "${SCRIPT_DIR}/../agents/pepe_la_tiza.md" "${INSTALL_DIR}/"
    cp -r "${SCRIPT_DIR}/../agents/internal/"* "${INTERNAL_DIR}/"
else
    echo "🌐 Descargando del repositorio..."
    TEMP_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/ArduinGlaber/Pepe_la_tiza.git "${TEMP_DIR}"
    cp "${TEMP_DIR}/agents/pepe_la_tiza.md" "${INSTALL_DIR}/"
    cp -r "${TEMP_DIR}/agents/internal/"* "${INTERNAL_DIR}/"
    rm -rf "${TEMP_DIR}"
fi

echo ""
echo "✅ Pepe_la_tiza instalado exitosamente!"
echo ""
echo "Para usar Pepe_la_tiza en OpenCode:"
echo "  1. Ejecuta /agent pepe_la_tiza"
echo "  2. O simplemente empieza a chatear"
echo ""
echo "Ubicación: ${INSTALL_DIR}/pepe_la_tiza.md"
