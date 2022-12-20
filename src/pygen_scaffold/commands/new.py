import click


@click.command()
@click.option('-n', '--name', prompt='project name', help='project name')
@click.option("-t", "--type", type=click.Choice(["project", "module"]), help="type of the new project")
def cli(name: str, type: str):
    """Create a new project."""
    click.echo(f'Creating project "{name}" ...')

