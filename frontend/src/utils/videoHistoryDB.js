/**
 * 视频历史记录 IndexedDB 迁移辅助函数
 * 将 video.js 中的 saveHistory 和 loadHistory 替换为这些函数
 */

import dbHelper, { STORES } from '../utils/indexedDB'

/**
 * 深度克隆对象，移除不可序列化的内容
 */
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  
  if (obj instanceof Date) {
    return obj.toISOString()
  }
  
  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item))
  }
  
  const cloned = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const value = obj[key]
      if (typeof value === 'function' || value === undefined) {
        continue
      }
      cloned[key] = deepClone(value)
    }
  }
  return cloned
}

/**
 * 保存视频历史到 IndexedDB
 */
export async function saveVideoHistory(videoHistory, username) {
  try {
    console.log(`💾 [VideoStore] 保存视频历史到 IndexedDB [用户: ${username}]`)
    
    // 先删除该用户的所有旧记录
    await dbHelper.deleteByIndex(STORES.VIDEO_HISTORY, 'username', username)
    
    // 保存完整的历史记录数据（包括图片）到 IndexedDB
    const promises = videoHistory.map(item => {
      const cleanItem = {
        video_id: item.video_id,
        video_info: deepClone(item.video_info),
        thumbnail: item.thumbnail,
        timestamp: item.timestamp,
        model: item.model,
        results: deepClone(item.results),
        username,
        savedAt: new Date().toISOString()
      }
      return dbHelper.add(STORES.VIDEO_HISTORY, cleanItem)
    })
    
    await Promise.all(promises)
    console.log(`✅ 视频历史已保存到 IndexedDB [用户: ${username}], 记录数: ${videoHistory.length}`)
  } catch (error) {
    console.error('❌ 保存视频历史失败:', error)
  }
}

/**
 * 从 IndexedDB 加载视频历史
 */
export async function loadVideoHistory(username) {
  try {
    console.log(`🔄 [VideoStore] 从 IndexedDB 加载视频历史 [用户: ${username}]`)
    
    // 从 IndexedDB 加载该用户的历史记录
    const items = await dbHelper.getByIndex(STORES.VIDEO_HISTORY, 'username', username)
    
    if (items && items.length > 0) {
      // 按时间戳倒序排列
      const sorted = items.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      
      // 规范化数据
      const normalized = sorted.map(item => ({
        id: item.id,
        video_id: item.video_id,
        video_info: item.video_info,
        thumbnail: item.thumbnail,
        timestamp: item.timestamp,
        model: item.model,
        results: item.results
      }))
      
      console.log(`✅ 成功加载视频历史 [用户: ${username}], 记录数: ${normalized.length}`)
      return normalized
    } else {
      console.log(`ℹ️  没有找到视频历史记录 [用户: ${username}]`)
      return []
    }
  } catch (error) {
    console.error('❌ 加载视频历史失败:', error)
    return []
  }
}

/**
 * 删除指定ID的视频历史
 */
export async function deleteVideoHistoryItem(id) {
  try {
    await dbHelper.delete(STORES.VIDEO_HISTORY, id)
    console.log(`🗑️ 已删除视频历史记录 [ID: ${id}]`)
  } catch (error) {
    console.error('❌ 删除视频历史失败:', error)
  }
}

/**
 * 清空用户的所有视频历史
 */
export async function clearVideoHistory(username) {
  try {
    await dbHelper.deleteByIndex(STORES.VIDEO_HISTORY, 'username', username)
    console.log(`🗑️  已清空视频历史记录 [用户: ${username}]`)
  } catch (error) {
    console.error('❌ 清空视频历史失败:', error)
  }
}
