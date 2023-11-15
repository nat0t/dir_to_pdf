from dataclasses import dataclass
from environs import Env


@dataclass
class Source:
    src_dir: str
    ignored_files: tuple


@dataclass
class PdfOptions:
    rows_on_page: int
    start_x: int
    start_y: int
    row_height: int


@dataclass
class PdfFile:
    full_pdf: str
    crop_pdf: str
    start_crop_page: int
    end_crop_page: int


@dataclass
class Config:
    source: Source
    pdf_options: PdfOptions
    pdf_file: PdfFile


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        source=Source(
            src_dir=env('SRC_DIR'),
            ignored_files=env.list('IGNORED_FILES'),
        ),
        pdf_options=PdfOptions(
            rows_on_page=env.int('ROWS_ON_PAGE'),
            start_x=env.int('START_X'),
            start_y=env.int('START_Y'),
            row_height=env.int('ROW_HEIGHT'),
        ),
        pdf_file=PdfFile(
            full_pdf=env('FULL_PDF'),
            crop_pdf=env('CROP_PDF'),
            start_crop_page=env.int('START_CROP_PAGE'),
            end_crop_page=env.int('END_CROP_PAGE'),
        ),
    )
