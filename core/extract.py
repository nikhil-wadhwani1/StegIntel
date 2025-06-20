import os
from pathlib import Path

def decode_hidden_data(filepath, methods):
    """
    Main extraction function that handles all detected steganography methods
    """
    filepath = str(filepath)  # Ensure string path for compatibility
    print(f"\n🔍 Beginning extraction on {os.path.basename(filepath)}")
    
    # Track successful extractions
    extracted_data = {
        'file': filepath,
        'methods': methods,
        'results': {}
    }

    # LSB Extraction
    if "lsb" in methods:
        from traditional_tools.lsb_decoder import decode_lsb
        print("\n[LSB] Attempting LSB extraction...")
        extracted_data['results']['lsb'] = decode_lsb(filepath)

    # File Appending (ZIP)
    if "file_appending" in methods:
        from traditional_tools.file_appender import extract_appended_zip
        print("\n[ZIP] Checking for appended files...")
        extracted_data['results']['file_appending'] = extract_appended_zip(filepath)

    # EXIF Data
    if "exif" in methods:
        from traditional_tools.exif_extractor import extract_exif
        print("\n[EXIF] Extracting metadata...")
        extracted_data['results']['exif'] = extract_exif(filepath)

    # EOF Injection
    if "eof_injection" in methods:
        from traditional_tools.eof_injector import extract_eof_data
        print("\n[EOF] Checking for end-of-file data...")
        extracted_data['results']['eof_injection'] = extract_eof_data(filepath)

    # DCT (JPEG)
    if "dct_jpeg" in methods:
        from traditional_tools.dct_decoder import decode_dct
        print("\n[DCT] Analyzing JPEG coefficients...")
        extracted_data['results']['dct_jpeg'] = decode_dct(filepath)

    # NTFS ADS (Windows only)
    if "ads_ntfs" in methods and os.name == "nt":
        from traditional_tools.ads_ntfs import detect_ads
        print("\n[ADS] Checking NTFS alternate streams...")
        extracted_data['results']['ads_ntfs'] = detect_ads(filepath)

    # Steghide (with interactive passphrase)
    if "steghide" in methods:
        from traditional_tools.steghide_wrapper import extract_steghide
        print("\n[Steghide] Starting steghide extraction...")
        extracted_data['results']['steghide'] = extract_steghide(filepath)

    # Generate consolidated report
    save_extraction_report(extracted_data)
    
    return extracted_data

def save_extraction_report(data):
    """Save all extraction results to a report file"""
    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", f"extraction_report_{os.path.basename(data['file'])}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Steganography Extraction Report\n{'='*40}\n")
        f.write(f"File: {data['file']}\n")
        f.write(f"Detected Methods: {', '.join(data['methods'])}\n\n")
        
        for method, result in data['results'].items():
            f.write(f"{method.upper()} Results:\n{'-'*20}\n")
            if result:
                if isinstance(result, str):
                    f.write(f"{result}\n")
                elif isinstance(result, dict):
                    for k, v in result.items():
                        f.write(f"{k}: {v}\n")
                else:
                    f.write("Data found (see individual files)\n")
            else:
                f.write("No data extracted\n")
            f.write("\n")
    
    print(f"\n✅ Extraction report saved to {report_path}")
