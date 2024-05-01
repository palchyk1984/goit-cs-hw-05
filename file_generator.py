import os
import random

# Функція для генерації випадкового тексту
def generate_random_content(size=1024):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz\n', k=size))

# Функція для створення файлів
def create_files_in_folder(folder_path, num_files=10):
    # Перевірити існування папки, створити, якщо не існує
    os.makedirs(folder_path, exist_ok=True)
    
    # Список можливих розширень файлів
    extensions = ['txt', 'csv', 'log', 'json', 'xml']

    # Генерація файлів
    for i in range(num_files):
        file_name = f"file_{i}.{random.choice(extensions)}"
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'w') as f:
            f.write(generate_random_content(random.randint(512, 2048)))  # Розмір файлу від 512 до 2048 байт

    print(f"Generated {num_files} files in {folder_path}")

# Виконання функції для створення файлів
if __name__ == '__main__':
    create_files_in_folder('My_files')
