import asyncio
import os
import shutil
import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

# Налаштування логера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Створення файлового обробника для запису логів у файл
log_file = 'file_sorter.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Форматування записів у лог-файлі
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Додавання файлового обробника до логера
logger.addHandler(file_handler)

executor = ThreadPoolExecutor(max_workers=4)

async def read_folder(source_path):
    """Асинхронно читає файли з вихідної папки та її підпапок."""
    files = []
    for root, _, filenames in os.walk(source_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

async def copy_file(file_path, output_path):
    """Асинхронно копіює файл в підпапку на основі його розширення."""
    try:
        extension = os.path.splitext(file_path)[1][1:] or "no_extension"
        target_folder = os.path.join(output_path, extension)
        os.makedirs(target_folder, exist_ok=True)
        target_path = os.path.join(target_folder, os.path.basename(file_path))
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, shutil.copy, file_path, target_path)
        logger.info(f"Copied {file_path} to {target_path}")
    except Exception as e:
        logger.error(f"Error copying file {file_path}: {e}")

async def main(source_path, output_path):
    """Асинхронна головна функція, яка керує усіма операціями."""
    files = await read_folder(source_path)
    tasks = [copy_file(file, output_path) for file in files]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = ArgumentParser(description="Asynchronously sort files by extension.")
    parser.add_argument("source_path", type=str, help="The source directory to sort files from.")
    parser.add_argument("output_path", type=str, help="The destination directory to sort files into.")
    args = parser.parse_args()

    if not os.path.exists(args.source_path):
        parser.error(f"The source path {args.source_path} does not exist.")
    if not os.path.exists(args.output_path):
        parser.error(f"The output path {args.output_path} does not exist.")

    asyncio.run(main(args.source_path, args.output_path))
