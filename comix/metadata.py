

from typing import Union, Optional
from xml.etree import ElementTree
from xml.dom import minidom
from pathlib import Path


class ComicRack:
    """
    ComicRack metadata (ComicInfo.xml) Reader/Writer

    Supported properties/tags:

        title                year             genre
        series               month            web
        number               day              page_count
        count                writer           language_iso
        volume               penciller        format
        alternate_series     inker            age_rating
        alternate_number     colorist         black_and_white
        story_arc            letterer         manga
        series_group         cover_artist     characters
        alternate_count      editor           teams
        summary              publisher        locations
        notes                imprint          scan_information

    Usage:

        # Create metadata object from ComicInfo.xml
        metadata = ComicRack('/folder_with_ComicInfo.xml_file')
        # Read text from tag <Title>...</Title>
        name = metadata.title
        # Write text to tag <Title>...</Title>
        metadata.title = "Asterix"


    # TODO <Pages> support
    """

    empty_xml = """<?xml version="1.0"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</ComicInfo>
"""

    def __init__(self, directory: Union[str, Path]) -> None:
        """
        Create metadata object from ComicInfo.xml file found in 'directory"
        """
        self.xml_path: Path = Path(str(directory)) / 'ComicInfo.xml'
        self.root: ElementTree.Element = ElementTree.fromstring(self.empty_xml)
        if self.xml_path.exists():
            try:
                tree = ElementTree.parse(self.xml_path)
                self.root = tree.getroot()
            except ElementTree.ParseError:
                # not valid xml file, ignore and use default self.root (empty_xml)
                # TODO raise self.changed flag?
                pass

    def _get(self, tag: str) -> Optional[str]:
        """
        Read text from custom tag in ComicInfo.xml
        """
        element = self.root.find(tag)
        if element is None:
            return None
        return element.text

    def _set(self, tag: str, value: str) -> None:
        """
        Write text to custom tag in ComicInfo.xml file
        and save file after any change
        """
        element = self.root.find(tag)
        if element is None:
            # tag is new
            ElementTree.SubElement(self.root, tag)
            new_element = self.root.find(tag)
            assert new_element is not None  # for mypy
            new_element.text = str(value)
        else:
            # tag already exists
            element.text = str(value)

        # Save xml file
        self._pretty_xml(self.root, '\t', '\n')
        new_data = ElementTree.tostring(self.root, encoding='utf-8')
        # pretty_data = minidom.parseString(new_data).toprettyxml()
        new_file = open(self.xml_path, "wb")
        new_file.write(new_data)

    def _pretty_xml(self, element, indent, newline, level=0) -> None:
        """
        Prettify XML output, from:
        https://www.programmersought.com/article/10663049555/
        Element is passed in Element class parameters for indentation indent, for wrapping NEWLINE
        """
        # Determine whether the element has child elements
        if element:
            if (element.text is None) or element.text.isspace():  # If there is no element of text content
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
                # Else: # here two lines if the Notes removed, Element will start a new line of text
                # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
        # Element will turn into a list
        temp = list(element)
        for sub_element in temp:
            # If it is not the last element of the list, indicating that the next line is the starting level of the
            # same elements, indentation should be consistent
            if temp.index(sub_element) < (len(temp) - 1):
                sub_element.tail = newline + indent * (level + 1)
            else:
                # If it is the last element of the list, indicating that the next line is the end of the
                # parent element, a small indentation should
                sub_element.tail = newline + indent * level
            # Sub-elements recursion
            self._pretty_xml(sub_element, indent, newline, level=level + 1)

    @property
    def title(self) -> Optional[str]:
        return self._get('Title')

    @title.setter
    def title(self, x: str) -> None:
        self._set('Title', x)

    @property
    def series(self) -> Optional[str]:
        return self._get('Series')

    @series.setter
    def series(self, x: str) -> None:
        self._set('Series', x)

    @property
    def number(self) -> Optional[str]:
        return self._get('Number')

    @number.setter
    def number(self, x: str) -> None:
        self._set('Number', x)

    @property
    def count(self) -> Optional[str]:
        return self._get('Count')

    @count.setter
    def count(self, x: str) -> None:
        self._set('Count', x)

    @property
    def volume(self) -> Optional[str]:
        return self._get('Volume')

    @volume.setter
    def volume(self, x: str) -> None:
        self._set('Volume', x)

    @property
    def alternate_series(self) -> Optional[str]:
        return self._get('AlternateSeries')

    @alternate_series.setter
    def alternate_series(self, x: str) -> None:
        self._set('AlternateSeries', x)

    @property
    def alternate_number(self) -> Optional[str]:
        return self._get('AlternateNumber')

    @alternate_number.setter
    def alternate_number(self, x: str) -> None:
        self._set('AlternateNumber', x)

    @property
    def story_arc(self) -> Optional[str]:
        return self._get('StoryArc')

    @story_arc.setter
    def story_arc(self, x: str) -> None:
        self._set('StoryArc', x)

    @property
    def series_group(self) -> Optional[str]:
        return self._get('SeriesGroup')

    @series_group.setter
    def series_group(self, x: str) -> None:
        self._set('SeriesGroup', x)

    @property
    def alternate_count(self) -> Optional[str]:
        return self._get('AlternateCount')

    @alternate_count.setter
    def alternate_count(self, x: str) -> None:
        self._set('AlternateCount', x)

    @property
    def summary(self) -> Optional[str]:
        return self._get('Summary')

    @summary.setter
    def summary(self, x: str) -> None:
        self._set('Summary', x)

    @property
    def notes(self) -> Optional[str]:
        return self._get('Notes')

    @notes.setter
    def notes(self, x: str) -> None:
        self._set('Notes', x)

    @property
    def year(self) -> Optional[str]:
        return self._get('Year')

    @year.setter
    def year(self, x: str) -> None:
        self._set('Year', x)

    @property
    def month(self) -> Optional[str]:
        return self._get('Month')

    @month.setter
    def month(self, x: str) -> None:
        self._set('Month', x)

    @property
    def day(self) -> Optional[str]:
        return self._get('Day')

    @day.setter
    def day(self, x: str) -> None:
        self._set('Day', x)

    @property
    def writer(self) -> Optional[str]:
        return self._get('Writer')

    @writer.setter
    def writer(self, x: str) -> None:
        self._set('Writer', x)

    @property
    def penciller(self) -> Optional[str]:
        return self._get('Penciller')

    @penciller.setter
    def penciller(self, x: str) -> None:
        self._set('Penciller', x)

    @property
    def inker(self) -> Optional[str]:
        return self._get('Inker')

    @inker.setter
    def inker(self, x: str) -> None:
        self._set('Inker', x)

    @property
    def colorist(self) -> Optional[str]:
        return self._get('Colorist')

    @colorist.setter
    def colorist(self, x: str) -> None:
        self._set('Colorist', x)

    @property
    def letterer(self) -> Optional[str]:
        return self._get('Letterer')

    @letterer.setter
    def letterer(self, x: str) -> None:
        self._set('Letterer', x)

    @property
    def cover_artist(self) -> Optional[str]:
        return self._get('CoverArtist')

    @cover_artist.setter
    def cover_artist(self, x: str) -> None:
        self._set('CoverArtist', x)

    @property
    def editor(self) -> Optional[str]:
        return self._get('Editor')

    @editor.setter
    def editor(self, x: str) -> None:
        self._set('Editor', x)

    @property
    def publisher(self) -> Optional[str]:
        return self._get('Publisher')

    @publisher.setter
    def publisher(self, x: str) -> None:
        self._set('Publisher', x)

    @property
    def imprint(self) -> Optional[str]:
        return self._get('Imprint')

    @imprint.setter
    def imprint(self, x: str) -> None:
        self._set('Imprint', x)

    @property
    def genre(self) -> Optional[str]:
        return self._get('Genre')

    @genre.setter
    def genre(self, x: str) -> None:
        self._set('Genre', x)

    @property
    def web(self) -> Optional[str]:
        return self._get('Web')

    @web.setter
    def web(self, x: str) -> None:
        self._set('Web', x)

    @property
    def page_count(self) -> Optional[str]:
        return self._get('PageCount')

    @page_count.setter
    def page_count(self, x: str) -> None:
        self._set('PageCount', x)

    @property
    def language_iso(self) -> Optional[str]:
        return self._get('LanguageISO')

    @language_iso.setter
    def language_iso(self, x: str) -> None:
        self._set('LanguageISO', x)

    @property
    def format(self) -> Optional[str]:
        return self._get('Format')

    @format.setter
    def format(self, x: str) -> None:
        self._set('Format', x)

    @property
    def age_rating(self) -> Optional[str]:
        return self._get('AgeRating')

    @age_rating.setter
    def age_rating(self, x: str) -> None:
        self._set('AgeRating', x)

    @property
    def black_and_white(self) -> Optional[str]:
        return self._get('BlackAndWhite')

    @black_and_white.setter
    def black_and_white(self, x: str) -> None:
        self._set('BlackAndWhite', x)

    @property
    def manga(self) -> Optional[str]:
        return self._get('Manga')

    @manga.setter
    def manga(self, x: str) -> None:
        self._set('Manga', x)

    @property
    def characters(self) -> Optional[str]:
        return self._get('Characters')

    @characters.setter
    def characters(self, x: str) -> None:
        self._set('Characters', x)

    @property
    def teams(self) -> Optional[str]:
        return self._get('Teams')

    @teams.setter
    def teams(self, x: str) -> None:
        self._set('Teams', x)

    @property
    def locations(self) -> Optional[str]:
        return self._get('Locations')

    @locations.setter
    def locations(self, x: str) -> None:
        self._set('Locations', x)

    @property
    def scan_information(self) -> Optional[str]:
        return self._get('ScanInformation')

    @scan_information.setter
    def scan_information(self, x: str) -> None:
        self._set('ScanInformation', x)
