import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import fitz
from datetime import datetime, timedelta
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  

class Volunteer:
    def __init__(self, username):
        self.username = username
        self.role = []
        self.time = []

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Running!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command()
async def schedule(ctx, inputDate=None):
    lines = []
    list_of_volunteers = []
    i = 0

    if inputDate:
            try:
                targetDate = datetime.strptime(inputDate, '%Y-%m-%d').date()
            except:
                    await ctx.send("Incorrect format for date. Please send it in YYYY-MM-DD format. (EX: 2025-07-07)")
                    return
    else:
            await ctx.send("No date provided. Will use today's date as default.")
            targetDate = datetime.now().date()   

    now = datetime.now()  

    if not ctx.message.attachments:
        await ctx.send("Please attach the schedule in PDF format.")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.content_type or not attachment.content_type.startswith("application/pdf"):
        await ctx.send("This is not the schedule. Please check your attachment again.")
        return

    filename = f"./{attachment.filename}"
    await attachment.save(filename)
    await ctx.send("Schedule has been saved!")

    doc = fitz.open(filename)
   
    for page_num, page in enumerate(doc):
        await ctx.send("Now processing schedule....")
        text = page.get_text()
        lines += text.strip().split("\n")

        increment = 0

        while (increment < len(lines)/18 - 1):
            volunteer = {
                lines[0]: lines[18 + (18 * increment)],
                lines[1]: lines[19 + (18 * increment)],
                lines[2]: lines[20 + (18 * increment)],
                lines[3]: lines[21 + (18 * increment)],
                lines[4]: lines[22 + (18 * increment)],
                lines[5]: lines[23 + (18 * increment)],
                lines[6]: lines[24 + (18 * increment)],
                lines[7]: lines[25 + (18 * increment)],
                lines[8]: lines[26 + (18 * increment)],
                lines[9]: lines[27 + (18 * increment)],
                lines[10]: lines[28 + (18 * increment)],
                lines[11]: lines[29 + (18 * increment)],
                lines[12]: lines[30 + (18 * increment)],
                lines[13]: lines[31 + (18 * increment)],
                lines[14]: lines[32 + (18 * increment)],
                lines[15]: lines[33 + (18 * increment)],
                lines[16]: lines[34 + (18 * increment)],
                lines[17]: lines[35 + (18 * increment)],
            }
            list_of_volunteers.append(volunteer)
            increment = increment + 1

    doc.close()


    await ctx.send("Done. Scheduled messages will be sent out on the inputted date.")

    for vol in list_of_volunteers:
        increment = 2
        while (increment < 18):
            if (vol[lines[increment]] != 'N/A'):
                if increment == 2:
                     target = datetime.combine(targetDate, datetime.min.time()) - timedelta(days=1)
                     target = target.replace(hour = 20, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()      
                elif increment == 3:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 10, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()                    
                elif increment == 4:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 11, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 5:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 12, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 6:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 13, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 7:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 14, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 8:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 15, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 9:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 16, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 10:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 17, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 11:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 18, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 12:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 19, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 13:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 20, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 14:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 21, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 15:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 22, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 16:
                     target = datetime.combine(targetDate, datetime.min.time())
                     target = target.replace(hour = 23, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()
                elif increment == 17:
                     target = datetime.combine(targetDate, datetime.min.time()) + timedelta(days=1)
                     target = target.replace(hour = 0, minute = 0, second = 0, microsecond=0)
                     delay = (target - now).total_seconds()

                asyncio.create_task(send_message(ctx, vol, delay, increment, lines))
                
            increment = increment + 1

            
       
                      
                  
    

async def send_message(ctx, volunteer, hour, int, lines):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=volunteer[lines[1]])
    await asyncio.sleep(hour)
    if member:
        await ctx.send(f"Hey, {member.mention}! You're on shift as {volunteer[lines[int]]}! Please be on time for your shift.")
    else:
        await ctx.send(f"Hey, {volunteer[lines[1]]}! You're on shift as {volunteer[lines[int]]}! Please be on time for your shift.")

async def send_message_daybefore(ctx, volunteer, hour, int):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=volunteer[1])
    await asyncio.sleep(hour)
    if member:
        await ctx.send(f"Hey, {member.mention}! You're on shift for set up the day before the event at 8pm. Please be on time for your shift.")
    else:
        await ctx.send(f"Hey, {volunteer.username}! You're on shift for set up the day before the event at 8pm. Please be on time for your shift.")
        
bot.run(os.getenv('DISCORD_TOKEN'))
