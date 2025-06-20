from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from datetime import datetime

def extract_exif(filepath):
    """Extract and display EXIF metadata in exiftool-like format"""
    try:
        print(f"\n[EXIF] Extracting metadata from {os.path.basename(filepath)}")
        print("-" * 60)
        
        # Get basic file info
        file_stats = os.stat(filepath)
        print(f"ExifTool Version Number         : 12.76 (simulated)")
        print(f"File Name                       : {os.path.basename(filepath)}")
        print(f"Directory                       : {os.path.dirname(filepath)}")
        print(f"File Size                       : {file_stats.st_size / 1024:.1f} kB")
        print(f"File Modification Date/Time     : {datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y:%m:%d %H:%M:%S%z')}")
        print(f"File Access Date/Time           : {datetime.fromtimestamp(file_stats.st_atime).strftime('%Y:%m:%d %H:%M:%S%z')}")
        print(f"File Inode Change Date/Time     : {datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y:%m:%d %H:%M:%S%z')}")
        print(f"File Permissions                : {oct(file_stats.st_mode)[-3:]}")
        
        with Image.open(filepath) as img:
            # Standard image attributes
            print(f"File Type                       : {img.format}")
            print(f"File Type Extension             : {img.format.lower()}")
            print(f"MIME Type                       : image/{img.format.lower()}")
            print(f"Image Width                     : {img.width}")
            print(f"Image Height                    : {img.height}")
            print(f"Image Size                      : {img.width}x{img.height}")
            print(f"Megapixels                      : {(img.width * img.height) / 1000000:.3f}")
            
            # EXIF-specific data
            exif_data = img._getexif() or {}
            print(f"JFIF Version                    : {exif_data.get(41728, '1.01')}")
            print(f"Resolution Unit                 : {exif_data.get(296, 'None')}")
            print(f"X Resolution                    : {exif_data.get(282, 1)}")
            print(f"Y Resolution                    : {exif_data.get(283, 1)}")
            print(f"Encoding Process                : Baseline DCT, Huffman coding")
            print(f"Bits Per Sample                 : 8")
            print(f"Color Components                : 3")
            print(f"Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)")
            
            # Process all other EXIF tags
            print("\n[Additional EXIF Metadata]")
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                # Format GPS data specially
                if tag_name == "GPSInfo":
                    print("GPS Info                        :")
                    for gps_tag in value:
                        gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                        print(f"  {gps_tag_name:30}: {value[gps_tag]}")
                else:
                    # Format standard tags
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='replace')
                        except:
                            value = str(value)[:50] + "..."
                    print(f"{tag_name:30}: {value}")
                    
    except Exception as e:
        print(f"[EXIF] Error extracting metadata: {str(e)}")
