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
        return urllib.request.urlopen(WebStatus.URL_TO).headers['Last-Modified']

    
    # Check if it's updated
    def check_if_updated():
        current_date = date.today()
        header_date_syntax = "%d %b %Y"
        return True if current_date.strftime(header_date_syntax) in WebStatus.last_modified() else False
    
    # Download pdf
    def download(path):
        try:
            open_page = urllib.request.urlopen(WebStatus.URL_TO)
            file = open(path, 'wb')
            file.write(open_page.read())
            file.close()
        except Exception as e:
            print(f"Error occurred: {e}")
    
    # Remove file from working directory
    async def remove_file():
        pwd = os.getcwd()
        try:

            for item in pwd:
                if item.endswith('.pdf') or item.endswith('.jpg'):
                    os.remove(os.path.join(pwd, item))

        except Exception as e:
            print(f"Error occurred: {e}")
           
              
def setup(bot: commands.Bot):
    bot.add_cog(WebStatus(bot))
