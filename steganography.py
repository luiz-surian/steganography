import os
import base64

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
        data = f.read().decode("utf-8")

    # Encode to base64
    b64_data = base64.b64encode(bytes(data, "utf-8"))

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


def extract_from_file(
    source_file,
    files_path="./",
    divider=default_divider
):
    source_path = os.path.join(files_path, source_file)
    new_file_path = os.path.join(files_path, "extracted")

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
        with open(new_file_path, "wb") as f:
            f.write(decoded_data)


# Run using example files
def example_run():
    # Set path and file names
    files_path = 'example'
    source_file = 'mapa_cptm.png'
    secret_file = 'lorem_ipsum.txt'

    # Hide secret file in source file
    hide_in_file(source_file, secret_file, files_path)

    # Show files names and sizes
    def get_size(files_path, file_name):
        return os.path.getsize(os.path.join(files_path, file_name))
    print(
        f"Source File: {source_file} - Size: "
        f"{get_size(files_path, source_file)} bytes"
    )
    print(
        f"Secret File: {secret_file} - Size: "
        f"{get_size(files_path, secret_file)} bytes"
    )
    print(
        f"New File: new_{source_file} - Size: "
        f"{get_size(files_path, f'new_{source_file}')} bytes"
    )

    # Extract secret file from new file
    extract_from_file(f"new_{source_file}", files_path)


if __name__ == "__main__":
    example_run()
