from unittest import TestCase
from unittest.mock import patch

from toml.decoder import TomlDecodeError

from app.core import ProjectConfigParser

SAMPLE_CONFIG = {
    "tool": {
        "poetry": {
            "name": "joke-api",
            "version": "0.0.1-alpha.1",
            "description": "Joke Api served with FastApi",
            "authors": ["Algirdas Jauniskis <jauniskis.a@gmail.com>"],
            "readme": "README.md",
            "packages": [{"include": "app"}],
            "repository": "https://github.com/ajauniskis/joke-api",
        }
    }
}


class TestProjectConfigParser(TestCase):
    @patch("toml.load")
    def setUp(self, mock_toml) -> None:
        mock_toml.return_value = SAMPLE_CONFIG
        self.pcp = ProjectConfigParser()

    @patch("toml.load")
    def test_read_project_config__returns_config(self, mock_toml):

        mock_toml.return_value = SAMPLE_CONFIG

        actual = ProjectConfigParser()

        self.assertEqual(
            actual.project_config,
            SAMPLE_CONFIG,
        )

    def test_read_project_config_invalid_file_location__logs_error_and_throws(self):
        self.pcp.config_file_path = "invalid/path"

        with self.assertLogs() as logger_context:
            with self.assertRaises(FileNotFoundError) as exception_context:
                self.pcp.read_project_config()

        self.assertEqual(
            logger_context.output[1],
            "ERROR:uvicorn.info:Failed to find project config at:"
            + f" {self.pcp.config_file_path}",
        )

        self.assertEqual(
            str(exception_context.exception),
            "[Errno 2] No such file or directory: 'invalid/path'",
        )

    @patch("toml.load", side_effect=TomlDecodeError("", "", 0))
    def test_read_project_config_invalid_file_structure__logs_error(self, mock_toml):
        with self.assertLogs() as logger_context:
            with self.assertRaises(TomlDecodeError):
                self.pcp.read_project_config()

        self.assertEqual(
            logger_context.output[1],
            "ERROR:uvicorn.info:Failed to parse project config at:"
            + f" {self.pcp.config_file_path}",
        )

    def test_get_project_version__returns_version(self):
        actual = self.pcp.version

        self.assertEqual(
            actual,
            SAMPLE_CONFIG["tool"]["poetry"]["version"],
        )

    def test_get_project_version_key_not_found__throws(self):
        self.pcp.project_config = {}

        with self.assertRaises(KeyError):
            self.pcp.version

    def test_get_project_description__returns_version(self):
        actual = self.pcp.description

        self.assertEqual(
            actual,
            SAMPLE_CONFIG["tool"]["poetry"]["description"],
        )

    def test_get_project_description_key_not_found__throws(self):
        self.pcp.project_config = {}
        with self.assertRaises(KeyError):
            self.pcp.description

    def test_get_project_contacts__returns_version(self):
        actual = self.pcp.contacts

        self.assertEqual(
            actual,
            {"url": SAMPLE_CONFIG["tool"]["poetry"]["repository"]},
        )

    def test_get_project_contacts_key_not_found__returns_empty(self):
        self.pcp.project_config = {}

        with self.assertRaises(KeyError):
            self.pcp.contacts
