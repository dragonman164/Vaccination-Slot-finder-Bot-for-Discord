import discord
from discord.ext import commands
import datetime
import json
import requests
import time 

hour = datetime.datetime.now().hour
client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    print("Bot is Ready")

@client.command(name='greet')
async def greet(ctx):
    if hour < 12:
        await ctx.send(f"Good Morning, {ctx.message.author.mention}")
    
    elif hour >= 12 and hour < 16:
        await ctx.send(f"Good Afternoon, {ctx.message.author.mention}")
    
    elif hour >=16 and hour < 20: 
        await ctx.send(f"Good Evening, {ctx.message.author.mention}")
    
    else:
        await ctx.send(f"Good Night, {ctx.message.author.mention}")

  

@client.command(name='slots')
async def vaccineSlots(ctx,pincode,age):
    
    await ctx.send(f"Showing you vaccination slots for pincode: {pincode} and age: {age} for next 10 days")
    headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    slot = 0
    for i in range(10):
        day = (datetime.date.today() + datetime.timedelta(i)).day
        month = (datetime.date.today() + datetime.timedelta(i)).month
        year = (datetime.date.today() + datetime.timedelta(i)).year
        slot = 0
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={day:02}-{month:02}-{year}"
        response = requests.request("GET", url, headers=headers)
        vaccineCenters = json.loads(response.text)
        await ctx.send(f"Date:{day:02}-{month:02}-{year}\n")
        for vaccineCenter in vaccineCenters['sessions']:
            if vaccineCenter['min_age_limit'] <=int(age) and vaccineCenter['available_capacity'] > 0:
                slot += 1
                await ctx.send(f"```Name:{vaccineCenter['name']}\nAddress:{vaccineCenter['address']}\nState:{vaccineCenter['state_name']}\nDistrict:{vaccineCenter['district_name']}\nVaccine:{vaccineCenter['vaccine']}\nSlots:{vaccineCenter['slots']}\nAge Limit : {vaccineCenter['min_age_limit']}\n\n```")
    
        time.sleep(2)
        if slot == 0:
            await ctx.send("```No Slots Available for the Day```")
    



@client.event
async def on_command_error(ctx,err):
    await ctx.send("Sorry! I didn't undertstand that")
    await ctx.send("```Help : To greet you type: '?greet' \nTo check vaccination slots type: '?slots pincode age' ```")


## Put your bot token here
client.run('Nzc0OTE5ODU4MjEwOTk2MjY2.X6eyWw.X_KtaNVSgqP26HbcvFqEhl9uK-E')