
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from yt_dlp.networking.impersonate import ImpersonateTarget
import subprocess
import os
#from config import api_id,api_hash,bot_token

api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
bot_token = os.environ.get("bot_token")

bot = Client("Bot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)



@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(clinet,message):
    await message.reply("Send a Video Url to get its Thumbnail in jpg format!")






@bot.on_message(filters.private & ~filters.command("start"))
async def send_thumbnail(client,message):

    url = message.text
    await message.reply("Downloading the Thumbnail.",quote=True)
    yt_opts = {
        "no_warnings": True,
        "skip_download": True,
        "writethumbnail": True,
        "cookiefile": "cookies.txt",
        
        "impersonate": ImpersonateTarget(client='chrome', version='124'),
        "nocheckcertificate": True,
        "socket_timeout": 10,
        "retries": 3,
        "proxy": "socks5://127.0.0.1:9050",
#        "quiet": True,
        "outtmpl": '%(title)s.%(ext)s',
        "windowsfilenames": False,
        "sleep_interval": 3,
#        "postprocessors": [
#            {
#                'key': "FFmpegThumbnailsConvertor",
#                'format': "jpg",
#                'when': "before_dl",
#                }
#
#            ],
#    'user_agent': 'Mozilla/5.0',    
        }
            
    

    with YoutubeDL(yt_opts) as yt:
#        yt.download([url])
        info = yt.extract_info(url,download=True)
#        filename = f"/data/data/com.termux/files/home/code/Telegram/{info['title']}.jpg"

        filename = f"{info['title']}.jpg"
        print("HERE IS THE FILE NAME ",filename)


    
    await bot.send_photo(message.chat.id, filename)

    os.remove(filename)

print("Starting the bot")
bot.run()

