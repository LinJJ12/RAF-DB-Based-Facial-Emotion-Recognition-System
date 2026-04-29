# 人脸情绪识别系统 · 总览说明

本项目是一个基于 RAF-DB 的人脸情绪识别系统，提供图片与视频的情绪识别能力，并扩展了“心理健康”功能（情绪汇总、自动评估、情绪日记与感恩记录），配套完整的前后端与认证管理。

## 系统做了什么

- 图片情绪识别：上传或拍照得到图片 → 可选人脸检测/对齐 → 模型推理（CNN/VGG16/SE-Net）→ 返回情绪、中文标签、概率分布与置信度。
- 视频情绪识别：上传视频 → 定间隔抽帧 → 批量推理 → 生成时间轴与情绪统计、主导情绪与稳定性指标。
- 心理健康：基于历史识别结果，按日/多日生成情绪汇总，自动给出心理健康评估与建议；支持记录情绪日记与感恩练习。
- 账号与管理：JWT 登录/刷新，用户信息维护；管理员可查看/维护用户与系统统计，前端路由按角色控制。

## 技术栈与结构

- 后端（`backend/`）
  - Flask + Flask-CORS + Flask-SQLAlchemy（默认 SQLite，可切 MySQL/PostgreSQL）
  - TensorFlow/Keras 模型推理；OpenCV/MTCNN 人脸检测与对齐
  - 主要模块：
    - `app.py`：主应用、推理与视频处理整合、模型加载
    - `health_api.py`：心理健康蓝图（汇总/评估/日记/感恩）
    - `auth.py`：认证蓝图（登录/注册/刷新/管理员功能）
    - `database.py`：SQLAlchemy 模型与初始化
    - `image_preprocess.py`、`face_quality.py`、`video_processor.py`：预处理与业务工具
- 前端（`frontend/`）
  - Vue 3 + Vite + Element Plus + Pinia + Vue Router
  - Axios 拦截器自动携带与刷新 Token；路由守卫控制访问权限
- 模型（`models/`）
  - 包含 `.h5` 与 SavedModel 格式：`cnn`, `vgg`, `se81`, `se83`

## 关键流程（简图）

1) 图片识别：前端（Base64）→ `POST /api/predict` → 预处理（Simple/VGG/EfficientNet）→ 模型推理 → 写入历史（可选）→ 前端展示结果与概率。
2) 视频识别：前端上传 → 后端保存与抽帧 → 批量推理 → 生成时间轴与统计 → 可写入 `VideoAnalysisResult` → 前端可视化。
3) 心理健康：前端请求 `/api/health/*` → 后端依据 `PredictionHistory` 聚合 → 生成汇总与评估/建议 → 前端展示卡片/图表；日记与感恩提供 CRUD。

## 主要 API（高层）

- 健康与模型：
  - `GET /api/health` 服务健康与可用模型键
  - `GET /api/models` 模型路径与可用性
- 推理：
  - `POST /api/predict` 单图情绪识别（Base64，可选人脸检测）
  - `POST /api/batch_predict` 批量识别
- 心理健康（蓝图 `/api/health`）：
  - `GET /emotion-summary` 按日/多日情绪汇总
  - `GET /assessment` 心理健康评估
  - `POST/GET/PUT/DELETE /journal` 情绪日记 CRUD
  - `POST/GET/GET(id)/DELETE /gratitude` 感恩记录 CRUD
- 认证（蓝图 `/api/auth`）：注册/登录/刷新/当前用户/管理员用户管理与系统统计

## 快速运行

后端（默认 http://localhost:5000）：

```bash
cd backend
pip install -r requirements.txt
python app.py
```

前端（默认 http://localhost:3000，经 Vite 代理 `/api` 到后端）：

```bash
cd frontend
npm install
npm run dev
```

可选：数据库迁移（Flask-Migrate/Alembic）详见后端文档。

## 数据与安全

- 上传限制：图片默认 ≤16MB，视频默认 ≤200MB；总请求 ≤64MB（见 `app.py` 配置）。
- JWT 鉴权 + 刷新；前端自动刷新失败则跳转登录；后端开启 CORS。
- 模型与运行环境需与训练时版本兼容；注意内存占用（建议 ≥4GB RAM）。

## 目录快照

```
backend/    # Flask 后端与推理逻辑
frontend/   # Vue 前端与路由/状态/接口
models/     # 训练好的模型文件
```

更多接口细节与模块说明，请参阅 `DOCS_BACKEND.md` 与 `DOCS_FRONTEND.md`。
