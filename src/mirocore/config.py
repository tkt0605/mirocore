import os
from pathlib import Path
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
    
def get_memory_index_dir() -> Path:
    memory_index_dir = os.getenv("MEMORY_INDEX_DIR")
    if memory_index_dir is None:
        return Path.home() / ".mirocore" / "memory_index"
    
    if memory_index_dir == "":
        raise ValueError("MEMORY_INDEX_DIR is empty")

    path = Path(memory_index_dir).expanduser()

    if not path.is_absolute():
        raise ValueError('MEMORY_INDEX_DIR must be an absolute path')

    return path