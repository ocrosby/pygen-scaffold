import click
import logging


class DebugLogger:
    def __init__(self):
        self._container = {
            "info": [],
            "error": []
        }

    def info(self, message):
        self._container.get("info").append(message)

    def error(self, message):
        self._container.get("error").append(message)


class ClickLogger:
    def __init__(self):
        self._module = click

    def info(self, message):
        self._module.echo(message)

    def error(self, message):
        self._module.echo(f"ERROR {message}")


class DefaultLogger:
    def __init__(self):
        self._module = logging

    def info(self, message):
        self._module.info(message)

    def error(self, message):
        self._module.error(message)


class NullLogger:
    def info(self, message):
        pass

    def error(self, message):
        pass
