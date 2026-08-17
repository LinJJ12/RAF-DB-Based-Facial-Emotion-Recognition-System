"""
为 health_assessment 表添加 updated_at 列
"""

import _bootstrap  # noqa: F401
from src.storage.database import db
from src.api.app import app
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_timestamp_columns():
    """为 health_assessment 表添加 updated_at 列"""
    with app.app_context():
        try:
            # 使用 connection 执行原生 SQL
            with db.engine.connect() as connection:
                # 检查列是否已存在
                result = connection.execute(db.text("PRAGMA table_info(health_assessment)"))
                columns = [row[1] for row in result]
                
                if 'updated_at' not in columns:
                    logger.info("添加 updated_at 列到 health_assessment 表...")
                    # SQLite 使用 ALTER TABLE ADD COLUMN
                    connection.execute(db.text(
                        "ALTER TABLE health_assessment ADD COLUMN updated_at DATETIME"
                    ))
                    connection.commit()
                    logger.info("✅ 成功添加 updated_at 列")
                else:
                    logger.info("ℹ️  updated_at 列已存在")
                
                # 更新所有现有记录的 updated_at 为 created_at 的值
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                connection.execute(db.text(
                    f"UPDATE health_assessment SET updated_at = '{current_time}' WHERE updated_at IS NULL"
                ))
                connection.commit()
                logger.info("✅ 已更新所有现有记录的 updated_at 时间戳")
                
        except Exception as e:
            logger.error(f"❌ 添加列时发生错误: {e}")
            raise

if __name__ == '__main__':
    print("=" * 60)
    print("开始为 health_assessment 表添加 updated_at 列...")
    print("=" * 60)
    
    try:
        add_timestamp_columns()
        print("\n✅ 数据库迁移完成！")
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        exit(1)
