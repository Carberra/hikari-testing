from __future__ import annotations

import lightbulb
from lightbulb import errors, plugins

from hikari_testing.bot import Bot


class Error(lightbulb.Plugin):
    @plugins.listener()
    async def on_command_error(self, event: lightbulb.CommandErrorEvent) -> None:
        if isinstance(event.exception, errors.CommandNotFound):
            return

        if isinstance(event.exception, errors.NotEnoughArguments):
            return await event.context.respond(
                "There are some missing arguments: " + ", ".join(event.exception.missing_args)
            )

        if isinstance(event.exception, errors.TooManyArguments):
            return await event.context.respond("Too many arguments were passed.")

        if isinstance(event.exception, errors.CommandIsOnCooldown):
            return await event.context.respond(
                f"Command is on cooldown. Try again in {event.exception.retry_after:.0f} second(s)."
            )

        if isinstance(event.exception, errors.CommandInvocationError):
            raise event.exception.original

        await event.context.respond("I have errored, and I cannot get up.")
        raise event.exception


def load(bot: Bot) -> None:
    bot.add_plugin(Error())


def unload(bot: Bot) -> None:
    bot.remove_plugin("Error")
