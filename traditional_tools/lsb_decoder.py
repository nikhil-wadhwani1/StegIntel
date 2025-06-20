from PIL import Image
import bitarray

def decode_lsb(image_path):
    print("[LSB] Attempting to decode LSB...")

    try:
        img = Image.open(image_path)
        binary_data = ""
        pixels = img.getdata()

        for pixel in pixels:
            for channel in pixel[:3]:  # RGB channels only
                binary_data += bin(channel)[-1]  # Get least significant bit

        bits = bitarray.bitarray(binary_data)

        try:
            decoded = bits.tobytes().decode('utf-8', errors='ignore')
            if 'EOF' in decoded:
                print("[LSB] Message Found:")
                print(decoded.split('EOF')[0])
            else:
                print("[LSB] Decoded message (no EOF marker):")
                print(decoded[:200])  # First 200 chars only
        except Exception as e:
            print(f"[LSB] Could not convert bits to string: {e}")

    except Exception as e:
        print(f"[LSB] Failed to decode LSB: {e}")
