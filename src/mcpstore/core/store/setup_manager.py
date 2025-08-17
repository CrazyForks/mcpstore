"""
设置管理器模块
负责处理 MCPStore 的初始化和设置相关功能
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class StoreSetupManager:
    """设置管理器 - 包含所有静态设置方法"""
    
    @staticmethod
    def setup_store(mcp_config_file: str = None, debug: bool = False, standalone_config=None,
                   tool_record_max_file_size: int = 30, tool_record_retention_days: int = 7,
                   monitoring: dict = None):
        """
        Initialize MCPStore instance

        Args:
            mcp_config_file: Custom mcp.json configuration file path, uses default path if not specified
                           🔧 New: This parameter now supports data space isolation, each JSON file path corresponds to an independent data space
            debug: Whether to enable debug logging, default is False (no debug info displayed)
            standalone_config: Standalone configuration object, if provided, does not depend on environment variables
            tool_record_max_file_size: Maximum size of tool record JSON file (MB), default 30MB, set to -1 for no limit
            tool_record_retention_days: Tool record retention days, default 7 days, set to -1 for no deletion
            monitoring: Monitoring configuration dictionary, optional parameters:
                - health_check_seconds: Health check interval (default 30 seconds)
                - tools_update_hours: Tool update interval (default 2 hours)
                - reconnection_seconds: Reconnection interval (default 60 seconds)
                - cleanup_hours: Cleanup interval (default 24 hours)
                - enable_tools_update: Whether to enable tool updates (default True)
                - enable_reconnection: Whether to enable reconnection (default True)
                - update_tools_on_reconnection: Whether to update tools on reconnection (default True)

                                 You can still manually call add_service method to add services

        Returns:
            MCPStore instance
        """
        # 🔧 New: Support standalone configuration
        if standalone_config is not None:
            return StoreSetupManager._setup_with_standalone_config(standalone_config, debug,
                                                        tool_record_max_file_size, tool_record_retention_days,
                                                        monitoring)

        # 🔧 New: Data space management
        if mcp_config_file is not None:
            return StoreSetupManager._setup_with_data_space(mcp_config_file, debug,
                                                 tool_record_max_file_size, tool_record_retention_days,
                                                 monitoring)

        # Original logic: Use default configuration
        from mcpstore.config.config import LoggingConfig
        from mcpstore.core.monitoring.config import MonitoringConfigProcessor

        LoggingConfig.setup_logging(debug=debug)

        # Process monitoring configuration
        processed_monitoring = MonitoringConfigProcessor.process_config(monitoring)
        orchestrator_config = MonitoringConfigProcessor.convert_to_orchestrator_config(processed_monitoring)

        from mcpstore.config.json_config import MCPConfig
        from mcpstore.core.registry import ServiceRegistry
        from mcpstore.core.orchestrator import MCPOrchestrator

        config = MCPConfig()
        registry = ServiceRegistry()

        # Merge base configuration and monitoring configuration
        base_config = config.load_config()
        base_config.update(orchestrator_config)

        orchestrator = MCPOrchestrator(base_config, registry)

        # Initialize orchestrator (including tool update monitor)
        import asyncio
        from mcpstore.core.async_sync_helper import AsyncSyncHelper

        # Use AsyncSyncHelper to properly manage async operations
        async_helper = AsyncSyncHelper()
        try:
            # Synchronously run orchestrator.setup(), ensure completion
            async_helper.run_async(orchestrator.setup())
        except Exception as e:
            logger.error(f"Failed to setup orchestrator: {e}")
            raise

        # Import MCPStore from store module to avoid circular import
        from mcpstore.core.store.base_store import BaseMCPStore
        from mcpstore.core.store.service_query import ServiceQueryMixin
        from mcpstore.core.store.tool_operations import ToolOperationsMixin
        from mcpstore.core.store.config_management import ConfigManagementMixin
        from mcpstore.core.store.data_space_manager import DataSpaceManagerMixin
        from mcpstore.core.store.api_server import APIServerMixin
        from mcpstore.core.store.context_factory import ContextFactoryMixin
        from mcpstore.core.store.setup_mixin import SetupMixin

        # Create MCPStore class dynamically to avoid circular import
        class MCPStore(
            ServiceQueryMixin,
            ToolOperationsMixin,
            ConfigManagementMixin,
            DataSpaceManagerMixin,
            APIServerMixin,
            ContextFactoryMixin,
            SetupMixin,
            BaseMCPStore
        ):
            pass

        store = MCPStore(orchestrator, config, tool_record_max_file_size, tool_record_retention_days)

        # 🔧 新增：设置orchestrator的store引用（用于统一注册架构）
        orchestrator.store = store

        # 🔧 新增：初始化缓存
        logger.info("🔄 [SETUP_STORE] 开始初始化缓存...")
        try:
            async_helper.run_async(store.initialize_cache_from_files())
            logger.info("✅ [SETUP_STORE] 缓存初始化完成")
        except Exception as e:
            logger.error(f"❌ [SETUP_STORE] 缓存初始化失败: {e}")
            import traceback
            logger.error(f"❌ [SETUP_STORE] 缓存初始化失败详情: {traceback.format_exc()}")
            # 缓存初始化失败不应该阻止系统启动

        return store

    @staticmethod
    def _setup_with_data_space(mcp_config_file: str, debug: bool = False,
                              tool_record_max_file_size: int = 30, tool_record_retention_days: int = 7,
                              monitoring: dict = None):
        """
        Initialize MCPStore with data space (supports independent data directory)

        Args:
            mcp_config_file: MCP JSON configuration file path (data space root directory)
            debug: Whether to enable debug logging
            tool_record_max_file_size: Maximum size of tool record JSON file (MB)
            tool_record_retention_days: Tool record retention days
            monitoring: Monitoring configuration dictionary

        Returns:
            MCPStore instance
        """
        from mcpstore.config.config import LoggingConfig
        from mcpstore.core.data_space_manager import DataSpaceManager
        from mcpstore.core.monitoring.config import MonitoringConfigProcessor

        # Setup logging
        LoggingConfig.setup_logging(debug=debug)

        try:
            # Initialize data space
            data_space_manager = DataSpaceManager(mcp_config_file)
            if not data_space_manager.initialize_workspace():
                raise RuntimeError(f"Failed to initialize workspace for: {mcp_config_file}")

            logger.info(f"Data space initialized: {data_space_manager.workspace_dir}")

            # Process monitoring configuration
            processed_monitoring = MonitoringConfigProcessor.process_config(monitoring)
            orchestrator_config = MonitoringConfigProcessor.convert_to_orchestrator_config(processed_monitoring)

            # Create configuration using specified MCP JSON file
            from mcpstore.config.json_config import MCPConfig
            from mcpstore.core.registry import ServiceRegistry
            from mcpstore.core.orchestrator import MCPOrchestrator

            config = MCPConfig(json_path=mcp_config_file)
            registry = ServiceRegistry()

            # Get file paths in data space (using defaults subdirectory)
            client_services_path = str(data_space_manager.get_file_path("defaults/client_services.json"))
            agent_clients_path = str(data_space_manager.get_file_path("defaults/agent_clients.json"))

            # Merge base configuration and monitoring configuration
            base_config = config.load_config()
            base_config.update(orchestrator_config)

            # Create orchestrator with data space support, pass correct mcp_config instance
            orchestrator = MCPOrchestrator(
                base_config,
                registry,
                client_services_path=client_services_path,
                agent_clients_path=agent_clients_path,
                mcp_config=config  # Pass in the config instance of data space
            )

            # 🔧 重构：为数据空间模式设置FastMCP适配器的工作目录
            from mcpstore.core.local_service_manager import set_local_service_manager_work_dir
            set_local_service_manager_work_dir(str(data_space_manager.workspace_dir))

            # Import MCPStore components to avoid circular import
            from mcpstore.core.store.base_store import BaseMCPStore
            from mcpstore.core.store.service_query import ServiceQueryMixin
            from mcpstore.core.store.tool_operations import ToolOperationsMixin
            from mcpstore.core.store.config_management import ConfigManagementMixin
            from mcpstore.core.store.data_space_manager import DataSpaceManagerMixin
            from mcpstore.core.store.api_server import APIServerMixin
            from mcpstore.core.store.context_factory import ContextFactoryMixin
            from mcpstore.core.store.setup_mixin import SetupMixin

            # Create MCPStore class dynamically
            class MCPStore(
                ServiceQueryMixin,
                ToolOperationsMixin,
                ConfigManagementMixin,
                DataSpaceManagerMixin,
                APIServerMixin,
                ContextFactoryMixin,
                SetupMixin,
                BaseMCPStore
            ):
                pass

            # Create store instance and set data space manager
            store = MCPStore(orchestrator, config, tool_record_max_file_size, tool_record_retention_days)
            store._data_space_manager = data_space_manager

            # 🔧 新增：设置orchestrator的store引用（用于统一注册架构）
            orchestrator.store = store

            # Initialize orchestrator (including tool update monitor)
            from mcpstore.core.async_sync_helper import AsyncSyncHelper

            # Use AsyncSyncHelper to properly manage async operations
            async_helper = AsyncSyncHelper()
            try:
                # Run orchestrator.setup() synchronously, ensure completion
                async_helper.run_async(orchestrator.setup())
            except Exception as e:
                logger.error(f"Failed to setup orchestrator: {e}")
                raise

            # 🔧 新增：初始化缓存
            try:
                async_helper.run_async(store.initialize_cache_from_files())
            except Exception as e:
                logger.warning(f"Failed to initialize cache from files: {e}")
                # 缓存初始化失败不应该阻止系统启动

            logger.info(f"MCPStore setup with data space completed: {mcp_config_file}")
            return store

        except Exception as e:
            logger.error(f"Failed to setup MCPStore with data space: {e}")
            raise

    @staticmethod
    def _setup_with_standalone_config(standalone_config, debug: bool = False,
                                     tool_record_max_file_size: int = 30, tool_record_retention_days: int = 7,
                                     monitoring: dict = None):
        """
        使用独立配置初始化MCPStore（不依赖环境变量）

        Args:
            standalone_config: 独立配置对象
            debug: 是否启用调试日志
            tool_record_max_file_size: 工具记录JSON文件最大大小(MB)
            tool_record_retention_days: 工具记录保留天数
            monitoring: 监控配置字典

        Returns:
            MCPStore实例
        """
        from mcpstore.core.standalone_config import StandaloneConfigManager, StandaloneConfig
        from mcpstore.core.registry import ServiceRegistry
        from mcpstore.core.orchestrator import MCPOrchestrator
        from mcpstore.core.monitoring.config import MonitoringConfigProcessor
        import logging

        # 处理配置类型
        if isinstance(standalone_config, StandaloneConfig):
            config_manager = StandaloneConfigManager(standalone_config)
        elif isinstance(standalone_config, StandaloneConfigManager):
            config_manager = standalone_config
        else:
            raise ValueError("standalone_config must be StandaloneConfig or StandaloneConfigManager")

        # 设置日志
        log_level = logging.DEBUG if debug or config_manager.config.enable_debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format=config_manager.config.log_format
        )

        # 处理监控配置
        processed_monitoring = MonitoringConfigProcessor.process_config(monitoring)
        monitoring_orchestrator_config = MonitoringConfigProcessor.convert_to_orchestrator_config(processed_monitoring)

        # 创建组件
        registry = ServiceRegistry()

        # 使用独立配置创建orchestrator
        mcp_config_dict = config_manager.get_mcp_config()
        timing_config = config_manager.get_timing_config()

        # 创建一个兼容的配置对象
        class StandaloneMCPConfig:
            def __init__(self, config_dict, config_manager):
                self._config = config_dict
                self._manager = config_manager
                self.json_path = config_manager.config.mcp_config_file or ":memory:"

            def load_config(self):
                return self._config

            def get_service_config(self, name):
                return self._manager.get_service_config(name)

        config = StandaloneMCPConfig(mcp_config_dict, config_manager)

        # 创建orchestrator，合并所有配置
        orchestrator_config = mcp_config_dict.copy()
        orchestrator_config["timing"] = timing_config
        orchestrator_config["network"] = config_manager.get_network_config()
        orchestrator_config["environment"] = config_manager.get_environment_config()

        # 合并监控配置（监控配置优先级更高）
        orchestrator_config.update(monitoring_orchestrator_config)

        orchestrator = MCPOrchestrator(orchestrator_config, registry, config_manager)

        # 初始化orchestrator（包括工具更新监控器）
        import asyncio
        try:
            # 尝试在当前事件循环中运行
            loop = asyncio.get_running_loop()
            # 如果已有事件循环，创建任务稍后执行
            asyncio.create_task(orchestrator.setup())
        except RuntimeError:
            # 没有运行的事件循环，创建新的
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(orchestrator.setup())
            finally:
                loop.close()

        from mcpstore.core.store import MCPStore
        return MCPStore(orchestrator, config, tool_record_max_file_size, tool_record_retention_days)
