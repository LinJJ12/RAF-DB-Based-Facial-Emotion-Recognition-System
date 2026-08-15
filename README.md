# 人脸情绪识别系统（基于 RAF-DB）

<p align="center">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-2.x-00A6D6" />
  <img alt="Vue 3" src="https://img.shields.io/badge/Vue-3.x-41B883" />
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00" />
</p>

一个基于 RAF-DB 数据集的人脸情绪识别项目，支持图片识别、视频分析、情绪历史与心理健康相关功能，前后端均可运行，适合学习、研究和二次开发。

> 许可证说明：本项目仅供学习、研究和个人技术交流使用，禁止任何商业用途，包括但不限于出售、商业部署、收费服务或其他盈利行为。
> 若需复用代码，请保留原始说明，并确保遵守本项目的非商用约定。

---

## 项目简介

该项目覆盖了从数据预处理、模型推理到结果展示的完整流程，包括：

- 图片情绪识别
- 视频情绪分析
- 人脸检测 / 对齐 / 质量评估
- 多模型支持：CNN、VGG、SE-Net
- 用户登录、管理后台、记录历史
- 心理健康模块：情绪汇总、日记、感恩记录、健康评估

基于 RAF-DB 的表情识别任务，后端使用 Flask + TensorFlow/Keras，前端使用 Vue 3 + Vite，整体结构清晰，便于扩展和部署。

---

## 功能特性

### 1. 情绪识别

- 单张图片预测
- 批量图片预测
- 视频抽帧分析
- 支持多种模型输出与切换

### 2. 图像增强与脸部处理

- MTCNN 人脸检测与对齐
- Haar 级联回退方案
- 人脸质量评估（清晰度、亮度、对比度）
- 图像增强用于前端展示与优化识别效果

### 3. 用户与管理能力

- JWT 认证
- 用户登录/注册/资料管理
- 管理员后台
- 历史记录查询与统计

### 4. 心理健康模块

- 情绪汇总
- 健康风险评估
- 情绪日记
- 感恩记录

---

## 技术栈

- 前端：Vue 3、Vite、Pinia、Vue Router、Element Plus、Axios、ECharts
- 后端：Python、Flask、Flask-CORS、OpenCV、Pillow、PyJWT
- 深度学习：TensorFlow / Keras
- 数据库：SQLite（可扩展为 MySQL / PostgreSQL）

---

## 系统架构

```text
RAF-DB-Facial-Emotion-Recognition-System
├── backend/                  # Flask 后端、API、模型加载、数据库逻辑
│   ├── app.py                # 主应用入口
│   ├── auth.py               # 认证与用户逻辑
│   ├── config.py             # 配置与路径定义
│   ├── database.py           # 数据模型与初始化
│   ├── health_api.py         # 心理健康接口
│   ├── image_preprocess.py   # 图像预处理
│   ├── face_quality.py       # 人脸质量检测
│   ├── video_processor.py    # 视频分析处理
│   ├── requirements.txt      # Python 依赖
│   ├── tests/                # 后端测试脚本
│   ├── instance/             # 运行时 SQLite 数据库目录（忽略提交）
│   ├── uploads/              # 上传文件与缓存（忽略提交）
│   └── logs/                 # 运行日志（忽略提交）
├── frontend/                 # Vue 前端
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── scripts/                  # 项目脚本工具
│   └── create_home.py
├── models/                   # 训练产物（.h5 / SavedModel，建议忽略）
├── .gitignore                # Git 忽略规则
├── README.md                 # 项目说明
├── LICENSE                   # 如需补充时添加
└── .vscode/                  # 本地编辑器配置（已忽略，不应提交）
```

> 注意：模型文件通常不适合直接提交到公共仓库，项目已在 `.gitignore` 中忽略大多数模型与生成产物。

---

## 快速开始

### 1. 克隆项目

```bash
git clone git@github.com:LinJJ12/RAF-DB-Based-Facial-Emotion-Recognition-System.git
cd RAF-DB-Based-Facial-Emotion-Recognition-System
```

### 2. 后端启动

Windows / cmd：

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install "tensorflow"
python app.py
```

默认服务地址：

```text
http://localhost:5000
```

### 3. 前端启动

```cmd
cd frontend
npm install
npm run dev
```

默认前端地址：

```text
http://localhost:3000
```

---

## 主要接口

后端主要接口包括：

- `GET /api/health`：服务健康检查
- `GET /api/models`：模型状态与路径
- `POST /api/predict`：单图情绪识别
- `POST /api/batch_predict`：批量识别
- `POST /api/video/upload`：上传视频
- `POST /api/video/analyze`：视频情绪分析

示例：

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"image":"data:image/jpeg;base64,/9j/4AAQ...","model":"cnn","detect_face":true}'
```

---

## 模型说明

目前项目支持以下模型类型：

- `cnn`
- `vgg`
- `se81`
- `se83`

模型文件应放置在 `models/` 目录中，后端会自动按 `MODEL_PATHS` 进行加载。

若要公开发布代码，建议保留代码、配置与训练脚本，但忽略大型模型文件与生成产物，这样更适合 GitHub 开源托管。

---

## 运行与部署注意事项

- 推荐 Python 3.10+ 环境
- TensorFlow 需单独安装，建议与训练环境版本保持一致
- 若 GPU 环境可使用对应版本的 TensorFlow + CUDA / cuDNN
- 生产部署建议使用 Gunicorn / uWSGI 等 Web Server
- 大模型、日志、上传文件和缓存目录建议保持在 `.gitignore` 中忽略

---

## 目录说明

- `backend/`：后端接口、数据库、预处理、推理逻辑
- `backend/tests/`：后端单元/接口测试脚本
- `frontend/`：前端页面、路由、状态管理、API 适配
- `scripts/`：项目辅助脚本
- `models/`：保存模型文件（通常应忽略不提交）
- `backend/uploads/`：上传图片和视频缓存，通常应忽略提交
- `backend/logs/`：运行日志，通常应忽略提交

---

## 许可与说明

本项目适合用于学习、研究和个人二次开发。若将其用于公开发布或商业场景，请根据具体需求补充清晰的开源许可证和项目说明。

---

## 相关参考

- RAF-DB 数据集：用于表情识别任务训练
- 前端与后端代码均位于当前仓库中，可直接本地运行

如果你希望，我还可以继续把这个 README 再调整成更偏“GitHub 风格”的版本，例如更适合正式开源仓库展示的布局。


