import discord
import os
import urllib.request
from datetime import date

URL_TO = "http://wt.ajp.edu.pl/images/Plany/II_rok_E-MiBM-I-AiR.pdf"
current_date = date.today()

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

#Store current date in variable
today_date = current_date.strftime("%d %b %Y")

#Check if header has been updated based on current date
def verify(response_page, url):
    if today_date in response_page:
        response = urllib.request.urlopen(url)    
        file = open("Schedule_" + today_date + ".pdf", 'wb')
        file.write(response.read())
        file.close()
    else:
        return "No update"

@client.event
async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

@client.event