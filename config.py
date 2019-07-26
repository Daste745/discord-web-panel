import json
from dataclasses import dataclass
from discord_entites.parsing_utils import from_str, Any


@dataclass
class Config:
    bot_token: str
    app_id: str
    app_secret: str
    
    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        bot_token = from_str(obj.get("bot_token"))
        app_id = from_str(obj.get("app_id"))
        app_secret = from_str(obj.get("app_secret"))
        return Config(bot_token=bot_token, app_id=app_id, app_secret=app_secret)


def get_config() -> Config:
    with open("config.json") as f:
        return Config.from_dict(json.load(f))
