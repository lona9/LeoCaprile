from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType
from discord.ext.commands import command
import os

class Tareas(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(name="tarea", aliases=["t"])
  async def tarea(self, ctx, *args):
    if args == ():
      await ctx.channel.send("¡Debes escribir una tarea!")
    else:
      tarea = " ".join(args)
      f = open('/root/leocaprile/data/pendientes.txt', 'a')
      f.write("\n" + tarea)
      f.close()
      await ctx.channel.send("Tarea agregada.")

  @command(aliases=["p"])
  async def pendientes(self, ctx):
    with open('/root/leocaprile/data/pendientes.txt') as f:
      tareas = f.read().splitlines()
      if os.stat("/root/leocaprile/data/pendientes.txt").st_size == 0:
        await ctx.channel.send("No hay tareas pendientes.")
      else:
        for tarea in tareas:
          if tarea == '':
            pass
          else:
            msg = await ctx.channel.send(tarea)
            await msg.add_reaction("✅")


  @Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.member.bot:
      pass

    else:
      if payload.emoji.name == "✅":
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        content = message.content

        check_task = content + " ✅"

        f = open('/root/leocaprile/data/terminados.txt', 'a')
        f.write(check_task + "\n")
        f.close()

        with open("/root/leocaprile/data/pendientes.txt", "r") as f:
          lines = f.readlines()
        with open("/root/leocaprile/data/pendientes.txt", "w") as f:
          for line in lines:
            if line.strip("\n") != message.content:
              f.write(line)


  @command(aliases=["terminados", "done", "l"])
  async def listos(self, ctx):
    with open("/root/leocaprile/data/terminados.txt", "r") as f:
      terminadas = f.read()
      if os.stat("/root/leocaprile/data/terminados.txt").st_size == 0:
        await ctx.channel.send("No hay tareas terminadas.")
      else:
        await ctx.channel.send(terminadas)

  @command(aliases=["lc"])
  async def clear(self, ctx):
    open("/root/leocaprile/data/terminados.txt", "w").close()
    await ctx.channel.send("¡Terminados limpio!")

  @command(aliases=["pc"])
  async def pclear(self, ctx):
    open("/root/leocaprile/data/pendientes.txt", "w").close()
    await ctx.channel.send("¡Pendientes limpio!")

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("tareas")

def setup(bot):
  bot.add_cog(Tareas(bot))
