from setuptools import setup, find_packages
from glob import glob

setup(
    name="naccbis",
    version="0.2",
    packages=find_packages(exclude=["scripts"]),
    scripts=glob('naccbis/scripts/*.py'),
)
