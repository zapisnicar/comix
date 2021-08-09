"""
Comic Book Tools
"""


from __future__ import annotations
from typing import Union, List, Dict, Iterator, Any, Optional
import os
from progressbar import progressbar  # type: ignore
from pathlib import Path
from tempfile import TemporaryDirectory
from comix.container import Cbz, Cbr, Pdf
from comix.metadata import ComicRack


def get_books(directory: Union[str, Path], show_progress: bool = True) -> Iterator[Path]:
    """
    Helper function - recursively scan folder for comic book files: CBZ, CBR and PDF
    with progress bar
    """
    comic_files_list = []
    for path in sorted(Path(directory).rglob('*')):
        if path.is_file() and path.suffix.lower() in ['.cbz', '.cbr', '.pdf']:
            comic_files_list.append(path)

    if show_progress:
        for path in progressbar(comic_files_list, redirect_stdout=True):
            yield path
    else:
        for path in comic_files_list:
            yield path


# noinspection PyAttributeOutsideInit
class Book:
    """
    Manipulate Comic Book files, CBZ/CBR/PDF. Extract container content
    and repack if something is changed

    Usage:
        with Book(filepath) as comic:
            # do something
            comic.meta.title = 'Asterix'
    or:
        comic = Book(filepath)
        comic.open()
        # do something
        comic.meta.number = 1
        comic.close()
    """
    def __init__(self, path: Union[str, Path]) -> None:
        self.path: Path = Path(str(path))
        self.__temporary_dir: TemporaryDirectory
        self.working_dir: Path
        self.meta: ComicRack
        self._content_old: Optional[List[Dict]] = None
        self._input_format: Optional[str] = self.format
        self._output_format: Optional[str] = self._input_format

    def __enter__(self) -> Book:
        self.open()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        self.close()

    def __str__(self) -> str:
        return f"Book({self.path.name})"

    def __repr__(self) -> str:
        return f"Book('{str(self.path)}')"

    def open(self) -> None:
        """
        Create self.working_dir and extract files there from comic book container
        Initiate self.meta for ComicRack metadata file
        """
        self.__temporary_dir = TemporaryDirectory()
        self.working_dir = Path(self.__temporary_dir.name)
        self.unpack()
        self.meta = ComicRack(self.working_dir)

    def close(self) -> None:
        """
        If something is changed in working directory, repack container and clear temporary files
        """
        if self.is_valid() and self.is_changed():
            # Content is changed, repack archive
            # print(f'Content is changed, repacking: {self.path}')
            self.pack()
        # Clear temporary directory
        self.__temporary_dir.cleanup()

    @property
    def format(self) -> Optional[str]:
        """
        Return type of comic book container: cbz, cbr or pdf
        """
        suffix = self.path.suffix.lower()
        if suffix in ['.cbz', '.cbr', '.pdf']:
            return suffix[1:]
        # TODO raise ValueError('Unknown comic file extension')
        return None

    @format.setter
    def format(self, format_str: str) -> None:
        """
        Set new format for comic book container: cbz, cbr od prd
        """
        format_str = format_str.lower()
        if format_str in ['cbz', 'cbr', 'pdf']:
            self._output_format = format_str
        else:
            raise ValueError('Unknown comic file extension')

    def snapshot(self) -> List[Dict]:
        """
        Create snapshot of working directory, as list of files with modification times
        """
        dir_content = []
        for path in sorted(self.working_dir.rglob('*')):
            dir_content.append({os.fspath(path): path.stat().st_mtime})
        return dir_content

    def is_valid(self) -> bool:
        """
        Check validity of container, maybe it's wrong suffix, like cbr for zip archive
        """
        if self._input_format == 'cbz' and Cbz.test(self.path):
            return True
        if self._input_format == 'cbr' and Cbr.test(self.path):
            return True
        if self._input_format == 'pdf' and Pdf.test(self.path):
            return True
        return False

    def is_changed(self) -> bool:
        """
        Is there any content change of working directory, or is it changed container format
        """
        if self._input_format != self._output_format:
            return True
        # Is there any change in working directory
        if self.snapshot() != self._content_old:
            return True
        return False

    def unpack(self) -> None:
        """
        Extract files from container
        """
        if self.is_valid():
            # Unpack archive
            if self._input_format == 'cbz':
                Cbz.unpack(self.path, self.working_dir)
            elif self._input_format == 'cbr':
                Cbr.unpack(self.path, self.working_dir)
            elif self._input_format == 'pdf':
                Pdf.unpack(self.path, self.working_dir)
            else:
                raise Exception(f'Unknown format for {self.path} - must be cbz, cbr or pdf')
            # Remember current state of files
            self._content_old = self.snapshot()
        else:
            raise TypeError(f'Wrong file type: {self.path}')

    def pack(self) -> None:
        """
        Pack files into container
        """
        if self._output_format == 'cbz':
            new_name = self.path.with_suffix('.cbz')
            self.backup()
            Cbz.pack(new_name, self.working_dir)
        elif self._output_format == 'cbr':
            new_name = self.path.with_suffix('.cbr')
            self.backup()
            Cbr.pack(new_name, self.working_dir)
        elif self._output_format == 'pdf':
            new_name = self.path.with_suffix('.pdf')
            self.backup()
            Pdf.pack(new_name, self.working_dir)
        else:
            raise TypeError(f'Wrong file type: {self.path}')

    def backup(self) -> None:
        """
        Backup/Rename original comic file
        """
        backup_path = self.path.with_suffix(self.path.suffix + '.bak')
        # Delete previous backup file, if exists. Probably needed for Windows
        if backup_path.exists():
            backup_path.unlink()
        self.path.rename(backup_path)
