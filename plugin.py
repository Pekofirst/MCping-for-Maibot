from typing import List, Tuple, Type
from src.plugin_system import BasePlugin, register_plugin, ComponentInfo,BaseCommand
from mcstatus import JavaServer


class MCpingCommand(BaseCommand):
    command_name = "mcping"
    command_description = "这是一个查询我的世界服务器状态的命令"
    command_pattern = r"/^信息$/"
    async def execute(self) -> Tuple[bool,  bool]:
            server = JavaServer.lookup("pekoserver.tech:18221")
            status = server.status()
            query = server.query()
            message = f"♥ 当前服务器人数：{status.players.online}服务器延迟{status.latency}♥\n♥在线玩家：{', '.join(query.players.names)}♥"
            await self.send_text(message)
            # ---- 执行命令的逻辑 ----
            return True, True  

@register_plugin # 注册插件
class HelloWorldPlugin(BasePlugin):
    """Hello World插件 - 你的第一个MaiCore插件"""

    # 以下是插件基本信息和方法（必须填写）
    plugin_name = "mcping"
    enable_plugin = True  # 启用插件
    dependencies = []  # 插件依赖列表（目前为空）
    python_dependencies = ["mcstatus"]  # Python依赖列表（目前为空）
    config_file_name = "config.toml"  # 配置文件名
    config_schema = {}  # 配置文件模式（目前为空）

    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]: # 获取插件组件
        return [MCpingCommand.get_command_info,MCpingCommand]
    
