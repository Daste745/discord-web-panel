from dataclasses import dataclass

from aiohttp import ClientResponse
from aiohttp.web_exceptions import HTTPBadRequest
from sanic_oauth.providers import DiscordClient

from .parsing_utils import *

ICON_BASE_URL: str = "https://cdn.discordapp.com/icons"
API_GUILDS_URL: str = "https://discordapp.com/api/users/@me/guilds"


@dataclass
class Guild:
    owner: bool
    permissions: int
    icon: str
    id: str
    name: str

    @property
    def icon_url(self) -> str:
        if not self.icon:
            return f"static/img/empty-server.png"
            # TODO: use sanic to get that path dynamically
        if self.icon.startswith("a_"):
            return f"{ICON_BASE_URL}/{self.id}/{self.icon}.gif?size=128"
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


async def get_guilds(provider: DiscordClient) -> Iterator[Guild]:
    guilds_dict: Dict[str, Union[str, int, bool]] = await _get_discord_guilds_dict(provider)
    return map(Guild.from_dict, guilds_dict)


async def _get_discord_guilds_dict(provider: DiscordClient) -> Dict[str, Union[str, int, bool]]:
    response: ClientResponse = await provider.request("GET", API_GUILDS_URL)
    if response.status != 200:
        raise HTTPBadRequest(
            reason=f'Failed to obtain User information. HTTP status code: {response.status}'
        )
    return await response.json()
