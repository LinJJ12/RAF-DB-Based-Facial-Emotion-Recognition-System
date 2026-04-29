# 后端说明（Flask + 推理 + 心理健康 + 认证）

本文档介绍后端的功能、模块划分、主要接口、数据库结构、模型与预处理、以及迁移与运行方法。

## 快速开始（Windows cmd）

```cmd
cd backend
pip install -r requirements.txt
python app.py
```

服务默认运行在 `http://localhost:5000`。

## 模块结构与职责

- `app.py`（主应用）
  - 健康与模型：`GET /api/health`、`GET /api/models`
  - 情绪识别：`POST /api/predict`、`POST /api/batch_predict`
  - 上传与限制：请求体/图片/视频大小限制；CORS；统一日志与计时装饰器
  - 模型加载：支持 `.h5`（Keras）与 SavedModel；统一推理接口
  - 依赖工具：
    - `image_preprocess.py`：推断输入形状、Simple/VGG/EfficientNet 预处理，人脸检测与对齐（MTCNN/Haar），清晰度增强
    - `face_quality.py`：清晰度、亮度、对比度综合评分与警告
    - `video_processor.py`：视频保存、抽帧、生成时间轴与情绪统计
  - 数据库：初始化与写入 `PredictionHistory`、`VideoAnalysisResult` 等

- `health_api.py`（心理健康蓝图，`/api/health`）
  - `GET /emotion-summary`：按日/多日汇总（总次数、正负比例、主导情绪、稳定性指标、活跃天数）
  - `GET /assessment`：基于汇总的自动评估（标题/类型/描述/建议列表/比率与稳定等级）
  - 情绪日记：`POST/GET/GET(id)/PUT/DELETE /journal`
  - 感恩记录：`POST/GET/GET(id)/DELETE /gratitude`

- `auth.py`（认证蓝图，`/api/auth`）
  - 注册/登录/刷新 Token/当前用户/更新资料/修改密码/登出
  - 管理员：用户列表、创建、详情（查/改/删）、启用禁用、系统统计
  - 用户来源：内存模拟用户 +（可选）数据库持久化（启用时自动读写）

- `database.py`（数据库与模型）
  - `PredictionHistory`：历史记录（轻量化存路径与小 JSON）
  - `User`、`UserEmotionSummary`、`HealthAssessment`、`VideoAnalysisResult`、`EmotionJournal`、`GratitudeRecord`
  - `init_db(app)`：自动建表；SQLite 轻量加列升级

- 其他：
  - `config.py`：模型路径与描述、端口、上传与日志目录
  - `image_preprocess.py`/`face_quality.py`/`video_processor.py`：见上

## 模型与预处理

- 模型键与路径（详见 `app.py` 的 `MODEL_PATHS` 与 `config.py` 的 `MODEL_CONFIG`）：
  - `cnn`：`../models/RAF_CNN_83_best_model.h5`
  - `vgg`：`../models/RAF_VGG_80_best_model.h5`
  - `se81`：`../models/RAF_SE_81_saved_model`
  - `se83`：`../models/RAF_SE_83_saved_model`
- 统一加载与推理：优先 Keras，失败回退 SavedModel；统一返回 `input_shape` 并使用相应预处理
- 预处理模式：
  - `simple`：缩放到 [0,1]
  - `vgg`：Caffe 风格（BGR + 均值减法）
  - `efficientnet`：若可用则调用 `tf.keras.applications.efficientnet.preprocess_input`，否则回退 [0,1]
- 人脸检测与对齐：优先 MTCNN（五点对齐到 112x112），失败回退 Haar；另提供仅用于展示的裁剪（避免黑边）
- 清晰度增强：LAB CLAHE + Unsharp Mask（前端预览友好）

## 主要 API（示例）

- 健康检查

```
GET /api/health
→ { status: 'ok', available_models: ['cnn','vgg','se81','se83'] }
```

- 模型列表

```
GET /api/models
→ { models: [{ name, display_name, available, path }, ...] }
```

- 单图情绪识别

```
POST /api/predict
Body: { image: 'data:image/jpeg;base64,...', model: 'cnn', detect_face: true }
→ { success, emotion, emotion_cn, confidence, probabilities, model_used, timestamp }
```

- 批量识别

```
POST /api/batch_predict
Body: { images: ['base64_1','base64_2',...], model: 'cnn', detect_face: true }
```

- 心理健康蓝图（节选）

```
GET /api/health/emotion-summary?date=YYYY-MM-DD&days=7
GET /api/health/assessment?date=YYYY-MM-DD
POST /api/health/journal  / GET /api/health/journal  / GET /api/health/journal/:id
PUT  /api/health/journal/:id  / DELETE /api/health/journal/:id
POST /api/health/gratitude   / GET  /api/health/gratitude
GET  /api/health/gratitude/:id  / DELETE /api/health/gratitude/:id
```

- 认证蓝图（节选）

```
POST /api/auth/register  / POST /api/auth/login  / POST /api/auth/refresh
GET  /api/auth/me  / PUT /api/auth/profile  / POST /api/auth/change-password
管理：GET/POST /api/auth/admin/users, GET/PUT/DELETE /api/auth/admin/users/:id, ...
```

## 数据库与迁移

- 默认 SQLite：`sqlite:///emotion_recognition.db`（可通过 `DATABASE_URL` 环境变量覆盖）
- 表结构：见 `database.py`；`PredictionHistory` 仅保存路径与小 JSON，避免冗大 base64
- 迁移（Flask-Migrate/Alembic）：

```cmd
cd backend
set FLASK_APP=app.py
set FLASK_ENV=development

python -m flask db init
python -m flask db migrate -m "init models"
python -m flask db upgrade
```

回滚：

```cmd
python -m flask db downgrade -1
```

切换到 MySQL/PostgreSQL：调整 `app.config['SQLALCHEMY_DATABASE_URI']` 或设置环境变量，再执行迁移命令。

## 运行配置与限制

- 上传限制（见 `app.py`）：
  - 总请求 ≤ 64MB；图片 ≤ 16MB；视频 ≤ 200MB（可按需调节）
- CORS 已启用；生产部署建议使用 Gunicorn/uWSGI，并开启 HTTPS；添加频率限制
- TensorFlow 与模型版本需兼容；建议内存 ≥ 4GB

## 故障排查（精选）

- 模型加载失败：核对路径与版本；SavedModel/Keras 两种加载方式均失败时检查导出格式
- 预处理不一致：确保前后端/训练阶段一致的预处理策略（VGG/EfficientNet/simple）
- 跨域报错：前端代理与后端 CORS 是否正确；生产环境需额外配置 CORS/反向代理
- 数据库字段缺失：SQLite 下 `init_db` 内含轻量加列逻辑；复杂演进使用 Alembic 迁移
