import subprocess
import tempfile
import os
import getpass

def extract_steghide(filepath):
    print("\n[Steghide] Steghide extraction requires a passphrase")
    
    # Get passphrase securely
    while True:
        passphrase = getpass.getpass("[Steghide] Enter passphrase (press Enter for none): ")
        confirm = getpass.getpass("[Steghide] Confirm passphrase: ")
        
        if passphrase == confirm:
            break
        print("[Steghide] Passphrases don't match! Try again")

    # Prepare temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        out_file = tmp.name

    # Build command
    command = [
        "steghide", "extract",
        "-sf", filepath,
        "-xf", out_file,
        "-p", passphrase,
        "-f"  # Force overwrite
    ]

    try:
        # Run steghide
        result = subprocess.run(command, 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True)

        # Handle output
        if "could not extract" in result.stderr.lower():
            print("\n[Steghide] Extraction failed - wrong passphrase or no data")
            return False
        
        if os.path.exists(out_file):
            with open(out_file, 'rb') as f:
                content = f.read()
                if content:
                    print("\n[Steghide] Extraction successful!")
                    print(f"Found {len(content)} bytes of hidden data")
                    
                    # Save to reports
                    os.makedirs("reports", exist_ok=True)
                    output_path = os.path.join("reports", "steghide_output.txt")
                    with open(output_path, 'wb') as out:
                        out.write(content)
                    print(f"Saved to {output_path}")
                    return True
                else:
                    print("\n[Steghide] No data found (empty file)")
                    return False
        else:
            print("\n[Steghide] No output file created")
            return False

    except Exception as e:
        print(f"[Steghide] Error: {str(e)}")
        return False
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)
