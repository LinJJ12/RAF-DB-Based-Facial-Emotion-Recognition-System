/**
 * IndexedDB 工具类
 * 完全替代 localStorage，用于存储所有应用数据
 */

const DB_NAME = 'EmotionRecognitionDB'
const DB_VERSION = 2 // 升级版本以添加新存储

// 对象存储名称
const STORES = {
  // 原有的视频和图片数据
  VIDEO_HISTORY: 'video_history',
  IMAGE_PREDICTIONS: 'image_predictions',
  VIDEO_ANALYSIS: 'video_analysis',
  
  // 新增：用户相关数据（替代 localStorage）
  USER_DATA: 'user_data',           // 用户信息、设置、成就等
  APP_SETTINGS: 'app_settings'      // 应用级设置（主题、语言等）
}

class IndexedDBHelper {
  constructor() {
    this.db = null
  }

  /**
   * 初始化数据库
   */
  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION)

      request.onerror = () => {
        console.error('❌ IndexedDB 打开失败:', request.error)
        reject(request.error)
      }

      request.onsuccess = () => {
        this.db = request.result
        console.log('✅ IndexedDB 已连接')
        resolve(this.db)
      }

      request.onupgradeneeded = (event) => {
        const db = event.target.result
        const oldVersion = event.oldVersion
        console.log(`🔄 IndexedDB 升级中... (v${oldVersion} → v${DB_VERSION})`)

        // 创建视频历史对象存储（按用户隔离）
        if (!db.objectStoreNames.contains(STORES.VIDEO_HISTORY)) {
          const videoStore = db.createObjectStore(STORES.VIDEO_HISTORY, { 
            keyPath: 'id', 
            autoIncrement: true 
          })
          videoStore.createIndex('username', 'username', { unique: false })
          videoStore.createIndex('video_id', 'video_id', { unique: false })
          videoStore.createIndex('timestamp', 'timestamp', { unique: false })
          console.log('✅ 创建 video_history 存储')
        }

        // 创建图片预测对象存储
        if (!db.objectStoreNames.contains(STORES.IMAGE_PREDICTIONS)) {
          const imageStore = db.createObjectStore(STORES.IMAGE_PREDICTIONS, { 
            keyPath: 'id', 
            autoIncrement: true 
          })
          imageStore.createIndex('username', 'username', { unique: false })
          imageStore.createIndex('timestamp', 'timestamp', { unique: false })
          console.log('✅ 创建 image_predictions 存储')
        }

        // 创建当前视频分析对象存储
        if (!db.objectStoreNames.contains(STORES.VIDEO_ANALYSIS)) {
          const analysisStore = db.createObjectStore(STORES.VIDEO_ANALYSIS, { 
            keyPath: 'username'
          })
          console.log('✅ 创建 video_analysis 存储')
        }

        // V2: 创建用户数据存储（替代 localStorage）
        if (!db.objectStoreNames.contains(STORES.USER_DATA)) {
          const userStore = db.createObjectStore(STORES.USER_DATA, {
            keyPath: 'key' // key 格式：'username:dataType' 如 'admin:settings'
          })
          userStore.createIndex('username', 'username', { unique: false })
          userStore.createIndex('dataType', 'dataType', { unique: false })
          console.log('✅ 创建 user_data 存储')
        }

        // V2: 创建应用设置存储（全局设置，不按用户隔离）
        if (!db.objectStoreNames.contains(STORES.APP_SETTINGS)) {
          const settingsStore = db.createObjectStore(STORES.APP_SETTINGS, {
            keyPath: 'key' // key: 'theme', 'language', 'sidebarExpanded' 等
          })
          console.log('✅ 创建 app_settings 存储')
        }
      }
    })
  }

  /**
   * 确保数据库已连接
   */
  async ensureConnection() {
    if (!this.db) {
      await this.init()
    }
  }

  /**
   * 检查数据库版本并强制升级
   */
  async checkAndUpgrade() {
    await this.ensureConnection()
    
    // 检查是否所有必需的存储都存在
    const requiredStores = Object.values(STORES)
    const missingStores = requiredStores.filter(
      storeName => !this.db.objectStoreNames.contains(storeName)
    )
    
    if (missingStores.length > 0) {
      console.warn(`⚠️ 检测到旧版本数据库，缺少存储: ${missingStores.join(', ')}`)
      console.log('🔄 正在删除旧数据库并创建新版本...')
      
      // 关闭当前连接
      this.db.close()
      this.db = null
      
      // 删除旧数据库
      return new Promise((resolve, reject) => {
        const deleteRequest = indexedDB.deleteDatabase(DB_NAME)
        
        deleteRequest.onsuccess = async () => {
          console.log('✅ 旧数据库已删除')
          // 重新初始化会创建新的 v2 数据库
          await this.init()
          console.log('✅ 新数据库创建完成')
          resolve(true)
        }
        
        deleteRequest.onerror = () => {
          console.error('❌ 删除数据库失败:', deleteRequest.error)
          reject(deleteRequest.error)
        }
        
        deleteRequest.onblocked = () => {
          console.warn('⚠️ 数据库删除被阻止，请关闭所有打开的标签页')
          reject(new Error('Database deletion blocked'))
        }
      })
    }
    
    return false
  }

  /**
   * 添加数据
   */
  async add(storeName, data) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite')
      const store = transaction.objectStore(storeName)
      const request = store.add(data)

      request.onsuccess = () => {
        resolve(request.result)
      }
      request.onerror = () => {
        console.error(`❌ 添加数据失败 [${storeName}]:`, request.error)
        reject(request.error)
      }
    })
  }

  /**
   * 更新数据（如果存在则更新，否则添加）
   */
  async put(storeName, data) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite')
      const store = transaction.objectStore(storeName)
      const request = store.put(data)

      request.onsuccess = () => {
        resolve(request.result)
      }
      request.onerror = () => {
        console.error(`❌ 更新数据失败 [${storeName}]:`, request.error)
        reject(request.error)
      }
    })
  }

  /**
   * 根据 key 获取数据
   */
  async get(storeName, key) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readonly')
      const store = transaction.objectStore(storeName)
      const request = store.get(key)

      request.onsuccess = () => {
        resolve(request.result)
      }
      request.onerror = () => {
        reject(request.error)
      }
    })
  }

  /**
   * 根据索引查询数据
   */
  async getByIndex(storeName, indexName, value) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readonly')
      const store = transaction.objectStore(storeName)
      const index = store.index(indexName)
      const request = index.getAll(value)

      request.onsuccess = () => {
        resolve(request.result)
      }
      request.onerror = () => {
        reject(request.error)
      }
    })
  }

  /**
   * 获取所有数据
   */
  async getAll(storeName) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readonly')
      const store = transaction.objectStore(storeName)
      const request = store.getAll()

      request.onsuccess = () => {
        resolve(request.result)
      }
      request.onerror = () => {
        reject(request.error)
      }
    })
  }

  /**
   * 删除数据
   */
  async delete(storeName, key) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite')
      const store = transaction.objectStore(storeName)
      const request = store.delete(key)

      request.onsuccess = () => {
        resolve()
      }
      request.onerror = () => {
        reject(request.error)
      }
    })
  }

  /**
   * 清空对象存储
   */
  async clear(storeName) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite')
      const store = transaction.objectStore(storeName)
      const request = store.clear()

      request.onsuccess = () => {
        resolve()
      }
      request.onerror = () => {
        reject(request.error)
      }
    })
  }

  /**
   * 根据索引删除多条数据
   */
  async deleteByIndex(storeName, indexName, value) {
    await this.ensureConnection()
    const items = await this.getByIndex(storeName, indexName, value)
    const promises = items.map(item => this.delete(storeName, item.id))
    return Promise.all(promises)
  }

  /**
   * 统计数据条数
   */
  async count(storeName) {
    await this.ensureConnection()
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readonly')
      const store = transaction.objectStore(storeName)
      const request = store.count()

      request.onsuccess = () => {
        resolve(request.result)
      }
      request.onerror = () => {
        reject(request.error)
      }
    })
  }
}

// 导出单例
const dbHelper = new IndexedDBHelper()

export default dbHelper
export { STORES }
