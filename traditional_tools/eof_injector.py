def extract_eof_data(filepath):
    print("[EOF Injection] Attempting to extract hidden data after EOF marker...")

    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        # Detect JPEG end of file marker
        eof_marker = b'\xFF\xD9'
        eof_index = data.find(eof_marker)

        if eof_index == -1:
            print("[EOF Injection] No EOF marker found.")
            return

        injected_data = data[eof_index + 2:]  # 2 bytes for marker
        if not injected_data.strip():
            print("[EOF Injection] No hidden data found after EOF.")
            return

        print("[EOF Injection] Hidden data found:")
        print(injected_data.decode(errors='replace'))

    except Exception as e:
        print(f"[EOF Injection] Error: {e}")
