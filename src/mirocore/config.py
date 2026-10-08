import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise RuntimeError("DATABASE_URL is not set")
        
        return cls(
            database_url= database_url,
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
