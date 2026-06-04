# 响应结构

统一的 API 响应格式，适用于 Store/Agent 视角的所有接口。

## 通用字段
| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| `success` | bool | 是否成功 |
| `message` | str | 描述信息 |
| `data` | object | 具体数据载体，结构随接口而定 |
| `timestamp` | int | 毫秒时间戳 |
| `error_code` | str | 失败时的错误码（可选） |
| `details` | object | 失败时的附加信息（可选） |
| `pagination` | object | 分页接口返回，含 `page`/`limit`/`total`（可选） |

## 错误码示例
- `CONFIGURATION_ERROR`：配置格式或校验失败
- `SERVICE_NOT_FOUND`：服务不存在
- `TOOL_NOT_FOUND`：工具不存在
- `VALIDATION_ERROR`：请求参数校验失败
- `INTERNAL_ERROR`：服务内部错误

## 示例
```json
{
  "success": true,
  "message": "ok",
  "data": {...},
  "timestamp": 1735718400000
}
```
```json
{
  "success": false,
  "message": "服务不存在",
  "error_code": "SERVICE_NOT_FOUND",
  "details": {"name": "weather"},
  "timestamp": 1735718400000
}
```
