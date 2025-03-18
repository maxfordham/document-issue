from __future__ import annotations

import pathlib  # noqa: TC003

from pydantic import HttpUrl, ImportString  # noqa: TC002
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """project configuration settings, enables custom project templates."""

    STATUS_REVISION: HttpUrl | pathlib.Path | ImportString | None = None

    model_config = SettingsConfigDict(env_prefix="PROJECT_CONFIGURATION_")

SETTINGS = Settings()


