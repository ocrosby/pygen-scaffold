from os import mkdir
from os.path import isfile, isdir, join

import jinja2
from yaml import FullLoader
from yaml import load as yaml_load
from json import dump as json_dump
from shutil import rmtree
from wget import download
from zipfile import ZipFile
from pathlib import Path
from time import time

from pygen_scaffold.common.logging import NullLogger, DefaultLogger


class StopWatch:
    def __init__(self, auto_start: bool = False):
        self.start_time = 0
        self.end_time = 0

        if auto_start:
            self.start()

    @property
    def peek(self):
        delta = time() - self.start_time
        return f"{delta:.2f} seconds"

    def start(self):
        self.start_time = time()
        self.end_time = self.start_time - 1

    def end(self):
        self.end_time = time()

    def __repr__(self):
        delta = self.end_time - self.start_time
        return f"{delta:.2f} seconds"


def convert_yaml_to_json(yaml_file_path: str, json_file_path: str, logger: any = None):
    """
    Converts a yaml file to JSON.
    :param yaml_file_path:
    :param json_file_path:
    :return:
    """
    if logger is None:
        logger = DefaultLogger()

    try:
        with open(yaml_file_path) as yaml_file:
            logger.info(f"Loading YAML file '{yaml_file_path}' ...")
            yaml_data = yaml_load(yaml_file, Loader=FullLoader)
            logger.info(f"YAML file '{yaml_file_path}' successfully loaded.")

        with open(json_file_path, "w") as json_file:
            logger.info(f"Dumping JSON file '{json_file_path}' ...")
            json_dump(yaml_data, json_file, indent=4)
            logger.info(f"JSON file written to '{json_file_path}'")
    except Exception as err:
        logger.error(err)
        raise err


def replace_in_file(file_path: str, search_text: str, replace_text: str):
    """
    Replace a string in a file.
    :param file_path:
    :param search_text:
    :param replace_text:
    :return:
    """
    with open(file_path, "r") as file:
        data = file.read()

    data = data.replace(search_text, replace_text)

    with open(file_path, "w") as file:
        file.write(data)


def directory_exists(directory: str) -> bool:
    """
    Determine if a directory exists.
    :param directory:
    :return:
    """
    return isdir(directory)


def file_exists(file: str | None) -> bool:
    """
    Determine if a file exists.
    :param file:
    :return:
    """
    return isfile(file)


def create_directories(directories: list, logger: any = NullLogger()):
    for directory in directories:
        create_directory(directory, logger)


def create_directory(directory: str | None, logger: any = NullLogger()):
    """
    Create a directory.
    :param directory: Directory path to create.
    :param logger: Logger to use for output.
    :return:
    """
    if logger is None:
        logger = DefaultLogger()

    logger.info(f"Creating directory '{directory}' ...")
    mkdir(directory)
    logger.info(f"Successfully created directory '{directory}' ...")


def delete_directory(directory: str | None, logger: any = NullLogger()):
    """
    Recursively delete a directory.
    :param directory: Directory path to delete.
    :param logger: Logger to use for output.
    :return:
    """
    logger.info(f"Recursively deleting directory '{directory}' ...")
    rmtree(directory)
    logger.info(f"Successfully deleted directory '{directory}'.")


def download_file(url: str, out: str | None):
    """
    Download a file.
    :param url:
    :param out:
    :return:
    """
    download(url, out=out)
    print()


def unzip_file(file: str, out: str):
    """
    Unzip a zip file.
    :param file:
    :param out:
    :return:
    """
    with ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(out)


def slugify(value: str | None) -> str | None:
    """
    Converts the given value into a slug.
    :param value:
    :return: A slug
    """
    if value is None:
        return None

    value = value.strip()
    value = value.lower()
    value = value.replace(" ", "-")
    value = value.replace(".", "")
    value = value.replace("'", "")

    return value


def get_extension(file_path: str | None) -> str | None:
    """
    Retrieve an extension from a file path.
    :param file_path:
    :return:
    """
    if file_path is None:
        return None

    if len(file_path) == 0:
        return None

    suffix = Path(file_path).suffix

    if len(suffix) == 0:
        return None

    if suffix.startswith("."):
        suffix = suffix[1:]

    return suffix


def urljoin(base: str | None, path: str | None) -> str:
    if base is None:
        raise ValueError("Undefined base URL!")

    if path is None:
        raise ValueError("Undefined path!")

    if len(base) == 0:
        if len(path) == 0:
            return ""
        else:
            return path

    if base.endswith("/"):
        base = base[:-1]

    if path.startswith("/"):
        path = path[1:]

    return str(f"{base}/{path}")


def read_file(file_path: str | None) -> str | None:
    """
    Read a file.
    :param file_path:
    :return:
    """
    if file_path is None:
        return None

    if not file_exists(file_path):
        return None

    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path: str | None, data: str | None):
    """
    Write a file.
    :param file_path:
    :param data:
    :return:
    """
    if file_path is None:
        raise ValueError("Undefined file path!")

    if data is None:
        raise ValueError("Undefined data!")

    with open(file_path, "w") as file:
        file.write(data)


class TemplateExecutor:
    def __init__(self, root_directory: str, project_directory: str, data: dict):
        self.root_directory = root_directory
        self.project_directory = project_directory
        self.data = data

    def generate_output_path(self, template_file: str):
        """Generate the output file path for a given template file path."""
        suffix = template_file.replace(self.root_directory, "")

        if suffix.startswith("/"):
            suffix = suffix[1:]

        suffix = suffix.replace(".jinja2", "")

        output_file = join(self.project_directory, suffix)

        return output_file

    def apply(self, template: str, output_file: str = None):
        """
        Applies the specified jinja template.

        :param template: The template file path.
        :param output_file: The output file path. If not specified, the output file path will be generated from the template file path.
        :return:
        """
        print(f"Applying template '{template}' ...")

        if output_file is None:
            output_file = self.generate_output_path(template)

        content = read_file(template)
        template = jinja2.Template(content)
        content = template.render(self.data)
        write_file(output_file, content)
