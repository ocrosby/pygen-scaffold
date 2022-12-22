import os
import click
import jinja2

from pygen_scaffold.common import utils


@click.group()
def cli():
    """Create a new project."""
    pass


@cli.command()
@click.option('-n', '--name', required=True, help="name of the new project")
def api(name: str):
    """Create a new API project."""
    project_name = name
    project_dir = os.path.abspath(f"./{project_name}")

    data = {
        'author': 'Omar Crosby',
        'author_email': 'omar.crosby@gmail.com',
        'github_username': 'ocrosby',
        'project_name': project_name,
        'version': '0.0.0'
    }

    click.echo(f'Creating API project "{project_name}"...')

    if utils.directory_exists(project_dir):
        click.echo(f'Project directory "{project_dir}" already exists.')
        exit(9)

    project_dir = os.path.abspath(f"./{project_name}")

    utils.create_directory(project_dir)

    click.echo(f'Project directory "{project_dir}" created.')

    click.echo("Overlaying flask api files ...")
    root_directory = "src/templates/api/flask"
    executor = utils.TemplateExecutor(root_directory, project_dir, data)
    for root, dirs, files in os.walk(root_directory, topdown=True):
        for name in dirs:
            idir = os.path.join(root, name)
            odir = executor.generate_output_path(idir)
            utils.create_directory(odir)

        for name in files:
            ifile = os.path.join(root, name)
            executor.apply(ifile)


    click.echo()
    click.echo("Overlaying root files ...")
    root_directory = "src/templates/root"
    executor = utils.TemplateExecutor(root_directory, project_dir, data)
    for root, dirs, files in os.walk("src/templates/root", topdown=True):
        for name in dirs:
            idir = os.path.join(root, name)
            odir = executor.generate_output_path(idir)
            utils.create_directory(odir)

        for name in files:
            ifile = os.path.join(root, name)
            executor.apply(ifile)






@cli.command()
@click.option('-n', '--name', help="name of the new project")
@click.option('-n', '--name', help="name of the new project")
def cmd(name: str):
    """Create a new CLI project."""
    project_name = name
    project_dir = os.path.abspath(f"./{project_name}")

    data = {
        'author': 'Omar Crosby',
        'author_email': 'omar.crosby@gmail.com',
        'github_username': 'ocrosby',
        'project_name': project_name,
        'version': '0.0.0'
    }

    click.echo(f'Creating CLI project "{project_name}"...')

    if utils.directory_exists(project_dir):
        click.echo(f'Project directory "{project_dir}" already exists.')
        exit(9)

    project_dir = os.path.abspath(f"./{project_name}")

    utils.create_directory(project_dir)

    click.echo(f'Project directory "{project_dir}" created.')

    click.echo("Overlaying flask api files ...")
    root_directory = "src/templates/cli"
    executor = utils.TemplateExecutor(root_directory, project_dir, data)
    for root, dirs, files in os.walk(root_directory, topdown=True):
        for name in dirs:
            idir = os.path.join(root, name)
            odir = executor.generate_output_path(idir)
            utils.create_directory(odir)

        for name in files:
            ifile = os.path.join(root, name)
            executor.apply(ifile)


    click.echo()
    click.echo("Overlaying root files ...")
    root_directory = "src/templates/root"
    executor = utils.TemplateExecutor(root_directory, project_dir, data)
    for root, dirs, files in os.walk("src/templates/root", topdown=True):
        for name in dirs:
            idir = os.path.join(root, name)
            odir = executor.generate_output_path(idir)
            utils.create_directory(odir)

        for name in files:
            ifile = os.path.join(root, name)
            executor.apply(ifile)


@cli.command()
@click.option('-n', '--name', help="name of the new project")
def module(name: str):
    """Create a new module project."""
    project_name = name
    project_dir = os.path.abspath(f"./{project_name}")

    data = {
        'author': 'Omar Crosby',
        'author_email': 'omar.crosby@gmail.com',
        'github_username': 'ocrosby',
        'project_name': project_name,
        'version': '0.0.0'
    }

    click.echo(f'Creating module project "{project_name}"...')

    if utils.directory_exists(project_dir):
        click.echo(f'Project directory "{project_dir}" already exists.')
        exit(9)

    project_dir = os.path.abspath(f"./{project_name}")

    utils.create_directory(project_dir)

    click.echo(f'Project directory "{project_dir}" created.')

    click.echo("Overlaying module files ...")
    root_directory = "src/templates/module"
    executor = utils.TemplateExecutor(root_directory, project_dir, data)
    for root, dirs, files in os.walk(root_directory, topdown=True):
        for name in dirs:
            idir = os.path.join(root, name)
            odir = executor.generate_output_path(idir)
            utils.create_directory(odir)

        for name in files:
            ifile = os.path.join(root, name)
            executor.apply(ifile)


    click.echo()
    click.echo("Overlaying root files ...")
    root_directory = "src/templates/root"
    executor = utils.TemplateExecutor(root_directory, project_dir, data)
    for root, dirs, files in os.walk("src/templates/root", topdown=True):
        for name in dirs:
            idir = os.path.join(root, name)
            odir = executor.generate_output_path(idir)
            utils.create_directory(odir)

        for name in files:
            ifile = os.path.join(root, name)
            executor.apply(ifile)

