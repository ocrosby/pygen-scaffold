import pytest

from pygen_scaffold.common.logging import ClickLogger, DebugLogger


@pytest.fixture
def debug_logger():
    """
    A pytest fixture to provide access to a logger that saves messages to a list.
    :return:
    """
    return DebugLogger()


class TestDebugLogger:
    def test_info(self, debug_logger):
        debug_logger.info("test")

        assert len(debug_logger._container.get("info")) == 1
        assert debug_logger._container.get("info")[0] == "test"

    def test_error(self, debug_logger):
        debug_logger.error("something")

        assert len(debug_logger._container.get("error")) == 1
        assert debug_logger._container.get("error")[0] == "something"


class TestClickLogger:
    def test_info(self, mocker):
        mock_echo = mocker.patch("click.echo")

        click_logger = ClickLogger()
        click_logger.info("test")

        mock_echo.assert_called_once_with("test")

    def test_error(self, mocker):
        mock_echo = mocker.patch("click.echo")

        click_logger = ClickLogger()
        click_logger.error("something")

        mock_echo.assert_called_once_with("ERROR something")
