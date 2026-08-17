# 人脸情绪识别系统（基于 RAF-DB）

<p align="center">
  <img src="frontend/public/logo.png" alt="Facial Emotion Recognition Logo" width="160" />
</p>

<p align="center">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-2.x-00A6D6" />
  <img alt="Vue 3" src="https://img.shields.io/badge/Vue-3.x-41B883" />
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00" />
  <img alt="License: CC BY-NC 4.0" src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey" />
</p>

<p align="center">
  <strong>基于 RAF-DB 的人脸情绪识别系统</strong><br />
  支持图片识别、视频分析、历史记录与心理健康辅助功能
</p>

---

## 简介

本项目面向学习与研究场景，完整覆盖人脸情绪识别的常见链路：图像预处理、多模型推理、结果展示与用户侧能力。后端基于 Flask 与 TensorFlow / Keras，前端基于 Vue 3 与 Vite。

主要能力包括：

- 单图 / 批量图片情绪识别
- 视频抽帧情绪分析
- 人脸检测、对齐与质量评估
- 多模型切换：CNN、VGG、SE-Net
- JWT 认证、用户管理与管理后台
- 情绪汇总、日记、感恩记录与健康评估等辅助模块

> **许可说明**：本项目采用 [CC BY-NC 4.0](LICENSE)。仅供学习、研究与个人技术交流；禁止商业用途（含出售、商业部署、收费服务等）。复用时请保留署名并遵守非商用约定。

---

## 功能特性

| 模块 | 说明 |
|------|------|
| 情绪识别 | 单图预测、批量预测、视频抽帧分析、多模型切换 |
| 图像处理 | MTCNN 人脸检测与对齐、Haar 回退、清晰度 / 亮度 / 对比度评估 |
| 用户与管理 | JWT 认证、注册登录、资料管理、管理后台、历史统计 |
| 心理健康辅助 | 情绪汇总、健康评估、情绪日记、感恩记录 |

> 本系统输出仅供参考，不构成医学或心理诊断建议。

---

## 技术栈

- **前端**：Vue 3、Vite、Pinia、Vue Router、Element Plus、Axios、ECharts
- **后端**：Python、Flask、Flask-CORS、Flask-SQLAlchemy、OpenCV、Pillow、PyJWT
- **深度学习**：TensorFlow / Keras
- **数据存储**：默认 SQLite（可通过 `DATABASE_URL` 切换）

---

## 仓库结构

```text
.
├── backend/                 # Flask API
│   ├── main.py              # 启动入口
│   ├── src/                 # 运行时代码（api / auth / config / storage / ml）
│   ├── scripts/             # 迁移与运维脚本
│   ├── tests/
│   └── data/                # 运行时数据（uploads / logs / db，内容默认忽略）
├── frontend/                # Vue 3 前端
│   ├── public/              # Favicon、Logo 等静态资源
│   └── src/                 # pages / api / assets / stores ...
├── models/                  # 模型权重（大文件，默认忽略）
├── docs/                    # 目录约定与设计源文件
├── LICENSE
└── README.md
```

详细约定见 [docs/directory-structure.md](docs/directory-structure.md)，后端说明见 [backend/README.md](backend/README.md)。

---

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+（建议）
- 将模型文件放置于仓库根目录 `models/`（路径由 `backend/src/config/settings.py` 统一管理）

### 1. 克隆

```bash
git clone https://github.com/LinJJ12/RAF-DB-Based-Facial-Emotion-Recognition-System.git
cd RAF-DB-Based-Facial-Emotion-Recognition-System
```

### 2. 后端

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install "tensorflow"
python main.py
```

默认地址：`http://localhost:5000`

也可从仓库根目录执行：`python backend/main.py`。

### 3. 前端

```cmd
cd frontend
npm install
npm run dev
```

默认地址：`http://localhost:3000`（开发服务器将 `/api` 代理至后端）。

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `JWT_SECRET_KEY` | JWT 签名密钥。**部署前必须设置为足够随机的强密钥** |
| `DATABASE_URL` | 可选。默认：`backend/data/db/emotion_recognition.db` |

---

## 主要 API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/health` | 服务健康检查 |
| `GET` | `/api/models` | 模型状态 |
| `POST` | `/api/predict` | 单图情绪识别 |
| `POST` | `/api/batch_predict` | 批量识别 |
| `POST` | `/api/video/upload` | 上传视频 |
| `POST` | `/api/video/analyze` | 视频情绪分析 |

示例：

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d "{\"image\":\"data:image/jpeg;base64,...\",\"model\":\"cnn\",\"detect_face\":true}"
```

---

## 模型说明

支持的模型键名：`cnn`、`vgg`、`se81`、`se83`。  
权重与 SavedModel 放置于 `models/`，由配置中的 `MODEL_PATHS` 加载。大型模型文件不纳入版本库，请按训练或发布说明自行准备。

---

## 安全与隐私

- 上传图片 / 视频默认保存在本地 `backend/data/`，请勿将含真实用户数据的数据库、日志或上传目录提交到公开仓库。
- 公网或共享环境部署前，务必配置 `JWT_SECRET_KEY`，并修改或禁用本地演示用账号与弱口令。
- 本仓库文档与示例不包含真实用户隐私数据；请勿在 Issue、截图或提交中粘贴个人身份信息、密钥或生产凭据。

---

## 部署注意

- TensorFlow 版本建议与训练环境保持一致；GPU 需匹配 CUDA / cuDNN。
- 生产环境建议使用 Gunicorn / uWSGI 等 WSGI 服务器，并关闭调试模式。
- 日志、上传缓存与数据库文件应继续保持在 `.gitignore` 中。

---

## 许可

详见 [LICENSE](LICENSE)（CC BY-NC 4.0）。

---

## 致谢与参考

- [RAF-DB](http://www.whdeng.cn/RAF/model1.html) 表情识别数据集及相关研究工作
