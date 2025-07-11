import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import fitz
from datetime import datetime, timedelta
import asyncio
import webserver

load_dotenv()
TOKEN = os.environ['discordkey']

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
    schedule_list = []
    list_of_volunteers = []
    i = 0
    chunk_size = 18

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

    doc.close()

 
    while (i < len(lines)):
        chunk = lines[i:i + chunk_size]
        i = i + 18
        if len(chunk) == chunk_size:
            schedule_list.append(chunk)

    
    for row in schedule_list:
        v = Volunteer(row[1])
        
        for x in range(2, 18):
            if row[x] != 'N/A':
                v.role.append(row[x])
                if x == 2:
                    v.time.append(2) 
                elif x == 3:
                    v.time.append(10)     
                elif x == 4:
                    v.time.append(11)
                elif x == 5:
                    v.time.append(12)
                elif x == 6:
                    v.time.append(13)
                elif x == 7:
                    v.time.append(14)
                elif x == 8:
                    v.time.append(15)
                elif x == 9:
                    v.time.append(16)
                elif x == 10:
                    v.time.append(17)
                elif x == 11:
                    v.time.append(18)
                elif x == 12:
                    v.time.append(19)
                elif x == 13:
                    v.time.append(20)
                elif x == 14:
                    v.time.append(21)
                elif x == 15:
                    v.time.append(22)
                elif x == 16:
                    v.time.append(23)
        
        list_of_volunteers.append(v)

    await ctx.send("Done. Scheduled messages will be sent out on the inputted date.")

    list_of_volunteers_no_header = list_of_volunteers[1:]  
    for vol in list_of_volunteers_no_header:
        x = 0
        while (x < len(vol.role)):
            if (vol.time[x] == 2): 
                target = datetime.combine(targetDate, datetime.min.time())
                reminder = target - timedelta(days=1)
                reminder = reminder.replace(hour=20, minute = 0, second = 0, microsecond=0)
                delay = (reminder - now).total_seconds()
                asyncio.create_task(send_message_daybefore(ctx, vol, delay, x))
                
            else:
                target = datetime.combine(targetDate, datetime.min.time())
                target = target.replace(hour=vol.time[x], minute = 0, second = 0, microsecond=0)
                delay = (target - now).total_seconds()
                asyncio.create_task(send_message(ctx, vol, delay, x))
            

            x = x+1

async def send_message(ctx, volunteer, hour, int):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=volunteer.username)
    await asyncio.sleep(hour)
    if member:
        await ctx.send(f"Hey, {member.mention}! You're on shift as {volunteer.role[int]}! Please be on time for your shift.")
    else:
        await ctx.send(f"Hey, {volunteer.username}! You're on shift as {volunteer.role[int]}! Please be on time for your shift.")

async def send_message_daybefore(ctx, volunteer, hour, int):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=volunteer.username)
    await asyncio.sleep(hour)
    if member:
        await ctx.send(f"Hey, {member.mention}! You're on shift for set up the day before the event. Please be on time for your shift.")
    else:
        await ctx.send(f"Hey, {volunteer.username}! You're on shift for set up the day before the event. Please be on time for your shift.")
        
webserver.keep_alive()
bot.run(TOKEN)
