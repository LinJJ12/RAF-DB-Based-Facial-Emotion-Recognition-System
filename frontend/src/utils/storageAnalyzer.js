/**
 * 存储空间分析工具
 * 用于检查 IndexedDB 的使用情况（已完全迁移，不再使用 localStorage）
 */

import dbHelper, { STORES } from './indexedDB'

/**
 * 分析 IndexedDB 使用情况
 */
export async function analyzeIndexedDB() {
  const analysis = {
    total: 0,
    stores: {},
    limit: 50 * 1024 * 1024, // 50MB (一般最小限制)
    percentage: 0
  }

  try {
    // 分析视频历史
    const videoHistory = await dbHelper.getAll(STORES.VIDEO_HISTORY)
    const videoHistorySize = estimateSize(videoHistory)
    analysis.stores.VIDEO_HISTORY = {
      count: videoHistory.length,
      size: videoHistorySize,
      sizeKB: (videoHistorySize / 1024).toFixed(2),
      sizeMB: (videoHistorySize / 1024 / 1024).toFixed(2),
      hasImages: checkForImages(videoHistory, 'results.timeline')
    }
    analysis.total += videoHistorySize

    // 分析图片预测
    const imagePredictions = await dbHelper.getAll(STORES.IMAGE_PREDICTIONS)
    const imagePredictionsSize = estimateSize(imagePredictions)
    analysis.stores.IMAGE_PREDICTIONS = {
      count: imagePredictions.length,
      size: imagePredictionsSize,
      sizeKB: (imagePredictionsSize / 1024).toFixed(2),
      sizeMB: (imagePredictionsSize / 1024 / 1024).toFixed(2),
      hasImages: checkForImages(imagePredictions, 'image')
    }
    analysis.total += imagePredictionsSize

    // 分析当前视频分析
    const videoAnalysis = await dbHelper.getAll(STORES.VIDEO_ANALYSIS)
    const videoAnalysisSize = estimateSize(videoAnalysis)
    analysis.stores.VIDEO_ANALYSIS = {
      count: videoAnalysis.length,
      size: videoAnalysisSize,
      sizeKB: (videoAnalysisSize / 1024).toFixed(2),
      sizeMB: (videoAnalysisSize / 1024 / 1024).toFixed(2),
      hasImages: checkForImages(videoAnalysis, 'analysisResults.timeline')
    }
    analysis.total += videoAnalysisSize

    // 检查数据库版本
    let needsUpgrade = false

    // 分析用户数据（V2 新增，可能不存在）
    try {
      const userData = await dbHelper.getAll(STORES.USER_DATA)
      const userDataSize = estimateSize(userData)
      analysis.stores.USER_DATA = {
        count: userData.length,
        size: userDataSize,
        sizeKB: (userDataSize / 1024).toFixed(2),
        sizeMB: (userDataSize / 1024 / 1024).toFixed(2),
        hasImages: false
      }
      analysis.total += userDataSize
    } catch (error) {
      console.log('ℹ️ USER_DATA 存储不存在（数据库未升级到 v2）')
      needsUpgrade = true
      analysis.stores.USER_DATA = {
        count: 0,
        size: 0,
        sizeKB: '0.00',
        sizeMB: '0.00',
        hasImages: false,
        notAvailable: true
      }
    }

    // 分析应用设置（V2 新增，可能不存在）
    try {
      const appSettings = await dbHelper.getAll(STORES.APP_SETTINGS)
      const appSettingsSize = estimateSize(appSettings)
      analysis.stores.APP_SETTINGS = {
        count: appSettings.length,
        size: appSettingsSize,
        sizeKB: (appSettingsSize / 1024).toFixed(2),
        sizeMB: (appSettingsSize / 1024 / 1024).toFixed(2),
        hasImages: false
      }
      analysis.total += appSettingsSize
    } catch (error) {
      console.log('ℹ️ APP_SETTINGS 存储不存在（数据库未升级到 v2）')
      needsUpgrade = true
      analysis.stores.APP_SETTINGS = {
        count: 0,
        size: 0,
        sizeKB: '0.00',
        sizeMB: '0.00',
        hasImages: false,
        notAvailable: true
      }
    }

    // 如果需要升级，添加提示
    if (needsUpgrade) {
      analysis.needsUpgrade = true
      console.warn('⚠️ 检测到旧版本数据库，请刷新页面以升级到 v2')
    }

    analysis.totalKB = (analysis.total / 1024).toFixed(2)
    analysis.totalMB = (analysis.total / 1024 / 1024).toFixed(2)
    analysis.percentage = ((analysis.total / analysis.limit) * 100).toFixed(2)

  } catch (error) {
    console.error('❌ 分析 IndexedDB 失败:', error)
  }

  return analysis
}

