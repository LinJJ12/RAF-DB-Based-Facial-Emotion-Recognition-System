"""
删除 health_tool_usage 表的迁移脚本
该表已不再使用，需要从数据库中删除
"""
import sqlite3
import os
from _db_path import resolve_db_path

def drop_tool_usage_table():
    """删除 health_tool_usage 表"""
    db_path = str(resolve_db_path())
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='health_tool_usage'
        """)
        
        if cursor.fetchone():
            print("🔍 找到 health_tool_usage 表，准备删除...")
            
            # 删除表
            cursor.execute("DROP TABLE IF EXISTS health_tool_usage")
            conn.commit()
            print("✅ 成功删除 health_tool_usage 表")
        else:
            print("ℹ️ health_tool_usage 表不存在，无需删除")
        
        # 显示剩余的表
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)
        
        tables = cursor.fetchall()
        print("\n📋 数据库中剩余的表:")
        for table in tables:
            print(f"  - {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 删除表时出错: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("删除 health_tool_usage 表")
    print("=" * 60)
    drop_tool_usage_table()
    print("=" * 60)
