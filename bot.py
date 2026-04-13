#import sys
#import logging

# Set up logging to send output to stdout immediately
#logging.basicConfig(
#    level=logging.INFO,
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#    handlers=[logging.StreamHandler(sys.stdout)] 
#)

from urllib.parse import urlparse
import subprocess
def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Testing it

from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from yt_dlp.networking.impersonate import ImpersonateTarget
#from yt_dlp.networking.impersonate import ImpersonateTarget
import subprocess
import os

api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
bot_token = os.environ.get("bot_token")


bot = Client("Bot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)


admin_ids = [8063495170]
path = "downloads"



from PIL import Image

def get_thumbnail(filename, thumb):
    print(filename)
    subprocess.run(["ffmpeg","-i", filename,"-ss", "00:00:01.000","-vframes", "1",thumb])



def get_size(thumb):
    img = Image.open(thumb)
    img.thumbnail((320,320))
    img.save(thumb)
    return img.size






@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(clinet,message):
    await message.reply("Send a Url to download the video")






@bot.on_message(filters.private & ~filters.command("start"))
async def send_video(client,message):
    print(is_url(message.text))
    if message.from_user.id in admin_ids:
        if is_url(message.text) :
            url = message.text
            await message.reply("Downloading the Video...",quote=True)
            yt_opts = {
#               "format" : "bestvideo+bestaudio/best",
                "format": "best",
                "no_warnings": True,
                "outtmpl": '%(title)s.%(ext)s',
                "merge_output_format": 'mp4',
                "windowsfilenames": False,
                'impersonate': ImpersonateTarget(client='chrome', version='136', os=None, os_version=None),
                "fragment_retries": 10,
                "sleep_interval": 3,
                "nocheckcertificate": True,
                "socket_timeout": 60,
                "retries": 10, 
#                "cookiefile": 'cookies.txt',
#                "proxy": "socks5://127.0.0.1:9050",
                }


            with YoutubeDL(yt_opts) as yt:
#                yt.download([url])
                info = yt.extract_info(url,download=True)
                duration = int(info.get('duration',0))
                filename = f"{info['title']}.mp4"
                thumb = f"{info['title']}.jpg"
                get_thumbnail(filename,thumb)
                width, height = get_size(thumb)
                caption = filename
                print(f"\nHERE IS THE FILE NAME {filename}\n")
                await message.reply(f"Sending: {filename}")
                await bot.send_video(
                    message.chat.id,
                    filename,
                    duration=duration,
                    thumb=thumb,
                    width=width,
                    height=height,
                    caption=caption,
                )
                print('SENT SUCCESSFULLY')
                os.remove(filename)
                os.remove(thumb)
                if os.path.exists(filename):
                    await message.reply(f"{filename} Still exist.")
                
                elif not os.path.exists(filename):
                    await message.reply(f"{filename} Does not exist.")

                    
        else:
            await message.reply("Please send a valid URL.")
    else:
        await message.reply("You are not Authorised to use this bot.\n Please ask admins for help.")

#    await bot.send_vidro(message.chat.id ) 


print("Starting the bot")
bot.run()
