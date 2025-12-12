import argparse
import asyncio
import logging
from pathlib import Path
import shutil
from aiofiles.os import wrap


async_copy = wrap(shutil.copy2)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="file_sorter.log",
    filemode="a"
)

async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []
    for file_path in source_folder.rglob("*"):
        if file_path.is_file():
            tasks.append(copy_file(file_path, output_folder))
    if tasks:
        await asyncio.gather(*tasks)


async def copy_file(file_path: Path, output_folder: Path):
    try:
        ext = file_path.suffix.lower()[1:] or "no_extension"
        target_dir = output_folder / ext
        target_dir.mkdir(parents=True, exist_ok=True)
        await async_copy(str(file_path), str(target_dir / file_path.name))
        logging.info(f"File {file_path} copied to {target_dir}")
    except Exception as e:
        logging.error(f"Copying error {file_path}: {e}")



def main():
    parser = argparse.ArgumentParser(description="Async file sorting by extensions")
    parser.add_argument("source", type=str, help="Source folder path")
    parser.add_argument("output", type=str, help="Output folder path")
    args = parser.parse_args()

    source_folder = Path(args.source).resolve()
    output_folder = Path(args.output).resolve()

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Source folder does not exist: {source_folder}")
        return

    try:
        asyncio.run(read_folder(source_folder, output_folder))
    except Exception as e:
        logging.error(f"Runtime error: {e}")

if __name__ == "__main__":
    main()
