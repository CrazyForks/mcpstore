import uvicorn
import typer
import asyncio
import sys
from typing_extensions import Annotated
from mcpstore.scripts.app import app  # 导入 app 对象
import logging

# 导入独立运行模式


# Set up logging for the CLI itself
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
cli_logger = logging.getLogger("cli_main")


app_cli = typer.Typer(no_args_is_help=True)

@app_cli.callback()
def callback():
    """
    MCP Store Command Line Interface.
    """
    cli_logger.info("【第4步】Typer 回调函数已执行，准备分发子命令。")
    pass

@app_cli.command()
def api(
    host: Annotated[
        str, typer.Option(help="The host to bind to.")
    ] = "0.0.0.0",
    port: Annotated[
        int, typer.Option(help="The port to bind to.")
    ] = 18611,
    reload: Annotated[
        bool,
        typer.Option(
            help="Enable auto-reloading.",
        ),
    ] = False,
):
    """启动 mcpstore API 服务"""
    cli_logger.info(f"【第5步】Typer 已成功匹配到 'api' 命令。")
    cli_logger.info(f"    - 接收到参数 Host: {host}")
    cli_logger.info(f"    - 接收到参数 Port: {port}")
    cli_logger.info(f"    - 接收到参数 Reload: {reload}")
    cli_logger.info("【第6步】CLI 任务完成，准备将控制权移交给 Uvicorn。")
    uvicorn.run("mcpstore.scripts.app:app", host=host, port=port, reload=reload)

def main():
    cli_logger.info("【第3步】Typer 主应用已启动，准备解析命令行参数。")
    app_cli()

if __name__ == "__main__":
    cli_logger.info("【第1步】命令行入口 (__name__ == '__main__') 已触发。")
    cli_logger.info("【第2步】即将调用 main() 函数。")
    main() 
