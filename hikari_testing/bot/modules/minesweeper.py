import asyncio
import random
import typing as t

import hikari
import tanjun
from hikari.interactions.base_interactions import ResponseType
from hikari.messages import ButtonStyle

from hikari_testing.bot.client import Client

component = tanjun.Component()


class Cell:
    __slots__ = ("style", "label", "index")

    def __init__(self, index: int) -> None:
        self.label = " "
        self.style = ButtonStyle.SECONDARY
        self.index = index

    def __str__(self) -> str:
        return self.label

    def __int__(self) -> int:
        return self.index

    def calculate_surrounding(self, n, matrix) -> int:
        b = 0
        surrounding = (n - 6, n - 5, n - 4, n - 1, n + 1, n + 4, n + 5, n + 6)
        for n in surrounding:
            if not 0 <= n <= 24:
                continue

            if matrix[n] == 1:
                b += 1


class Board:
    __slots__ = ("matrix", "rows", "cells")

    def __init__(self, bombs: int) -> None:
        self.matrix = random.sample([0, 1], counts=[25 - bombs, bombs], k=25)
        self.rows = []
        self.cells = []

    def create_rows(self, ctx: tanjun.abc.Context, update=False) -> None:
        i = 0
        self.rows = []

        for row in range(5):
            row = ctx.rest.build_action_row()

            for col in range(5):
                if update:
                    cell = self.cells[i]
                else:
                    cell = Cell(i)
                    self.cells.append(cell)

                (
                    row.add_button(cell.style, f"{i}")
                    .set_label(cell.label)
                    .add_to_container()
                )
                i += 1

            self.rows.append(row)

        return self


@component.with_slash_command
@tanjun.with_int_slash_option("bombs", "The number of bombs.", default=5)
@tanjun.as_slash_command("minesweeper", "Play a game of Minesweeper.")
async def command_minesweeper(ctx: tanjun.abc.Context, bombs: int) -> None:
    board = Board(bombs).create_rows(ctx)
    await ctx.respond("Welcome to Minesweeper!", components=board.rows)

    while True:
        try:
            event = await ctx.client.events.wait_for(hikari.InteractionCreateEvent, timeout=60)
        except asyncio.TimeoutError:
            await ctx.edit_initial_response("Your game was timed out.", components=[])
        else:
            if not isinstance(event, hikari.ComponentInteraction):
                continue

            number = int(event.interaction.custom_id)
            message = await ctx.fetch_last_response()
            buttons = [b for row in message.components for b in row.components]

            if board.matrix[number] == 1:
                for i, value in enumerate(board.matrix):
                    if value == 1:
                        board.cells[i].style = ButtonStyle.DANGER
                        board.cells[i].label = "💣"

                await ctx.edit_initial_response("Game over!", components=board.create_rows(ctx, update=True).rows)

            else:
                b = board.cells[number].calculate_surrounding(number, board.matrix)
                if board.matrix[number] == 0:
                    board.cells[number].style = ButtonStyle.PRIMARY
                    board.cells[number].label = f"{b}"
                    await ctx.edit_initial_response("Welcome to Minesweeper!", components=board.create_rows(ctx, update=True).rows)

            # await ctx.edit_initial_response(f"Bombs: {bombs}")
            await event.interaction.create_initial_response(
                ResponseType.DEFERRED_MESSAGE_UPDATE,
            )


@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())
