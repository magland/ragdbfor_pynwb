import os
import json
import hashlib
import base64
import numpy as np
from pathlib import Path
from semantic_embeddings import compute_semantic_embedding_vector

def get_sha1_hash(content: str) -> str:
    """Compute SHA1 hash of content"""
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

def process_summaries(output_json_path: str = 'embeddings.json'):
    """Process all summary.md files and generate/update semantic embeddings"""

    embeddings_list = []
    if os.path.exists(output_json_path):
        with open(output_json_path, 'r') as f:
            embeddings_list = json.load(f)

    new_embeddings_list = []

    # Find all summary.md files
    summaries_dir = Path('summaries')
    if not summaries_dir.exists():
        print(f"Error: {summaries_dir} directory not found")
        return

    for summary_file in summaries_dir.rglob('*.summary.md'):
        # Get relative path from summaries directory
        rel_path = str(summary_file.relative_to(summaries_dir))
        path_key = "summaries/" + rel_path

        print(f"Processing {rel_path}")

        # Read content and compute hash
        with open(summary_file, 'r', encoding='utf-8') as f:
            content = f.read()
        content_hash = get_sha1_hash(content)

        # Check if we already have this file with same hash
        existing_entry = next((entry for entry in embeddings_list if entry['path'] == path_key and entry['sha1'] == content_hash), None)
        if existing_entry:
            print(f"  Using existing embedding (hash match)")
            new_embeddings_list.append(existing_entry)
            continue

        # Compute new embedding
        print(f"  Computing new embedding")
        embedding = compute_semantic_embedding_vector(content)

        # Convert embedding to float32 and base64 encode
        embedding_float32 = np.array(embedding, dtype=np.float32)
        embedding_bytes = embedding_float32.tobytes()
        embedding_base64 = base64.b64encode(embedding_bytes).decode('utf-8')

        # Get file size
        size_bytes = os.path.getsize(summary_file)

        # Create new entry
        new_entry = {
            'path': path_key,
            'sha1': content_hash,
            'embedding_float32_base64': embedding_base64,
            'size_bytes': size_bytes
        }
        new_embeddings_list.append(new_entry)

        # Save after each file in case of errors
        with open(output_json_path, 'w') as f:
            json.dump(new_embeddings_list, f, indent=2)

    # No need to explicitly track stale entries since we build a new list

    # Final save
    with open(output_json_path, 'w') as f:
        json.dump(new_embeddings_list, f, indent=2)

    print("\nComplete!")
    print(f"Processed {len(new_embeddings_list)} files")
    print(f"Final JSON file: {output_json_path}")

if __name__ == "__main__":
    process_summaries()
