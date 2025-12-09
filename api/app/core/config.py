import os

from pydantic import BaseModel


class Settings(BaseModel):
    db_host: str = os.getenv("DB_HOST", "db")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_name: str = os.getenv("DB_NAME", "demo_db")
    db_user: str = os.getenv("DB_USER", "demo_user")
    db_password: str = os.getenv("DB_PASSWORD", "demo_password")

    @property
    def sqlalchemy_database_uri(self) -> str:
        # mysql+pymysql uses the pure-Python pymysql driver
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()

