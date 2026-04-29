/**
 * 图片预测历史 IndexedDB 辅助函数
 * 替代 emotion.js 中的 localStorage 操作
 */

import dbHelper, { STORES } from './indexedDB'

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
 * 保存图片预测数据
 */
export async function saveImagePredictions(predictions, currentPrediction, currentModel, username) {
  try {
    console.log(`💾 [EmotionStore] 保存图片预测到 IndexedDB [用户: ${username}]`)
    
    // 先删除该用户的所有旧记录
    await dbHelper.deleteByIndex(STORES.IMAGE_PREDICTIONS, 'username', username)
    
    // 等待删除操作完成后再添加新记录
    await new Promise(resolve => setTimeout(resolve, 50))
    
    // 保存每条预测记录（移除旧的 id 字段）
    const promises = predictions.map(pred => {
      const cleanPred = deepClone(pred)
      // 删除旧的 id 字段，让 IndexedDB 自动生成新的
      delete cleanPred.id
      return dbHelper.add(STORES.IMAGE_PREDICTIONS, {
        ...cleanPred,
        username,
        savedAt: new Date().toISOString()
      })
    })
    
    await Promise.all(promises)
    
    // 如果有当前预测，也保存（使用特殊标记）
    if (currentPrediction) {
      const cleanCurrent = deepClone(currentPrediction)
      delete cleanCurrent.id
      await dbHelper.add(STORES.IMAGE_PREDICTIONS, {
        ...cleanCurrent,
        username,
        isCurrent: true,
        savedAt: new Date().toISOString()
      })
    }
    
    console.log(`✅ 图片预测已保存到 IndexedDB [用户: ${username}], 记录数: ${predictions.length}`)
  } catch (error) {
    console.error('❌ 保存图片预测失败:', error)
  }
}

/**
 * 从 IndexedDB 加载图片预测数据
 */
export async function loadImagePredictions(username) {
  try {
    console.log(`🔄 [EmotionStore] 从 IndexedDB 加载图片预测 [用户: ${username}]`)
    
    const items = await dbHelper.getByIndex(STORES.IMAGE_PREDICTIONS, 'username', username)
    
    if (items && items.length > 0) {
      // 分离当前预测和历史记录
      const currentPred = items.find(item => item.isCurrent)
      const predictions = items.filter(item => !item.isCurrent)
      
      // 按时间戳倒序排列
      predictions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      
      console.log(`✅ 加载成功 [用户: ${username}], 历史: ${predictions.length} 条, 当前: ${currentPred ? '1' : '0'} 条`)
      
      return {
        predictions: predictions.map(item => ({
          id: item.id,
          emotion: item.emotion,
          emotion_cn: item.emotion_cn,
          confidence: item.confidence,
          model: item.model,
          timestamp: item.timestamp,
          probabilities: item.probabilities,
          probabilities_cn: item.probabilities_cn,
          image: item.image,
          original_image: item.original_image,
          face_image: item.face_image
        })),
        currentPrediction: currentPred ? {
          id: currentPred.id,
          emotion: currentPred.emotion,
          emotion_cn: currentPred.emotion_cn,
          confidence: currentPred.confidence,
          model: currentPred.model,
          timestamp: currentPred.timestamp,
          probabilities: currentPred.probabilities,
          probabilities_cn: currentPred.probabilities_cn,
          image: currentPred.image,
          original_image: currentPred.original_image,
          face_image: currentPred.face_image
        } : null
      }
    }
    
    console.log(`ℹ️  用户 ${username} 暂无图片预测数据`)
    return { predictions: [], currentPrediction: null }
    
  } catch (error) {
    console.error('❌ 加载图片预测失败:', error)
    return { predictions: [], currentPrediction: null }
  }
}

/**
 * 删除单条图片预测记录
 */
export async function deleteImagePrediction(id) {
  try {
    await dbHelper.delete(STORES.IMAGE_PREDICTIONS, id)
    console.log(`🗑️ 已删除图片预测记录: ${id}`)
  } catch (error) {
    console.error('❌ 删除图片预测失败:', error)
  }
}

/**
 * 清空用户的所有图片预测
 */
export async function clearImagePredictions(username) {
  try {
    await dbHelper.deleteByIndex(STORES.IMAGE_PREDICTIONS, 'username', username)
    console.log(`🗑️ 已清空用户 ${username} 的所有图片预测`)
  } catch (error) {
    console.error('❌ 清空图片预测失败:', error)
  }
}

/**
 * 清理图片数据（移除 Base64 图片，保留分析结果）
 */
export async function cleanupImagePredictionData(username) {
  try {
    console.log(`🧹 [EmotionStore] 清理图片预测数据 [用户: ${username}]`)
    
    const items = await dbHelper.getByIndex(STORES.IMAGE_PREDICTIONS, 'username', username)
    
    if (items && items.length > 0) {
      for (const item of items) {
        const cleaned = {
          ...item,
          image: undefined,
          original_image: undefined,
          face_image: undefined
        }
        await dbHelper.put(STORES.IMAGE_PREDICTIONS, cleaned)
      }
      
      console.log(`✅ 已清理 ${items.length} 条图片预测的图片数据`)
      return items.length
    }
    
    return 0
  } catch (error) {
    console.error('❌ 清理图片预测数据失败:', error)
    return 0
  }
}
