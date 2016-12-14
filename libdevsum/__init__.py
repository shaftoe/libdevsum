"""Devsum utils lib."""
from __future__ import print_function


PROJECT_URL = 'https://github.com/shaftoe/libdevsum'


# pylint: disable=too-few-public-methods
class TempDownloader(object):
    """Context manager to ease download with tempfiles."""

    def __init__(self, url):
        """Initialize context manager."""
        from tempfile import mkstemp
        self._url, self._temp_file = url, mkstemp()[1]

    def __enter__(self):
        """Enter the context."""
        from urllib import urlretrieve

        print('dowloading from %s\nsaving content to tempfile %s' % (
            self._url, self._temp_file))

        urlretrieve(self._url, self._temp_file)
        return self._temp_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Do cleanups."""
        from os import remove
        print('cleaning up tempfile')
        remove(self._temp_file)
# pylint: enable=too-few-public-methods


class Validator(object):
    """Class wrapper for validation logics."""

    @staticmethod
    def semver(version=None):
        """Return true if version is a valid segver version string."""
        from re import match
        try:
            return bool(match(r'^\d+\.\d+\.\d+$', version))
        except TypeError:
            return False

    @staticmethod
    def command_available(command):
        """Return true if command is available in current PATH."""
        # pylint: disable=no-name-in-module,import-error
        # We need to disable some pylint checks here:
        # https://github.com/PyCQA/pylint/issues/73
        from distutils.spawn import find_executable
        # pylint: enable=no-name-in-module,import-error
        return bool(find_executable(command))

    @staticmethod
    def linted(filepath):
        """Lint given file path with linters."""
        from subprocess import call, CalledProcessError

        linters = [['pylint', '--rcfile=/dev/null', '--reports=n',
                    '--disable=locally-disabled,locally-enabled'],
                   ['pydocstyle'],
                   ['flake8']]

        for linter in linters:
            linter.append(filepath)
            if not Validator.command_available(linter[0]):
                print('WARNING: disabling %s tests, binary not found '
                      'in current PATH' % linter[0])

        linters = [linter for linter in linters
                   if Validator.command_available(linter[0])]

        try:
            returncodes = [not bool(call(linter)) for linter in linters]
            return all(returncodes)
        except CalledProcessError:
            return False


class Repo(object):
    """Class wrapper for Git tasks utilities."""

    @staticmethod
    def get_remote_tags(git_repo, regexp=r'.*'):
        """Fetch remote tags references and return list with ref names."""
        from re import match
        from subprocess import check_output

        raw_output = check_output(['git', 'ls-remote', '--tags',
                                   git_repo]).rstrip()

        return [ref.split('\t')[1] for ref in raw_output.split('\n')
                if len(ref.split('\t')) == 2 and match(regexp,
                                                       ref.split('\t')[1])]

    @staticmethod
    def get_latest_remote_tag(git_repo, regexp):
        """Return latest tags matching regexp."""
        from re import match

        tags = Repo.get_remote_tags(git_repo, regexp)

        if tags and match(regexp, tags[-1]).groups():
            return match(regexp, tags[-1]).group(1)
