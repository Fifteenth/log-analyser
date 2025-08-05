# log_utils.py

def split_logs(log_text, chunk_size=500):
    """
    Splits a log file string into smaller chunks for embedding.
    """
    lines = log_text.split("\n")
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + "\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
