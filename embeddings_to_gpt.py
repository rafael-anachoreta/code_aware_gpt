import os
import sqlite3
import numpy as np
from openai import OpenAI
from utils import api_key, debug_print
from datetime import datetime

client = OpenAI(api_key=api_key)

def fetch_relevant_embeddings(conn, query_embedding, initial_threshold=0.5, fallback_threshold=0.3, top_n=2):
    cursor = conn.cursor()
    cursor.execute('SELECT file_path, embedding FROM embeddings')
    rows = cursor.fetchall()

    query_embedding = np.array(query_embedding)
    similarities = []

    for file_path, embedding_blob in rows:
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
        similarities.append((file_path, similarity))
        debug_print(f"Similarity for {file_path}: {similarity}")

    # Sort files by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Try to find files above the initial threshold
    relevant_files = [(file_path, similarity) for file_path, similarity in similarities if similarity > initial_threshold]

    # If no files are found, try the fallback threshold
    if not relevant_files:
        relevant_files = [(file_path, similarity) for file_path, similarity in similarities if similarity > fallback_threshold]

    # If still no files are found, take the top N most similar files
    if not relevant_files:
        relevant_files = similarities[:top_n]
    else:
        relevant_files = relevant_files[:top_n]

    return [file_path for file_path, similarity in relevant_files]

def generate_query_embedding(query):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )
    embedding = response.data[0].embedding
    debug_print(f"Generated query embedding dimensions: {len(embedding)}")
    return embedding

def provide_context_to_gpt(query):
    query_embedding = generate_query_embedding(query)
    conn = sqlite3.connect('code_embeddings.db')
    relevant_files = fetch_relevant_embeddings(conn, query_embedding)

    context = ""
    for file_path in relevant_files:
        normalized_file_path = os.path.normpath(file_path).replace('\\', '/')  # Normalize and replace backslashes
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
            context += f"\n\n{normalized_file_path}:\n```python\n{code_content}\n```"
    
    detailed_query = f"{query}\n\nProject Context:\n{context}"
    
    debug_print(f"Detailed query: {detailed_query}")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "I'm a Python code assistant. I can help you with your code-related queries specifically about Pygame."},
            {"role": "user", "content": detailed_query},
        ],
    )
    
    answer = response.choices[0].message.content
    return answer, detailed_query

def save_response_to_file(query, response):
    # Ensure the responses directory exists
    if not os.path.exists('responses'):
        os.makedirs('responses')

    # Get the current date and time
    now = datetime.now().strftime("%Y-%m-%d-%H%M")
    file_name = f"responses/response-{now}.md"

    # Write the query and response to the file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"# Query\n\n{query}\n\n")
        file.write(f"# Response\n\n{response}\n")

    debug_print(f"Response saved to ./{file_name}")

if __name__ == '__main__':
    query = """
    I need help understanding what StateManager is doing. Can you provide some guidance?
    """
    response, detailed_query = provide_context_to_gpt(query)
    print(response)
    save_response_to_file(detailed_query, response)
