# 生命周期管理示例

本文档提供 MCPStore 服务生命周期管理的完整实际示例，涵盖监控、故障恢复、配置优化等各种场景。

## 🚀 基础生命周期管理

### 服务状态监控

```python
from mcpstore import MCPStore
from mcpstore.core.models.service import ServiceConnectionState
import time

def monitor_service_states():
    """监控服务状态变化"""
    store = MCPStore.setup_store()
    
    # 注册测试服务
    store.for_store().add_service({
        "name": "test_service",
        "url": "https://httpbin.org/delay/2"  # 模拟慢响应
    })
    
    print("🔍 开始监控服务状态变化...")
    last_states = {}
    
    for i in range(120):  # 监控2分钟
        services = store.for_store().list_services()
        
        for service in services:
            current_state = service.status
            last_state = last_states.get(service.name)
            
            if current_state != last_state:
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] 🔄 {service.name}: {last_state} → {current_state}")
                last_states[service.name] = current_state
                
                # 获取详细状态信息
                service_info = store.for_store().get_service_info(service.name)
                if service_info and service_info.state_metadata:
                    metadata = service_info.state_metadata
                    print(f"         失败次数: {metadata.consecutive_failures}")
                    print(f"         重连次数: {metadata.reconnect_attempts}")
                    if metadata.error_message:
                        print(f"         错误信息: {metadata.error_message}")
        
        time.sleep(1)

# 使用
monitor_service_states()
```

### 生命周期事件处理

```python
def lifecycle_event_handler():
    """生命周期事件处理器"""
    store = MCPStore.setup_store()
    
    def on_service_state_change(service_name, old_state, new_state, metadata):
        """服务状态变化回调"""
        print(f"📢 服务状态变化事件:")
        print(f"   服务: {service_name}")
        print(f"   状态: {old_state} → {new_state}")
        
        # 根据状态变化执行不同操作
        if new_state == ServiceConnectionState.WARNING:
            print(f"⚠️ 服务 {service_name} 进入警告状态，开始密切监控")
            
        elif new_state == ServiceConnectionState.RECONNECTING:
            print(f"🔄 服务 {service_name} 开始重连，预计恢复时间: 30-60秒")
            
        elif new_state == ServiceConnectionState.UNREACHABLE:
            print(f"❌ 服务 {service_name} 不可达，考虑手动干预")
            # 可以在这里发送告警
            # send_alert(service_name, new_state, metadata.error_message)
            
        elif new_state == ServiceConnectionState.HEALTHY:
            print(f"✅ 服务 {service_name} 恢复健康")
    
    # 注册事件处理器（伪代码，实际需要根据具体实现）
    # store._orchestrator.lifecycle_manager.on_state_change = on_service_state_change
    
    return on_service_state_change

# 使用
handler = lifecycle_event_handler()
```

## 🛡️ 故障恢复管理

### 自动故障恢复

```python
def auto_recovery_system():
    """自动故障恢复系统"""
    store = MCPStore.setup_store()
    
    def check_and_recover():
        """检查并恢复故障服务"""
        services = store.for_store().list_services()
        
        for service in services:
            if service.status == ServiceConnectionState.UNREACHABLE:
                print(f"🔧 检测到不可达服务: {service.name}")
                
                # 获取详细信息
                service_info = store.for_store().get_service_info(service.name)
                if service_info and service_info.state_metadata:
                    metadata = service_info.state_metadata
                    
                    # 检查服务不可达时间
                    if metadata.state_entered_time:
                        from datetime import datetime
                        duration = datetime.now() - metadata.state_entered_time
                        
                        if duration.total_seconds() > 300:  # 5分钟
                            print(f"   服务已不可达 {duration.total_seconds():.0f} 秒，尝试重启")
                            
                            try:
                                # 尝试重启服务
                                success = store.for_store().restart_service(service.name)
                                if success:
                                    print(f"   ✅ 服务 {service.name} 重启成功")
                                else:
                                    print(f"   ❌ 服务 {service.name} 重启失败")
                                    
                                    # 重启失败，尝试重新注册
                                    if service_info.config:
                                        print(f"   🔄 尝试重新注册服务 {service.name}")
                                        store.for_store().remove_service(service.name)
                                        store.for_store().add_service(service_info.config)
                                        
                            except Exception as e:
                                print(f"   ❌ 恢复服务 {service.name} 时出错: {e}")
    
    # 定期检查和恢复
    import threading
    import time
    
    def recovery_loop():
        while True:
            try:
                check_and_recover()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                print(f"自动恢复系统错误: {e}")
                time.sleep(120)  # 出错时等待更长时间
    
    recovery_thread = threading.Thread(target=recovery_loop, daemon=True)
    recovery_thread.start()
    
    print("🛡️ 自动故障恢复系统已启动")
    return recovery_thread

# 使用
recovery_thread = auto_recovery_system()
```

