import os

import fitz

from config import load_config
from utils import delete_escape_chr


def get_text_pages(dir_path: str, rows_on_page: int, ignored: tuple = tuple()) -> list[tuple]:
    """Return list of text pages from all files in directory."""
    text: list = []
    if not os.path.exists(dir_path):
        print(f'Directory "{dir_path}" not found.')
        return text
    for address, dirs, files in os.walk(dir_path):
        for name in files:
            filename = os.path.join(address, name)
            if any(x in filename for x in ignored):
                continue
            with open(filename) as f:
                raw_text = [delete_escape_chr(row) for row in f.readlines()]
            text.extend(row for row in raw_text if len(row))
    return [tuple(text[i:i + rows_on_page]) for i in range(0, len(text), rows_on_page)]


def write_pdf_page(rows: tuple, filename: str, start_x: int = 20, start_y: int = 50,
                   row_height: int = 14) -> None:
    """Write page to pdf-file with transferred content."""
    if not os.path.exists(filename):
        with fitz.open() as pdf:
            page = pdf.new_page()
            tw = fitz.TextWriter(page.rect)
            for idx, line in enumerate(rows):
                tw.append((start_x, start_y + idx * row_height), line)
            tw.write_text(page)
            pdf.ez_save(filename)
    else:
        with fitz.open(filename) as pdf:
            page = pdf.new_page()
            tw = fitz.TextWriter(page.rect)
            for idx, line in enumerate(rows):
                tw.append((start_x, start_y + idx * row_height), line)
            tw.write_text(page)
            pdf.ez_save(filename, incremental=True, garbage=0, encryption=False)


def remove_pdf_pages(src_file: str, dst_file: str, start: int, end: int) -> None:
    """Remove pages from pdf-file."""
    try:
        if os.path.exists(src_file):
            with fitz.open(src_file) as pdf:
                pdf.delete_pages(start, pdf.page_count - (end + 1))
                pdf.save(dst_file)
    except ValueError:
        print(f'Incorrect values of start or end for cropping.')


if __name__ == '__main__':
    config = load_config()

    pages = get_text_pages(config.source.src_dir, config.pdf_options.rows_on_page, config.source.ignored_files)
    for page in pages:
        write_pdf_page(page, config.pdf_file.full_pdf, config.pdf_options.start_x, config.pdf_options.start_y,
                       config.pdf_options.row_height)
    remove_pdf_pages(config.pdf_file.full_pdf, config.pdf_file.crop_pdf, config.pdf_file.start_crop_page,
                     config.pdf_file.end_crop_page)
