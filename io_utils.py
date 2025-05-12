import os

def read_file_bytes(path: str) -> bytes:
    """Read a file and return its raw bytes."""
    with open(path, 'rb') as f:
        return f.read()


def write_file_bytes(path: str, data: bytes) -> None:
    """Write raw bytes to a file, creating directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)