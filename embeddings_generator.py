import os
import time
from openai import OpenAI
import openai
from utils import api_key, debug_print, target_directory
from db_manager import setup_database, insert_embeddings
from git_tree import get_git_files

client = OpenAI(api_key=api_key)

def extract_code_elements(directory):
    code_elements = []
    git_files = get_git_files(directory)
    for file in git_files:
        if file.endswith('.py') and file != '__init__.py':
            file_path = os.path.join(directory, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    if code.strip():  # Check if the file is not empty
                        normalized_file_path = os.path.normpath(file_path).replace('\\', '/')
                        code_elements.append((normalized_file_path, code))
            except Exception as e:
                debug_print(f"Error reading file {file_path}: {e}")
    return code_elements

def generate_embeddings(code_elements):
    embeddings = []
    for file_path, code in code_elements:
        success = False
        while not success:
            try:
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=[code]
                )
                embedding = response.data[0].embedding
                debug_print(f"Generated embedding for {file_path}: {len(embedding)} dimensions")
                embeddings.append((file_path, embedding))
                success = True
            except openai.RateLimitError:
                debug_print("Rate limit exceeded. Waiting for 60 seconds.")
                time.sleep(60)  # Wait for 60 seconds before retrying
            except openai.APIStatusError as e:
                debug_print(f"Invalid request error: {e}")
                success = True  # Skip to next file
            time.sleep(1)  # Add a short delay between requests to respect rate limits
    print("Finished generating embedding!")
    return embeddings

if __name__ == '__main__':
    conn = setup_database()
    code_elements = extract_code_elements(target_directory)
    if not code_elements:
        print("No Python files found to process.")
    else:
        embeddings = generate_embeddings(code_elements)
        insert_embeddings(conn, embeddings)
        print("Embeddings generated and inserted successfully.")
