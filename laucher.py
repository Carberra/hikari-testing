import os

from hikari_testing import __version__
from hikari_testing.bot import Bot

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    bot = Bot()
    bot.run()
