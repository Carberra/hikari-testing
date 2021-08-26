import typing as t
from pathlib import Path

import tanjun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

_ClientT = t.TypeVar("_ClientT", bound="Client")


class Client(tanjun.Client):
    __slots__ = tanjun.Client.__slots__ + ("scheduler",)

    def __init__(self: _ClientT, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

    def load_modules(self: _ClientT) -> _ClientT:
        return super().load_modules(
            *[
                f"hikari_testing.bot.modules.{m.stem}"
                for m in Path(__file__).parent.glob("modules/*.py")
            ]
        )
        # Fixed in #55, need to wait until @task/components is merged.
        # return super().load_modules(*Path(__file__).parent.glob("modules/*.py"))
