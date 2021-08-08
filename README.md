# ComiX

Comic Book Tools for Python. 

A handy tool for bulk comic book editing and organization:

- Scan directories for file formats CBZ, CBR, and PDF

- Convert between file formats CBZ, CBR, and PDF

- Extract files from CBZ, CBR, and PDF

- Edit content of files extracted from CBZ, CBR, and PDF

- Edit metadata in ComicInfo.xml (Note: PDF container will ignore metadata)

Examples:

    from comix import Book, get_books

    # Scan folder for comic book files:    
    for comic_file in get_books('folder_with_comics'):
        # With context manager, set <Series> tag to Asterix
        with Book(comic_file) as comic:
            comic.meta.series = 'Asterix'
            # Get issue from filename and write to <Number> tag
            comic.meta.number = comic.path.stem[8:10]

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
