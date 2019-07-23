from dataclasses import dataclass
from .parsing_utils import *

ICON_BASE_URL = "https://cdn.discordapp.com/icons"


@dataclass
class Guild:
    owner: bool
    permissions: int
    icon: str
    id: str
    name: str

    @property
    def icon_url(self) -> str:
        if self.icon.startswith("a_"):
            return f"{ICON_BASE_URL}/{self.id}/{self.icon}.gif?size=128"
        else:
            return f"{ICON_BASE_URL}/{self.id}/{self.icon}.webp?size=128"

    @staticmethod
    def from_dict(obj: Any) -> 'Guild':
        assert isinstance(obj, dict)
        owner = from_bool(obj.get("owner"))
        permissions = from_int(obj.get("permissions"))
        icon = from_str(obj.get("icon") if obj.get("icon") else "")
        snowflake = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return Guild(owner, permissions, icon, snowflake, name)

