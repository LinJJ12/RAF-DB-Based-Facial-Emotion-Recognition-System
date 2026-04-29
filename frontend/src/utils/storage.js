/**
 * 存储适配器 - 使用 IndexedDB 替代 localStorage
 * 提供与 localStorage 相同的 API，但存储在 IndexedDB 中
 */

import dbHelper, { STORES } from './indexedDB'

/**
 * 存储管理器
 */
class StorageManager {
  constructor() {
    this.migrated = false
  }

  /**
   * 一次性迁移 localStorage 到 IndexedDB
   */
  async migrateFromLocalStorage() {
    if (this.migrated) return
    
    console.log('🔄 开始迁移 localStorage 数据到 IndexedDB...')
    
    // 等待数据库完全就绪（确保升级完成）
    await dbHelper.ensureConnection()
    
    // 添加小延迟确保数据库升级完成
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // 检查 v2 存储是否已创建
    const db = dbHelper.db
    if (!db.objectStoreNames.contains(STORES.USER_DATA) || 
        !db.objectStoreNames.contains(STORES.APP_SETTINGS)) {
      console.warn('⚠️ 数据库尚未升级到 v2，跳过迁移')
      console.log('💡 提示：数据将继续使用 localStorage，刷新页面后会自动升级')
      return
    }
    
    try {
      const keysToMigrate = [
        'userInfo',
        'theme',
        'language',
        'sidebarExpanded',
        'animations',
        'userSettings',
        'admin_activeTab'
      ]
      
      let migratedCount = 0
      
      for (const key of keysToMigrate) {
        const value = localStorage.getItem(key)
        if (value !== null) {
          try {
            await this.setItem(key, value)
            migratedCount++
          } catch (err) {
            console.error(`设置 ${key} 失败:`, err)
          }
        }
      }
      
      // 迁移用户特定的数据
      const emotionKeys = []
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i)
        if (key.startsWith('emotion_predictions_')) {
          emotionKeys.push(key)
        }
      }
      
      for (const key of emotionKeys) {
        const value = localStorage.getItem(key)
        if (value !== null) {
          try {
            await this.setItem(key, value)
            migratedCount++
          } catch (err) {
            console.error(`设置 ${key} 失败:`, err)
          }
        }
      }
      
      this.migrated = true
      console.log(`✅ 迁移完成，共迁移 ${migratedCount} 条数据`)
      
