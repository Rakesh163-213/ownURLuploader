import os
import asyncio
import sys
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
    img = Image.open(path).convert("RGB")
    img.thumbnail((320, 320))
    img.save(path, "JPEG", quality=75, optimize=True)
    return img.size

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
    if message.from_user.id not in admin_ids:
        return await message.reply("Not authorized.")

    url = message.text
    if "http" not in url:
        return await message.reply("Please send a valid URL.")

    msg = await message.reply("Processing...", quote=True)

    try:
        # 1. Get info first
        info_cmd = ["yt-dlp", "--dump-json", "--cookiefile", "cookies.txt", url]
        stdout, _ = await run_command(info_cmd)
        import json
        info = json.loads(stdout)
        
        title = info.get("title", "video")
        filename = f"{title}.mp4"
        thumb_name = f"{title}.jpg"
        duration = int(info.get("duration", 0))

        await msg.edit(f"Downloading: {title}")

        # 2. Download using subprocess (efficient for RAM)
        dl_cmd = [
            "yt-dlp",
            "-f", "bestvideo[height<=720]+bestaudio/best",
            "--merge-output-format", "mp4",
            "--cookiefile", "cookies.txt",
            "--writethumbnail",
            "--postprocessor-args", "ffmpeg:-ss 00:00:01 -vframes 1",
            "-o", filename,
            url
        ]
        await run_command(dl_cmd)

        # 3. Handle Thumbnail
        # yt-dlp might save thumb as .webp or .jpg; check what exists
        actual_thumb = thumb_name if os.path.exists(thumb_name) else f"{title}.webp"
        if os.path.exists(actual_thumb):
            os.rename(actual_thumb, thumb_name) # Ensure it's named .jpg for fix_thumbnail
            width, height = fix_thumbnail(thumb_name)
        else:
            thumb_name, width, height = None, None, None

        # 4. Upload
        await msg.edit("Uploading to Telegram...")
        await bot.send_video(
            chat_id=message.chat.id,
            video=filename,
            duration=duration,
            thumb=thumb_name,
            width=width,
            height=height,
            caption=f"`{filename}`",
            supports_streaming=True
        )

    except Exception as e:
        await message.reply(f"Error: {str(e)}")
    
    finally:
        # 5. Cleanup
        await msg.delete()
        if os.path.exists(filename): os.remove(filename)
        if thumb_name and os.path.exists(thumb_name): os.remove(thumb_name)

print("Bot is running...")
bot.run()
