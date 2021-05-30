import lightbulb

from hikari_testing.bot import Bot


class Admin(lightbulb.Plugin):
    @lightbulb.owner_only()
    @lightbulb.command(name="shutdown", aliases=("sd",))
    async def command_shutdown(self, ctx: lightbulb.Context) -> None:
        await ctx.bot.close()


def load(bot: Bot) -> None:
    bot.add_plugin(Admin())


def unload(bot: Bot) -> None:
    bot.remove_plugin("Admin")
