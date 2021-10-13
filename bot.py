from logging import exception
import discord
from discord.ext import commands, tasks

import os
import urllib.request, urllib.parse
from dotenv import load_dotenv
from datetime import date, datetime

#Init
client = discord.Client()
bot = commands.Bot(command_prefix='-')


#Store current date in variable
current_date = date.today()
today_date_header = current_date.strftime("%d %b %Y") #header syntax
today_date = current_date.strftime("%d-%m-%Y")

URL_TO = "http://wt.ajp.edu.pl/images/Plany/II_rok_E-MiBM-I-AiR.pdf"
file_name = "Schedule_" + today_date + ".pdf"
path = file_name


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
        return "error 404"

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



#Login
@client.event
async def on_ready():
    print('Logged in as {0.user}!'.format(client))



#Task that will at least run once every day
@tasks.loop(hours=8)
async def run_daily_verify():

    current_time = datetime.now()
    today_time = current_time.strftime("%d/%m/%Y %H:%M:%S")

    status_page = check_status(URL_TO)
    header_get = last_modified(URL_TO, status_page)
    check_if_updated = verify(header_get)

    if status_page == True and check_if_updated == True:
        print("Update occurred on:" + header_get)
        download(URL_TO)
        
        try:
            channel = client.get_channel(897232495244881961) #Schedule channel
            await channel.send(file=discord.File(path))
            await remove_file(path)
        except Exception as e:
            print(f"Error occured: {e}")
        
    elif check_if_updated != True:
        print("No update: " + today_time)
    
    else:
        print("Could not find specified page")


#Execute command
@client.event
async def on_message(mssg):
    
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Hentai"))

    if mssg.content.startswith('-check'): #manual verification
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
        await mssg.channel.send("Schedule last updated on: " + header_get)
    
    else:
        return "Error occured"

run_daily_verify.start()

load_dotenv()

client.run(os.getenv("DISCORD_TOKEN"))