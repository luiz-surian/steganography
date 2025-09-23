# Steganography

This project is a proof of concept (POC) for hiding and extracting files within other files using a command-line steganography script.

## Description

The `steganography.py` script allows you to hide any file (text, image, binary) inside another file (for example, a PNG image) and later extract the hidden file. The process uses base64 encoding and a custom divider string to separate the data.

## Requirements

- Python 3.10 or higher
- [python-magic](https://pypi.org/project/python-magic/) (optional, for automatic detection of the extracted file type)

To install the optional requirement:

```bash
pip install -r requirements.txt
```

On Debian/Ubuntu, it is needed to install:

```bash
sudo apt-get install libmagic1
```

On Windows, it is needed to install:

```bash
pip install python-magic-bin
```

## Usage

### Hide a file

```bash
python steganography.py hide <base_file> --secret_file <secret_file> [--files_path <folder>] [--divider <divider>]
```

**Example:**

```bash
python steganography.py hide mapa_cptm.png --secret_file lorem_ipsum.txt --files_path example
```

### Extract a hidden file

```bash
python steganography.py extract <base_file> [--files_path <folder>] [--divider <divider>]
```

**Example:**

```bash
python steganography.py extract new_mapa_cptm.png --files_path example
```

## Arguments

- `hide` or `extract`: desired action.
- `<base_file>`: file where the content will be hidden or extracted.
- `--secret_file` / `-s`: secret file to be hidden (required for `hide`).
- `--files_path` / `-p`: path to the files (default: `./`).
- `--divider` / `-d`: divider string between files (default: internal value in the script).

## Automatic Example

If the script is run without arguments, it executes an example using files from the `example` folder:

```bash
python steganography.py
```

## Notes

- The extracted file receives an automatic extension if `python-magic` is installed.
- You can customize the divider if you don't desire to utilize the default one, but be aware it will appear in plain text within the generated file.
- There is no encryption, only simple hiding.

## License

This project is for educational and demonstration purposes only.
