# 目录结构说明

本仓库参照 OmniStream 的原则做了适配：**运行时代码 / 一次性脚本 / 文档 / 品牌资源分离**。  
不引入 OmniStream 的 agent / skills / workflows 分层。

更完整的启动说明见根目录 [README.md](../README.md) 与 [backend/README.md](../backend/README.md)。

## 仓库布局

```text
基于RAF-DB的人脸情绪识别系统/
├── README.md / LICENSE / .gitignore
├── docs/                              # 文档与设计稿（非运行时）
│   ├── directory-structure.md
│   └── brand/logo-design-source.png   # Logo 设计源图
├── models/                            # 训练产物（通常 gitignore）
├── backend/
│   ├── main.py                        # 启动入口
│   ├── requirements.txt
│   ├── README.md
│   ├── src/
│   │   ├── api/                       # Flask HTTP（app、health）
│   │   ├── auth/                      # JWT 认证
│   │   ├── config/settings.py         # 路径 / 模型 / 服务配置（单一来源）
│   │   ├── storage/                   # SQLAlchemy
│   │   └── ml/                        # 预处理、人脸质量、视频
│   ├── scripts/                       # 迁移与运维一次性脚本
│   ├── tests/
│   └── data/                          # 运行时 uploads / logs / db（内容忽略）
└── frontend/
    ├── public/                        # favicon.png、logo.png；演示视频（忽略）
    ├── index.html / package.json / vite.config.js
    └── src/
        ├── pages/                     # 路由页面
        ├── api/                       # HTTP 客户端（client / health）
        ├── utils/                     # IndexedDB 等非 HTTP 工具
        ├── components/ / stores/ / router/ / data/
        └── assets/
            ├── brand/logo.png         # 页面内引用的品牌图
            └── styles/theme.css
```

## 品牌资源放哪里

| 路径 | 用途 |
|------|------|
| `frontend/src/assets/brand/` | 前端组件通过 `@/assets/brand/logo.png` 引用 |
| `frontend/public/` | 浏览器 Favicon、README 展示图、静态 URL |
| `docs/brand/` | 设计源文件，不参与前端打包 |
| ~~仓库根 `assets/`~~ | **已废弃**，勿再放应用图标 |

## 导入与路径约定

- 后端在 `backend/` 下运行：`python main.py`；业务导入形如 `from src.api.app import app`
- 配置只读 `src.config.settings`（含 `MODEL_PATHS`、`UPLOAD_FOLDER`、`DATABASE_URI`）
- 上传文件相对 `backend/data/uploads/` 存库，经 `/api/uploads/<path>` 访问
- 运维脚本：`import _bootstrap` 后再 `from src....`
- 前端 HTTP 只放在 `src/api/`；页面在 `src/pages/`

## 明确不要放错的地方

- 不要把迁移脚本放回 `backend/` 根目录
- 不要把 Vue 页面放回 `views/`（已统一为 `pages/`）
- 不要把 axios 封装放回 `utils/`（已在 `api/`）
- 不要在仓库根再建 `assets/` 放 Logo
