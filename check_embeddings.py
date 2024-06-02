import sqlite3
import numpy as np

def fetch_all_embeddings():
    conn = sqlite3.connect('code_embeddings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_path, embedding FROM embeddings')
    rows = cursor.fetchall()
    conn.close()
    return rows

def main():
    embeddings = fetch_all_embeddings()
    for file_path, embedding_blob in embeddings:
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        print(f"File: {file_path}, Embedding dimensions: {embedding.shape}")

if __name__ == '__main__':
    main()
