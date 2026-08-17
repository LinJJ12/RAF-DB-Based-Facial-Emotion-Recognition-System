"""
删除 health_advice_interaction 表的迁移脚本
用于清理不再使用的建议交互记录表
"""

import _bootstrap  # noqa: F401
from src.storage.database import db
from src.api.app import app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def drop_advice_interaction_table():
    """删除 health_advice_interaction 表"""
    with app.app_context():
        try:
            # 检查表是否存在
            from sqlalchemy import text
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'health_advice_interaction' in tables:
                # 删除表 - 使用 session.execute 和 text()
                db.session.execute(text('DROP TABLE IF EXISTS health_advice_interaction'))
                db.session.commit()
                logger.info("✅ 成功删除 health_advice_interaction 表")
            else:
                logger.info("ℹ️ health_advice_interaction 表不存在，无需删除")
                
        except Exception as e:
            logger.error(f"❌ 删除表时发生错误: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("=" * 60)
    print("开始删除 health_advice_interaction 表...")
    print("=" * 60)
    
    try:
        drop_advice_interaction_table()
        print("\n✅ 迁移完成！")
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        exit(1)
