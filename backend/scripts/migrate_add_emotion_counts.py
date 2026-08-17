"""
添加 emotion_counts 和 dominant_emotion_count 字段到 user_emotion_summary 表
"""
import sqlite3
import os
from _db_path import resolve_db_path

def migrate():
    db_path = str(resolve_db_path())
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        print("尝试查找数据库文件...")
        if os.path.exists('emotion_recognition.db'):
            db_path = 'emotion_recognition.db'
        else:
            return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(user_emotion_summary)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"当前字段: {columns}")
        
        # 添加 emotion_counts 字段
        if 'emotion_counts' not in columns:
            print("添加 emotion_counts 字段...")
            cursor.execute(
                "ALTER TABLE user_emotion_summary ADD COLUMN emotion_counts TEXT"
            )
            print("✅ emotion_counts 字段已添加")
        else:
            print("⚠️  emotion_counts 字段已存在")
        
        # 添加 dominant_emotion_count 字段
        if 'dominant_emotion_count' not in columns:
            print("添加 dominant_emotion_count 字段...")
            cursor.execute(
                "ALTER TABLE user_emotion_summary ADD COLUMN dominant_emotion_count INTEGER DEFAULT 0"
            )
            print("✅ dominant_emotion_count 字段已添加")
        else:
            print("⚠️  dominant_emotion_count 字段已存在")
        
        conn.commit()
        print("\n✅ 数据库迁移完成！")
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
