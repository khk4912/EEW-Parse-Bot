from datetime import datetime
import discord
import asyncio
import inspect
from discord import app_commands
from discord.ext import commands

from async_pews import PEWSClient, EEWInfo
from CONSTANT import CHANNEL_ID

MMI_CLASS = ["", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ+"]


class PEWS(commands.Cog, PEWSClient):
    def __init__(self, bot: commands.Bot, is_sim: bool = False):
        PEWSClient.__init__(self, is_sim)
        self.bot = bot

    async def on_new_eew_info(self, eew_info: EEWInfo):
        channel = self.bot.get_channel(CHANNEL_ID)
        assert isinstance(channel, discord.TextChannel)

        embed = discord.Embed(
            title="⚠ 새로운 지진속보 발생!",
            description=f"{eew_info.eqk_str}",
            color=discord.Color.red(),
        )
        embed.add_field(name="추정규모", value=f"M{eew_info.mag}")
        embed.add_field(name="위치", value=f"{eew_info.lat}, {eew_info.lon}")
        embed.add_field(
            name="예상최대진도",
            value=f"{MMI_CLASS[eew_info.max_intensity]} ({', '.join(eew_info.max_area)})",
            inline=False,
        )
        embed.add_field(
            name="주요 지점 도달 예상시각",
            value=f"서울시 동작구: {int((eew_info.est_time(37.512462,126.939485) - datetime.now()).total_seconds())}초 후\n",
            inline=False,
        )
        embed.add_field(
            name="주요 지점 예상진도",
            value=f"서울시 동작구: {MMI_CLASS[eew_info.est_mag(37.512462,126.939485)]}",
            inline=False,
        )
        embed.set_footer(text="사용자 맞춤형 지진정보서비스")
        await channel.send(embed=embed)

    @app_commands.command(name="status")
    async def wrapper_test(self, interaction: discord.Interaction):
        await interaction.response.send_message("This is status!")


async def setup(bot: commands.Bot):
    cog = PEWS(bot, is_sim=True)

    asyncio.create_task(cog._looper())

    await bot.add_cog(cog)
