import os
import qrcode
import hashlib
import math

def create_qr_codes(file_path, max_qr_bytes=1000):
    # Read the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file's binary data
        binary_data = file.read()

    # Calculate the MD5 checksum of the original file
    md5_hash = hashlib.md5(binary_data).hexdigest()
    
    # Convert the binary data to hexadecimal
    hex_data = binary_data.hex()
    
    # Calculate the number of chunks
    chunk_size = max_qr_bytes * 2  # 1 byte = 2 hex characters
    total_chunks = math.ceil(len(hex_data) / chunk_size)

    # Create a folder with the name of the file (without extension)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_folder = os.path.join(os.getcwd(), base_name)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through and create a QR code for each chunk
    for i in range(total_chunks):
        # Extract the hex chunk
        chunk = hex_data[i * chunk_size:(i + 1) * chunk_size]
        
        # Create a QR code
        qr = qrcode.QRCode(
            version=40,  # Maximum version to store large data
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(chunk)
        qr.make(fit=True)
        
        # Create an image and save it
        img = qr.make_image(fill_color="black", back_color="white")
        img_file_name = os.path.join(output_folder, f"{i + 1}.png")
        img.save(img_file_name)

    # Create a final QR code for the MD5 checksum
    checksum_qr = qrcode.QRCode(
        version=40,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    checksum_qr.add_data(md5_hash)
    checksum_qr.make(fit=True)
    checksum_img = checksum_qr.make_image(fill_color="black", back_color="white")
    checksum_img.save(os.path.join(output_folder, "checksum.png"))

    print(f"QR code images and checksum saved in folder: {output_folder}")

# Example usage:
# create_qr_codes("path/to/your/file.bin")
filename = input("give the full filename: ")
create_qr_codes(filename)