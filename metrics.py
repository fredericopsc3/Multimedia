import time
import csv
import os

def compute_compression_ratio(original: bytes, encoded: bytes) -> float:
    """Return compression ratio = original_size / encoded_size."""
    if not encoded:
        return float('inf')
    return len(original) / len(encoded)

def time_function(func, *args, **kwargs):
    """Measure execution time of a function in seconds."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

def avg_codelenght(encoded: bytes, lenght: int ) -> float:
    return len(encoded)/lenght


def write_metrics_csv(results: list, path: str) -> None:
    """Write list of metrics dicts to CSV file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ['file', 'orig_size', 'enc_size', 'compression_ratio', 'encode_time_s', 'decode_time_s', 'avg_code_len']
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({
                'file': r['file'],
                'orig_size': r['orig_size'],
                'enc_size': r['enc_size'],
                'compression_ratio': f"{r['cr']:.4f}",
                'encode_time_s': f"{r['t_enc']:.6f}",
                'decode_time_s': f"{r['t_dec']:.6f}",
                'avg_code_len': f"{r['avg_code_len']:.6f}"
            })