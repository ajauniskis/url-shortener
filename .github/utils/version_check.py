import os
from typing import Dict, Union
from app.core import logger
import toml
from packaging import version
import re


class VersionChecker:
    def __init__(
        self,
        local_pyproject_loc: str = "pyproject.toml",
        prod_pyproject_loc: str = "tmp/pyproject.toml",
    ) -> None:
        self.local_pyproject_loc = local_pyproject_loc
        self.prod_pyproject_loc = prod_pyproject_loc

        self.version_regex = r'\d.\d.\d[^"]*'

    def _read_pyproject(self, pyproject_loc: str) -> Dict:
        logger.info(f"Reading project config from: {pyproject_loc}")
        try:
            return toml.load(pyproject_loc)
        except FileNotFoundError:
            logger.error(f"Failed to find pyproject at: {pyproject_loc}")
            raise FileNotFoundError(f"Failed to find pyproject at: {pyproject_loc}")
        except toml.decoder.TomlDecodeError as e:
            logger.error(f"Failed to parse pyproject at: {pyproject_loc}")
            raise e

    def _parse_version(self, value: str) -> str:
        try:
            return re.findall(self.version_regex, value)[0]
        except IndexError:
            logger.error(f"Could not parse version from: {value}")
            raise Exception(f"Could not parse version from: {value}")

    def _get_version(self, pyproject: Dict) -> version.Version:
        try:
            out = pyproject["tool"]["poetry"]["version"]
        except KeyError:
            logger.error("Could not find version.")
            raise Exception("Could not find version.")

        local_version = self._parse_version(out)
        logger.info(f"Found local version: {local_version}")

        return version.parse(local_version)

    def is_version_upgraded(self) -> bool:
        local_pyproject = self._read_pyproject(self.local_pyproject_loc)
        prod_pyproject = self._read_pyproject(self.prod_pyproject_loc)

        local_version = self._get_version(local_pyproject)
        prod_version = self._get_version(prod_pyproject)

        if local_version < prod_version:
            print(f"Version was upgraded from {local_version} to {prod_version}.")

            return True

        else:
            raise Exception(
                "Version is not upgraded."
                + f" Version in prod: {prod_version}, version in branch: {local_version}"
            )


def main():
    vc = VersionChecker()
    vc.is_version_upgraded()


if __name__ == "__main__":
    main()
