#!/usr/bin/env python3
"""材料价格数据库模型"""
import sqlite3
from datetime import datetime, date
from typing import List, Optional, Tuple

DB_PATH = "material_prices.db"


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 创建材料分类表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS material_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        unit TEXT NOT NULL,
        description TEXT
    )
    """)
    
    # 创建材料价格表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS material_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        material_name TEXT NOT NULL,
        specification TEXT,
        brand TEXT,
        price REAL NOT NULL,
        city TEXT DEFAULT '全国',
        source TEXT,
        collect_date DATE NOT NULL,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES material_categories(id),
        UNIQUE(category_id, material_name, specification, brand, city, collect_date)
    )
    """)
    
    # 创建索引
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_prices_date 
    ON material_prices(collect_date)
    """)
    
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_prices_material 
    ON material_prices(material_name, collect_date)
    """)
    
    # 插入默认材料分类
    default_categories = [
        ("钢筋", "吨", "螺纹钢、盘螺、线材等"),
        ("水泥", "吨", "P.O 42.5、P.O 52.5等"),
        ("混凝土", "立方米", "C30、C40等商品混凝土"),
        ("砂石", "吨", "中砂、碎石、机制砂等"),
        ("木材", "立方米", "方木、模板等"),
        ("玻璃", "平方米", "浮法玻璃、钢化玻璃等"),
        ("铝合金", "吨", "铝型材、铝板等"),
        ("沥青", "吨", "道路石油沥青等"),
        ("电缆", "米", "电力电缆、控制电缆等"),
        ("管材", "米", "PVC管、PE管、钢管等"),
    ]
    
    for name, unit, desc in default_categories:
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO material_categories (name, unit, description)
            VALUES (?, ?, ?)
            """, (name, unit, desc))
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    print("数据库初始化完成")


def insert_price(category_id: int, material_name: str, price: float,
                 specification: str = None, brand: str = None,
                 city: str = "全国", source: str = None,
                 collect_date: str = None, source_url: str = None,
                 unit: str = "元/吨", change_amount: float = None,
                 change_percent: float = None) -> bool:
    """插入一条价格记录"""
    if collect_date is None:
        collect_date = date.today().isoformat()
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO material_prices 
        (category_id, material_name, specification, brand, price, city, source, 
         collect_date, source_url, unit, change_amount, change_percent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (category_id, material_name, specification, brand, price, city, source,
              collect_date, source_url, unit, change_amount, change_percent))
        conn.commit()
        return True
    except Exception as e:
        print(f"插入价格失败: {e}")
        return False
    finally:
        conn.close()


def get_price_trend(material_name: str, days: int = 30, city: str = None) -> List[dict]:
    """获取材料价格趋势"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT collect_date, price, specification, brand, city, source
    FROM material_prices 
    WHERE material_name LIKE ?
    AND collect_date >= date('now', ?)
    """
    params = [f"%{material_name}%", f"-{days} days"]
    
    if city:
        query += " AND city = ?"
        params.append(city)
    
    query += " ORDER BY collect_date ASC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_latest_prices(category_name: str = None, city: str = None) -> List[dict]:
    """获取最新价格"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT p.*, c.name as category_name, c.unit
    FROM material_prices p
    JOIN material_categories c ON p.category_id = c.id
    WHERE p.collect_date = (
        SELECT MAX(collect_date) FROM material_prices
    )
    """
    params = []
    
    if category_name:
        query += " AND c.name = ?"
        params.append(category_name)
    
    if city:
        query += " AND p.city = ?"
        params.append(city)
    
    query += " ORDER BY c.name, p.material_name"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_categories() -> List[dict]:
    """获取所有材料分类"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM material_categories ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_materials(keyword: str) -> List[dict]:
    """搜索材料"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT DISTINCT material_name, category_id 
    FROM material_prices 
    WHERE material_name LIKE ?
    ORDER BY material_name
    """, (f"%{keyword}%",))
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_price(price_id: int) -> bool:
    """删除单条价格记录"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM material_prices WHERE id = ?", (price_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"删除失败: {e}")
        return False
    finally:
        conn.close()


def delete_prices_batch(price_ids: List[int]) -> int:
    """批量删除价格记录"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        placeholders = ','.join(['?' for _ in price_ids])
        cursor.execute(f"DELETE FROM material_prices WHERE id IN ({placeholders})", price_ids)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"批量删除失败: {e}")
        return 0
    finally:
        conn.close()


def delete_prices_by_source(source: str) -> int:
    """按来源删除价格记录"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM material_prices WHERE source = ?", (source,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"按来源删除失败: {e}")
        return 0
    finally:
        conn.close()


def delete_prices_by_date(collect_date: str) -> int:
    """按日期删除价格记录"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM material_prices WHERE collect_date = ?", (collect_date,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"按日期删除失败: {e}")
        return 0
    finally:
        conn.close()


def get_price_by_id(price_id: int) -> dict:
    """获取单条价格记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, c.name as category_name, c.unit
        FROM material_prices p
        JOIN material_categories c ON p.category_id = c.id
        WHERE p.id = ?
    """, (price_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


if __name__ == "__main__":
    init_db()
