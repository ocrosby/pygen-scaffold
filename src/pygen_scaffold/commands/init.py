import click


@click.command()
@click.option('-t', '--type', type=click.Choice(["api", "cmd", "module"]), help="type of the new project")
def cli():
    """Initialize a project in the current directory."""
    click.echo('Initializing project ...')
