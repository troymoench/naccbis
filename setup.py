from setuptools import setup, find_packages
from glob import glob

setup(
    name="naccbis",
    version="0.1",
    packages=find_packages(exclude=["scripts"]),
    scripts=glob('naccbis/scripts/*.py'),
)
