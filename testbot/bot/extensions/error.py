from __future__ import annotations

import logging

import hikari
import lightbulb
from lightbulb import plugins

from testbot.bot import Bot


class ErrorHandler(lightbulb.Plugin):
    @plugins.listener()
    async def on_command_error(self, event: lightbulb.CommandErrorEvent) -> None:
        if isinstance(event.exception, lightbulb.errors.CommandNotFound):
            return None

        if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
            return await event.context.respond(
                "There are some missing arguments: " + ", ".join(event.exception.missing_args)
            )

        if isinstance(event.exception, lightbulb.errors.TooManyArguments):
            return await event.context.respond("Too many arguments were passed.")

        if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
            return await event.context.respond(
                f"Command is on cooldown. Try again in {event.exception.retry_after:.0f} second(s)."
            )

        await event.context.respond("I have errored, and I cannot get up.")
        raise event.exception


def load(bot: Bot) -> None:
    bot.add_plugin(ErrorHandler())


def unload(bot: Bot) -> None:
    bot.remove_plugin("ErrorHandler")
