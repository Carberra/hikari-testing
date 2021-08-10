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

        p = getattr(target.presence, "formatted", "No presence.") or "No presence."

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
            .add_field(name="ID", value=target.id)
            .add_field(name="Discriminator", value=target.discriminator, inline=True)
            .add_field(name="Bot?", value=target.is_bot, inline=True)
            .add_field(name="No. of roles", value=len(target.roles) - 1, inline=True)
            .add_field(name="Created on", value=target.created_at.strftime("%d %b %Y"), inline=True)
            .add_field(name="Joined on", value=target.joined_at.strftime("%d %b %Y"), inline=True)
            .add_field(
                name="Boosted since",
                value=getattr(target.premium_since, "strftime", lambda x: "Not boosting.")("%d %b %Y"),
                inline=True
            )
            # .add_field(name="Presence", value=f"{target.presence}")  # Submit PR
            .add_field(
                name="Presence",
                value=p,
            )
            .add_field(name="Roles", value=" | ".join(r.mention for r in reversed(target.roles[1:])))
        )

        await ctx.respond(embed)


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())


def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")
