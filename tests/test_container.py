

import pytest
from shutil import which


class TestInstallation:
    def test_zip(self):
        assert which('zip')

    def test_unzip(self):
        assert which('unzip')

    def test_rar(self):
        assert which('rar')

    def test_unrar(self):
        assert which('unrar')
