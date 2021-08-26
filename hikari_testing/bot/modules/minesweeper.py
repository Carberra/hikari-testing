import asyncio
import random

import hikari
import tanjun
from hikari.interactions.base_interactions import ResponseType
from hikari.messages import ButtonStyle

from hikari_testing.bot.client import Client

component = tanjun.Component()


@component.with_slash_command
@tanjun.with_int_slash_option("bombs", "The number of bombs.")
@tanjun.as_slash_command("minesweeper", "Play a game of Minesweeper.")
async def command_minesweeper(ctx: tanjun.abc.Context, bombs: int) -> None:
    board = random.sample([0, 1], counts=[25 - bombs, bombs], k=25)
    rows = []
    i = 0

    for row in range(5):
        row = ctx.rest.build_action_row()

        for col in range(5):
            (
                row.add_button(ButtonStyle.SECONDARY, f"{i}")
                .set_label(f"{board[i]}")
                .add_to_container()
            )
            i += 1

        rows.append(row)

    await ctx.respond("Welcome to Minesweeper!", components=rows)

    while True:
        try:
            event = await ctx.client.events.wait_for(hikari.InteractionCreateEvent, timeout=60)
        except asyncio.TimeoutError:
            await ctx.edit_initial_response("Your game was timed out.", components=[])
        else:
            number = int(event.interaction.custom_id)
            if board[number] == 1:
                components = (await ctx.fetch_initial_response()).components
                print(len(components))
                component = components[number]
                print(component)
                await ctx.edit_initial_response("Game over!")
                await event.interaction.create_initial_response(
                    ResponseType.DEFERRED_MESSAGE_UPDATE,
                )
                return

            # surrounding = (number - 6, number - 5, number - 4, number - 1, number + 1, number + 4, number + 5, number + 6)
            # for n in surrounding:
            #     if not 0 <= n <= 24:
            #         continue

            #     if board[n] == 0:
            #         pass

            # await ctx.edit_initial_response(f"Bombs: {bombs}")
            await event.interaction.create_initial_response(
                ResponseType.DEFERRED_MESSAGE_UPDATE,
            )


@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())
