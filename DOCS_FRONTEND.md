# 前端说明（Vue 3 + Vite + Element Plus）

本文档介绍前端的功能、目录结构、路由与权限、API 调用、开发与构建方式。

## 功能概览

- 图片上传与预览、摄像头拍照
- 模型切换（CNN/VGG16/SE-Net）与可选人脸检测
- 概率分布与结果展示，历史记录与统计
- 视频上传与抽帧时间轴、情绪分布与主导情绪
- 心理健康：情绪汇总/评估、情绪日记与感恩记录
- 账号体系：登录/注册，管理员面板与系统统计

## 快速开始

```bash
cd frontend
npm install
npm run dev
```

开发服默认运行在 `http://localhost:3000`，通过 Vite 代理将 `/api` 转发至后端 `http://localhost:5000`。

生产构建：

```bash
npm run build
```

产物输出至 `frontend/dist/`。

## 目录结构（简要）

```
frontend/
├─ public/              # 静态资源
├─ src/
│  ├─ assets/           # 资源
│  ├─ components/       # 复用组件（含 Layout 布局）
│  ├─ router/           # 路由（守卫、标题、管理员权限）
│  ├─ stores/           # Pinia 状态（user/emotion/video 等）
│  ├─ utils/            # api.js、healthApi.js、indexedDB 等工具
│  └─ views/            # 各页面（Home/History/Health/Video 等）
├─ index.html
├─ package.json
└─ vite.config.js
```

## 路由与权限（`src/router/index.js`）

- 公共：`/login`
- 受保护（需登录）：`/`（Layout 下多子路由）
  - `Home` 首页：上传、拍照、识别与概览
  - `ImageAnalysis` 图片识别
  - `VideoAnalysis` 视频分析
  - `Analysis` 数据分析
  - `Health` 心理健康
  - `History` 历史记录
  - `User` 个人中心
  - `Admin` 管理员面板（`meta.requiresAdmin: true`）
  - `About`/`Help`

路由守卫：

- 未登录访问受保护路由 → 跳转 `/login` 并带 `redirect`
- 已登录访问 `/login` → 重定向首页
- 进入受保护路由前会调用 `userStore.fetchUserInfo()` 校验 Token；失败会清空本地并跳转登录
- 访问 `Admin` 需 `userStore.isAdmin`，否则提示并重定向

## API 调用（`src/utils/api.js`, `src/utils/healthApi.js`）

- 全局 axios 实例：
  - `baseURL: '/api'`，`timeout: 300000`（兼容视频处理耗时）
  - 请求拦截器：如本地有 Token，自动添加 `Authorization: Bearer <token>`
  - 响应拦截器：401 时尝试 `POST /api/auth/refresh` 刷新 Token → 失败清理本地并跳转登录

- 心理健康 API（`healthApi.js`）：
  - 情绪汇总：`GET /health/emotion-summary?date&days`
  - 健康评估：`GET /health/assessment?date`
  - 日记：`POST/GET/GET(id)/PUT/DELETE /health/journal`
  - 感恩：`POST/GET/GET(id)/DELETE /health/gratitude`
  - 建议交互：`POST/GET /health/advice-interaction`（预留/扩展）

## 配置要点

- 代理（`vite.config.js`）：

```js
server: {
  port: 3000,
  proxy: {
    '/api': { target: 'http://localhost:5000', changeOrigin: true }
  }
}
```

- API 基址（`utils/api.js`）：`baseURL: '/api'`

## 交互与体验

- Element Plus 组件与消息提示；页面标题按路由动态设置
- 懒加载路由/组件，图片懒加载，移动端适配

## 常见问题

- 摄像头不可用：确认浏览器权限；需 HTTPS 或 localhost；排除设备占用
- API 失败：确保后端已启动；核对代理与 CORS；查看控制台与 Network 面板
- 刷新 Token 失败后跳转登录：属预期保护；需要重新登录
