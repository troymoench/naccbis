import pytest
from click.testing import CliRunner

from naccbis.scripts import DumpNames, GenerateIds, clean, cli, scrape, verify


@pytest.fixture
def cli_runner():
    return CliRunner()


class TestGenerateIds:
    def test_cli_help(self, cli_runner):
        result = cli_runner.invoke(GenerateIds.cli, ["--help"])
        assert result.exit_code == 0
        assert "generate player ids" in result.output
        assert "--load" in result.output
        assert "--clear" in result.output
        assert "--season" in result.output
        assert "--dir" in result.output


class TestDumpNames:
    def test_cli_help(self, cli_runner):
        result = cli_runner.invoke(DumpNames.cli, ["--help"])
        assert result.exit_code == 0
        assert "Identify inconsistencies with player names" in result.output
        assert "-c, --corrections" in result.output
        assert "-f, --fname" in result.output
        assert "-l, --lname" in result.output
        assert "--nicknames" in result.output
        assert "--duplicates" in result.output
        assert "--dir" in result.output


class TestClean:
    def test_cli_help(self, cli_runner):
        result = cli_runner.invoke(clean.cli, ["--help"])
        assert result.exit_code == 0
        assert "cleaning controller" in result.output

    def test_cli_final_help(self, cli_runner):
        result = cli_runner.invoke(clean.cli, ["final", "--help"])
        assert result.exit_code == 0
        assert "final [OPTIONS] YEAR" in result.output
        assert "-S, --stat" in result.output
        assert "-s, --split" in result.output
        assert "--load" in result.output
        assert "-v, --verbose" in result.output


class TestScrape:
    def test_cli_help(self, cli_runner):
        result = cli_runner.invoke(scrape.cli, ["--help"])
        assert result.exit_code == 0
        assert "scraping controller" in result.output

    def test_cli_final_help(self, cli_runner):
        result = cli_runner.invoke(scrape.cli, ["final", "--help"])
        assert result.exit_code == 0
        assert "final [OPTIONS] YEAR" in result.output
        assert "-S, --stat" in result.output
        assert "-s, --split" in result.output
        assert "-o, --output" in result.output
        assert "-v, --verbose" in result.output

    def test_cli_inseason_help(self, cli_runner):
        result = cli_runner.invoke(scrape.cli, ["inseason", "--help"])
        assert result.exit_code == 0
        assert "inseason [OPTIONS]" in result.output
        assert "-S, --stat" in result.output
        assert "-s, --split" in result.output
        assert "-o, --output" in result.output
        assert "-v, --verbose" in result.output


class TestVerify:
    def test_cli_help(self, cli_runner):
        result = cli_runner.invoke(verify.cli, ["--help"])
        assert result.exit_code == 0
        assert "verify" in result.output


class TestCli:
    def test_cli_help(self, cli_runner):
        result = cli_runner.invoke(cli.cli, ["--help"])
        assert result.exit_code == 0
        assert "NACCBIS Command Line Interface" in result.output
        assert "Commands:" in result.output
        assert "scrape" in result.output
        assert "clean" in result.output
        assert "dump-names" in result.output
        assert "generate-ids" in result.output
        assert "verify" in result.output

    def test_cli_version(self, cli_runner):
        result = cli_runner.invoke(cli.cli, ["--version"])
        assert result.exit_code == 0
        assert "naccbis" in result.output
