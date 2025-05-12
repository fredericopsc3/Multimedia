import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from io_utils import read_file_bytes, write_file_bytes
from rle import rle_encode, rle_decode
from metrics import compute_compression_ratio, time_function, write_metrics_csv


def process_file(input_path: str, output_dirs: dict) -> dict:
    from PIL import Image
    ext = os.path.splitext(input_path)[1].lower()
    is_image = ext in ['.png', '.jpg', '.jpeg', '.bmp']
    # Load data: raw bytes for non-images, raw RGB bytes for images
    if is_image:
        raw_bytes = read_file_bytes(input_path)
        img = Image.open(input_path)
        data = img.convert('RGB').tobytes()
    else:
        raw_bytes = None
        data = read_file_bytes(input_path)
    # Measure encoding and decoding time on RLE output
    encoded, t_enc = time_function(rle_encode, data)
    decoded_rle, t_dec = time_function(rle_decode, encoded)
    if decoded_rle != data:
        raise ValueError(f"Decoded data mismatch for {input_path}")
    cr = compute_compression_ratio(data, encoded)

    enc_file = os.path.basename(input_path) + '.rle'
    enc_path = os.path.join(output_dirs['compressed'], enc_file)
    dec_path = os.path.join(output_dirs['decompressed'], os.path.basename(input_path))

    if cr < 1.0:
        # Skip RLE: write original binary file
        write_file_bytes(enc_path, read_file_bytes(input_path))
        write_file_bytes(dec_path, read_file_bytes(input_path))
        enc_size = os.path.getsize(input_path)
    else:
        # Write RLE compressed file
        write_file_bytes(enc_path, encoded)
        # For decompressed folder: restore original file
        if is_image:
            # write original PNG/JPG bytes
            write_file_bytes(dec_path, raw_bytes)
        else:
            # write decoded data back
            write_file_bytes(dec_path, decoded_rle)
        enc_size = len(encoded)

    return {
        'file': os.path.basename(input_path),
        'orig_size': len(data),
        'enc_size': enc_size,
        'cr': cr if cr >= 1.0 else 1.0,
        't_enc': t_enc,
        't_dec': t_dec,
    }


def plot_results(results_csv: str, output_dir: str):
    df = pd.read_csv(results_csv)
    # Compression Ratio plot
    plt.figure()
    plt.bar(df['file'], df['compression_ratio'])
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Compression Ratio')
    plt.title('Compression Ratio for Silesia Corpus Files')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'compression_ratios.png'))
    plt.close()
    # Times plot
    plt.figure()
    plt.plot(df['file'], df['encode_time_s'], marker='o', label='Encode Time (s)')
    plt.plot(df['file'], df['decode_time_s'], marker='o', label='Decode Time (s)')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Time (seconds)')
    plt.title('Encode and Decode Times for Silesia Corpus Files')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'times.png'))
    plt.close()
    print(f"Plots saved to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='RLE compressor for Silesia corpus')
    parser.add_argument('--input', required=True, help='Path to Silesia corpus folder')
    parser.add_argument('--output', required=True, help='Output base folder')
    args = parser.parse_args()

    base = args.output
    dirs = {
        'compressed': os.path.join(base, 'compressed'),
        'decompressed': os.path.join(base, 'decompressed'),
        'results': os.path.join(base, 'results')
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    results = []
    for fname in os.listdir(args.input):
        fin = os.path.join(args.input, fname)
        if os.path.isfile(fin):
            print(f"Processing {fname}...")
            res = process_file(fin, dirs)
            results.append(res)

    csv_path = os.path.join(dirs['results'], 'metrics.csv')
    write_metrics_csv(results, csv_path)
    print(f"Completed. Metrics saved to {csv_path}")

    # Generate plots
    plot_results(csv_path, dirs['results'])


if __name__ == '__main__':
    main()