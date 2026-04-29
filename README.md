# 人脸情绪识别系统（基于 RAF‑DB）

## 项目概述

一个端到端的人脸情绪识别系统，覆盖数据预处理、模型训练、导出与工程化部署。支持图片和视频的离线/在线情绪分析、历史记录与可视化分析界面。模型文件位于 `models/` 目录（示例：`RAF_CNN_83_best_model.h5`, `RAF_SE_83_saved_model/`）。

## 主要功能
- 图片/视频情绪识别（单张预测 / 批量预测 / 视频分析）
- 人脸检测、对齐（MTCNN 回退至 Haar）、人脸质量评估
- 多模型支持：CNN / VGG / SE(Net) 变体（.h5 与 SavedModel）
- 前端使用 Vue3 提供交互页面与可视化（ECharts）
- 本地历史存储（IndexedDB）与服务器端轻量持久化

## 技术栈
- 前端：Vue 3, Vite, Pinia, Vue Router, Element Plus, Axios, ECharts
- 后端：Python, Flask, flask-cors, OpenCV, Pillow, PyJWT
- 深度学习：TensorFlow / Keras（.h5 与 SavedModel）
- 模型文件：放在 `models/` 目录

## 目录结构（简要）
- `backend/`：Flask 服务、模型加载、视频与图像预处理、数据库代码
- `frontend/`：Vue 前端代码（`frontend/src/`）
- `models/`：训练后保存的模型文件（.h5 / SavedModel）
- `uploads/`：上传的视频与预测图片缓存

## 快速开始（开发/本地）

推荐在虚拟环境中运行后端服务，并在前端单独启动开发服务器。

1. 克隆仓库到本地：

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. 后端（Windows / cmd）：

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# 安装 TensorFlow（根据是否有 GPU，选择 tensorflow 或 tensorflow-cpu）
pip install "tensorflow"
python app.py
```

默认后台服务监听 `http://0.0.0.0:5000`。生产部署建议使用 WSGI 容器（gunicorn、uvicorn 或 Docker）。

3. 前端：

```cmd
cd frontend
npm install
npm run dev
```

默认前端开发服务器由 Vite 提供，详情见 `frontend/package.json`。

4. 模型文件

已包含示例训练好的模型在 `models/` 目录。后端会根据 `backend/app.py` 中的 `MODEL_PATHS` 自动查找并加载这些模型。

## 常用 API（后端示例）

- `GET /api/health` — 健康检查与可用模型列表
- `GET /api/models` — 列出可用模型与路径
- `POST /api/predict` — 单张图片预测（JSON，image 为 base64）
- `POST /api/batch_predict` — 批量图片预测
- `POST /api/video/upload` — 上传视频（multipart/form-data）
- `POST /api/video/analyze` — 分析已上传视频（video_id）

示例：使用 curl 对单张图片预测（假设已将图片编码为 base64 并去掉前缀）

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"image":"data:image/jpeg;base64,/9j/4AAQ...","model":"cnn","detect_face":true}'
```

返回 JSON 中包含：`emotion`, `emotion_cn`, `confidence`, `probabilities`, `face_quality` 与 `performance` 信息。

## 运行注意事项与依赖
- `backend/requirements.txt` 列出基础依赖（Flask、OpenCV 等），但未指定 TensorFlow（需手动安装）。
- 若使用 GPU 训练/推理，请安装对应的 GPU 版 TensorFlow 并配置 CUDA/cuDNN。
- 推荐为 Python 3.8+ 环境。

## 模型训练与导出（简要）
- 训练基于 RAF‑DB 数据集，尝试的模型包括 VGG、常规 CNN、以及带 SE 模块的网络。
- 导出为 Keras `.h5` 或 `SavedModel` 格式以便后端加载。

## 常见问题与调试
- 如果后端提示找不到模型，请检查 `models/` 路径与 `backend/app.py` 中 `MODEL_PATHS` 配置。
- 若遇到 MTCNN 未安装或检测回退，可安装 `mtcnn` 或回退使用 Haar 级联。

## 贡献与许可
欢迎 issue 与 PR。可按需补充训练脚本、Dockerfile、CI 配置等。

（示例仓库说明，默认许可请替换为合适的 License，例如 MIT）

---

项目文件已生成 README，若需要我可以：
- 1) 生成英文版 README；
- 2) 添加 `requirements.txt` 中缺失的 TensorFlow 说明或具体版本；
- 3) 创建 `Dockerfile` 与 `docker-compose.yml` 示例用于一键部署。
