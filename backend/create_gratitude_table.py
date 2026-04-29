"""
创建 gratitude_record 表的迁移脚本
用于存储用户的感恩记录（积极心理学练习）
"""
import sqlite3
import os

def create_gratitude_table():
    """创建 gratitude_record 表"""
    db_path = 'instance/emotion_recognition.db'
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否已存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='gratitude_record'
        """)
        
        if cursor.fetchone():
            print("ℹ️ gratitude_record 表已存在，无需创建")
        else:
            print("🔍 开始创建 gratitude_record 表...")
            
            # 创建表
            cursor.execute("""
                CREATE TABLE gratitude_record (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(80) NOT NULL,
                    items TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 创建索引以提高查询性能
            cursor.execute("""
                CREATE INDEX idx_gratitude_username 
                ON gratitude_record(username)
            """)
            
            cursor.execute("""
                CREATE INDEX idx_gratitude_created_at 
                ON gratitude_record(created_at DESC)
            """)
            
            conn.commit()
            print("✅ 成功创建 gratitude_record 表")
            print("✅ 成功创建索引: idx_gratitude_username, idx_gratitude_created_at")
        
        # 显示表结构
        cursor.execute("PRAGMA table_info(gratitude_record)")
        columns = cursor.fetchall()
        print("\n📋 gratitude_record 表结构:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # 显示所有表
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)
        
        tables = cursor.fetchall()
        print("\n📋 数据库中的所有表:")
        for table in tables:
            print(f"  - {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 创建表时出错: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("创建 gratitude_record 表")
    print("=" * 60)
    create_gratitude_table()
    print("=" * 60)
