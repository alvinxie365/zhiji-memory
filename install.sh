# 识海插件 · 安装脚本

set -e

echo "🔮 识海插件安装程序"
echo "===================="

# 检测 HERMES_HOME
if [ -z "$HERMES_HOME" ]; then
    HERMES_HOME="$HOME/.hermes"
fi

PLUGIN_DIR="$HERMES_HOME/plugins/zhiji_memory"
BACKUP_DIR="$HERMES_HOME/plugins/zhiji_memory.backup_$(date +%Y%m%d%H%M%S)"

echo "📁 HERMES_HOME: $HERMES_HOME"

# 1. 检查 hermes-agent 是否存在
if [ ! -d "$HERMES_HOME" ]; then
    echo "❌ 错误：未找到 hermes-agent 配置目录 ($HERMES_HOME)"
    echo "   请先安装 hermes-agent：https://github.com/nousresearch/hermes-agent"
    exit 1
fi

echo "✅ hermes-agent 目录存在"

# 2. 如果已存在旧版本，先备份
if [ -d "$PLUGIN_DIR" ]; then
    echo "📦 检测到旧版本，正在备份到 $BACKUP_DIR"
    mv "$PLUGIN_DIR" "$BACKUP_DIR"
fi

# 3. 创建插件目录
mkdir -p "$PLUGIN_DIR"

# 4. 复制插件文件
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/__init__.py" "$PLUGIN_DIR/"
cp "$SCRIPT_DIR/plugin.yaml" "$PLUGIN_DIR/"
cp "$SCRIPT_DIR/zhiji_memory_provider.py" "$PLUGIN_DIR/"

echo "✅ 插件文件已复制"

# 5. 启用插件（修改 config.yaml）
CONFIG_FILE="$HERMES_HOME/config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    if grep -q "memory.provider:" "$CONFIG_FILE"; then
        # 已存在 memory.provider 配置
        if grep -q "memory.provider: zhiji_memory" "$CONFIG_FILE"; then
            echo "✅ memory.provider 已配置为 zhiji_memory"
        else
            echo "⚠️ 发现其他 memory.provider 配置，请手动检查 $CONFIG_FILE"
        fi
    else
        # 添加 memory.provider 配置
        echo "" >> "$CONFIG_FILE"
        echo "memory.provider: zhiji_memory" >> "$CONFIG_FILE"
        echo "✅ 已添加 memory.provider: zhiji_memory"
    fi
else
    echo "⚠️ 未找到 config.yaml，请手动添加: memory.provider: zhiji_memory"
fi

# 6. 清理 __pycache__
find "$PLUGIN_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "===================="
echo "✅ 安装完成！"
echo ""
echo "📖 详细文档：https://feishu.cn/docx/Q0Uodru86oxCHAxoutmcIEJ6nJf"
echo "🐛 问题反馈：https://github.com/alvinxie365/zhiji-memory/issues"
echo ""
echo "🚀 重启 hermes-agent 即可生效"
