import os
import subprocess
import re
import sys

SOURCE_DIR = "."
OUTPUT_FILE = "Notes.pdf"
METADATA_FILE = "metadata.yaml"
PANDOC_ARGS = [
    "--toc",
    "--toc-depth=2",
    "--pdf-engine=xelatex",
    "--variable",
    "geometry:margin=1in",
]


def get_sorted_files(directory):

    files = [f for f in os.listdir(directory) if f.endswith(".md")]

    def numerical_sort_key(filename):
        match = re.match(r"(\d+)_", filename)
        if match:
            return int(match.group(1))
        return float("inf")

    return sorted(files, key=numerical_sort_key)


def main():

    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Directory '{SOURCE_DIR}' not found.")
        return

    files = get_sorted_files(SOURCE_DIR)
    if not files:
        print("No markdown files found.")
        return

    file_paths = [os.path.join(SOURCE_DIR, f) for f in files]

    print("Found files in this order:")
    for f in file_paths:
        print(f" - {f}")

    command = [
        "pandoc",
    ]

    if os.path.exists(METADATA_FILE):
        command.append(METADATA_FILE)

    command.extend(file_paths)
    command.append("-o")
    command.append(OUTPUT_FILE)
    command.extend(PANDOC_ARGS)

    print(f"\nGenerating {OUTPUT_FILE}...")
    try:
        subprocess.run(command, check=True)
        print(f"Success! Created {OUTPUT_FILE}")
    except subprocess.CalledProcessError as e:
        print("Error running pandoc.")
        print(e)
    except FileNotFoundError:
        print("Error: Pandoc is not installed or not in your PATH.")


if __name__ == "__main__":
    main()
