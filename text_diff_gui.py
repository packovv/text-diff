#!/usr/bin/env python3
import sys
import difflib
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                            QFileDialog, QSplitter, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from docx import Document
from PyPDF2 import PdfReader
import os

class DiffWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Diff")
        self.setMinimumSize(1000, 600)
        
        # Устанавливаем стиль с пастельными цветами
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px;
                background-color: #fafafa;
                color: #333333;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 14px;
                font-weight: 400;
            }
            QPushButton {
                background-color: #a8d8ea;
                color: #333333;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #97c7d9;
            }
            QPushButton#clearButton {
                background-color: #ffb3ba;
            }
            QPushButton#clearButton:hover {
                background-color: #ffa2a9;
            }
            QLabel {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 14px;
                font-weight: 600;
                color: #333333;
                margin-bottom: 8px;
            }
        """)
        
        # Создаем центральный виджет и главный layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)
        
        # Создаем сплиттер для разделения текстовых полей
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Левая панель
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 12, 0)
        left_label = QLabel("Первый текст")
        self.left_text = QTextEdit()
        self.left_text.setPlaceholderText("Введите или вставьте первый текст")
        self.load_left_button = QPushButton("Загрузить файл")
        self.load_left_button.clicked.connect(lambda: self.load_file(self.left_text))
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.left_text)
        left_layout.addWidget(self.load_left_button)
        
        # Правая панель
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(12, 0, 0, 0)
        right_label = QLabel("Второй текст")
        self.right_text = QTextEdit()
        self.right_text.setPlaceholderText("Введите или вставьте второй текст")
        self.load_right_button = QPushButton("Загрузить файл")
        self.load_right_button.clicked.connect(lambda: self.load_file(self.right_text))
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.right_text)
        right_layout.addWidget(self.load_right_button)
        
        # Добавляем панели в сплиттер
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        self.compare_button = QPushButton("Сравнить")
        self.compare_button.clicked.connect(self.compare_texts)
        self.clear_button = QPushButton("Очистить")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addStretch()
        button_layout.addWidget(self.compare_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        # Панель результатов
        result_label = QLabel("Результат сравнения")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Здесь будет отображаться результат сравнения")
        
        # Добавляем все элементы в главный layout
        main_layout.addWidget(splitter)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_text)
        
    def load_file(self, text_edit):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Текстовые файлы (*.txt);;Word документы (*.doc *.docx);;PDF файлы (*.pdf);;Все файлы (*.*)"
        )
        if file_name:
            try:
                file_extension = os.path.splitext(file_name)[1].lower()
                
                if file_extension == '.pdf':
                    # Загружаем PDF документ
                    reader = PdfReader(file_name)
                    text = ""
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if not page_text.strip():
                            raise ValueError("Не удалось извлечь текст из PDF файла. Возможно, файл содержит только изображения или защищен от копирования.")
                        text += page_text + "\n"
                    if not text.strip():
                        raise ValueError("PDF файл не содержит текста или текст не может быть извлечен.")
                    text_edit.setText(text)
                elif file_extension in ['.doc', '.docx']:
                    # Загружаем Word документ
                    doc = Document(file_name)
                    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                    text_edit.setText(text)
                else:
                    # Загружаем обычный текстовый файл
                    with open(file_name, 'r', encoding='utf-8') as file:
                        text_edit.setText(file.read())
            except Exception as e:
                self.result_text.setText(f"Ошибка при чтении файла: {str(e)}")
    
    def compare_texts(self):
        text1 = self.left_text.toPlainText()
        text2 = self.right_text.toPlainText()
        
        # Проверка на полное совпадение
        if text1 == text2:
            self.result_text.setHtml('<span style="color: #333333; font-weight: 600; font-size: 16px;">Тексты полностью идентичны</span>')
            return
        
        # Разбиваем тексты на строки
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()
        
        # Создаем объект Differ
        differ = difflib.Differ()
        
        # Получаем различия
        diff = list(differ.compare(text1_lines, text2_lines))
        
        # Форматируем результат с HTML для цветового выделения
        result = ""
        for line in diff:
            if line.startswith('+'):
                result += f'<span style="color: #7ac5a3; font-weight: 600;">{line}</span><br>'
            elif line.startswith('-'):
                result += f'<span style="color: #e68a91; font-weight: 600;">{line}</span><br>'
            else:
                result += f'<span style="color: #333333; font-weight: 400;">{line}</span><br>'
        
        self.result_text.setHtml(result)
    
    def clear_all(self):
        self.left_text.clear()
        self.right_text.clear()
        self.result_text.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiffWindow()
    window.show()
    sys.exit(app.exec()) 