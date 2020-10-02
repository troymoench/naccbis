from setuptools import setup, find_packages

setup(
    name="naccbis",
    version="0.2",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": [
        "scrape = naccbis.scripts.scrape:main",
        "clean = naccbis.scripts.clean:main",
        "GenerateIds = naccbis.scripts.GenerateIds:main",
        "DumpNames = naccbis.scripts.DumpNames:main",
        "verify = naccbis.scripts.verify:main",
        ]
    },
    python_requires='>=3.6',
)
