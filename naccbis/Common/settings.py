from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "naccbis"
    db_url: str = "postgresql://localhost/naccbisdb"
    log_level: str = "INFO"

    def get_db_url(self):
        return f"{self.db_url}?application_name={self.app_name}"

    class Config:
        env_prefix = "naccbis_"
        env_file = ".env"
