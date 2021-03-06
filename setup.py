import os
import re
from setuptools import setup, find_packages


with open(
    os.path.join(os.path.dirname(__file__), "naccbis", "__init__.py")
) as v_file:
    VERSION = (
        re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S)
        .match(v_file.read())
        .group(1)
    )

setup(
    name="naccbis",
    version=VERSION,
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": [
        "naccbis = naccbis.scripts.cli:cli",
        ]
    },
    python_requires='>=3.6',
)
