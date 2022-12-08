from os import path
import codecs

from setuptools import setup, find_packages


def read(rel_path):
    here = path.abspath(path.dirname(__file__))
    with codecs.open(path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]


### Do the setup
setup(
    name="automate",
    author="C. Dhainaut",
    version=get_version("automate/__init__.py"),
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "automate = automate.cli:main",
        ],
    },
)
