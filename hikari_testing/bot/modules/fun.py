import random

import hikari
import tanjun

from hikari_testing.bot.client import Client

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("hello", "Say hello!")
async def command_hello(ctx: tanjun.abc.Context) -> None:
    greeting = random.choice(("Hello", "Hi", "Hey"))
    await ctx.respond(f"{greeting} {ctx.member.mention}!", user_mentions=True)


@component.with_slash_command
@tanjun.with_int_slash_option("number", "The number of dice to roll (max: 25).")
@tanjun.with_int_slash_option("sides", "The number of sides each die will have.", default=6)
@tanjun.with_int_slash_option("bonus", "A fixed number to add to the total roll.", default=0)
@tanjun.as_slash_command("dice", "Roll one or more dice.")
async def command_dice(ctx: tanjun.abc.Context, number: int, sides: int, bonus: int) -> None:
    if number > 25:
        await ctx.respond("No more than 25 dice can be rolled at once.")
        return

    if sides > 100:
        await ctx.respond("The dice cannot have more than 100 sides.")
        return

    rolls = [random.randint(1, sides) for i in range(number)]
    await ctx.respond(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )


@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())
