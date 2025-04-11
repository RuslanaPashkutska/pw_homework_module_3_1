import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from shutil import copy

logging.basicConfig(level=logging.INFO, format="%(threadName)s - %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="Sort files by extension")
    parser.add_argument("--source", "-s", default="Trash", help="Sours folder")
    parser.add_argument("--output", "-o", default="dist", help="Destination folder")
    return parser.parse_args()

# Function to copy a file to the appropriate folder based on its extension
def copy_file(file_path: Path, output_dir: Path):
    ext = file_path.suffix[1:].lower() if file_path.suffix else None

    if ext:
        # Create a folder named after the extension
        target_folder = output_dir / ext
        target_folder.mkdir(parents=True, exist_ok=True)
        # Define the final file name in the destination folder
        target_file = target_folder / file_path.name
        # Copy the file to the target folder
        copy(file_path, target_file)
        logging.info(f"File {file_path} copied to {target_file}")
    else:
        logging.info(f"Skipping file without extention: {file_path}")

def process_directory(source_dir: Path, output_dir: Path, executor: ThreadPoolExecutor):
    futures = [] # List to store tasks running in parallel

    try:
        for item in source_dir.iterdir():
            if item.is_dir():
                futures.append(executor.submit(process_directory, item, output_dir, executor))
            elif item.is_file():
                futures.append(executor.submit(copy_file, item, output_dir))

        # Wait for all tasks to finish
        for future in futures:
            future.result()

    except Exception as e:
        logging.error(f"Error processing directory {source_dir}: {e}")

def main():
    args = parse_args()
    source_dir = Path(args.source)
    output_dir = Path(args.output)

    # Check if the source directory exists
    if not source_dir.exists() or not source_dir.is_dir():
        logging.error(f"The directory {source_dir} does not exist or is not a directory.")
        return
    # Create a ThreadPoolExecutor to run tasks in parallel
    with ThreadPoolExecutor() as executor:
        process_directory(source_dir, output_dir, executor)

    logging.info("Done! Files have been sorted.")

if __name__ == "__main__":
    main()