import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'
import { useAppStore } from './app'

/**
 * 工具执行状态管理Store
 * 专门管理工具的执行状态、历史记录、统计信息等
 */
export const useToolExecutionStore = defineStore('toolExecution', () => {
  const appStore = useAppStore()

  // ==================== 状态定义 ====================
  
  // 执行历史和记录
  const executionHistory = ref([])
  const toolRecords = ref({
    executions: [],
    summary: {
      total_executions: 0,
      by_tool: {},
      by_service: {}
    }
  })

  // 当前执行状态
  const currentExecutions = ref(new Map()) // executionId -> execution info
  const executionQueue = ref([]) // 待执行的工具队列
  
  // 执行统计
  const statistics = ref({
    totalExecutions: 0,
    successfulExecutions: 0,
    failedExecutions: 0,
    averageResponseTime: 0,
    successRate: 0,
    todayExecutions: 0
  })

  // 加载状态
  const loading = ref({
    executing: false,
    records: false,
    history: false
  })

  // 错误状态
  const errors = ref([])
  const lastError = ref(null)

  // 配置
  const config = ref({
    maxHistorySize: 1000,
    maxRecordsSize: 500,
    autoSaveHistory: true,
    defaultTimeout: 30000,
    retryAttempts: 3,
    batchSize: 10
  })

  // ==================== 计算属性 ====================
  
  // 是否正在执行
  const isExecuting = computed(() => {
    return currentExecutions.value.size > 0 || loading.value.executing
  })

  // 是否有任何加载状态
  const isLoading = computed(() => {
    return Object.values(loading.value).some(Boolean)
  })

  // 是否有错误
  const hasErrors = computed(() => {
    return errors.value.length > 0
  })

  // 最近的执行记录
  const recentExecutions = computed(() => {
    return executionHistory.value
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      .slice(0, 10)
  })

  // 热门工具（按执行次数排序）
  const popularTools = computed(() => {
    const toolCounts = {}

    // 🔧 修复：确保executions数组存在
    if (!toolRecords.value.executions || !Array.isArray(toolRecords.value.executions)) {
      console.warn('⚠️ toolRecords.executions 不是有效数组:', toolRecords.value.executions)
      return []
    }

    toolRecords.value.executions.forEach(execution => {
      const toolName = execution.tool_name
      if (!toolName) return // 跳过无效记录

      if (!toolCounts[toolName]) {
        toolCounts[toolName] = {
          // 🔧 修复：使用模板期望的字段名
          tool_name: toolName,                    // 模板期望 tool_name
          service_name: execution.service_name,   // 模板期望 service_name
          last_executed: execution.execution_time, // 模板期望 last_executed
          execution_count: 0,                     // 模板期望 execution_count
          average_response_time: 0,               // 模板期望 average_response_time
          success_rate: 0,                        // 模板期望 success_rate
          total_response_time: 0,                 // 内部计算用
          successful_count: 0,                    // 内部计算用
          failed_count: 0                         // 内部计算用
        }
      }

      const tool = toolCounts[toolName]
      tool.execution_count++
      tool.total_response_time += execution.response_time || 0
      tool.average_response_time = tool.total_response_time / tool.execution_count

      // 统计成功/失败次数
      if (execution.error) {
        tool.failed_count++
      } else {
        tool.successful_count++
      }

      // 计算成功率
      tool.success_rate = tool.execution_count > 0 ?
        (tool.successful_count / tool.execution_count * 100) : 0

      // 更新最后执行时间
      if (execution.execution_time &&
          (!tool.last_executed || new Date(execution.execution_time) > new Date(tool.last_executed))) {
        tool.last_executed = execution.execution_time
      }
    })

    // 🔧 修复：返回正确格式的数据
    const result = Object.values(toolCounts)
      .sort((a, b) => b.execution_count - a.execution_count)
      .slice(0, 10)
      .map(tool => ({
        tool_name: tool.tool_name,
        service_name: tool.service_name,
        last_executed: tool.last_executed,
        execution_count: tool.execution_count,
        average_response_time: Math.round(tool.average_response_time * 100) / 100, // 保留2位小数
        success_rate: Math.round(tool.success_rate * 10) / 10 // 保留1位小数
      }))

    console.log('🔍 [DEBUG] popularTools 计算结果:', result)
    return result
  })

  // 执行成功率
  const successRate = computed(() => {
    const total = statistics.value.totalExecutions
    const successful = statistics.value.successfulExecutions
    return total > 0 ? (successful / total * 100).toFixed(1) : 0
  })

  // 今天的执行统计 - 🔧 修复：基于真实API数据
  const todayStats = computed(() => {
    const today = new Date().toDateString()

    // 🔧 优先使用真实的API数据
    if (toolRecords.value.executions && Array.isArray(toolRecords.value.executions)) {
      const todayExecutions = toolRecords.value.executions.filter(exec => {
        if (!exec.execution_time) return false
        return new Date(exec.execution_time).toDateString() === today
      })

      const successful = todayExecutions.filter(exec => !exec.error).length
      const failed = todayExecutions.filter(exec => exec.error).length

      console.log('🔍 [DEBUG] 今日统计 (基于API数据):', {
        total: todayExecutions.length,
        successful,
        failed,
        todayDate: today
      })

      return {
        total: todayExecutions.length,
        successful,
        failed,
        successRate: todayExecutions.length > 0 ? (successful / todayExecutions.length * 100).toFixed(1) : 0
      }
    }

    // 🔧 回退到本地历史数据
    const todayExecutions = executionHistory.value.filter(exec =>
      new Date(exec.timestamp).toDateString() === today
    )

    const successful = todayExecutions.filter(exec => exec.success).length
    const failed = todayExecutions.filter(exec => !exec.success).length

    console.log('🔍 [DEBUG] 今日统计 (基于本地数据):', {
      total: todayExecutions.length,
      successful,
      failed,
      todayDate: today
    })

    return {
      total: todayExecutions.length,
      successful,
      failed,
      successRate: todayExecutions.length > 0 ? (successful / todayExecutions.length * 100).toFixed(1) : 0
    }
  })

  // 按服务分组的执行统计
  const executionsByService = computed(() => {
    const serviceStats = {}
    toolRecords.value.executions.forEach(execution => {
      const serviceName = execution.service_name || 'unknown'
      if (!serviceStats[serviceName]) {
        serviceStats[serviceName] = {
          name: serviceName,
          count: 0,
          tools: new Set(),
          avgResponseTime: 0,
          totalResponseTime: 0
        }
      }
      serviceStats[serviceName].count++
      serviceStats[serviceName].tools.add(execution.tool_name)
      serviceStats[serviceName].totalResponseTime += execution.response_time || 0
      serviceStats[serviceName].avgResponseTime = serviceStats[serviceName].totalResponseTime / serviceStats[serviceName].count
    })
    
    // 转换Set为数组
    Object.values(serviceStats).forEach(stat => {
      stat.tools = Array.from(stat.tools)
    })
    
    return serviceStats
  })

  // 最近的错误
  const recentErrors = computed(() => {
    return errors.value.slice(-5).reverse()
  })

  // 执行队列状态
  const queueStatus = computed(() => {
    return {
      pending: executionQueue.value.length,
      running: currentExecutions.value.size,
      isEmpty: executionQueue.value.length === 0 && currentExecutions.value.size === 0
    }
  })

  // ==================== 操作方法 ====================

  // 设置加载状态
  const setLoading = (type, status) => {
    if (type in loading.value) {
      loading.value[type] = status
    }
  }

  // 添加错误
  const addError = (error) => {
    const errorObj = {
      id: Date.now(),
      message: error.message || error,
      timestamp: new Date().toISOString(),
      type: error.type || 'execution-error',
      source: error.source || 'tool-execution-store',
      toolName: error.toolName
    }
    
    errors.value.push(errorObj)
    lastError.value = errorObj
    
    // 限制错误数量
    if (errors.value.length > 100) {
      errors.value = errors.value.slice(-100)
    }

    // 同时添加到应用级错误
    if (appStore) {
      appStore.addError(errorObj)
    }
  }

  // 清除错误
  const clearErrors = () => {
    errors.value = []
    lastError.value = null
  }

  // 添加执行记录到历史
  const addExecutionToHistory = (execution) => {
    executionHistory.value.unshift(execution)
    
    // 限制历史记录数量
    if (executionHistory.value.length > config.value.maxHistorySize) {
      executionHistory.value = executionHistory.value.slice(0, config.value.maxHistorySize)
    }
    
    // 更新统计
    updateStatistics()
    
    // 自动保存到localStorage
    if (config.value.autoSaveHistory) {
      saveHistoryToStorage()
    }
  }

  // 更新统计信息
  const updateStatistics = () => {
    const total = executionHistory.value.length
    const successful = executionHistory.value.filter(exec => exec.success).length
    const failed = total - successful
    
    let totalResponseTime = 0
    executionHistory.value.forEach(exec => {
      if (exec.duration) {
        totalResponseTime += exec.duration
      }
    })
    
    statistics.value = {
      totalExecutions: total,
      successfulExecutions: successful,
      failedExecutions: failed,
      averageResponseTime: total > 0 ? Math.round(totalResponseTime / total) : 0,
      successRate: total > 0 ? (successful / total * 100).toFixed(1) : 0,
      todayExecutions: todayStats.value.total
    }
  }

  // 保存历史到localStorage
  const saveHistoryToStorage = () => {
    try {
      const historyToSave = executionHistory.value.slice(0, 100) // 只保存最近100条
      localStorage.setItem('mcpstore-execution-history', JSON.stringify(historyToSave))
    } catch (error) {
      console.warn('Failed to save execution history to localStorage:', error)
    }
  }

  // 从localStorage加载历史
  const loadHistoryFromStorage = () => {
    try {
      const saved = localStorage.getItem('mcpstore-execution-history')
      if (saved) {
        const parsed = JSON.parse(saved)
        if (Array.isArray(parsed)) {
          executionHistory.value = parsed
          updateStatistics()
        }
      }
    } catch (error) {
      console.warn('Failed to load execution history from localStorage:', error)
    }
  }

  // 获取工具执行记录
  const fetchToolRecords = async (limit = 50, force = false) => {
    if (loading.value.records && !force) return toolRecords.value

    try {
      setLoading('records', true)

      console.log('🔍 [DEBUG] 开始获取工具执行记录...')
      const response = await api.store.getToolRecords(limit)
      console.log('🔍 [DEBUG] API响应:', response)

      // 🔧 修复：正确处理API响应格式
      let data = null

      // 处理不同的响应格式
      if (response.data && response.data.success && response.data.data) {
        // 新格式：{ success: true, data: { executions: [...], summary: {...} } }
        data = response.data.data
        console.log('✅ [DEBUG] 使用新格式 response.data.data')
      } else if (response.data && response.data.executions) {
        // 直接格式：{ executions: [...], summary: {...} }
        data = response.data
        console.log('✅ [DEBUG] 使用直接格式 response.data')
      } else {
        console.warn('⚠️ [DEBUG] 无法识别的API响应格式')
        data = { executions: [], summary: { total_executions: 0, by_tool: {}, by_service: {} } }
      }

      console.log('🔍 [DEBUG] 提取的数据:', data)
      console.log('🔍 [DEBUG] executions数量:', data.executions?.length || 0)

      // 确保数据结构正确
      if (data && typeof data === 'object') {
        // 确保executions字段存在且为数组
        if (!data.executions || !Array.isArray(data.executions)) {
          console.warn('⚠️ [DEBUG] executions字段无效，使用空数组')
          data.executions = []
        }

        // 确保summary字段存在
        if (!data.summary || typeof data.summary !== 'object') {
          console.warn('⚠️ [DEBUG] summary字段无效，使用默认结构')
          data.summary = { total_executions: 0, by_tool: {}, by_service: {} }
        }

        toolRecords.value = data
      } else {
        // 如果数据格式不正确，使用默认结构
        console.warn('⚠️ [DEBUG] 数据格式不正确，使用默认结构')
        toolRecords.value = {
          executions: [],
          summary: {
            total_executions: 0,
            by_tool: {},
            by_service: {}
          }
        }
      }

      // 限制记录数量
      if (toolRecords.value.executions && toolRecords.value.executions.length > config.value.maxRecordsSize) {
        toolRecords.value.executions = toolRecords.value.executions.slice(0, config.value.maxRecordsSize)
      }

      console.log(`📊 Loaded ${toolRecords.value.executions?.length || 0} tool execution records`)
      console.log('🔍 [DEBUG] 最终toolRecords:', toolRecords.value)

      return toolRecords.value
    } catch (error) {
      console.error('获取工具记录失败:', error)
      addError({
        message: `获取工具记录失败: ${error.message}`,
        type: 'fetch-error',
        source: 'fetchToolRecords'
      })
      throw error
    } finally {
      setLoading('records', false)
    }
  }

  // 清除执行历史
  const clearExecutionHistory = () => {
    executionHistory.value = []
    updateStatistics()
    saveHistoryToStorage()
    
    appStore?.addNotification({
      title: '执行历史已清除',
      message: '所有工具执行历史记录已清除',
      type: 'info'
    })
  }

  // 清除工具记录
  const clearToolRecords = () => {
    toolRecords.value = {
      executions: [],
      summary: {
        total_executions: 0,
        by_tool: {},
        by_service: {}
      }
    }
  }

  // 重置Store状态
  const resetStore = () => {
    executionHistory.value = []
    clearToolRecords()
    currentExecutions.value.clear()
    executionQueue.value = []
    statistics.value = {
      totalExecutions: 0,
      successfulExecutions: 0,
      failedExecutions: 0,
      averageResponseTime: 0,
      successRate: 0,
      todayExecutions: 0
    }
    errors.value = []
    lastError.value = null
    
    Object.keys(loading.value).forEach(key => {
      loading.value[key] = false
    })
    
    // 清除localStorage
    localStorage.removeItem('mcpstore-execution-history')
    
    console.log('🔄 Tool execution store reset')
  }

  return {
    // 状态
    executionHistory,
    toolRecords,
    currentExecutions,
    executionQueue,
    statistics,
    loading,
    errors,
    lastError,
    config,
    
    // 计算属性
    isExecuting,
    isLoading,
    hasErrors,
    recentExecutions,
    popularTools,
    successRate,
    todayStats,
    executionsByService,
    recentErrors,
    queueStatus,
    
    // 方法
    setLoading,
    addError,
    clearErrors,
    addExecutionToHistory,
    updateStatistics,
    saveHistoryToStorage,
    loadHistoryFromStorage,
    fetchToolRecords,
    clearExecutionHistory,
    clearToolRecords,
    resetStore
  }
})
