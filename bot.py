import discord
from discord.ext import commands, tasks

import os
import urllib.request, urllib.parse
from dotenv import load_dotenv
from datetime import date

client = discord.Client()
bot_args = commands.Bot(command_prefix='-')

#Store current date in variable
current_date = date.today()
today_date_header = current_date.strftime("%d %b %Y") #header syntax
today_date = current_date.strftime("%d-%m-%Y")

URL_TO = "http://wt.ajp.edu.pl/images/Plany/II_rok_E-MiBM-I-AiR.pdf"
channel_id = client.get_channel(897232495244881961)
file_name = "Schedule_" + today_date + ".pdf"
path = file_name



client = discord.Client()
bot_args = commands.Bot(command_prefix='-')

#Check if website is online
def check_status(url):
    if urllib.request.urlopen(url).getcode() == 200:
        return True
    else:
        return False

#Check last modified date from HTML header
def last_modified(url, status):
    if status == True:
        response = urllib.request.urlopen(url)
        return response.headers['Last-Modified']
    else:
        return "Could not find page"

#Check if header has been updated based on current date
def verify(response_page):
    if today_date_header in response_page:
        return True
    else:
        return False

def download(url):
    response = urllib.request.urlopen(url)    
    file = open("Schedule_" + today_date + ".pdf", 'wb')
    file.write(response.read())
    file.close()

async def remove_file(given_path):
    os.remove(given_path)


status_page = check_status(URL_TO)
header_get = last_modified(URL_TO, status_page)
check_if_updated = verify(header_get)


@tasks.loop(hours=12)

#Login
@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client))


#Execute command
@client.event
async def on_message(mssg):
    
    if mssg.content.startswith('-check'):
        if check_if_updated == True:
            download(URL_TO)
            await mssg.channel.send(file=discord.File(path))
            await remove_file(path)
        else:
            await mssg.channel.send("No updates")
    

    elif mssg.content.startswith('-show'):
        download(URL_TO)
        await mssg.channel.send(file=discord.File(path))
        await remove_file(path)


    elif mssg.content.startswith('-last'):
        await mssg.channel.send("Schedule last updated in: " + header_get)
    

    else:
        return "Error occured"

load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
