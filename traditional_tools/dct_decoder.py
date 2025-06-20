import jpegio as jio
import numpy as np
import bitarray

def decode_dct(filepath):
    print("[DCT] Scanning JPEG DCT coefficients for hidden data...")

    try:
        # Load JPEG and extract DCT coefficient array (Y channel)
        jpeg = jio.read(filepath)
        Y_dct = jpeg.coef_arrays[0]  # luminance (brightness) component

        message_bits = []

        # Flatten DCT coefficients to a 1D array
        flat = Y_dct.flatten()

        for coeff in flat:
            # Skip DC or zero values
            if coeff == 0 or abs(coeff) > 2048:
                continue

            # Extract LSB of non-zero AC coefficient
            lsb = abs(coeff) & 1
            message_bits.append(str(lsb))

            if len(message_bits) > 8000:
                break  # prevent overload

        # Convert bitstream to text
        bits = bitarray.bitarray(''.join(message_bits))

        try:
            decoded = bits.tobytes().decode('utf-8', errors='ignore')
            print("[DCT] ✅ Message extracted:\n")
            if "EOF" in decoded:
                print(decoded.split("EOF")[0])
            else:
                print(decoded[:500])  # show first 500 chars if no EOF

            # Save to report
            import os
            os.makedirs("reports", exist_ok=True)
            with open("reports/dct_output.txt", "w", encoding="utf-8") as f:
                f.write(decoded)
            print("\n[DCT] Message saved to: reports/dct_output.txt")

        except Exception as e:
            print("[DCT] Bitstream decoded but not valid UTF-8:", e)

    except Exception as e:
        print(f"[DCT] Failed to process JPEG: {e}")
