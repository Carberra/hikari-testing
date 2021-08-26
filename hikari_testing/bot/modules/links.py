import asyncio
import random

import hikari
import tanjun
from hikari.interactions.base_interactions import ResponseType

from hikari_testing.bot.client import Client

component = tanjun.Component()

LINKS = (
    "Docs",
    "Donate",
    "GitHub",
    "Instagram",
    "LBRY",
    "Patreon",
    "Plans",
    "Twitch",
    "Twitter",
    "YouTube",
)


@component.with_slash_command
@tanjun.with_str_slash_option("name", "The link to show.", choices=(l.lower() for l in LINKS))
@tanjun.as_slash_command("link", "Show a specific Carberra link.")
async def command_link(ctx: tanjun.abc.Context, name: str) -> None:
    await ctx.respond(f"<https://{name}.carberra.xyz>")


@component.with_slash_command
@tanjun.as_slash_command("links", "Show all Carberra links.")
async def command_links(ctx: tanjun.abc.Context) -> None:
    select_menu = (
        ctx.rest.build_action_row()
        .add_select_menu("link_select")
        .set_placeholder("Choose a link")
    )

    for option in LINKS:
        select_menu.add_option(option, option.lower()).add_to_menu()

    await ctx.respond(
        "Select a link from the dropdown:",
        component=select_menu.add_to_container(),
    )

    try:
        event = await ctx.client.events.wait_for(hikari.InteractionCreateEvent, timeout=60)
    except asyncio.TimeoutError:
        # select_menu = select_menu.set_is_disabled(True)
        await ctx.edit_initial_response("Timed out.", components=[])
        # await ctx.delete_initial_response()
    else:
        await ctx.edit_initial_response(
            f"<https://{event.interaction.values[0].lower()}.carberra.xyz>",
            components=[],
        )


@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())
