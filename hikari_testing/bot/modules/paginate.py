import asyncio

import hikari
import tanjun
from hikari.interactions.base_interactions import ResponseType
from hikari.messages import ButtonStyle

from hikari_testing.bot.client import Client

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("paginate", "Paginate through a list of options!")
async def command_paginate(ctx: tanjun.abc.Context) -> None:
    values = ("Page 1", "Page 2", "Page 3", "Page 4", "Page 5", "Page 6")
    index = 0

    button_menu = (
        ctx.rest.build_action_row()
        .add_button(ButtonStyle.SECONDARY, "<<")
        .set_label("<<")
        .add_to_container()
        .add_button(ButtonStyle.PRIMARY, "<")
        .set_label("<")
        .add_to_container()
        .add_button(ButtonStyle.PRIMARY, ">")
        .set_label(">")
        .add_to_container()
        .add_button(ButtonStyle.SECONDARY, ">>")
        .set_label(">>")
        .add_to_container()
    )

    await ctx.respond(values[0], component=button_menu)

    while True:
        try:
            event = await ctx.client.events.wait_for(hikari.InteractionCreateEvent, timeout=60)
        except asyncio.TimeoutError:
            await ctx.edit_initial_response("Timed out.", components=[])
        else:
            if event.interaction.custom_id == "<<":
                index = 0
            elif event.interaction.custom_id == "<":
                index = (index - 1) % len(values)
            elif event.interaction.custom_id == ">":
                index = (index + 1) % len(values)
            elif event.interaction.custom_id == ">>":
                index = len(values) - 1

            await ctx.edit_initial_response(values[index])
            await event.interaction.create_initial_response(
                ResponseType.DEFERRED_MESSAGE_UPDATE,
                values[index]
            )


@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())