      // 可选：清理已迁移的 localStorage 数据
      // this.cleanupLocalStorage()
      
    } catch (error) {
      console.error('❌ 迁移失败:', error)
    }
  }

  /**
   * 清理已迁移的 localStorage 数据
   */
  cleanupLocalStorage() {
    const keysToKeep = ['token', 'refreshToken'] // 认证相关的保留
    const keysToRemove = []
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (!keysToKeep.includes(key)) {
        keysToRemove.push(key)
      }
    }
    
    keysToRemove.forEach(key => {
      localStorage.removeItem(key)
      console.log(`🗑️ 已清理 localStorage: ${key}`)
    })
    
    console.log(`✅ 清理完成，保留 ${keysToKeep.length} 条认证数据`)
  }

  /**
   * 获取数据 (异步)
   * @param {string} key 键名
   * @returns {Promise<string|null>}
   */
  async getItem(key) {
    try {
      await dbHelper.ensureConnection()
      
      // 判断是应用设置还是用户数据
      const storeName = this._getStoreName(key)
      
      // 检查存储是否存在
      if (!dbHelper.db.objectStoreNames.contains(storeName)) {
        console.warn(`⚠️ 存储 ${storeName} 不存在，使用 localStorage`)
        return localStorage.getItem(key)
      }
      
      const data = await dbHelper.get(storeName, key)
      
      return data ? data.value : null
    } catch (error) {
      console.error(`获取 ${key} 失败:`, error)
      // 降级到 localStorage
      return localStorage.getItem(key)
    }
  }

  /**
   * 设置数据 (异步)
   * @param {string} key 键名
   * @param {string} value 值
   */
  async setItem(key, value) {
    try {
      await dbHelper.ensureConnection()
      
      const storeName = this._getStoreName(key)
      
      // 检查存储是否存在
      if (!dbHelper.db.objectStoreNames.contains(storeName)) {
        console.warn(`⚠️ 存储 ${storeName} 不存在，使用 localStorage`)
        localStorage.setItem(key, value)
        return
      }
      
      const data = {
        key,
        value,
        timestamp: new Date().toISOString()
      }
      
      // 如果是用户特定数据，添加 username 和 dataType
      if (storeName === STORES.USER_DATA) {
        const parts = key.split('_')
        data.username = parts[parts.length - 1] || 'guest'
        data.dataType = parts.slice(0, -1).join('_')
      }
      
      await dbHelper.put(storeName, data)
      
      // 同时写入 localStorage 作为备份（可选）
      // localStorage.setItem(key, value)
      
    } catch (error) {
      console.error(`设置 ${key} 失败:`, error)
      // 降级到 localStorage
      localStorage.setItem(key, value)
    }
  }

  /**
   * 删除数据 (异步)
   * @param {string} key 键名
   */
  async removeItem(key) {
    try {
      await dbHelper.ensureConnection()
      
      const storeName = this._getStoreName(key)
      
      // 检查存储是否存在
      if (!dbHelper.db.objectStoreNames.contains(storeName)) {
        console.warn(`⚠️ 存储 ${storeName} 不存在，使用 localStorage`)
        localStorage.removeItem(key)
        return
      }
      
      await dbHelper.delete(storeName, key)
      
      // localStorage.removeItem(key)
      
    } catch (error) {
      console.error(`删除 ${key} 失败:`, error)
      localStorage.removeItem(key)
    }
  }

  /**
   * 清空所有数据 (异步)
   */
  async clear() {
    try {
      await dbHelper.ensureConnection()
      
      await dbHelper.clear(STORES.APP_SETTINGS)
      await dbHelper.clear(STORES.USER_DATA)
      
      // localStorage.clear()
      
    } catch (error) {
      console.error('清空数据失败:', error)
    }
  }

  /**
   * 获取所有键名 (异步)
   * @returns {Promise<string[]>}
   */
  async keys() {
    try {
      await dbHelper.ensureConnection()
      
      const appSettings = await dbHelper.getAll(STORES.APP_SETTINGS)
      const userData = await dbHelper.getAll(STORES.USER_DATA)
      
      const allKeys = [
        ...appSettings.map(item => item.key),
        ...userData.map(item => item.key)
      ]
      
      return allKeys
    } catch (error) {
      console.error('获取键名列表失败:', error)
      return []
    }
  }

  /**
   * 判断应该使用哪个对象存储
   */
  _getStoreName(key) {
    // 应用级设置（不按用户隔离）
    const appSettingKeys = [
      'theme',
      'language',
      'sidebarExpanded',
      'animations',
      'admin_activeTab'
    ]
    
    if (appSettingKeys.includes(key)) {
      return STORES.APP_SETTINGS
    }
    
    // 其他都是用户数据
    return STORES.USER_DATA
  }
}

// 创建单例
const storageManager = new StorageManager()

// 导出实例
export default storageManager

/**
 * 同步版本的存储 API（保持向后兼容）
 * 注意：这些是包装的异步调用，实际仍然是异步的
 */
export const storage = {
  /**
   * 获取数据（同步接口，内部异步）
   * 注意：这个函数返回 Promise，使用时需要 await
   */
  getItem: (key) => storageManager.getItem(key),
  
  /**
   * 设置数据（同步接口，内部异步）
   */
  setItem: (key, value) => storageManager.setItem(key, value),
  
  /**
   * 删除数据（同步接口，内部异步）
   */
  removeItem: (key) => storageManager.removeItem(key),
  
  /**
   * 清空数据（同步接口，内部异步）
   */
  clear: () => storageManager.clear(),
  
  /**
   * 获取所有键名
   */
  keys: () => storageManager.keys()
}

/**
 * 初始化存储系统（在应用启动时调用）
 */
export async function initStorage() {
  try {
    // 1. 初始化数据库
    await dbHelper.init()
    
    // 2. 检查并升级数据库到最新版本（如果需要）
    const needsUpgrade = await dbHelper.checkAndUpgrade()
    if (needsUpgrade) {
      console.log('✅ 数据库已升级到最新版本')
      // 数据库已重建，需要重新加载页面
      console.log('💡 提示：建议刷新页面以确保所有功能正常工作')
    }
    
    // 3. 迁移 localStorage 数据（仅在 v2 就绪时执行）
    await storageManager.migrateFromLocalStorage()
    
    console.log('✅ 存储系统初始化完成')
  } catch (error) {
    console.error('❌ 存储系统初始化失败:', error)
    console.log('⚠️ 将使用 localStorage 作为降级方案')
  }
}
