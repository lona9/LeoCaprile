from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import command
from datetime import datetime
from discord.ext import tasks
from datetime import timedelta
from..db import db
import random
import pandas as pd

class Reminders(Cog):
  def __init__(self, bot):
    self.bot = bot

  @command(aliases=["r"])
  async def set_reminder(self, ctx, time, *args):
      time_conversion = {"s": 1, "m": 60, "h": 3600, "d": 86400}
      raw_time = int("".join([x for x in time if x.isdigit()]))
      time_unit = time[-1]
      time_to_add = raw_time * time_conversion[time_unit]

      remindertext = str(" ".join(args))

      reminder_time = datetime.now() + timedelta(seconds=time_to_add)
      print(reminder_time)

      rm_id = random.randint(1, 10000)

      db.execute("INSERT OR IGNORE INTO reminders (ReminderID, ReminderTime) VALUES (?, ?)", rm_id, reminder_time)

      db.commit()

      await ctx.send(f"Te recordaré de {remindertext} en {time}.")

      self.check_reminder.start(ctx, rm_id, remindertext)


  @tasks.loop(seconds = 10)
  async def check_reminder(self, ctx, rm_id, remindertext):

    time_to_check = db.record("SELECT ReminderTime FROM reminders WHERE ReminderID = ?", rm_id)

    time_to_check = pd.to_datetime(time_to_check)

    if time_to_check > datetime.now():
        pass
    else:
        await ctx.send(f"<@485054727755792410>: acuérdate de {remindertext}!")

        db.execute("DELETE FROM reminders WHERE ReminderID = ?", rm_id)

        db.commit()

        self.check_reminder.stop()

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("reminders")

def setup(bot):
  bot.add_cog(Reminders(bot))
