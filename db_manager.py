import sqlite3
import struct
from utils import debug_print

def setup_database():
    conn = sqlite3.connect('code_embeddings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS embeddings (
            file_path TEXT PRIMARY KEY,
            embedding BLOB
        )
    ''')
    conn.commit()
    return conn

def clear_database():
    conn = sqlite3.connect('code_embeddings.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM embeddings')
    conn.commit()
    conn.close()
    debug_print("Database cleared.")

def insert_embeddings(conn, embeddings):
    cursor = conn.cursor()
    for file_path, embedding in embeddings:
        embedding_blob = struct.pack(f'{len(embedding)}f', *embedding)
        try:
            cursor.execute('''
            INSERT INTO embeddings (file_path, embedding)
            VALUES (?, ?)
            ''', (file_path, embedding_blob))
        except sqlite3.IntegrityError:
            cursor.execute('''
            UPDATE embeddings
            SET embedding = ?
            WHERE file_path = ?
            ''', (embedding_blob, file_path))
    conn.commit()

if __name__ == '__main__':
    conn = setup_database()
    clear_database()
