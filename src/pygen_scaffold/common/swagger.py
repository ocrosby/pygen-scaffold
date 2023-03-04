import os
import shutil
import zipfile

import bs4
import requests
import wget

from pygen_scaffold.common.logging import ClickLogger, NullLogger
from pygen_scaffold.common.utils import (StopWatch, convert_yaml_to_json, create_directories,
                                         create_directory, delete_directory, directory_exists,
                                         download_file, file_exists, get_extension,
                                         replace_in_file, unzip_file, TemplateExecutor)

RELEASE_URL = "https://github.com/swagger-api/swagger-ui/releases/latest"

null_logger = NullLogger()


def get_latest_release() -> str:
    """Returns the latest release of Swagger UI"""
    response = requests.get(RELEASE_URL)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.content, "html.parser")

    version_item = soup.find("li", class_=["breadcrumb-item-selected"])
    version = version_item.find("a").text
    version = version.strip()

    return version


class Swagger:
    def __init__(self):
        self.latest_release = get_latest_release()

    @property
    def latest_release(self) -> str:
        return self._latest_release

    @latest_release.setter
    def latest_release(self, value: str):
        self._latest_release = value

    @property
    def version(self) -> str:
        version = self.latest_release
        if version.startswith("v"):
            version = version[1:]

        return version

    @property
    def archive_url(self) -> str:
        return f"https://github.com/swagger-api/swagger-ui/archive/refs/tags/{self.latest_release}.zip"

    @property
    def url(self):
        return f"https://github.com/swagger-api/swagger-ui/archive/refs/tags/{self.version}.zip"

    @property
    def current_directory(self) -> str:
        return os.getcwd()

    def download(self, out: str):
        wget.download(self.url, out=out)

        with zipfile.ZipFile("swagger-ui.zip", "r") as zip_ref:
            zip_ref.extractall("swagger-ui")

    def _inject_templates(self, index_file: str):
        soup = bs4.BeautifulSoup(open(index_file), "html.parser")

        links = soup.find_all("link")
        for link in links:
            href = link.get("href")
            extension = get_extension(href)

            if extension == "css":
                if href.startswith("./"):
                    href_new = (
                        "{{ url_for('static', filename='css/" + href[2:] + "') }}"
                    )
                else:
                    href_new = "{{ url_for('static', filename='css/" + href + "') }}"
            elif extension == "png":
                if href.startswith("./"):
                    href_new = (
                        "{{ url_for('static', filename='img/" + href[2:] + "') }}"
                    )
                else:
                    href_new = "{{ url_for('static', filename='img/" + href + "') }}"
            else:
                href_new = href

            link["href"] = href_new

        scripts = soup.find_all("script")
        for script in scripts:
            src = script.get("src")

            if src.startswith("./"):
                src_new = "{{ url_for('static', filename='js/" + src[2:] + "') }}"
            else:
                src_new = "{{ url_for('static', filename='js/" + src + "') }}"

            script["src"] = src_new

        with open(index_file, "w") as file:
            file.write(str(soup))

    def _copy_dist_files(self, dist_directory: str, logger: any = null_logger):
        logger.info("Copying dist files ...")
        for root, dirs, files in os.walk(dist_directory):
            for file in files:
                source = os.path.join(root, file)

                extension = get_extension(source)

                if extension == "js":
                    destination = os.path.join("temp/swagger/static/js", file)
                    logger.info(f"Copying '{source}' to '{destination}'")
                    shutil.copy(source, destination)
                elif extension == "css":
                    destination = os.path.join("temp/swagger/static/css", file)
                    logger.info(f"Copying '{source}' to '{destination}'")
                    shutil.copy(source, destination)
                elif extension == "png":
                    destination = os.path.join("temp/swagger/static/img", file)
                    logger.info(f"Copying '{source}' to '{destination}'")
                    shutil.copy(source, destination)
                else:
                    destination = os.path.join("temp/swagger/templates", file)
                    logger.info(f"Copying '{source}' to '{destination}'")
                    shutil.copy(source, destination)
        logger.info("Done copying dist files")

    def _ensure_api_directories(self, logger: any = null_logger):
        # Make sure the top level directories exist
        if not directory_exists("api/static"):
            create_directory("api/static")

        if not directory_exists("api/templates"):
            create_directory("api/templates")

        # Remove the js directory if it exists for copytree.
        if directory_exists("api/static/js"):
            delete_directory("api/static/js", logger)

        # Remove the css directory if it exists for copytree.
        if directory_exists("api/static/css"):
            delete_directory("api/static/css", logger)

        # Remove the img directory if it exists for copytree.
        if directory_exists("api/static/img"):
            delete_directory("api/static/img", logger)

    def _copy_static_files(self, logger: any = null_logger):
        logger.info("Copying static files")
        shutil.copytree("temp/swagger/static/js", "api/static/js")
        shutil.copytree("temp/swagger/static/css", "api/static/css")
        shutil.copytree("temp/swagger/static/img", "api/static/img")
        logger.info("Done copying static files")

    def _copy_templates(self, logger: any = null_logger):
        logger.info("Copying templates")
        template_files = os.listdir("temp/swagger/templates")
        for file in template_files:
            source = os.path.join("temp/swagger/templates", file)
            destination = os.path.join("api/templates", file)

            logger.info(f"Copying '{source}' to '{destination}'")
            shutil.copy(source, destination)
        logger.info("Done copying templates")

    def build(self,
              author_name: str,
              author_email: str,
              project_name: str,
              yaml_file: str,
              logger: any = null_logger):

        data = {
            "author": author_name,
            "author_email": author_email,
            "project_name": project_name
        }

        if logger is None:
            logger = ClickLogger()

        archive_url = f"https://github.com/swagger-api/swagger-ui/archive/refs/tags/{self.latest_release}.zip"
        archive_file = f"temp/downloads/swagger-ui-{self.latest_release}.zip"

        logger.info(f"Latest release: {self.latest_release}")
        logger.info(f"Archive URL: {archive_url}")

        if directory_exists("temp"):
            delete_directory("temp", logger)

        create_directory("temp", logger)
        create_directory("temp/swagger-ui", logger)
        create_directory("temp/downloads", logger)

        logger.info(f"Downloading the archive '{archive_url}' ...")
        stop_watch = StopWatch(auto_start=True)
        download_file(archive_url, archive_file)
        stop_watch.end()
        logger.info(
            f"Successfully downloaded the archive to '{archive_file}' in {stop_watch}."
        )

        if not file_exists(archive_file):
            logger.info(f"Failed to download the archive file: '{archive_file}'!")
            raise FileNotFoundError(f"File not found: {archive_file}")

        unzip_file(archive_file, "temp/swagger-ui")
        delete_directory("temp/downloads", logger)

        create_directories(
            [
                "temp/swagger",
                "temp/swagger/static",
                "temp/swagger/static/js",
                "temp/swagger/static/css",
                "temp/swagger/static/img",
                "temp/swagger/templates",
            ],
            logger,
        )

        self._copy_dist_files(f"temp/swagger-ui/swagger-ui-{self.version}/dist", logger)

        logger.info("Renaming the index file to swaggerui.html ...")
        os.rename(
            "temp/swagger/templates/index.html", "temp/swagger/templates/swaggerui.html"
        )

        self._inject_templates("temp/swagger/templates/swaggerui.html")

        # This is where the failure is occurring because the input file is not present.
        # I think I need to specify the location of the openapi yaml document.
        #
        # Note: I've created a swagger directory in templates so the first step should
        #       probably be to generate the target document from the swagger template.
        #
        # Question: Where should the target document be placed?
        
        root_directory = ""
        project_dir = ""
        executor = TemplateExecutor(root_directory, project_dir, data)

        template_file = os.path.join(root_directory, "templates/swagger/openapi.yaml.jinja2")
        output_file = os.path.join(project_dir, "openapi.yaml")
        executor.apply(template_file, output_file)

        convert_yaml_to_json("api/static/openapi.yaml", "api/static/openapi.json")

        # Updating the URL for the swagger document.
        # -----------------------------------------------------------------------------------------------
        search_text = '"https://petstore.swagger.io/v2/swagger.json"'
        # replace_text = "\"{{ url_for('static', filename='openapi.json') }}\""
        replace_text = "'/static/openapi.json'"

        replace_in_file(
            "temp/swagger/static/js/swagger-initializer.js", search_text, replace_text
        )
        # -----------------------------------------------------------------------------------------------

        delete_directory("temp/swagger-ui", logger)

        self._ensure_api_directories(logger)
        self._copy_static_files(logger)
        self._copy_templates(logger)

        delete_directory("temp", logger)