### 手动故障诊断和恢复

```python
def manual_recovery_toolkit():
    """手动故障恢复工具包"""
    store = MCPStore.setup_store()
    
    def diagnose_service(service_name):
        """诊断单个服务"""
        print(f"🔍 诊断服务: {service_name}")
        print("=" * 40)
        
        service_info = store.for_store().get_service_info(service_name)
        if not service_info:
            print("❌ 服务不存在")
            return False
        
        print(f"当前状态: {service_info.status}")
        print(f"服务类型: {'远程服务' if service_info.url else '本地服务'}")
        
        if service_info.state_metadata:
            metadata = service_info.state_metadata
            print(f"连续失败: {metadata.consecutive_failures}")
            print(f"重连次数: {metadata.reconnect_attempts}")
            print(f"最后成功: {metadata.last_success_time}")
            print(f"最后失败: {metadata.last_failure_time}")
            print(f"响应时间: {metadata.response_time}ms")
            
            if metadata.error_message:
                print(f"错误信息: {metadata.error_message}")
        
        # 执行健康检查
        print("\n🏥 执行健康检查...")
        health_info = store.for_store().check_services()
        
        # 查找当前服务的健康信息
        for health in health_info:
            if health.name == service_name:
                print(f"健康状态: {health.status}")
                print(f"响应时间: {health.response_time:.2f}ms")
                print(f"成功率: {health.success_rate:.1f}%")
                break
        
        return True
    
    def recover_service(service_name):
        """恢复单个服务"""
        print(f"🔧 恢复服务: {service_name}")
        
        # 方法1: 重启服务
        print("尝试重启服务...")
        success = store.for_store().restart_service(service_name)
        if success:
            print("✅ 重启成功")
            return True
        
        # 方法2: 重新注册服务
        print("重启失败，尝试重新注册...")
        service_info = store.for_store().get_service_info(service_name)
        if service_info and service_info.config:
            try:
                store.for_store().remove_service(service_name)
                store.for_store().add_service(service_info.config)
                print("✅ 重新注册成功")
                return True
            except Exception as e:
                print(f"❌ 重新注册失败: {e}")
        
        print("❌ 所有恢复方法都失败了")
        return False
    
    def batch_recovery():
        """批量恢复故障服务"""
        services = store.for_store().list_services()
        problem_services = [
            s for s in services 
            if s.status in [
                ServiceConnectionState.UNREACHABLE,
                ServiceConnectionState.RECONNECTING
            ]
        ]
        
        if not problem_services:
            print("✅ 没有发现问题服务")
            return
        
        print(f"🚨 发现 {len(problem_services)} 个问题服务")
        
        for service in problem_services:
            print(f"\n处理服务: {service.name}")
            diagnose_service(service.name)
            
            user_input = input(f"是否尝试恢复服务 {service.name}? (y/n): ")
            if user_input.lower() == 'y':
                recover_service(service.name)
    
    return {
        'diagnose': diagnose_service,
        'recover': recover_service,
        'batch_recovery': batch_recovery
    }

# 使用
toolkit = manual_recovery_toolkit()

# 诊断特定服务
# toolkit['diagnose']('weather')

# 恢复特定服务
# toolkit['recover']('weather')

# 批量恢复
# toolkit['batch_recovery']()
```

