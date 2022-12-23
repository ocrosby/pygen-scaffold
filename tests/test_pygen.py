from click.testing import CliRunner

from pygen_scaffold.__main__ import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'A scaffolding utility for python projects.' in result.output
