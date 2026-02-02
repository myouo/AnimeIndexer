from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AnimeIndexer API"
    db_path: str = "./data/anime.db"
    bangumi_api_base: str = "https://api.bgm.tv"
    bangumi_access_token: str = ""
    user_agent: str = "AnimeIndexer/0.1 (+desktop)"
    sync_page_size: int = 50
    sync_recent_pages: int = 40

    class Config:
        env_file = ".env"


settings = Settings()
