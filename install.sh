# 识海插件 · 安装脚本
# Zhiji Memory Plugin · Install Script

set -e

echo "🔮 识海插件安装程序"
echo "========================================"
echo "🔮 Zhiji Memory Plugin Installation"
echo "========================================"

# Detect HERMES_HOME
if [ -z "$HERMES_HOME" ]; then
    HERMES_HOME="$HOME/.hermes"
fi

PLUGIN_DIR="$HERMES_HOME/plugins/zhiji_memory"
BACKUP_DIR="$HERMES_HOME/plugins/zhiji_memory.backup_$(date +%Y%m%d%H%M%S)"

echo ""
echo "📁 HERMES_HOME: $HERMES_HOME"
echo "📁 Plugin directory: $PLUGIN_DIR"
echo ""

# 1. Check hermes-agent exists
if [ ! -d "$HERMES_HOME" ]; then
    echo "❌ Error: hermes-agent config directory not found ($HERMES_HOME)"
    echo "   Please install hermes-agent first: https://github.com/nousresearch/hermes-agent"
    exit 1
fi
echo "✅ hermes-agent directory found"

# 2. Backup old version if exists
if [ -d "$PLUGIN_DIR" ]; then
    echo ""
    echo "📦 Old version detected, backing up to:"
    echo "   $BACKUP_DIR"
    mv "$PLUGIN_DIR" "$BACKUP_DIR"
    echo "✅ Backup complete"
fi

# 3. Create plugin directory
mkdir -p "$PLUGIN_DIR"

# 4. Copy plugin files
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/__init__.py" "$PLUGIN_DIR/"
cp "$SCRIPT_DIR/plugin.yaml" "$PLUGIN_DIR/"
cp "$SCRIPT_DIR/zhiji_memory_provider.py" "$PLUGIN_DIR/"

echo "✅ Plugin files copied"

# 5. Enable plugin in config.yaml
CONFIG_FILE="$HERMES_HOME/config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    if grep -q "memory.provider:" "$CONFIG_FILE"; then
        if grep -q "memory.provider: zhiji_memory" "$CONFIG_FILE"; then
            echo "✅ memory.provider already configured as zhiji_memory"
        else
            echo "⚠️ Another memory.provider is configured. Please check: $CONFIG_FILE"
        fi
    else
        echo "" >> "$CONFIG_FILE"
        echo "memory.provider: zhiji_memory" >> "$CONFIG_FILE"
        echo "✅ Added memory.provider: zhiji_memory to config.yaml"
    fi
else
    echo "⚠️ config.yaml not found. Please add manually: memory.provider: zhiji_memory"
fi

# 6. Clean pycache
find "$PLUGIN_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "========================================"
echo "✅ Installation complete!"
echo "========================================"
echo ""
echo "📖 Documentation:"
echo "   🌐 Bilingual: https://feishu.cn/docx/MKC0ddVyVoQEjsxU5koc6VR9nVc"
echo "   📦 GitHub:   https://github.com/alvinxie365/zhiji-memory"
echo ""
echo "🚀 Please restart hermes-agent to activate the plugin"
