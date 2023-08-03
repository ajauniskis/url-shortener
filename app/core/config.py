from typing import Dict, Optional, Union

import toml
from pydantic import HttpUrl

from app.core.logger import logger


class ProjectConfigParser:
    def __init__(self) -> None:
        self.config_file_path = "pyproject.toml"
        self.project_config = self.read_project_config()

    def read_project_config(self) -> Dict:
        logger.info(f"Reading project config from: {self.config_file_path}")
        try:
            return toml.load(self.config_file_path)
        except FileNotFoundError as e:
            logger.error(f"Failed to find project config at: {self.config_file_path}")
            raise e
        except toml.decoder.TomlDecodeError as e:
            logger.error(f"Failed to parse project config at: {self.config_file_path}")
            raise e

    @property
    def version(self) -> str:
        return self.project_config["tool"]["poetry"]["version"]

    @property
    def description(self) -> str:
        return self.project_config["tool"]["poetry"]["description"]

    @property
    def contacts(self) -> Dict[str, HttpUrl]:
        return {
            "url": HttpUrl(
                self.project_config["tool"]["poetry"]["repository"],
            ),
        }

    @property
    def license_name(self) -> str:
        return self.project_config["tool"]["poetry"]["license"]

    @property
    def license_url(self) -> HttpUrl:
        return (
            self.project_config["tool"]["poetry"]["repository"] + "/blob/main/LICENSE"
        )

    @property
    def license(self) -> Optional[Dict[str, Union[str, HttpUrl]]]:
        if self.license_name and self.license_url:
            return {
                "name": self.license_name,
                "url": self.license_url,
            }
