"""
Скрипт для створення ZIP архіву домашнього завдання.
Використання: python create_zip.py
"""

import zipfile
import os
from datetime import datetime

def create_homework_zip():
    """Створює ZIP архів з файлами домашнього завдання."""
    
    # Список файлів для включення в архів
    files_to_include = [
        'task1_max_flow.py',
        'task2_trie.py',
        'trie.py',
        'README.md',
        'INSTRUCTIONS.md',
        'LICENSE'
    ]
    
    # Назва архіву (замініть ПІБ на своє)
    zip_filename = 'ДЗ4_Palamarchuk_Serhii.zip'
    
    print("="*70)
    print("СТВОРЕННЯ ZIP АРХІВУ")
    print("="*70)
    print(f"\nНазва архіву: {zip_filename}")
    print("\nФайли для включення:")
    
    # Створюємо ZIP архів
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in files_to_include:
            if os.path.exists(filename):
                zipf.write(filename)
                file_size = os.path.getsize(filename)
                print(f"  ✓ {filename} ({file_size:,} байт)")
            else:
                print(f"  ✗ {filename} - файл не знайдено!")
    
    # Виводимо інформацію про створений архів
    archive_size = os.path.getsize(zip_filename)
    print(f"\n{'='*70}")
    print(f"Архів успішно створено: {zip_filename}")
    print(f"Розмір архіву: {archive_size:,} байт")
    print(f"Дата створення: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    print("\nНаступні кроки:")
    print("1. Завантажте архів у LMS")
    print("2. Прикріпіть посилання на GitHub репозиторій")
    print("3. Вкажіть підхід до виконання ДЗ у коментарі")

if __name__ == "__main__":
    create_homework_zip()
