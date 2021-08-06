

import pytest
from pathlib import Path
import shutil


SAMPLE_DIR = Path(__file__).resolve().parent / 'data'
SAMPLE_LIST = [
                'Stupendous.Man.01.Vigilant.Watch.cbz',
                'Stupendous.Man.02.cbr',
                'Stupendous.Man.03.pdf'
]


@pytest.fixture()
def prepare_comics_dir(tmpdir):
    for filename in SAMPLE_LIST:
        source = SAMPLE_DIR / filename
        destination = tmpdir / filename
        shutil.copy(source, destination)
    return tmpdir
