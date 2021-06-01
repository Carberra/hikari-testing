import logging
from pathlib import Path

import hikari
import lightbulb
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from hikari_testing import STDOUT_CHANNEL_ID, __version__


class Bot(lightbulb.Bot):
    def __init__(self) -> None:
        self._extensions = [p.stem for p in Path("./hikari_testing/bot/extensions/").glob("*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        with open("./secrets/token", mode="r", encoding="utf-8") as f:
            token = f.read().strip("\n")

        super().__init__(
            prefix="-",
            insensitive_commands=True,
            token=token,
            intents=hikari.Intents.ALL,
        )

    @staticmethod
    async def guild_only(message: hikari.Message) -> bool:
        return message.guild_id is not None

    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)

        super().run(
            activity=hikari.Activity(
                name=f"-help | Version {__version__}",
                type=hikari.ActivityType.WATCHING,
            )
        )

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        for ext in self._extensions:
            self.load_extension(f"hikari_testing.bot.extensions.{ext}")
            logging.info(f"'{ext}' extension loaded")

    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        self.add_check(self.guild_only)

        self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        await self.stdout_channel.send(f"Testing v{__version__} now online!")

        logging.info("BOT READY!")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        # This is gonna be fixed.
        await self.stdout_channel.send(f"Testing v{__version__} is shutting down.")
        self.scheduler.shutdown()
