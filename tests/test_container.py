

import pytest
from shutil import which


class TestInstallation:
    def test_rar(self):
        assert which('rar')

    def test_unrar(self):
        assert which('unrar')
