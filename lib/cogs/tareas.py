from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import command
from datetime import datetime
from discord.ext import tasks
from discord.utils import get
from..db import db

class Tareas(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(aliases=["t"])
  async def set_task(self, ctx, *args):

      print(args)

      if args == ():
          await ctx.send("Mensaje inválido!")

      elif args[0] in ["corner", "super"]:
          if len(args) == 1:
              await ctx.send("Mensaje inválido!")

          else:
              tasktext = str(" ".join(args[1:]))

              taskid = datetime.now().strftime("%d/%m %H:%M:%S")

              taskstatus = "pending"

              category = args[0]

              db.execute("INSERT OR IGNORE INTO tasks (TaskID, TaskText, TaskStatus, TaskCategory) VALUES (?, ?, ?, ?)", taskid, tasktext, taskstatus, category)

              db.commit()

              await ctx.send(f"Tarea guardada bajo **{category}**.")

      else:
          tasktext = str(" ".join(args))

          taskid = datetime.now().strftime("%d/%m %H:%M:%S")

          taskstatus = "pending"

          category = "Otros"

          db.execute("INSERT OR IGNORE INTO tasks (TaskID, TaskText, TaskStatus, TaskCategory) VALUES (?, ?, ?, ?)", taskid, tasktext, taskstatus, category)

          db.commit()

          await ctx.send(f"Tarea guardada bajo **{category}**.")


  @command(aliases=["p", "pending"])
  async def check_pending(self, ctx, *args):

      pending = "pending"

      if args != ():
          category = str("".join(args))

          await ctx.send(f"**Categoría {category}**")
          pending_tasks = db.column("SELECT TaskText FROM tasks WHERE TaskStatus = ? AND TaskCategory = ?", pending, category)

          for task in pending_tasks:
              try:
                  taskmsg = await ctx.send(task)
                  await taskmsg.add_reaction("✅")
              except:
                  pass

      else:
          categories = db.column("SELECT DISTINCT TaskCategory FROM tasks WHERE TaskStatus = ?", pending)

          if categories == []:
              await ctx.send("No hay tareas pendientes.")

          else:
                    for category in categories:
                        await ctx.send(f"**Categoría {category}**")
                        pending_tasks = db.column("SELECT TaskText FROM tasks WHERE TaskStatus = ? AND TaskCategory = ?", pending, category)

                        for task in pending_tasks:
                            try:
                                taskmsg = await ctx.send(task)
                                await taskmsg.add_reaction("✅")
                            except:
                                pass

  @command(aliases=["l", "listas"])
  async def check_done(self, ctx):
      done = "done"
      categories = db.column("SELECT DISTINCT TaskCategory FROM tasks WHERE TaskStatus = ?", done)

      if categories == []:
          await ctx.send("No hay tareas completadas.")
      else:
          for category in categories:
              await ctx.send(f"**{category} category**")

              done_tasks = db.column("SELECT TaskText FROM tasks WHERE TaskStatus = ? AND TaskCategory = ?", done, category)

              for task in done_tasks:
                  try:
                      taskmsg = await ctx.send(task)
                  except:
                      pass


  @command(aliases=["pc"])
  async def pending_clear(self, ctx):
      pending = "pending"
      db.execute("DELETE FROM tasks WHERE TaskStatus = ?", pending)
      db.commit()
      await ctx.send("Lista de pendientes borrada!")

  @command(aliases=["lc"])
  async def done_clear(self, ctx):
      done = "done"
      db.execute("DELETE FROM tasks WHERE TaskStatus = ?", done)
      db.commit()
      await ctx.send("Lista de completadas borrada!")

  @Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.member.bot:
      pass

    else:
      if payload.emoji.name == "✅":
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        content = message.content

        done = "done"
        db.execute("UPDATE tasks SET TaskStatus = ? WHERE TaskText = ?", done, content)
        db.commit()

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("tareas")

def setup(bot):
  bot.add_cog(Tareas(bot))
