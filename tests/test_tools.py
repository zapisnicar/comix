

import pytest
from comix.tools import Book, get_books
from pathlib import Path
from shutil import which


def directory_list(comic_working_directory):
    files_list = []
    for item in sorted(comic_working_directory.rglob('*')):
        if item.is_file():
            files_list.append(str(item.name))
    files_list.sort()
    return files_list


def test_create_empty_book():
    comic = Book('')
    assert comic.path == Path('')


def test_open_cbz(prepare_comics_dir):
    comic = Book(prepare_comics_dir / 'Stupendous.Man.01.Vigilant.Watch.cbz')
    comic.open()
    files_list = directory_list(comic.working_dir)
    assert files_list == [
        'stupendous.man.01.page.01.png',
        'stupendous.man.01.page.02.png'
    ]


def test_open_cbr(prepare_comics_dir):
    comic = Book(prepare_comics_dir / 'Stupendous.Man.02.cbr')
    comic.open()
    files_list = directory_list(comic.working_dir)
    assert files_list == [
        'Stupendous.Man.02.page.01.png',
        'Stupendous.Man.02.page.02.png'
    ]


def test_open_pdf(prepare_comics_dir):
    comic = Book(prepare_comics_dir / 'Stupendous.Man.03.pdf')
    comic.open()
    files_list = directory_list(comic.working_dir)
    assert files_list == [
        'image_0001_001.png',
        'image_0002_001.png'
    ]
