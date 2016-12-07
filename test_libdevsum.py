"""Unit tests."""
from libdevsum import (Validator, TempDownloader)


def test_validator_semver():
    """Test Validator.semver() ."""
    assert Validator.semver('1.2.3')
    assert Validator.semver('0.123.456')
    assert not Validator.semver('1.2.3z')
    assert not Validator.semver('blah')


def test_validator_commandavailable():
    """Test Validator.command_available() ."""
    assert Validator.command_available('python')
    assert not Validator.command_available('C:> troll.exe')


def test_validator_linted():
    """Test Validator.linted() ."""
    assert Validator.linted(__file__)
    assert Validator.linted('libdevsum')
    assert Validator.linted('setup.py')
    assert Validator.linted('fixtures/linted_file.py')
    assert not Validator.linted('fixtures/not_linted_file.py')


def test_temp_downloader():
    """Test TempDownloader context manager."""
    from os.path import isfile
    with TempDownloader(__file__) as downloaded:
        assert isfile(downloaded)
