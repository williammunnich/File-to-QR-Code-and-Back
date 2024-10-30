from pyzbar.pyzbar import decode
from PIL import Image
import os
import re
import hashlib

def reassemble_file_from_qr(folder_path, output_file_path):
    # List and sort the images in the folder, excluding the "checksum.png" file
    qr_images = sorted(
        [f for f in os.listdir(folder_path) if re.match(r'\d+\.png$', f)],
        key=lambda x: int(re.match(r'(\d+)\.png$', x).group(1))
    )

    # Initialize an empty string to hold the combined hex data
    combined_hex_data = ""

    # Loop through each QR code image and decode it using pyzbar
    for image_file in qr_images:
        img_path = os.path.join(folder_path, image_file)
        img = Image.open(img_path)
        
        # Decode the QR code using pyzbar
        decoded_objects = decode(img)
        if decoded_objects:
            # Assuming there's only one QR code per image
            combined_hex_data += decoded_objects[0].data.decode('utf-8')
        else:
            print(f"Warning: No QR code found in {image_file}")

    # Convert the combined hex data back to binary data
    binary_data = bytes.fromhex(combined_hex_data)

    # Write the binary data to the output file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(binary_data)

    # Calculate the MD5 checksum of the reassembled file
    new_md5_hash = hashlib.md5(binary_data).hexdigest()

    # Read the checksum from the "checksum.png" QR code
    checksum_img_path = os.path.join(folder_path, "checksum.png")
    checksum_img = Image.open(checksum_img_path)
    decoded_checksum = decode(checksum_img)
    
    if decoded_checksum:
        original_md5_hash = decoded_checksum[0].data.decode('utf-8')
        print(f"Original MD5 Checksum from QR: {original_md5_hash}")
        print(f"Newly Calculated MD5 Checksum: {new_md5_hash}")
        
        if original_md5_hash == new_md5_hash:
            print("Success: Checksums match! The file has been reassembled correctly.")
        else:
            print("Error: Checksums do not match! The reassembled file may be corrupted.")
    else:
        print("Error: Could not read checksum QR code.")

if __name__ == "__main__":
    folder = input("Please give the path of the folder that contains the QR codes: ")
    filepath = input("Please give the filename of the file to be created from the QR codes: ")
    reassemble_file_from_qr(folder, filepath)
