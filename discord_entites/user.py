from dataclasses import dataclass
from .parsing_utils import *

AVATAR_BASE_URL = "https://cdn.discordapp.com/avatars"


@dataclass
class User:
    username: str
    locale: str
    mfa_enabled: bool
    flags: int
    avatar: str
    discriminator: str
    id: str

    @property
    def avatar_url(self) -> str:
        if self.avatar.startswith("a_"):
            return f"{AVATAR_BASE_URL}/{self.id}/{self.avatar}.gif?size=128"
        else:
            return f"{AVATAR_BASE_URL}/{self.id}/{self.avatar}.webp?size=128"

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        locale = from_str(obj.get("locale"))
        mfa_enabled = from_bool(obj.get("mfa_enabled"))
        flags = from_int(obj.get("flags"))
        avatar = from_str(obj.get("avatar") if obj.get("avatar") else "")
        discriminator = from_str(obj.get("discriminator"))
        snowflake = from_str(obj.get("id"))
        return User(username, locale, mfa_enabled, flags, avatar, discriminator, snowflake)
