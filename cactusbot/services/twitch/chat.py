"""Interact with Beam chat."""


from logging import getLogger

import re

from .. import WebSocket


class TwitchChat(WebSocket):
    """Interact with Beam chat."""

    PACKET_EXPR = re.compile(
        r'^:([a-zA-Z0-9][\w]{3,24})!\1@\1.tmi.twitch.tv '
        r'([A-Z]+) #([a-zA-Z0-9][\w]{3,24}) :(.+)$'
    )

    def __init__(self, channel, *endpoints):
        super().__init__(*endpoints)

        self.logger = getLogger(__name__)

        assert isinstance(channel, str), "Channel name must be a string."
        self.channel = channel

    async def send(self, command, data):
        """Send a packet."""

        if data is None:
            return
        if command == "JOIN":
            await super().send("JOIN #{}".format(self.channel))
        elif command == "PRIVMSG":
            await super().send("PRIVMSG #{chan} :{msg}".format(
                chan=self.channel, msg=data)
            )
        elif command == "PONG":
            await super().send("PONG: {}".format(data))
        else:
            await super().send("{command} {data}".format(
                command=command, data=data)
            )

    async def initialize(self, username, oauth):
        """Send an authentication packet."""

        await self.send("CAP REQ",
                        ":twitch.tv/commands twitch.tv/membership")
        await self.send("PASS", oauth)
        await self.send("NICK", username)
        await self.send("JOIN", self.channel)

    async def parse(self, message):
        """Parse a chat packet."""

        for line in re.split(r'-?\r\n', message):
            match = re.match(self.PACKET_EXPR, line)

            if match is not None:
                if match.group(2) == "PING":
                    await self.send("PONG", match.group(1))
                    return None
                elif match.group(2) == "PRIVMSG":
                    return {
                        "username": match.group(1),
                        "message": match.group(4)
                    }
