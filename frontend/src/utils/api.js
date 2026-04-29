import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000,  // 5分钟超时，适用于视频分析等耗时操作
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 添加认证token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    let message = '请求失败'
    
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求参数错误'
          break
        case 401:
          // Token过期或无效
          const token = localStorage.getItem('token')
          const refreshToken = localStorage.getItem('refreshToken')
          
          if (token && refreshToken && !error.config._retry) {
            error.config._retry = true
            
            try {
              // 尝试刷新token
              const response = await axios.post('/api/auth/refresh', {
                refreshToken: refreshToken
              })
              
              const { token: newToken, refreshToken: newRefreshToken } = response.data
              localStorage.setItem('token', newToken)
              localStorage.setItem('refreshToken', newRefreshToken)
              
              // 重新发送原始请求
              error.config.headers.Authorization = `Bearer ${newToken}`
              return api(error.config)
            } catch (refreshError) {
              // 刷新失败，清除用户信息并跳转到登录页
              localStorage.removeItem('token')
              localStorage.removeItem('refreshToken')
              localStorage.removeItem('userInfo')
              
              // 只有在非登录页面才跳转
              if (window.location.pathname !== '/login') {
                window.location.href = '/login'
              }
            }
          }
          message = '登录已过期，请重新登录'
          break
        case 403:
          message = '没有权限访问此资源'
          break
        case 404:
          message = '请求的资源不存在'
          break
        case 500:
          message = '服务器错误'
          break
        default:
          message = error.response.data?.error || error.response.data?.message || '请求失败'
      }
    } else if (error.request) {
      message = '无法连接到服务器'
    }
    
    // 只在非401错误时显示消息，401错误由上面的逻辑处理
    if (error.response?.status !== 401) {
      ElMessage.error(message)
    }
    
    return Promise.reject(error)
  }
)

export default api
