from dataclasses import dataclass

from aiohttp import ClientResponse
from aiohttp.web_exceptions import HTTPBadRequest
from sanic_oauth.providers import DiscordClient

from .parsing_utils import *

AVATAR_BASE_URL: str = "https://cdn.discordapp.com/avatars"
API_USER_URL: str = "https://discordapp.com/api/users/@me"


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
        if not self.avatar:
            return f"{AVATAR_BASE_URL}/{self.id}/{int(self.discriminator) % 5}.webp?size=128"
        if self.avatar.startswith("a_"):
            return f"{AVATAR_BASE_URL}/{self.id}/{self.avatar}.gif?size=128"
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


async def get_user(provider: DiscordClient) -> User:
    return User.from_dict(await _get_user_dict(provider))


async def _get_user_dict(provider: DiscordClient) -> Dict[str, Union[str, int]]:
    response: ClientResponse = await provider.request("GET", API_USER_URL)
    if response.status != 200:
        raise HTTPBadRequest(
            reason=f'Failed to obtain User information. HTTP status code: {response.status}'
        )
    return await response.json()