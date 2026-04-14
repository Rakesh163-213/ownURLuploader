from urllib.parse import urlparse
def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Testing it

from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import subprocess
import os
from PIL import Image
from yt_dlp.networking.impersonate import ImpersonateTarget




api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
bot_token = os.environ.get("bot_token")

bot = Client("Main",api_id=api_id,api_hash=api_hash,bot_token=bot_token)



admin_ids = [8063495170]
path = "downloads"





import subprocess

def get_thumbnail(filename, thumb):
    print(filename)
    subprocess.run(["ffmpeg","-i", filename,"-ss", "00:00:01.000","-vframes", "1",thumb])



def get_size(thumb):
    with Image.open(thumb) as img:
        img.thumbnail((320,320))
        img.save(thumb)
        return img.size



 





@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(clinet,message):
    await message.reply("Send a Url to download the video")
    

@bot.on_message(filters.private & ~filters.command("start"))
async def send_video(client,message):
    if message.from_user.id in admin_ids:
        if is_url(message.text) :
            url = message.text
            await message.reply("Downloading the Video.",quote=True)


            def my_hook(data):
                if data['status'] == 'downloading':
                    total_size = data.get("_total_bytes_str",0)
                    
                    print("HERE IS THE TOTAL SIZE: ",total_size)

            yt_opts = {
                "format" : "best",
                "no_warnings": True,
                "outtmpl": '%(title)s.%(ext)s',
                "merge_output_format": 'mp4',
                "windowsfilenames": False,
                "noprogress":False,
                "quiet": True,
                'progress_hooks': [my_hook],
                "impersonate":  ImpersonateTarget(client='chrome', version='136', os=None, os_version=None),
#                "proxy": "socks5://127.0.0.1:9050",                 
#                "cookiefile": 'cookies.txt',
                }


            with YoutubeDL(yt_opts) as yt:
                info = yt.extract_info(url,download=True)
                
                file_size = info.get("filesize")
                duration = int(info.get('duration',0))
                thumb = f"{info['title']}.jpg"
                filename = f"{info['title']}.mp4"
                print("HERE: ",filename)
                get_thumbnail(filename,thumb)
                width, height = get_size(thumb)
                caption = f"{filename}"
                
                
                print(f"\nFILE NAME: {filename}\n")

                
                await message.reply(f"Sending {filename}")
                
                await bot.send_video(
                    message.chat.id, 
                    filename,
                    duration=duration,
                    thumb=thumb,
                    width=width,
                    height=height,
                    caption=caption)
                print('SENT SUCCESSFULLY')
                print(filename,"\n",thumb)
                os.remove(filename)
                os.remove(thumb)
        else:
            await message.reply("Please send a valid URL.")
    else:
        await message.reply("You are not Authorised to use this bot.\n Please ask admins for help.")



print("Starting the bot")
bot.run()
