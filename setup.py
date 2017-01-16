"""Setup script."""
from setuptools import setup
from libdevsum import PROJECT_URL, __version__


setup(
    name='libdevsum',
    version=__version__,
    description='Collection of utilities I do not know where else to keep.',
    author='Alexander Fortin',
    author_email='alex@devsum.it',
    url=PROJECT_URL,
    packages=['libdevsum'],
    zip_safe=True,
)
