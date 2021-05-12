""" NACCBIS Command Line Interface """
import click
from . import scrape, clean, DumpNames, GenerateIds, verify
from naccbis import __version__


@click.group(help=__doc__)
@click.version_option(version=__version__, message="naccbis %(version)s")
def cli():
    pass


cli.add_command(scrape.cli, name="scrape")
cli.add_command(clean.cli, name="clean")
cli.add_command(DumpNames.cli, name="dump-names")
cli.add_command(GenerateIds.cli, name="generate-ids")
cli.add_command(verify.cli, name="verify")


if __name__ == "__main__":
    cli()  # pragma: no cover
