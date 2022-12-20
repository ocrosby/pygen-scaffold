import click

@click.command()
@click.option('-t', '--type', type=click.Choice(["project", "module"]), help="type of the new project")
def cli():
    """Initialize a project in the current directory."""
    click.echo(f'Initializing project ...')

