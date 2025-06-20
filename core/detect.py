import os

def detect_methods(filepath):
    methods = []

    with open(filepath, 'rb') as f:
        content = f.read()

    # Check for ZIP file signature
    if b'PK\x03\x04' in content:
        methods.append("file_appending")

    # Crude EOF marker test (optional refinement)
    if content.endswith(b'\x00' * 10):
        methods.append("eof_injection")

    # EXIF is worth checking for any image
    if filepath.lower().endswith(('.jpg', '.jpeg', '.png')):
        methods.append("exif")

    # LSB: PNG/BMP are good candidates
    if filepath.lower().endswith(('.png', '.bmp')):
        methods.append("lsb")

    # JPEG: DCT detection
    if filepath.lower().endswith(('.jpg', '.jpeg')):
        methods.append("dct_jpeg")

    # NTFS ADS (only detect on Windows)
    if os.name == "nt":
        methods.append("ads_ntfs")

    # steghide: works with .jpg, .bmp, .wav
    if filepath.lower().endswith(('.jpg', '.jpeg', '.bmp', '.wav')):
        methods.append("steghide")

    return methods
