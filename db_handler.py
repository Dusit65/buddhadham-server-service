# db_handler.py
import os
import pickle
import numpy as np
from sqlalchemy import create_engine, text
from debugger import log
from dotenv import load_dotenv

# โหลด .env
load_dotenv()  # จะอ่านไฟล์ .env ใน directory เดียวกับ script

def get_engine():
    # อ่านค่าจาก env
    conn_str = os.getenv("conn_str")
    if not conn_str:
        raise ValueError("conn_str ไม่ถูกตั้งค่าใน .env")
    return create_engine(conn_str, pool_pre_ping=True)

def fetch_documents():
    """ดึงข้อมูลทั้งหมดจาก DB -> flatten"""
    engine = get_engine()
    with engine.connect() as conn:
        sql = """
        SELECT b.bookId, b.bookName, c.chapterId, c.chapterName, c.chapterText
        FROM book_tb b
        JOIN chapter_tb c ON b.bookId = c.bookId
        """
        rows = conn.execute(text(sql)).fetchall()

    docs = []
    for r in rows:
        docs.append({
            "bookId": r.bookId,
            "bookName": r.bookName,
            "chapter": r.chapterId,
            "chapterName": r.chapterName,
            "content": r.chapterText
        })
    log(f"โหลดเอกสารจาก DB {len(docs)} รายการ")
    return docs

def get_last_update_time():
    """ดึงเวลาล่าสุดของ book_tb และ chapter_tb"""
    log("ดึงเวลาล่าสุดของ book_tb และ chapter_tb")
    engine = get_engine()
    with engine.connect() as conn:
        q1 = conn.execute(text("SELECT MAX(updatedAt) as last_update FROM book_tb")).scalar()
        q2 = conn.execute(text("SELECT MAX(updatedAt) as last_update FROM chapter_tb")).scalar()

    last_update = max(q1 or "1970-01-01", q2 or "1970-01-01")
    return str(last_update)

def save_embeddings_to_db(embeddings, docs):
    """บันทึก embeddings และ metadata ลง DB (dynamic dimension, no timestamp)"""
    engine = get_engine()
    
    # เก็บ dimension ของ embeddings ไว้ใน metadata
    docs_with_dim = []
    for doc in docs:
        new_doc = dict(doc) if isinstance(doc, dict) else {"content": doc}
        new_doc["dim"] = embeddings.shape[1] if embeddings.ndim > 1 else embeddings.size
        docs_with_dim.append(new_doc)
    
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM embeddings_tb"))  # เก็บล่าสุดแค่ชุดเดียว
        conn.execute(
            text("INSERT INTO embeddings_tb (embeddings, metadata) VALUES (:emb, :meta)"),
            {
                "emb": embeddings.astype("float32").tobytes(),
                "meta": pickle.dumps(docs_with_dim)
            }
        )
    log("บันทึก embeddings/metadata ลง DB สำเร็จ")

def load_embeddings_from_db():
    """โหลด embeddings และ metadata จาก DB (dynamic dimension)"""
    engine = get_engine()
    dialect = engine.dialect.name.lower()

    # SQL แยกตาม DB
    if dialect == "mysql":
        sql = "SELECT embeddings, metadata FROM embeddings_tb ORDER BY id DESC LIMIT 1"
    else:  # สมมติใช้ SQL Server
        sql = "SELECT TOP 1 embeddings, metadata FROM embeddings_tb ORDER BY id DESC"

    with engine.connect() as conn:
        row = conn.execute(text(sql)).first()
        if not row:
            return None, None
        
        docs = pickle.loads(row.metadata)
        # อ่าน dimension จาก metadata ของ doc แรก
        dim = docs[0]["dim"] if isinstance(docs, list) and "dim" in docs[0] else None
        if dim is None:
            raise ValueError("ไม่พบ dimension ของ embeddings ใน metadata")
        
        embeddings = np.frombuffer(row.embeddings, dtype="float32").reshape(-1, dim)
        return embeddings, docs