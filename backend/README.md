# 人脸情绪识别系统 - 后端API

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动

## 📡 API接口文档

### 1. 健康检查
**GET** `/api/health`

响应:
```json
{
  "status": "ok",
  "message": "服务运行正常",
  "available_models": ["cnn", "vgg", "se"]
}
```

### 2. 获取模型列表
**GET** `/api/models`

响应:
```json
{
  "models": [
    {
      "name": "cnn",
      "display_name": "CNN",
      "available": true,
      "path": "../models/RAF_CNN_83_best_model.h5"
    }
  ]
}
```

### 3. 情绪识别
**POST** `/api/predict`

请求体:
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQ...",
  "model": "cnn",
  "detect_face": true
}
```

响应:
```json
{
  "success": true,
  "emotion": "happy",
  "emotion_cn": "高兴",
  "confidence": 0.95,
  "probabilities": {
    "anger": 0.01,
    "disgust": 0.01,
    "fear": 0.01,
    "happy": 0.95,
    "normal": 0.01,
    "sad": 0.005,
    "surprised": 0.005
  },
  "model_used": "CNN",
  "timestamp": "2025-10-15T10:30:00"
}
```

### 4. 批量识别
**POST** `/api/batch_predict`

请求体:
```json
{
  "images": ["base64_image_1", "base64_image_2"],
  "model": "cnn",
  "detect_face": true
}
```

## 🔧 配置说明

### 模型路径
在 `config.py` 中配置模型路径:
```python
MODEL_CONFIG = {
    'cnn': {
        'path': MODEL_DIR / 'RAF_CNN_83_best_model.h5',
        'input_shape': (100, 100, 3),
    }
}
```

### 数据库(可选)
如果需要保存识别历史:
1. 取消注释 `requirements.txt` 中的 Flask-SQLAlchemy
2. 在 `app.py` 中导入 `database.py`
3. 配置数据库连接

## 🐛 常见问题

### 1. 模型加载失败
- 检查模型文件路径是否正确
- 确认TensorFlow版本与训练时一致
- SE模型需要先定义模型结构

### 2. 跨域问题
已使用 `flask-cors` 处理,如仍有问题检查前端配置

### 3. 图像格式问题
- 支持 base64 编码的图像
- 支持 PNG, JPG, JPEG 格式
- 最大 16MB

## 📝 注意事项

1. **Python版本**: 建议使用 Python 3.8-3.10
2. **TensorFlow版本**: 确保与训练时版本一致
3. **内存占用**: 模型会占用一定内存,建议至少 4GB RAM
4. **生产部署**: 使用 Gunicorn 或 uWSGI
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## 🔐 安全建议

1. 添加请求频率限制
2. 使用HTTPS
3. 添加用户认证
4. 验证上传文件类型和大小
