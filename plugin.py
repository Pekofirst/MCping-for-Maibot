from typing import List, Tuple, Type, Optional
from src.plugin_system import BasePlugin, register_plugin, ComponentInfo,BaseCommand
from mcstatus import JavaServer
import random

class MCpingCommand(BaseCommand):
    command_name = "mcping"
    command_description = "这是一个查询我的世界服务器状态的命令"
    command_pattern = r"^信息$"
    async def execute(self) -> Tuple[bool, Optional[str], bool]:
            try:
                server = JavaServer.lookup("pekoserver.tech:18221")
                status = server.status()
                message = f"♥ 当前服务器人数：{status.players.online}服务器延迟{status.latency:.0f}ms♥"
                try:
                    query = server.query()
                    # 有完整列表则直接打印
                    message+=f"\n♥ 在线玩家：{', '.join(query.players.names)} ♥"
                except (ConnectionError, TimeoutError, IOError):
                    pass
                await self.send_text(message)
                return True,'success', True
            except Exception as e:
                    await self.send_text(f"♥ 查询出错：{str(e)} ♥")
                    return False,'error', True

class RollCommand(BaseCommand):
    # 命令名称
    command_name = "roll"
    # 命令描述
    command_description = "随机数/随机选择工具：无参数时生成1-120的随机数；跟参数时随机选一个参数；跟数字时随机一个数字"
    # 正则匹配模式：匹配roll开头，可选跟随任意参数（支持空格分隔的多个参数）
    command_pattern = r"^roll(?:\s+(?P<params>.+))?$"

    async def execute(self) -> Tuple[bool,Optional[str], bool]:
        try:
            # 获取命令匹配的参数（self.args 是正则匹配后的分组结果，不同框架可能略有差异，此处按原插件逻辑适配）
            # 正则分组1对应匹配到的参数部分，若无参数则为None
            command_args = self.matched_groups.get("params")

            if command_args:
                # 有参数：分割参数（按空格分割，支持多个参数）
                args_list = command_args.strip().split()
                if not args_list:  # 处理参数全是空格的情况
                    result = "♥ 参数格式错误！请输入有效参数（如 roll 苹果 香蕉 橘子）♥"
                elif len(args_list) == 1:
                     # 单个参数：判断是否为有效正整数
                    single_arg = args_list[0]
                    if single_arg.isdigit():
                        # 是数字：生成1到该数字的随机数
                        max_num = int(single_arg)
                        if max_num < 1:
                            result = "♥ 数字不能小于1！请输入正整数（如 roll 50）♥"
                        else:
                            random_num = random.randint(1, max_num)
                            result = f"♥ 随机数结果：{random_num}（范围1-{max_num}）♥"
                else:
                    # 随机选择一个参数
                    selected = random.choice(args_list)
                    result = f"♥ 随机选择结果：{selected} ♥"
            else:
                # 无参数：生成1-120的随机整数
                random_num = random.randint(1, 120)
                result = f"♥ 随机数结果：{random_num}（范围1-120）♥"

            # 发送结果文本
            await self.send_text(result)
            return True,"Success", True
        except Exception as e:
            # 异常处理：捕获所有可能的错误并提示
            await self.send_text(f"♥ 执行出错：{str(e)} ♥")
            return False,"error", True
@register_plugin # 注册插件
class MCpingPlugin(BasePlugin):
    # 以下是插件基本信息和方法（必须填写）
    plugin_name = "mcping"
    enable_plugin = True  # 启用插件
    dependencies = []  # 插件依赖列表（目前为空）
    python_dependencies = ["mcstatus"]  # Python依赖列表（目前为空）
    config_file_name = "config.toml"  # 配置文件名
    config_schema = {}  # 配置文件模式（目前为空）

    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]: # 获取插件组件
        return [(MCpingCommand.get_command_info(),MCpingCommand),(RollCommand.get_command_info(),RollCommand)]
    
