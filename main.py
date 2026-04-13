import os
import asyncio
import json
from pyrogram import Client, filters
from PIL import Image

# --- CONFIG ---
api_id = int(os.environ.get("api_id", 0))
api_hash = os.environ.get("api_hash", "")
bot_token = os.environ.get("bot_token", "")
admin_ids = [8063495170]

bot = Client("Bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# --- UTILS ---
def fix_thumbnail(path):
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path).convert("RGB")
        img.thumbnail((320, 320))
        img.save(path, "JPEG", quality=75, optimize=True)
        return img.size
    except Exception:
        return None

async def run_command(cmd):
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()

# --- HANDLERS ---
@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply("Send a link to download the video.")

@bot.on_message(filters.private & ~filters.command("start"))
async def send_video(client, message):
    # Initialize variables at the start to prevent UnboundLocalError
    filename = None
    thumb_name = None
    msg = None

    if message.from_user.id not in admin_ids:
        return await message.reply("Not authorized.")

    url = message.text
    if "http" not in url:
        return await message.reply("Please send a valid URL.")

    try:
        msg = await message.reply("Processing link...", quote=True)

        # 1. Extract Metadata
        info_cmd = ["yt-dlp", "--dump-json", "--cookiefile", "cookies.txt", url]
        stdout, stderr = await run_command(info_cmd)
        
        if not stdout:
            return await msg.edit(f"Failed to get info. Error: {stderr[:100]}")
            
        info = json.loads(stdout)
        title = info.get("title", "video").replace("/", "_") # Simple fix for invalid filenames
        filename = f"{title}.mp4"
        thumb_name = f"{title}.jpg"
        duration = int(info.get("duration", 0))

        await msg.edit(f"Downloading: **{title}**")

        # 2. Download (Limited to 720p for Koyeb stability)
        dl_cmd = [
            "yt-dlp",
            "-f", "bestvideo[height<=720]+bestaudio/best",
            "--merge-output-format", "mp4",
            "--cookiefile", "cookies.txt",
            "--referer", "https://www.google.com",
            "--writethumbnail",
            "--postprocessor-args", "ffmpeg:-ss 00:00:01 -vframes 1",
            "-o", filename,
            url
        ]
        await run_command(dl_cmd)

        # 3. Handle Thumbnail (check webp/jpg/png)
        possible_thumbs = [thumb_name, f"{title}.webp", f"{title}.png"]
        found_thumb = None
        for pt in possible_thumbs:
            if os.path.exists(pt):
                os.rename(pt, thumb_name)
                found_thumb = thumb_name
                break

        width, height = (None, None)
        if found_thumb:
            size = fix_thumbnail(found_thumb)
            if size:
                width, height = size

        # 4. Upload to Telegram
        await msg.edit("Uploading...")
        await bot.send_video(
            chat_id=message.chat.id,
            video=filename,
            duration=duration,
            thumb=found_thumb,
            width=width,
            height=height,
            caption=f"`{filename}`",
            supports_streaming=True
        )

    except Exception as e:
        if msg:
            await msg.edit(f"Error: {str(e)}")
        else:
            await message.reply(f"Error: {str(e)}")
    
    finally:
        # 5. Guaranteed Cleanup
        if msg:
            await msg.delete()
        if filename and os.path.exists(filename): 
            os.remove(filename)
        if thumb_name and os.path.exists(thumb_name): 
            os.remove(thumb_name)

print("Bot is starting...")
bot.run()
