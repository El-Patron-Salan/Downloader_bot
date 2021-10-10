import discord
import os
import urllib.request
from datetime import date

#Store current date in variable
current_date = date.today()
today_date_header = current_date.strftime("%d %b %Y") #header syntax
today_date = current_date.strftime("%d-%m-%Y")

URL_TO = "http://wt.ajp.edu.pl/images/Plany/II_rok_E-MiBM-I-AiR.pdf"
file_name = "Schedule_" + today_date + ".pdf"
path = "/mnt/For_linux_use/Discord_bots/Downloader_bot/" + file_name


client = discord.Client()

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
        return "Currently page is down"



#Check if header has been updated based on current date
def verify(response_page, url):
    if today_date_header in response_page:
        response = urllib.request.urlopen(url)    
        file = open("Schedule_" + today_date + ".pdf", 'wb')
        file.write(response.read())
        file.close()
    else:
        return 

#Login
@client.event
async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

#Execute command
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('-check'):
        status_page = check_status(URL_TO)
        header_get = last_modified(URL_TO, status_page)
        verify(header_get, URL_TO)
        await message.channel.send(file=discord.File(path))

client.run(os.getenv('DISCORD_TOKEN'))
        