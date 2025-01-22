import os
from PyPDF2 import PdfReader
from docx import Document
from ebooklib import epub
from lxml import etree

def pdf_to_word(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    doc = Document()
    for page in reader.pages:
        doc.add_paragraph(page.extract_text())
    doc.save(output_path)

def pdf_to_epub(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title("Converted PDF")
    book.set_language("en")
    chapter_content = ""
    for page in reader.pages:
        chapter_content += page.extract_text() + "\n\n"
    chapter = epub.EpubHtml(title="Chapter 1", file_name="chap_1.xhtml", lang="en")
    chapter.content = f"<h1>Converted PDF</h1><p>{chapter_content.replace('\n', '<br>')}</p>"
    book.add_item(chapter)
    book.spine = ["nav", chapter]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(output_path, book)

def pdf_to_fb2(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    root = etree.Element("FictionBook", xmlns="http://www.gribuser.ru/xml/fictionbook/2.0")
    body = etree.SubElement(root, "body")
    section = etree.SubElement(body, "section")
    title = etree.SubElement(section, "title")
    etree.SubElement(title, "p").text = "Converted PDF"
    for page in reader.pages:
        etree.SubElement(section, "p").text = page.extract_text()
    tree = etree.ElementTree(root)
    tree.write(output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def main():
    print("Добро пожаловать в PDF-конвертер!")
    print("Доступные форматы: Word (docx), EPUB (epub), FB2 (fb2)")
    format_choice = input("Введите желаемый формат (word, epub, fb2): ").strip().lower()
    if format_choice not in ["word", "epub", "fb2"]:
        print("Неверный формат. Программа завершена.")
        return
    
    pdf_path = input("Перетащите файл PDF в окно консоли и нажмите Enter: ").strip().strip('"')
    if not os.path.exists(pdf_path):
        print("Файл не найден. Программа завершена.")
        return
    
    output_path = input("Введите имя выходного файла (без расширения): ").strip()
    output_path = f"{output_path}.{format_choice}"
    
    try:
        if format_choice == "word":
            pdf_to_word(pdf_path, output_path)
        elif format_choice == "epub":
            pdf_to_epub(pdf_path, output_path)
        elif format_choice == "fb2":
            pdf_to_fb2(pdf_path, output_path)
        print(f"Файл успешно конвертирован и сохранен как: {output_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
