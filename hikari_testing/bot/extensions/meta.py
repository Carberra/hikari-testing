import datetime as dt

import hikari
import lightbulb

from hikari_testing.bot import Bot


class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping")
    async def command_ping(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(f"Latency: {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")

    @lightbulb.command(name="userinfo", aliases=("ui",))
    async def command_userinfo(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        target = target or ctx.member

        embed = (
            hikari.Embed(
                title="User information",
                description=f"Displaying information for {target.mention}.",
                colour=target.top_role.colour,
                timestamp=dt.datetime.now().astimezone(),
            )
            .set_author(name="Information")
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
            .set_thumbnail(target.avatar_url)
            .add_field(name="Test", value="Test", inline=True)
        )

        await ctx.respond(embed)


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())


def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")
