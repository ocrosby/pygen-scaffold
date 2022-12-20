import pytest

from click.testing import CliRunner

from pygen_scaffold.__main__ import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Interact with pygen-scaffold projects.' in result.output


def test_new():
    runner = CliRunner()
    result = runner.invoke(cli, ['new', '--type', 'module', '--name', 'test'])
    assert result.exit_code == 0
    assert 'Create a new pygen-scaffold project.' in result.output


def test_init():
    runner = CliRunner()
    result = runner.invoke(cli, ['init', '--type', 'module'])
    assert result.exit_code == 0
    assert 'Initializing project ...' in result.output

