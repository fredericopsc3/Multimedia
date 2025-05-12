# We implement a thresholded RLE with escape marker to avoid expanding non-repeated data.
# Escape byte chosen as 0x00; threshold for encoding runs is 4.

ESC = 0
THRESHOLD = 4


def rle_encode(data: bytes) -> bytes:
    """Encode input bytes with thresholded RLE and escape marker."""
    encoded = bytearray()
    i, n = 0, len(data)
    while i < n:
        run_val = data[i]
        run_len = 1
        j = i + 1
        while j < n and data[j] == run_val and run_len < 255:
            run_len += 1
            j += 1
        if run_len >= THRESHOLD:
            encoded.extend([ESC, run_len, run_val])
        else:
            for k in range(run_len):
                b = data[i + k]
                if b == ESC:
                    encoded.extend([ESC, 0, ESC])
                else:
                    encoded.append(b)
        i = j
    return bytes(encoded)

def rle_decode(encoded: bytes) -> bytes:
    """Decode thresholded RLE with escape marker."""
    decoded = bytearray()
    i, n = 0, len(encoded)
    while i < n:
        b = encoded[i]
        if b == ESC:
            if i + 2 >= n:
                raise ValueError("Malformed RLE data: incomplete escape sequence")
            count, val = encoded[i+1], encoded[i+2]
            if count == 0 and val == ESC:
                decoded.append(ESC)
            else:
                decoded.extend(bytes([val]) * count)
            i += 3
        else:
            decoded.append(b)
            i += 1
    return bytes(decoded)