/**
 * 估算对象大小（字节）
 */
function estimateSize(obj) {
  const str = JSON.stringify(obj)
  return new Blob([str]).size
}

/**
 * 检查是否包含图片数据
 */
function checkForImages(data, path) {
  if (!data || data.length === 0) return false
  
  for (const item of data) {
    const obj = getNestedValue(item, path)
    if (Array.isArray(obj)) {
      // 检查数组中的每一项
      for (const frame of obj) {
        if (frame.original_frame || frame.face_image || frame.image) {
          return true
        }
      }
    } else if (obj) {
      if (obj.original_frame || obj.face_image || obj.image) {
        return true
      }
    }
  }
  
  return false
}

/**
 * 获取嵌套对象的值
 */
function getNestedValue(obj, path) {
  const keys = path.split('.')
  let current = obj
  
  for (const key of keys) {
    if (current && typeof current === 'object' && key in current) {
      current = current[key]
    } else {
      return null
    }
  }
  
  return current
}

/**
 * 完整的存储分析报告
 */
export async function getFullStorageReport() {
  const indexedDB = await analyzeIndexedDB()
  
  const report = {
    indexedDB,
    total: {
      size: indexedDB.total,
      sizeKB: (indexedDB.total / 1024).toFixed(2),
      sizeMB: (indexedDB.total / 1024 / 1024).toFixed(2)
    },
    warnings: []
  }

  // 检查是否需要升级数据库
  if (indexedDB.needsUpgrade) {
    report.warnings.push({
      type: 'upgrade',
      level: 'warning',
      message: '数据库版本过旧，请刷新页面以升级到最新版本'
    })
  }

  // 生成警告
  if (indexedDB.percentage > 80) {
    report.warnings.push({
      type: 'indexedDB',
      level: 'danger',
      message: `IndexedDB 使用率 ${indexedDB.percentage}%，接近限制！`
    })
  } else if (indexedDB.percentage > 60) {
    report.warnings.push({
      type: 'indexedDB',
      level: 'warning',
      message: `IndexedDB 使用率 ${indexedDB.percentage}%，建议清理`
    })
  }

  // 检查是否有图片数据可清理
  const hasImagesInIndexedDB = 
    indexedDB.stores.VIDEO_HISTORY?.hasImages ||
    indexedDB.stores.VIDEO_ANALYSIS?.hasImages ||
    indexedDB.stores.IMAGE_PREDICTIONS?.hasImages

  if (hasImagesInIndexedDB) {
    report.warnings.push({
      type: 'cleanup',
      level: 'info',
      message: '检测到图片数据，可以通过清理释放空间'
    })
  }

  return report
}

/**
 * 打印存储报告到控制台
 */
export async function printStorageReport() {
  const report = await getFullStorageReport()
  
  console.group('📊 IndexedDB 存储空间分析报告')
  
  console.group('�️ 存储详情')
  console.log(`总大小: ${report.indexedDB.totalMB} MB (${report.indexedDB.percentage}%)`)
  console.log(`限制: ${(report.indexedDB.limit / 1024 / 1024).toFixed(2)} MB`)
  console.log(`可用空间: ${((report.indexedDB.limit - report.indexedDB.total) / 1024 / 1024).toFixed(2)} MB`)
  console.table(Object.entries(report.indexedDB.stores).map(([name, data]) => ({
    存储: name,
    记录数: data.count,
    大小: `${data.sizeMB} MB`,
    占比: `${((data.size / report.indexedDB.total) * 100).toFixed(1)}%`,
    包含图片: data.hasImages ? '✅' : '❌'
  })))
  console.groupEnd()
  
  if (report.warnings.length > 0) {
    console.group('⚠️ 警告')
    report.warnings.forEach(warning => {
      const icon = warning.level === 'danger' ? '🔴' : warning.level === 'warning' ? '🟡' : 'ℹ️'
      console.log(`${icon} [${warning.type}] ${warning.message}`)
    })
    console.groupEnd()
  } else {
    console.log('✅ 存储使用正常')
  }
  
  console.groupEnd()
  
  return report
}
