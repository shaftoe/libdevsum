"""Unit tests."""
# pylint: disable=import-error
import pytest
# pylint: enable=import-error
from libdevsum import (PROJECT_URL, Repo, SEMVER_MATCH, TempDownloader,
                       Validator, __version__)


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
    with pytest.raises(IOError):
        Validator.command_available('C:> troll.exe', abort=True)


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


def test_repo_remote_tags():
    """Test Repo.get_remote_tags()."""
    regexp = r'^refs/tags/test\d+'
    test_tags = ['refs/tags/test01', 'refs/tags/test02']
    assert Repo.get_remote_tags(PROJECT_URL, regexp) == test_tags

    regexp = r'^notExistent$'
    assert Repo.get_remote_tags(PROJECT_URL, regexp) == []


def test_repo_latest_tag():
    """Test Repo.get_latest_remote_tag()."""
    regexp = r'^refs/tags/test(\d+)'
    assert Repo.get_latest_remote_tag(PROJECT_URL, regexp) == '02'

    regexp = r'^notExistent$'
    assert Repo.get_latest_remote_tag(PROJECT_URL, regexp) is None

    regexp = r'^(notExistentWithGroup)$'
    assert Repo.get_latest_remote_tag(PROJECT_URL, regexp) is None


def test_changelog_uptodate():
    """Test that CHANGELOG.md has been updated with latest __version__."""
    from re import findall

    match_string = r'## \[(%s)\]' % SEMVER_MATCH

    with open('CHANGELOG.md') as changelog:
        matches = findall(match_string, changelog.read())

    assert len(matches) > 0
    assert matches[0] == __version__
