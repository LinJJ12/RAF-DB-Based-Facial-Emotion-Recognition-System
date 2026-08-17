# 后端说明

基于 RAF-DB 的人脸情绪识别 Flask API。

## 目录

```text
backend/
├── main.py                 # 启动：python main.py
├── requirements.txt
├── src/
│   ├── api/                # HTTP（app 路由、health 蓝图）
│   ├── auth/               # JWT 认证
│   ├── config/             # settings（路径、模型、服务）
│   ├── storage/            # SQLAlchemy 模型与初始化
│   └── ml/                 # 预处理、人脸质量、视频处理
├── scripts/                # 一次性迁移 / 运维脚本
├── tests/
└── data/                   # 运行时 uploads、logs、sqlite（内容默认忽略）
```

## 启动

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install "tensorflow"
python main.py
```

服务地址：`http://localhost:5000`

建议通过环境变量设置强随机 `JWT_SECRET_KEY`（未设置时会有警告）。

也可从仓库根目录执行：`python backend/main.py`（入口会自动处理 `sys.path`）。

## 运维脚本

脚本位于 `scripts/`。建议在该目录下执行（会自动把 `backend/` 加入 `sys.path`）：

```cmd
cd backend\scripts
python migrate_database.py
```

新脚本推荐写法：

```python
import _bootstrap  # noqa: F401
from src.storage.database import db
from src.api.app import app
```

SQLite 路径解析见 `_db_path.py`（优先 `data/db/`，兼容旧 `instance/`）。

## 测试

```cmd
cd backend
python tests\test_upload_paths.py
python tests\test_preprocessing.py
```

依赖真实模型文件的用例需先将权重放到仓库根 `models/`。