## 📊 高级监控和分析

### 性能分析仪表板

```python
def performance_dashboard():
    """性能分析仪表板"""
    import time
    import os
    from collections import defaultdict, deque
    
    store = MCPStore.setup_store()
    
    # 性能数据收集器
    performance_data = defaultdict(lambda: {
        'response_times': deque(maxlen=100),
        'success_count': 0,
        'failure_count': 0,
        'state_history': deque(maxlen=50)
    })
    
    def collect_performance_data():
        """收集性能数据"""
        services = store.for_store().list_services()
        
        for service in services:
            service_data = performance_data[service.name]
            
            # 记录状态历史
            service_data['state_history'].append({
                'timestamp': time.time(),
                'state': service.status
            })
            
            # 获取详细信息
            service_info = store.for_store().get_service_info(service.name)
            if service_info and service_info.state_metadata:
                metadata = service_info.state_metadata
                
                if metadata.response_time:
                    service_data['response_times'].append(metadata.response_time)
                
                if service.status == ServiceConnectionState.HEALTHY:
                    service_data['success_count'] += 1
                else:
                    service_data['failure_count'] += 1
    
    def display_dashboard():
        """显示仪表板"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("📊 MCPStore 性能分析仪表板")
        print("=" * 60)
        print(f"更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        services = store.for_store().list_services()
        
        # 总体统计
        total_services = len(services)
        healthy_services = sum(1 for s in services if s.status == ServiceConnectionState.HEALTHY)
        health_rate = (healthy_services / total_services * 100) if total_services > 0 else 0
        
        print(f"📈 总体状态:")
        print(f"   总服务数: {total_services}")
        print(f"   健康服务: {healthy_services}")
        print(f"   健康率: {health_rate:.1f}%")
        print()
        
        # 服务详情
        print(f"📋 服务性能详情:")
        for service in services:
            service_data = performance_data[service.name]
            
            # 计算平均响应时间
            avg_response_time = 0
            if service_data['response_times']:
                avg_response_time = sum(service_data['response_times']) / len(service_data['response_times'])
            
            # 计算可用性
            total_checks = service_data['success_count'] + service_data['failure_count']
            availability = (service_data['success_count'] / total_checks * 100) if total_checks > 0 else 0
            
            status_icon = {
                ServiceConnectionState.HEALTHY: "✅",
                ServiceConnectionState.WARNING: "⚠️",
                ServiceConnectionState.RECONNECTING: "🔄",
                ServiceConnectionState.UNREACHABLE: "❌",
                ServiceConnectionState.INITIALIZING: "🔧"
            }.get(service.status, "❓")
            
            print(f"   {status_icon} {service.name}")
            print(f"      状态: {service.status}")
            print(f"      平均响应: {avg_response_time:.2f}ms")
            print(f"      可用性: {availability:.1f}%")
            print()
    
    # 主循环
    while True:
        try:
            collect_performance_data()
            display_dashboard()
            time.sleep(5)  # 每5秒更新一次
        except KeyboardInterrupt:
            print("\n仪表板已停止")
            break
        except Exception as e:
            print(f"仪表板错误: {e}")
            time.sleep(10)

# 使用
# performance_dashboard()  # 启动仪表板
```

### 生命周期报告生成

