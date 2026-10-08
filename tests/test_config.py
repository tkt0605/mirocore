# tests/test_config.py

from mirocore.config import Settings
import pytest

def test_loads_databaseurl(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://miroc:miroc@db:5432/miroc")
    monkeypatch.delenv("LOG_LEVEL", raising = False)

    settings = Settings.from_env()

    assert settings.database_url == "postgresql://miroc:miroc@db:5432/miroc"
    assert settings.log_level == "INFO"

def test_uses_log_level_from_env(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://miroc:miroc@db:5432/miroc")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings.from_env()

    assert settings.log_level == "DEBUG"

def test_missing_database_url_raises(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising = False)

    with pytest.raises(RuntimeError) as exc_info:
        Settings.from_env()

def test_blank_database_url_raises(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "")

    with pytest.raises(RuntimeError):
        Settings.from_env()