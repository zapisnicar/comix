# ComiX -> work in progress...

Comic Book Tools for Python:

- Scan directories for comic book files (CBZ/CBR/PDF).
  
- Change content, extract files, convert to another format or edit metadata from ComicInfo.xml file. PDF container will ignore metadata.

- Useful for bulk editing.

Examples:

    from comix import Book, get_books

    # With context manager, set <Title> tag text to 'Asterix'
    with Book('filepath') as comic:
        comic.meta.title = 'Asterix'

    or:
    
    # Manualy open Comic Book file, then set <Number> tag text to 1
    comic = Book('filepath')
    comic.open()
    # Change text of <Number> tag
    comic.meta.number = 1
    # Don't forget to close
    comic.close()

    or:

    # Convert all CBR and PDF books in 'folder_with_comics' to CBZ format
    for comic_file in get_books('folder_with_comics'):
        comic = Book(comic_file)
        if comic.format in ['pdf', 'cbr']:
            comic.open()
            comic.format = 'cbz'
            comic.close()


Required programs: zip, unzip, rar and unrar - command line versions, installed in PATH:

https://sourceforge.net/projects/infozip/files/

https://www.rarlab.com/download.htm

Tested in Python 3.7 for Linux.

Test setup:

    python -m pip install --upgrade pip
    pip install pytest
    pip install -e ./
    pytest

Build setup:

    pip install build
    python -m build
