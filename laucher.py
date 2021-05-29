import os

from testbot import __version__
from testbot.bot import Bot

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    bot = Bot()
    bot.run()
