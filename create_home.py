content = """<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="gradient-text">🎯 智能情绪识别系统</span>
        </h1>
        <p class="hero-subtitle">基于深度学习的人脸情绪分析平台</p>
        <p class="hero-description">利用先进的卷积神经网络技术，准确识别7种基本情绪表情</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="goToImageAnalysis">
            <el-icon><camera /></el-icon>
            开始图片识别
          </el-button>
          <el-button type="success" size="large" @click="goToVideoAnalysis">
            <el-icon><video-camera /></el-icon>
            视频情绪分析
          </el-button>
        </div>
      </div>
      <div class="hero-image">
        <div class="floating-card">
          <div class="emotion-showcase">
            <div v-for="(emotion, index) in emotions" :key="index" class="emotion-item" :style="{ animationDelay: `${index * 0.1}s` }">
              <span class="emotion-emoji">{{ emotion.emoji }}</span>
              <span class="emotion-name">{{ emotion.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useEmotionStore } from '../stores/emotion'
import { Camera, VideoCamera } from '@element-plus/icons-vue'

const router = useRouter()
const emotionStore = useEmotionStore()

const emotions = [
  { emoji: '😊', name: '开心' },
  { emoji: '😢', name: '悲伤' },
  { emoji: '😱', name: '惊讶' },
  { emoji: '😠', name: '愤怒' },
  { emoji: '😰', name: '恐惧' },
  { emoji: '🤢', name: '厌恶' },
  { emoji: '😐', name: '平静' }
]

const goToImageAnalysis = () => router.push('/image-analysis')
const goToVideoAnalysis = () => router.push('/video')
</script>

<style scoped>
.home-container { max-width: 1400px; margin: 0 auto; padding: 0 20px 40px; }
.hero-section { display: flex; align-items: center; justify-content: space-between; min-height: 500px; margin-bottom: 60px; gap: 40px; }
.hero-content { flex: 1; max-width: 600px; }
.hero-title { font-size: 48px; font-weight: 700; margin-bottom: 20px; line-height: 1.2; }
.gradient-text { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { font-size: 24px; color: #606266; margin-bottom: 10px; font-weight: 500; }
.hero-description { font-size: 16px; color: #909399; margin-bottom: 30px; line-height: 1.6; }
.hero-actions { display: flex; gap: 16px; flex-wrap: wrap; }
.hero-image { flex: 1; display: flex; justify-content: center; align-items: center; }
.floating-card { background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1); animation: float 3s ease-in-out infinite; }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-20px); } }
.emotion-showcase { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.emotion-item { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); transition: transform 0.3s; animation: fadeInUp 0.6s ease-out backwards; }
.emotion-item:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.emotion-emoji { font-size: 36px; }
.emotion-name { font-size: 14px; color: #606266; font-weight: 500; }
@media (max-width: 1024px) {
  .hero-section { flex-direction: column; text-align: center; }
  .hero-content { max-width: 100%; }
  .hero-actions { justify-content: center; }
  .emotion-showcase { grid-template-columns: repeat(4, 1fr); }
}
@media (max-width: 768px) {
  .hero-title { font-size: 32px; }
  .hero-subtitle { font-size: 18px; }
  .emotion-showcase { grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .emotion-item { padding: 12px; }
  .emotion-emoji { font-size: 28px; }
}
</style>
"""

with open(r'd:\项目\初版\10.23基于RAF-DB的人脸情绪识别系统\基于RAF-DB的人脸情绪识别系统\frontend\src\views\Home.vue', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Home.vue created successfully!")
