from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BotConfig(BaseModel):
    name: str | None
    token: str | None
    system_prompt: str | None

class BotSettings(BaseSettings):
    bots: list[BotConfig]
