# mcpstore

A composable, ready-to-use MCP toolkit for agents and rapid integration.

## Features
- Modular MCP service orchestration
- Fast integration for intelligent agents
- Extensible plugin and configuration system
- Built on FastAPI, fastmcp, and httpx

## Installation
```bash
pip install mcpstore
```

## Quick Start

### 1. Configure Services (`mcp.json`)
Edit `src/mcpstore/data/mcp.json` to configure MCP services, for example:
```json
{
  "mcpServers": {
    "OfficialDemo": {
      "url": "http://127.0.0.1:8000/mcp"
    },
    "Amap": {
      "url": "https://mcp.amap.com/sse?key=YOUR_KEY"
    }
  }
}
```

### 2. Start the API Service
In the project root directory, run:
```bash
python -m mcpstore.cli.main api --reload
```
By default, the service listens on `0.0.0.0:18200`. You can customize with `--host` and `--port`.

### 3. Main API Endpoints
All endpoints follow RESTful conventions and support JSON interaction.

#### Health Check
- **GET /health**
- Returns the health status of all registered services.
```json
{
  "orchestrator_status": "running",
  "active_services": 2,
  "total_tools": 19,
  "services": [
    {"name": "OfficialDemo", "url": "http://127.0.0.1:8000/mcp", "status": "healthy", ...},
    {"name": "Amap", "url": "https://mcp.amap.com/sse?...", "status": "healthy", ...}
  ]
}
```

#### Service Registration & Configuration
- **POST /register**: Register a single service
- **POST /register/json**: Register multiple services
- **PUT /register/json**: Update multiple services
- **GET /register/json**: Get current service configuration

#### Tool Execution
- **POST /execute**
- Request body:
```json
{
  "service_name": "OfficialDemo",
  "tool_name": "OfficialDemo_get_current_weather",
  "parameters": {"city": "Beijing"}
}
```
- Response:
```json
{
  "result": [
    {"type": "text", "text": "Current weather in Beijing: Sunny"}
  ]
}
```

#### Service & Tool Information
- **GET /services**: List all service names
- **GET /tools**: List all tool information
- **GET /service_info?name=ServiceName**: Get details for a specific service

### 4. Typical Integration
- Integrate with agents, frontends, or automation scripts via RESTful API
- Unified orchestration and health monitoring for multiple services
- Plugin system for custom tools and services

## Project Structure
```
src/mcpstore/
    core/       # Core orchestration and management
    plugins/    # Plugin system
    config/     # Configuration management
    data/       # Data and schema files
    scripts/    # API and CLI scripts
```

## Contributing
Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/whillhill/mcpstore).

## License
MIT License. See [LICENSE](LICENSE) for details.
