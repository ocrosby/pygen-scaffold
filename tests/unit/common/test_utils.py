import pytest

from pygen_scaffold.common import utils


class TestUrlJoin:
    def test_undefined_base(self):
        with pytest.raises(ValueError, match="Undefined base URL!"):
            utils.urljoin(None, "path")

    def test_undefined_path(self):
        with pytest.raises(ValueError, match="Undefined path!"):
            utils.urljoin("base", None)

    # def test_empty_base(self):
    #     with pytest.raises(ValueError, match="Empty base URL!"):
    #         utils.urljoin("", "path")

    # def test_empty_path(self):
    #     with pytest.raises(ValueError, match="Empty path!"):
    #         utils.urljoin("base", "")

    def test_base_ends_with_slash(self):
        assert utils.urljoin("base/", "path") == "base/path"

    def test_path_starts_with_slash(self):
        assert utils.urljoin("base", "/path") == "base/path"

    def test_base_ends_with_slash_and_path_starts_with_slash(self):
        assert utils.urljoin("base/", "/path") == "base/path"

    def test_base_does_not_end_with_slash_and_path_does_not_start_with_slash(self):
        assert utils.urljoin("base", "path") == "base/path"

    def test_base_ends_with_slash_and_path_does_not_start_with_slash(self):
        assert utils.urljoin("base/", "path") == "base/path"

    def test_base_does_not_end_with_slash_and_path_starts_with_slash(self):
        assert utils.urljoin("base", "/path") == "base/path"

    def test_base_ends_with_slash_and_path_is_empty(self):
        assert utils.urljoin("base/", "") == "base/"

    def test_base_is_empty_and_path_starts_with_slash(self):
        assert utils.urljoin("", "/path") == "/path"

    def test_base_is_empty_and_path_is_empty(self):
        assert utils.urljoin("", "") == ""

    def test_base_is_empty_and_path_does_not_start_with_slash(self):
        assert utils.urljoin("", "path") == "path"

    def test_base_is_empty_and_path_ends_with_slash(self):
        assert utils.urljoin("", "path/") == "path/"


class TestTemplateExecutor:
    def test_generate_output_path_file(self):
        root_directory = "src/templates/api/flask"
        project_directory = "test1"
        input_path = "src/templates/api/flask/bin/run.sh.jinja2"

        data = {
            "project_name": "test1",
        }

        executor = utils.TemplateExecutor(root_directory, project_directory, data)
        output_path = executor.generate_output_path(input_path)

        assert output_path == "test1/bin/run.sh"

    def test_generate_output_path_directory(self):
        root_directory = "src/templates/api/flask"
        project_directory = "test1"
        input_path = "src/templates/api/flask/bin"

        data = {
            "project_name": "test1",
        }

        executor = utils.TemplateExecutor(root_directory, project_directory, data)
        output_path = executor.generate_output_path(input_path)

        assert output_path == "test1/bin"