```python
def generate_lifecycle_report():
    """生成生命周期报告"""
    store = MCPStore.setup_store()
    from datetime import datetime, timedelta
    
    def collect_report_data():
        """收集报告数据"""
        services = store.for_store().list_services()
        
        report_data = {
            'timestamp': datetime.now(),
            'total_services': len(services),
            'services': [],
            'summary': {
                'healthy': 0,
                'warning': 0,
                'reconnecting': 0,
                'unreachable': 0,
                'other': 0
            }
        }
        
        for service in services:
            service_info = store.for_store().get_service_info(service.name)
            
            service_data = {
                'name': service.name,
                'status': service.status,
                'type': 'remote' if service.url else 'local',
                'url': service.url or '',
                'command': service.command or '',
                'tool_count': service.tool_count,
                'uptime': None,
                'last_failure': None,
                'failure_count': 0,
                'reconnect_count': 0
            }
            
            if service_info and service_info.state_metadata:
                metadata = service_info.state_metadata
                service_data.update({
                    'failure_count': metadata.consecutive_failures,
                    'reconnect_count': metadata.reconnect_attempts,
                    'last_failure': metadata.last_failure_time,
                    'response_time': metadata.response_time
                })
                
                # 计算运行时间
                if metadata.state_entered_time and service.status == ServiceConnectionState.HEALTHY:
                    uptime = datetime.now() - metadata.state_entered_time
                    service_data['uptime'] = uptime.total_seconds()
            
            report_data['services'].append(service_data)
            
            # 统计状态分布
            if service.status == ServiceConnectionState.HEALTHY:
                report_data['summary']['healthy'] += 1
            elif service.status == ServiceConnectionState.WARNING:
                report_data['summary']['warning'] += 1
            elif service.status == ServiceConnectionState.RECONNECTING:
                report_data['summary']['reconnecting'] += 1
            elif service.status == ServiceConnectionState.UNREACHABLE:
                report_data['summary']['unreachable'] += 1
            else:
                report_data['summary']['other'] += 1
        
        return report_data
    
    def format_report(data):
        """格式化报告"""
        report = []
        report.append("📊 MCPStore 生命周期报告")
        report.append("=" * 50)
        report.append(f"生成时间: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"总服务数: {data['total_services']}")
        report.append("")
        
        # 状态摘要
        report.append("📈 状态摘要:")
        summary = data['summary']
        total = data['total_services']
        
        if total > 0:
            report.append(f"   ✅ 健康: {summary['healthy']} ({summary['healthy']/total*100:.1f}%)")
            report.append(f"   ⚠️ 警告: {summary['warning']} ({summary['warning']/total*100:.1f}%)")
            report.append(f"   🔄 重连中: {summary['reconnecting']} ({summary['reconnecting']/total*100:.1f}%)")
            report.append(f"   ❌ 不可达: {summary['unreachable']} ({summary['unreachable']/total*100:.1f}%)")
            report.append(f"   ❓ 其他: {summary['other']} ({summary['other']/total*100:.1f}%)")
        
        report.append("")
        
        # 服务详情
        report.append("📋 服务详情:")
        for service in data['services']:
            report.append(f"   🔸 {service['name']}")
            report.append(f"      状态: {service['status']}")
            report.append(f"      类型: {service['type']}")
            report.append(f"      工具数: {service['tool_count']}")
            
            if service['uptime']:
                uptime_hours = service['uptime'] / 3600
                report.append(f"      运行时间: {uptime_hours:.1f} 小时")
            
            if service['failure_count'] > 0:
                report.append(f"      失败次数: {service['failure_count']}")
            
            if service['reconnect_count'] > 0:
                report.append(f"      重连次数: {service['reconnect_count']}")
            
            report.append("")
        
        return "\n".join(report)
    
    def save_report(report_text, filename=None):
        """保存报告"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mcpstore_lifecycle_report_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"📄 报告已保存到: {filename}")
        return filename
    
    # 生成报告
    data = collect_report_data()
    report_text = format_report(data)
    
    print(report_text)
    
    # 询问是否保存
    save_choice = input("\n是否保存报告到文件? (y/n): ")
    if save_choice.lower() == 'y':
        filename = save_report(report_text)
        return filename
    
    return report_text

# 使用
# report = generate_lifecycle_report()
```

## 🔗 相关文档

- [服务生命周期概览](service-lifecycle.md) - 了解生命周期架构
- [健康检查机制](health-check.md) - 深入了解健康检查
- [服务重启方法](restart-service.md) - 掌握服务重启
- [监控系统](../../advanced/monitoring.md) - 完整的监控解决方案

## 🎯 下一步

- 学习 [健康检查机制](health-check.md)
- 了解 [服务重启方法](restart-service.md)
- 掌握 [监控和调试](../../advanced/monitoring.md)
- 查看 [最佳实践](../../advanced/best-practices.md)
