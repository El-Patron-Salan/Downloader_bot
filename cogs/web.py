import discord
from discord.ext import commands


import urllib.request, urllib.parse
from datetime import date
import os

class WebStatus(commands.Cog):

    URL_TO = 'http://wt.ajp.edu.pl/images/Plany/II_rok_E-MiBM-I-AiR.pdf'

    def __init__(self,bot):
        self.bot = bot

    # Check if page is alive
    def page_status():
        return True if urllib.request.urlopen(WebStatus.URL_TO).getcode() == 200 else False
    
    # Get last modified date from header
    def last_modified():
        try:
            return urllib.request.urlopen(WebStatus.URL_TO).headers['Last-Modified']
        except Exception as e:
            print(f"Error occurred: {e}")
    
    # Check if it's updated
    def check_if_updated():
        current_date = date.now()
        header_date_syntax = "%d %b %Y"
        return True if current_date.strftime(header_date_syntax) in WebStatus.last_modified else False
    
    # Download pdf
    def download(name):
        try:
            open_page = urllib.request.urlopen(WebStatus.URL_TO)
            file = open(name)
            file.write(open_page.read())
            file.close()
        except Exception as e:
            print(f"Error occurred: {e}")
    
    # Remove file from working directory
    def remove_file(file_name):
        pwd = os.getcwd()
        try:

            for item in pwd:
                if item.endswith('.pdf') or item.endswith('.jpg'):
                    os.remove(file_name)

        except Exception as e:
            print(f"Error occurred: {e}")
    
    def setup(bot):
        bot.add_cog(WebStatus(bot))
