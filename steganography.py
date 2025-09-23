#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""\
Steganography: Hide and Extract Files within Other Files

usage:
    python steganography.py hide <source_file> --secret_file <secret_file> \
        [--files_path <path>] [--divider <divider>]
    python steganography.py extract <source_file> \
        [--files_path <path>] [--divider <divider>]
"""

import os
import base64
import argparse
from datetime import datetime

# Check for python-magic availability
try:
    import magic
    has_magic = True
except ImportError:
    try:
        from winmagic import magic
        has_magic = True
    except ImportError:
        has_magic = False
        print(
            "Warning: 'python-magic' library not found. "
            "File type detection will be disabled. "
            "Check required dependencies at "
            "https://pypi.org/project/python-magic/"
        )


# Default divider string
default_divider = 'I8x6euHQiG'


# File Handling
def hide_in_file(
    source_file,
    secret_file,
    files_path="./",
    divider=default_divider
):
    source_path = os.path.join(files_path, source_file)
    secret_path = os.path.join(files_path, secret_file)
    new_file_path = os.path.join(files_path, f"new_{source_file}")

    with open(secret_path, "rb") as f:
        # Read desired file in binary mode
        data = f.read()

    # Encode to base64
    b64_data = base64.b64encode(data)

    # Write encoded data to a temporary file
    encoded_file = "encoded_file.txt"
    with open(encoded_file, "wb") as f:
        # Write base64 data to file and append the divider in the beginning
        f.write(bytes(divider, "utf-8"))
        f.write(b64_data)

    # Combine source file and encoded file into a new file
    with open(source_path, "rb") as src, \
         open(encoded_file, "rb") as enc, \
         open(new_file_path, "wb") as out:
        out.write(src.read())
        out.write(enc.read())

    # Remove temporary encoded file
    os.remove(encoded_file)

    return new_file_path


def extract_from_file(
    source_file,
    files_path="./",
    divider=default_divider
):
    # Generate a unique name for the extracted file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extracted_name = f"extracted_{timestamp}"

    source_path = os.path.join(files_path, source_file)
    extracted_file = os.path.join(files_path, extracted_name)

    with open(source_path, "rb") as f:
        # Read desired file in binary mode
        data = f.read()

    # Find the divider as bytes
    divider_bytes = bytes(divider, "utf-8")
    split_data = data.split(divider_bytes)

    if len(split_data) > 1:
        # Decode only the base64 part (after the divider)
        b64_data = split_data[1]
        decoded_data = base64.b64decode(b64_data)

        # Write decoded data to a new file
        with open(extracted_file, "wb") as f:
            f.write(decoded_data)

        if has_magic:
            # Detect file type using python-magic
            mime = magic.from_buffer(decoded_data, mime=True)

            # Check edge cases
            match mime:
                # If mime type is unknown, default to 'bin'
                case 'application/octet-stream':
                    ext = 'bin'
                # If mime type is text/plain, use .txt extension
                case 'text/plain':
                    ext = 'txt'
                case _:
                    ext = mime.split('/')[-1]

            new_name = os.path.join(files_path, f"{extracted_name}.{ext}")
            os.rename(extracted_file, new_name)
            return new_name
        else:
            print(
                "python-magic not installed. "
                "File extracted without extension."
            )
            return extracted_file

    else:
        print("Divider not found in the file. No hidden data extracted.")
        return None


# Run using example files
def example_run():
    # Set path and file names
    files_path = 'example'
    source_file = 'mapa_cptm.png'
    secret_file = 'lorem_ipsum.txt'

    # Function to get file size
    def get_size(files_path, file_name):
        return os.path.getsize(os.path.join(files_path, file_name))

    # Show files names and sizes
    print(
        f"Source File: {source_file} - Size: "
        f"{get_size(files_path, source_file)} bytes"
    )
    print(
        f"Secret File: {secret_file} - Size: "
        f"{get_size(files_path, secret_file)} bytes"
    )

    # Hide secret file in source file
    new_file_path = hide_in_file(source_file, secret_file, files_path)
    print(
        f"New File: {new_file_path} - Size: "
        f"{os.path.getsize(new_file_path)} bytes"
    )

    # Extract secret file from new file
    extracted_file = extract_from_file(f"new_{source_file}", files_path)
    print(
        f"Extracted File: {extracted_file} - Size: "
        f"{os.path.getsize(extracted_file)} bytes"
    )


if __name__ == "__main__":
    # Check if script is called without arguments then run example
    if len(os.sys.argv) == 1:
        example_run()
        os.sys.exit(0)

    # Argument parser setup
    parser = argparse.ArgumentParser(
        description='Steganography: Hide and Extract Files within Other Files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'action',
        choices=['hide', 'extract'],
        help='Action to perform: hide or extract'
    )
    parser.add_argument(
        'source_file',
        help='The source file to hide data in or extract data from'
    )
    parser.add_argument(
        '--secret_file', '-s',
        help='The secret file to hide (required for hide action)'
    )
    parser.add_argument(
        '--files_path', '-p',
        default='./',
        help='Path to the files'
    )
    parser.add_argument(
        '--divider', '-d',
        default=default_divider,
        help='Divider string to separate data'
    )

    args = parser.parse_args()

    if args.action == 'hide':
        if not args.secret_file:
            parser.error(
                'The --secret_file argument is required for the hide action.'
            )
            os.sys.exit(1)
        hide_in_file(
            args.source_file,
            args.secret_file,
            args.files_path,
            args.divider
        )
    elif args.action == 'extract':
        extract_from_file(
            args.source_file,
            args.files_path,
            args.divider
        )
