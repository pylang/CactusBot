"""Handle data from Twitch."""

from logging import getLogger

import asyncio

from .. import Handler

from .api import TwitchAPI
from .chat import TwitchChat


class TwitchHandler(Handler):
    """Handle data from Twitch services."""

    def __init__(self, channel):
        super().__init__()

        self.logger = getLogger(__name__)

        self.api = TwitchAPI()

        self.channel = channel.lower()

        self.chat = None

    async def run(self, *auth):
        """Connect to Twitch chat and handle incoming packets."""

        server = await self.api.get_chat(self.channel)

        self.chat = TwitchChat(self.channel, server)
        await self.chat.connect(*auth)
        asyncio.ensure_future(self.chat.read(self.handle_chat))

    async def handle_chat(self, packet):
        """Handle chat packets."""
        await self.on_message(packet["message"], packet["username"])

    async def send(self, message):
        """Send a packet to Twitch."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send("PRIVMSG", message)

    async def on_message(self, message, username):
        """Handle chat message packets from chat."""

        response = await super().on_message(message, username)
        await self.send(response)

    async def on_join(self, data):
        """Handle user join packets from chat."""
        await self.send(await super().on_join(data["username"]))

    async def on_leave(self, data):
        """Handle user leave packets from chat."""
        if data["username"] is not None:
            await self.send(await super().on_leave(data["username"]))

    async def on_follow(self, data):
        """Handle follow packets from liveloading."""
        if data["following"]:
            await self.send(await super().on_follow(data["user"]["username"]))

    async def on_subscribe(self, data):
        """Handle subscribe packets from liveloading."""
        await self.send(await super().on_subscribe(data["user"]["username"]))
