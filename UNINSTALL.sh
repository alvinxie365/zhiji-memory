# 识海插件 · 卸载脚本

set -e

echo "🔮 识海插件卸载程序"
echo "===================="

if [ -z "$HERMES_HOME" ]; then
    HERMES_HOME="$HOME/.hermes"
fi

PLUGIN_DIR="$HERMES_HOME/plugins/zhiji_memory"

echo "📁 HERMES_HOME: $HERMES_HOME"
echo "📁 插件目录: $PLUGIN_DIR"

# 1. 备份重要数据
BACKUP_DIR="$HERMES_HOME/sea.backup_$(date +%Y%m%d%H%M%S)"
if [ -d "$HERMES_HOME/sea" ]; then
    echo "📦 正在备份识海数据到 $BACKUP_DIR"
    cp -r "$HERMES_HOME/sea" "$BACKUP_DIR"
    echo "✅ 识海数据已备份"
fi

# 2. 恢复 config.yaml（移除 memory.provider 配置）
CONFIG_FILE="$HERMES_HOME/config.yaml"
if [ -f "$CONFIG_FILE" ] && grep -q "memory.provider: zhiji_memory" "$CONFIG_FILE"; then
    echo "🔧 正在恢复 config.yaml"
    sed -i '' 's/memory.provider: zhiji_memory//g' "$CONFIG_FILE"
    echo "✅ config.yaml 已恢复"
fi

# 3. 删除插件目录
if [ -d "$PLUGIN_DIR" ]; then
    echo "🗑️ 正在删除插件目录"
    rm -rf "$PLUGIN_DIR"
    echo "✅ 插件目录已删除"
fi

echo ""
echo "===================="
echo "✅ 卸载完成！"
echo ""
echo "📌 如需完全清除，请手动删除："
echo "   - $BACKUP_DIR（识海数据备份）"
echo "   - ~/.hermes/scripts/zhiji-daily-backup.sh（备份脚本）"
