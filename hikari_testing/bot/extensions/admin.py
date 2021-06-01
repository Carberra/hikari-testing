import logging

import lightbulb

from hikari_testing.bot import Bot


class Admin(lightbulb.Plugin):
    @lightbulb.owner_only()
    @lightbulb.command(name="shutdown", aliases=("sd",))
    async def command_shutdown(self, ctx: lightbulb.Context) -> None:
        await ctx.bot.close(force=False)

    async def handle_extensions(self, ctx: lightbulb.Context, extensions: str, action: str) -> None:
        if extensions:
            extensions = extensions.split(" ")
        else:
            extensions = [e.split(".")[-1] for e in ctx.bot.extensions]

        count = 0
        for ext in extensions:
            try:
                getattr(ctx.bot, f"{action}_extension")(f"hikari_testing.bot.extensions.{ext.lower()}")
                logging.info(f"'{ext}' extension {action}ed")
                count += 1
            except lightbulb.errors.ExtensionAlreadyLoaded:
                logging.error(f"Extension '{ext}' is already loaded")
            except lightbulb.errors.ExtensionNotLoaded:
                logging.error(f"Extension '{ext}' is not currently loaded")

        await ctx.respond(f"{count} extension(s) {action}ed.")

    @lightbulb.owner_only()
    @lightbulb.command(name="load")
    async def command_load(self, ctx: lightbulb.Context, *, extensions: str = "") -> None:
        await self.handle_extensions(ctx, extensions, "load")

    @lightbulb.owner_only()
    @lightbulb.command(name="unload")
    async def command_unload(self, ctx: lightbulb.Context, *, extensions: str = "") -> None:
        await self.handle_extensions(ctx, extensions, "unload")

    @lightbulb.owner_only()
    @lightbulb.command(name="reload")
    async def command_reload(self, ctx: lightbulb.Context, *, extensions: str = "") -> None:
        await self.handle_extensions(ctx, extensions, "reload")


def load(bot: Bot) -> None:
    bot.add_plugin(Admin())


def unload(bot: Bot) -> None:
    bot.remove_plugin("Admin")
