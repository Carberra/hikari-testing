from collections import defaultdict
import datetime as dt

import hikari
import lightbulb
from hikari.channels import ChannelType
from hikari.presences import Status

from hikari_testing.bot import Bot


class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping")
    async def command_ping(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(f"Latency: {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")

    @lightbulb.command(name="userinfo", aliases=("ui",))
    async def command_userinfo(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        target = target or ctx.member
        created_at = int(target.created_at.timestamp())
        joined_at = int(target.joined_at.timestamp())
        presence = target.presence.activities[0]

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
            .add_field(
                name="Created on",
                value=f"<t:{created_at}:d> (<t:{created_at}:R>)",
                inline=False
            )
            .add_field(
                name="Joined on",
                value=f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
                inline=False
            )
            .add_field(name="Presence", value=f"{presence.type} {presence}")
            .add_field(name="Roles", value=" | ".join(r.mention for r in reversed(target.roles[1:])))
        )

        await ctx.respond(embed)

    @lightbulb.command(name="serverinfo", aliases=("si",))
    async def command_serverinfo(self, ctx: lightbulb.Context) -> None:
        owner = ctx.guild.get_member(ctx.guild.owner_id)
        created_at = int(ctx.guild.created_at.timestamp())
        joined_at = int(ctx.guild.joined_at.timestamp())
        channels = ctx.guild.channels.values()
        text_channels = list(filter(lambda c: c.type == ChannelType.GUILD_TEXT, channels))
        voice_channels = list(filter(lambda c: c.type == ChannelType.GUILD_VOICE, channels))

        # statuses = defaultdict(int)
        # for m in ctx.guild.members.values():
        #     statuses[m.presence.visible_status.value] += 1

        embed = (
            hikari.Embed(
                title="Server information",
                description=f"Displaying information for {ctx.guild.name}.",
                colour=owner.top_role.colour,
                timestamp=dt.datetime.now().astimezone(),
            )
            .set_author(name="Information")
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
            .set_thumbnail(ctx.guild.icon_url)
            .add_field(name="ID", value=ctx.guild.id)
            .add_field(name="Owner", value=owner.mention, inline=True)
            .add_field(name="Top role", value=ctx.guild.get_role(list(ctx.guild.roles)[-1]).mention, inline=True)
            .add_field(name="Members", value=f"{ctx.guild.member_count:,}", inline=True)
            .add_field(name="Bans", value=f"{len(await ctx.bot.rest.fetch_bans(ctx.guild)):,}", inline=True)
            .add_field(name="Roles", value=len(ctx.guild.roles) - 1, inline=True)
            .add_field(name="Text channels", value=f"{len(text_channels):,}", inline=True)
            .add_field(name="Voice channels", value=f"{len(voice_channels):,}", inline=True)
            .add_field(name="Invites", value=f"{len(ctx.bot.cache.get_invites_view_for_guild(ctx.guild)):,}", inline=True)
            .add_field(name="Emojis", value=f"{len(ctx.guild.emojis):,}", inline=True)
            # .add_field(name="Boosts", value=f"{len(ctx.guild.emojis):,}", inline=True)
            .add_field(
                name="Created on",
                value=f"<t:{created_at}:d> (<t:{created_at}:R>)",
                inline=False
            )
            .add_field(
                name="Joined on",
                value=f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
                inline=False
            )
            # .add_field(
            #     name="Statuses",
            #     value=(
            #         f"🟢 {statuses[0]} "
            #         f"🟠 {statuses[1]} "
            #         f"🔴 {statuses[2]} "
            #         f"⚪ {statuses[3]}"
            #     ),
            #     inline=False
            # )
        )

        await ctx.respond(embed)


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())


def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")
