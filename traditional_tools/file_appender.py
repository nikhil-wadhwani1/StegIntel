import zipfile
import tempfile
import os

def extract_appended_zip(filepath):
    print("[File Appending] Trying to extract ZIP from file...")

    try:
        with open(filepath, 'rb') as f:
            content = f.read()

        zip_start = content.find(b'PK\x03\x04')
        if zip_start == -1:
            print("[File Appending] No ZIP data found.")
            return

        zip_data = content[zip_start:]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            temp_zip.write(zip_data)
            temp_zip_path = temp_zip.name

        print(f"[File Appending] Extracted ZIP archive to temporary file: {temp_zip_path}")
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            extract_dir = tempfile.mkdtemp()
            zip_ref.extractall(extract_dir)
            print(f"[File Appending] Files extracted to: {extract_dir}")

            # Prepare a report content list
            report_lines = []

            for file_name in zip_ref.namelist():
                file_path = os.path.join(extract_dir, file_name)
                if file_name.lower().endswith(('.txt', '.log')):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as txt_file:
                            content = txt_file.read()
                            print(f"\n[Extracted File: {file_name}]\n{content.strip()}\n")
                            report_lines.append(f"--- {file_name} ---\n{content.strip()}\n\n")
                    except Exception as e:
                        print(f"[File Appending] Error reading {file_name}: {e}")

            # Save to forensic report
            if report_lines:
                os.makedirs("reports", exist_ok=True)
                out_path = os.path.join("reports", "appended_zip_output.txt")
                with open(out_path, "w", encoding="utf-8") as out_file:
                    out_file.writelines(report_lines)
                print(f"[File Appending] Text content saved to: {out_path}")

    except Exception as e:
        print(f"[File Appending] Error: {e}")
