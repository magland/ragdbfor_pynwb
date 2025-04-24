import os
from pathlib import Path
from run_completion import run_completion

def create_summary(file_path: str) -> tuple[int, int]:
    """Create a summary markdown file for the given file."""
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # Create the corresponding summary path
    rel_path = os.path.relpath(file_path, 'submodules/pynwb/docs')
    summary_path = os.path.join('summaries/pynwb/docs', rel_path + '.summary.md')

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)

    # Skip if summary already exists
    if os.path.exists(summary_path):
        print(f"Skipping {file_path} - summary already exists")
        return (0, 0)  # Return zero tokens for skipped files

    print(f"Processing {file_path}")

    # Read system message
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, 'system_message.txt'), 'r', encoding='utf-8') as f:
        system_message = f.read().strip()

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": file_content}
    ]

    # Get the completion
    response, _, prompt_tokens, completion_tokens = run_completion(
        messages=messages,
        model='google/gemini-2.0-flash-001'
    )

    print(f"Tokens used - Prompt: {prompt_tokens}, Completion: {completion_tokens}")

    # Save the summary
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(response)

    return prompt_tokens, completion_tokens

def main():
    # Track total token usage
    total_prompt_tokens = 0
    total_completion_tokens = 0
    files_processed = 0
    files_skipped = 0

    # Walk through the docs directory
    docs_gallery_path = 'submodules/pynwb/docs/gallery'
    for root, _, files in os.walk(docs_gallery_path):
        for file in files:
            if file.endswith(('.rst', '.py')):
                file_path = os.path.join(root, file)

                # Check if summary already exists
                rel_path = os.path.relpath(file_path, docs_gallery_path)
                summary_path = os.path.join('summaries/pynwb/docs', rel_path + '.summary.md')

                if os.path.exists(summary_path):
                    print(f"Skipping {file_path} - summary already exists")
                    files_skipped += 1
                    continue

                try:
                    p_tokens, c_tokens = create_summary(file_path)
                    total_prompt_tokens += p_tokens
                    total_completion_tokens += c_tokens
                    files_processed += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    continue

    print("\nSummary:")
    print(f"Files processed: {files_processed}")
    print(f"Files skipped: {files_skipped}")
    print(f"Total files: {files_processed + files_skipped}")
    print(f"Total tokens used - Prompt: {total_prompt_tokens}, Completion: {total_completion_tokens}")

if __name__ == "__main__":
    main()
