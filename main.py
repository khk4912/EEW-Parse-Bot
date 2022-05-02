import discord
from discord.ext import commands

from CONSTANT import TOKEN


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=discord.Intents.default(),
        )

    async def on_ready(self) -> None:
        print(f"{self.user}로 로그인 완료!")

    async def setup_hook(self) -> None:
        await self._load_cogs()

    async def _load_cogs(self) -> None:
        await self.load_extension("cogs.pews")


bot = Bot()
bot.run(TOKEN)
