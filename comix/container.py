"""
Comic book containers: CBZ CBR PDF
"""


from typing import Union
import fitz  # type: ignore
import io
from pathlib import Path
from subprocess import DEVNULL, STDOUT, check_call
from PIL import Image  # type: ignore
from zipfile import is_zipfile
from unrar import rarfile  # type: ignore
from shutil import which


class Container:
    """
    Base class for container classes Cbz, Cbr and Pdf

    Methods:
        unpack: extract files from container
        pack:   create container from files
        test:   test container
    """
    @staticmethod
    def unpack(filename: Union[str, Path], extract_to: Union[str, Path]) -> None:
        """
        Extract files from container
        """
        raise NotImplemented

    @staticmethod
    def pack(filename: Union[str, Path], source_dir: Union[str, Path]) -> None:
        """
        Create container from files in source dir
        """
        raise NotImplemented

    @staticmethod
    def test(filename: Union[str, Path]) -> bool:
        """
        Test container
        """
        raise NotImplemented


class Cbz(Container):
    """
    CBZ (ZIP) container methods
    """
    @staticmethod
    def unpack(filename: Union[str, Path], extract_to: Union[str, Path]) -> None:
        if which('unzip'):
            check_call(['unzip', str(filename), '-d', str(extract_to)], stdout=DEVNULL, stderr=STDOUT)
        else:
            raise FileNotFoundError("Program 'unzip' is not installed")

    @staticmethod
    def pack(filename: Union[str, Path], source_dir: Union[str, Path]) -> None:
        if which('zip'):
            check_call(['zip', '-r', str(filename), '.'], stdout=DEVNULL, stderr=STDOUT, cwd=str(source_dir))
        else:
            raise FileNotFoundError("Program 'zip' is not installed")

    @staticmethod
    def test(filename: Union[str, Path]) -> bool:
        return is_zipfile(str(filename))


class Cbr(Container):
    """
    CBR (RAR) container methods
    """
    @staticmethod
    def unpack(filename: Union[str, Path], extract_to: Union[str, Path]) -> None:
        if which('unrar'):
            check_call(['unrar', 'x', str(filename), str(extract_to)], stdout=DEVNULL, stderr=STDOUT)
        else:
            raise FileNotFoundError("Program 'unrar' is not installed")

    @staticmethod
    def pack(filename: Union[str, Path], source_dir: Union[str, Path]) -> None:
        if which('rar'):
            check_call(['rar', 'a', '-r', str(filename), '*'], stdout=DEVNULL, stderr=STDOUT, cwd=str(source_dir))
        else:
            raise FileNotFoundError("Program 'rar' is not installed")

    @staticmethod
    def test(filename: Union[str, Path]) -> bool:
        return rarfile.is_rarfile(str(filename))


class Pdf(Container):
    """
    PDF container methods
    """
    @staticmethod
    def unpack(filename: Union[str, Path], extract_to: Union[str, Path]) -> None:
        pdf_file = fitz.open(str(filename))
        # iterate over PDF pages
        for page_count, page in enumerate(pdf_file, start=1):
            # iterate over images on current page
            for image_count, image in enumerate(page.getImageList(), start=1):
                # get the XREF of the image
                xref = image[0]
                # extract the image bytes
                base_image = pdf_file.extractImage(xref)
                image_bytes = base_image['image']
                # get the image extension
                image_ext = base_image['ext']
                # save image with PIL
                output_path = Path(str(extract_to)) / f'image_{page_count:0>4d}_{image_count:0>3d}.{image_ext}'
                output_file = Image.open(io.BytesIO(image_bytes))
                output_file.save(open(output_path, 'wb'))
                output_file.close()
        pdf_file.close()

    @staticmethod
    def pack(filename: Union[str, Path], source_dir: Union[str, Path]) -> None:
        pdf_doc = fitz.open()
        for path in sorted(Path(str(source_dir)).rglob('*')):
            if path.is_file() and path.suffix in ['.jpg', '.jpeg', '.png', '.gif']:
                image = fitz.open(path)  # open pic as document
                rect = image[0].rect  # pic dimension
                pdf_bytes = image.convert_to_pdf()  # make a PDF stream
                image.close()  # no longer needed
                image_pdf = fitz.open('pdf', pdf_bytes)  # open stream as PDF
                page = pdf_doc.new_page(width=rect.width,  # new page with ...
                                        height=rect.height)  # pic dimension
                page.show_pdf_page(rect, image_pdf, 0)  # image fills the page

        pdf_doc.save(str(filename))
        pdf_doc.close()

    # TODO test() method for pdf container
