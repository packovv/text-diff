#!/usr/bin/env python3
import difflib
import sys
import os

def read_file(file_path):
    """
    Читает текст из файла
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {str(e)}")
        sys.exit(1)

def compare_texts(text1, text2):
    """
    Сравнивает два текста и возвращает различия в них
    """
    # Разбиваем тексты на строки, заменяя \n на реальные переносы строк
    text1_lines = text1.replace('\\n', '\n').splitlines()
    text2_lines = text2.replace('\\n', '\n').splitlines()
    
    # Создаем объект Differ
    differ = difflib.Differ()
    
    # Получаем различия
    diff = list(differ.compare(text1_lines, text2_lines))
    
    return diff

def main():
    if len(sys.argv) != 3:
        print("Использование:")
        print("1. Сравнение текстов из аргументов командной строки:")
        print("   ./text_diff.py \"первый текст\" \"второй текст\"")
        print("2. Сравнение текстов из файлов:")
        print("   ./text_diff.py file1.txt file2.txt")
        sys.exit(1)
    
    text1 = sys.argv[1]
    text2 = sys.argv[2]
    
    # Проверяем, являются ли аргументы файлами
    if os.path.isfile(text1) and os.path.isfile(text2):
        text1 = read_file(text1)
        text2 = read_file(text2)
    
    # Получаем различия
    differences = compare_texts(text1, text2)
    
    # Выводим результат
    print("\nРезультат сравнения:")
    print("-" * 50)
    for line in differences:
        if line.startswith('+'):
            print(f"\033[92m{line}\033[0m")  # Зеленый цвет для добавленных строк
        elif line.startswith('-'):
            print(f"\033[91m{line}\033[0m")  # Красный цвет для удаленных строк
        else:
            print(line)
    print("-" * 50)

if __name__ == "__main__":
    main() 