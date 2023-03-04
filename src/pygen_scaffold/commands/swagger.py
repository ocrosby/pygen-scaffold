import click

from pygen_scaffold.common.logging import ClickLogger
from pygen_scaffold.common.swagger import Swagger

swagger = Swagger()


@click.group()
def cli():
    """Interact with Swagger UI"""


@cli.command("version")
def get_version():
    """
    Get the latest Swagger UI version.
    """
    click.echo(swagger.version)


@cli.command("build")
@click.option("-a", "--author", help="Author name")
@click.option("-e", "--email", help="Author email")
@click.option("-p", "--project", help="Project name")
@click.option("-y", "--yaml", help="Path to YAML file")
def build(author: str, email: str, project: str, yaml_file: str):
    """Build the Swagger UI."""
    swagger.build(author,
                  email,
                  project,
                  yaml_file,
                  ClickLogger())
