"""Interact with the Twitch API."""

from ..api import API


class TwitchAPI(API):
    """Interact with the Twitch API."""

    URL = "https://api.twitch.tv/api/"

    async def get_chat(self, username):
        """Get required data for connecting to a chat server by channel ID."""
        return "wss://" + (await self.get("channels/{username}/chat_properties".format(
            username=username))
        )["web_socket_servers"][0].split(':')[0]
