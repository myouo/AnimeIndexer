from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AnimeIndexer API"
    db_path: str = "./data/anime.db"
    bangumi_api_base: str = "https://api.bgm.tv"
    bangumi_access_token: str = ""
    user_agent: str = "AnimeIndexer/0.1 (+desktop)"


settings = Settings()
