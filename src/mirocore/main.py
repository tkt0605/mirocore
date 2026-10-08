from mirocore.config import Settings

def main() -> None:
    print("Hello from mirocore!")
    settings = Settings.from_env()
    print(f"Database URL: {settings.database_url}")
    print(f"Log Level: {settings.log_level}")