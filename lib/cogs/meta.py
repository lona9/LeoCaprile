from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType
from discord.ext.commands import command

class Meta(Cog):
  def __init__(self, bot):
    self.bot = bot

    self.message = "Watching La Vega"

  async def set(self):
    _type, _name = self.message.split(" ", maxsplit=1)

    await self.bot.change_presence(activity=Activity(
      name=_name, type=getattr(ActivityType, _type, ActivityType.watching)
    ))

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("meta")

def setup(bot):
  bot.add_cog(Meta(bot))