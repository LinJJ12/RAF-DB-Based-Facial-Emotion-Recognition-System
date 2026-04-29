<<<<<<< HEAD
"""
配置文件
"""
import os
from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

# 模型配置
MODEL_DIR = PROJECT_DIR / 'models'
MODEL_CONFIG = {
    'cnn': {
        'path': MODEL_DIR / 'RAF_CNN_83_best_model.h5',
        'input_shape': (100, 100, 3),
        'description': 'CNN基础模型',
        'accuracy': 0.8377
    },
    'vgg': {
        'path': MODEL_DIR / 'RAF_VGG_80_best_model.h5',
        'input_shape': (100, 100, 3),
        'description': 'VGG16迁移学习模型',
        'accuracy': 0.8000
    },
    'se81': {
        'path': MODEL_DIR / 'RAF_SE_81_saved_model',
        'input_shape': (100, 100, 3),
        'description': 'SE注意力机制模型',
        'accuracy': 0.8100
    },
    'se83': {
        'path': MODEL_DIR / 'RAF_SE_83_saved_model',
        'input_shape': (100, 100, 3),
        'description': 'SE注意力机制模型(最佳)',
        'accuracy': 0.8300
    }
}

# 服务器配置
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# 上传配置
UPLOAD_FOLDER = BASE_DIR / 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 数据库配置(可选)
DATABASE_CONFIG = {
    'type': 'sqlite',  # sqlite, mysql, postgresql
    'sqlite_path': BASE_DIR / 'emotion_recognition.db',
    # MySQL配置(如果使用)
    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'your_password',
        'database': 'emotion_db'
    }
}

# 日志配置
LOG_DIR = BASE_DIR / 'logs'
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': LOG_DIR / 'app.log'
}

# 确保目录存在
UPLOAD_FOLDER.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
=======
"""
配置文件
"""
import os
from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

# 模型配置
MODEL_DIR = PROJECT_DIR / 'models'
MODEL_CONFIG = {
    'cnn': {
        'path': MODEL_DIR / 'RAF_CNN_83_best_model.h5',
        'input_shape': (100, 100, 3),
        'description': 'CNN基础模型',
        'accuracy': 0.8377
    },
    'vgg': {
        'path': MODEL_DIR / 'RAF_VGG_80_best_model.h5',
        'input_shape': (100, 100, 3),
        'description': 'VGG16迁移学习模型',
        'accuracy': 0.8000
    },
    'se81': {
        'path': MODEL_DIR / 'RAF_SE_81_saved_model',
        'input_shape': (100, 100, 3),
        'description': 'SE注意力机制模型',
        'accuracy': 0.8100
    },
    'se83': {
        'path': MODEL_DIR / 'RAF_SE_83_saved_model',
        'input_shape': (100, 100, 3),
        'description': 'SE注意力机制模型(最佳)',
        'accuracy': 0.8300
    }
}

# 服务器配置
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# 上传配置
UPLOAD_FOLDER = BASE_DIR / 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 数据库配置(可选)
DATABASE_CONFIG = {
    'type': 'sqlite',  # sqlite, mysql, postgresql
    'sqlite_path': BASE_DIR / 'emotion_recognition.db',
    # MySQL配置(如果使用)
    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'your_password',
        'database': 'emotion_db'
    }
}

# 日志配置
LOG_DIR = BASE_DIR / 'logs'
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': LOG_DIR / 'app.log'
}

# 确保目录存在
UPLOAD_FOLDER.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
>>>>>>> 138c776de10fc6103a4f59748d2d365b9b0350e6
