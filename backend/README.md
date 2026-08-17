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

也可从仓库根目录执行：`python backend/main.py`。

## 安全配置

- 通过环境变量设置 `JWT_SECRET_KEY`（强随机值）。未设置时仅适合本地调试。
- `data/` 下的数据库、上传文件与日志可能包含用户数据，**请勿提交到公开仓库**。
- 本地开发若存在演示账号，公网部署前必须修改口令或删除演示用户。

## 运维脚本

脚本位于 `scripts/`：

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

依赖真实模型文件的用例需先将权重放到仓库根目录 `models/`。
